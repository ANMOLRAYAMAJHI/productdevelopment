"""
Main Flask application for AI-Powered Customer Helpdesk System
"""
import html
import os
import logging
from functools import wraps
from datetime import datetime, timedelta

# Provide clearer error messages when optional third-party
# dependencies are not installed in the user's environment.
try:
    import flask
except Exception as _err: 
    raise RuntimeError(
    ) from _err

try:
    from sqlalchemy.exc import IntegrityError
except Exception as _err:  # pragma: no cover - environment issue
    raise RuntimeError(
    ) from _err
from config import config
from models import (
    db, Admin, Ticket, ServiceItem, BlogPost,
    EventTimeline, GalleryItem, Feedback, ContactMessage,
    SiteSetting
)
from forms import (
    TicketForm, LoginForm, RegisterForm, UpdateStatusForm,
    ContactForm, ContentItemForm, EventForm, ChangePasswordForm,
    SiteSettingsForm
)
from sqlalchemy import create_engine
from sentiment import SentimentAnalyzer
import oracle_sync
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect, generate_csrf, validate_csrf
from flask_wtf.csrf import CSRFError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize limiter at module level for decorators
limiter = Limiter(key_func=get_remote_address)

def create_app(config_name='development'):
    """Application factory"""
    app = flask.Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config[config_name])
    limiter.init_app(app)
    # Ensure database directory exists for SQLite file-based DB
    db_path = app.config.get('DATABASE_PATH')
    if db_path:
        db_dir = os.path.dirname(db_path)
        try:
            os.makedirs(db_dir, exist_ok=True)
        except Exception:
            logger.warning('Could not create database directory: %s', db_dir)

    # If Oracle should be the primary backend, test the connection first.
    if app.config.get('ORACLE_USE_AS_PRIMARY'):
        try:
            engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
            conn = engine.connect()
            conn.close()
            logger.info('Oracle primary database is available.')
        except Exception as exc:
            logger.warning('Oracle primary database unavailable, falling back to SQLite: %s', exc)
            app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
            app.config['ORACLE_ENABLED'] = False
            app.config['ORACLE_USE_AS_PRIMARY'] = False

    # Initialize CSRF protection (ensures forms validate CSRF tokens)
    csrf = CSRFProtect()
    csrf.init_app(app)
    # Make `csrf_token()` available in templates for meta tags or ajax calls
    app.jinja_env.globals['csrf_token'] = generate_csrf

    # Initialize database
    db.init_app(app)

    with app.app_context():
        db.create_all()
        # Initialize Oracle sync only if enabled
        if app.config.get('ORACLE_ENABLED'):
            oracle_sync.init_oracle_sync(app)
    
    return app

# Create application instance
app = create_app(os.environ.get('FLASK_ENV', 'development'))

# ==================== DECORATORS ====================

LOCKOUT_THRESHOLD = 5
LOCKOUT_DURATION_MINUTES = 15


def sanitize_text(value):
    if isinstance(value, str):
        return html.escape(value.strip())
    return value


def login_required(f):
    """Decorator to require login for admin routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in flask.session:
            flask.flash('Please login first', 'warning')
            return flask.redirect(flask.url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== CUSTOMER ROUTES ====================

@app.route('/')
def index():
    """Home page"""
    return flask.render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit_ticket():
    """Submit a support ticket"""
    form = TicketForm()
    
    # Support both normal form POST and JSON (AJAX) POST
    if flask.request.is_json:
        data = flask.request.get_json() or {}
        # Validate CSRF token from header
        token = flask.request.headers.get('X-CSRFToken') or flask.request.headers.get('X-CSRF-Token')
        try:
            validate_csrf(token)
        except Exception as e:
            return flask.jsonify({'success': False, 'errors': {'csrf': ['Invalid CSRF token']}}), 400

        # Build form from JSON payload (disable automatic CSRF on the form)
        form_json = TicketForm(formdata=None, data=data, meta={'csrf': False})
        if form_json.validate():
            try:
                analysis = SentimentAnalyzer.analyze(form_json.message.data)
                sentiment = analysis['sentiment']
                priority = SentimentAnalyzer.get_priority(sentiment)

                ticket = Ticket(
                    customer_name=form_json.customer_name.data,
                    email=form_json.email.data,
                    category=form_json.category.data,
                    subject=form_json.subject.data,
                    message=form_json.message.data,
                    sentiment=sentiment,
                    priority=priority,
                    status='Open'
                )
                db.session.add(ticket)
                db.session.commit()
                logger.info(f'Ticket #{ticket.id} created via AJAX')
                return flask.jsonify({'success': True, 'ticket_id': ticket.id}), 201
            except Exception as e:
                db.session.rollback()
                logger.error(f'Error creating ticket via AJAX: {str(e)}')
                return flask.jsonify({'success': False, 'errors': {'server': ['Failed to create ticket']}}), 500
        else:
            return flask.jsonify({'success': False, 'errors': form_json.errors}), 400

    if form.validate_on_submit():
        try:
            # Analyze sentiment
            analysis = SentimentAnalyzer.analyze(form.message.data)
            sentiment = analysis['sentiment']
            priority = SentimentAnalyzer.get_priority(sentiment)
            
            # Create ticket
            ticket = Ticket(
                customer_name=sanitize_text(form.customer_name.data),
                email=sanitize_text(form.email.data),
                category=sanitize_text(form.category.data),
                subject=sanitize_text(form.subject.data),
                message=sanitize_text(form.message.data),
                sentiment=sentiment,
                priority=priority,
                status='Open'
            )
            
            db.session.add(ticket)
            db.session.commit()
            
            logger.info(f'Ticket #{ticket.id} created - Sentiment: {sentiment}, Priority: {priority}')
            flask.session['ticket_id'] = ticket.id
            
            return flask.redirect(flask.url_for('success'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error creating ticket: {str(e)}')
            flask.flash('Error submitting ticket. Please try again.', 'danger')
    else:
        # If this was a POST but validation failed, log details to help debugging
        if flask.request.method == 'POST':
            logger.info('Ticket form validation failed: %s', form.errors)
            # Show user the first validation error (keep it friendly)
            first_err = None
            for field, errs in form.errors.items():
                if errs:
                    first_err = errs[0]
                    break
            if first_err:
                flask.flash(first_err, 'warning')
    
    return flask.render_template('submit.html', form=form)

@app.route('/success')
def success():
    """Success page after ticket submission"""
    ticket_id = flask.session.pop('ticket_id', None)
    
    if ticket_id:
        ticket = Ticket.query.get(ticket_id)
        if ticket:
            return flask.render_template('success.html', ticket=ticket)
    
    return flask.redirect(flask.url_for('index'))

@app.route('/about')
def about():
    """About page"""
    return flask.render_template('about.html')

@app.route('/services')
def services():
    """Service portfolio page"""
    items = ServiceItem.query.filter_by(active=True).order_by(ServiceItem.created_date.desc()).all()
    return flask.render_template('services.html', services=items)

@app.route('/blog')
def blog():
    """Blogs page"""
    posts = BlogPost.query.filter_by(active=True).order_by(BlogPost.published_date.desc()).all()
    return flask.render_template('blog.html', posts=posts)

@app.route('/events')
def events():
    """Events timeline page"""
    timeline = EventTimeline.query.filter_by(active=True).order_by(EventTimeline.event_date.asc()).all()
    return flask.render_template('events.html', timeline=timeline)

@app.route('/gallery')
def gallery():
    """Photo gallery page"""
    photos = GalleryItem.query.filter_by(active=True).order_by(GalleryItem.created_date.desc()).all()
    if not photos:
        photos = [
            {
                'image_url': 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800&q=80',
                'title': 'Product Launch Night',
                'caption': 'Unveiling our newest release to a packed room.'
            },
            {
                'image_url': 'https://images.unsplash.com/photo-1511578314322-379afb476865?w=800&q=80',
                'title': 'Team Offsite',
                'caption': 'Strategy sessions and team bonding by the coast.'
            },
            {
                'image_url': 'https://images.unsplash.com/photo-1505373877841-8d25f7d46678?w=800&q=80',
                'title': 'Conference Keynote',
                'caption': 'Sharing our roadmap on the main stage.'
            },
            {
                'image_url': 'https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=800&q=80',
                'title': 'Office Culture',
                'caption': 'A glimpse into our day-to-day workspace.'
            }
        ]
    return flask.render_template('gallery.html', photos=photos)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page"""
    form = ContactForm()
    if form.validate_on_submit():
        try:
            message = ContactMessage(
                name=sanitize_text(form.name.data),
                email=sanitize_text(form.email.data),
                subject=sanitize_text(form.subject.data),
                message=sanitize_text(form.message.data)
            )
            db.session.add(message)
            db.session.commit()
            flask.flash('Your message has been sent successfully.', 'success')
            return flask.redirect(flask.url_for('contact'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Contact form error: {str(e)}')
            flask.flash('Unable to send your message right now.', 'danger')
    return flask.render_template('contact.html', form=form)

def generate_assistant_response(question):
    """Generate a lightweight AI-style assistant response."""
    normalized = question.strip().lower()
    analysis = SentimentAnalyzer.analyze(question)
    polarity = analysis['polarity']
    sentiment = analysis['sentiment']

    responses = {
        'ticket': 'You can submit a ticket from the support page. Describe your issue clearly and we will prioritize it automatically.',
        'status': 'After submitting a ticket, you can check the status from your ticket details page or contact us if you need faster updates.',
        'contact': 'Use the contact page to send us a message directly. We monitor inquiries and respond quickly.',
        'service': 'Visit our Services page to explore the software solutions we offer, including AI helpdesk, analytics, and customer support workflows.',
        'blog': 'The blog page features insight articles and helpdesk best practices to keep your team informed.',
        'gallery': 'The gallery shows recent project snapshots, events, and product highlights in a visual layout.',
        'event': 'Our events page displays timeline milestones, product launches, and community updates.'
    }

    if any(token in normalized for token in ['submit', 'ticket', 'support', 'issue', 'problem']):
        return responses['ticket']
    if any(token in normalized for token in ['status', 'update', 'progress']):
        return responses['status']
    if any(token in normalized for token in ['contact', 'email', 'message', 'support team']):
        return responses['contact']
    if any(token in normalized for token in ['service', 'solution', 'software']):
        return responses['service']
    if any(token in normalized for token in ['blog', 'article', 'news']):
        return responses['blog']
    if any(token in normalized for token in ['gallery', 'photo', 'image']):
        return responses['gallery']
    if any(token in normalized for token in ['event', 'timeline', 'launch', 'milestone']):
        return responses['event']

    if sentiment == 'Negative':
        return 'I detected concern in your message. Please describe the issue in more detail so I can help prioritize it as urgent.'
    if sentiment == 'Positive':
        return 'That sounds good. If you have more details, I can guide you to the right support page.'

    return 'I can help you with tickets, contact, services, blog, gallery, and events. Please tell me what you need help with.'


@app.route('/assistant')
def assistant():
    """Virtual assistant page"""
    return flask.render_template('assistant.html')


@app.route('/assistant/query', methods=['POST'])
def assistant_query():
    """Handle assistant chat queries."""
    data = flask.request.get_json() or {}
    question = data.get('question', '').strip()

    token = flask.request.headers.get('X-CSRFToken') or flask.request.headers.get('X-CSRF-Token')
    try:
        validate_csrf(token)
    except Exception as e:
        logger.warning(f'Invalid CSRF token on assistant query: {e}')
        return flask.jsonify({'success': False, 'message': 'Invalid CSRF token.'}), 400

    if not question:
        return flask.jsonify({'success': False, 'message': 'Please enter a question.'}), 400

    answer = generate_assistant_response(question)
    return flask.jsonify({'success': True, 'answer': answer})


@app.route('/feedback')
def feedback_page():
    """Customer ratings and feedback page"""
    reviews = Feedback.query.filter_by(active=True).order_by(Feedback.created_date.desc()).all()
    total_reviews = len(reviews)
    average_rating = round(sum([review.rating for review in reviews]) / total_reviews, 1) if total_reviews else 0
    positive_count = len([review for review in reviews if review.rating >= 4])
    positive_ratio = int((positive_count / total_reviews) * 100) if total_reviews else 0
    return flask.render_template(
        'feedback.html',
        reviews=reviews,
        total_reviews=total_reviews,
        average_rating=average_rating,
        positive_ratio=positive_ratio
    )

# ==================== ADMIN ROUTES ====================

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit('5 per minute')
def login():
    """Admin login"""
    if 'admin_id' in flask.session:
        return flask.redirect(flask.url_for('dashboard'))

    form = LoginForm()

    lockout_until = flask.session.get('login_lockout_until')
    if lockout_until:
        try:
            lockout_until_dt = datetime.fromisoformat(lockout_until)
            if datetime.utcnow() < lockout_until_dt:
                remaining = int((lockout_until_dt - datetime.utcnow()).total_seconds() / 60) + 1
                flask.flash(
                    f'Too many failed login attempts. Please wait {remaining} minutes and try again.',
                    'danger'
                )
                return flask.render_template('login.html', form=form)
        except Exception:
            flask.session.pop('login_lockout_until', None)
            flask.session['login_attempts'] = 0

    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()

        if admin and admin.check_password(form.password.data):
            flask.session['admin_id'] = admin.id
            flask.session['username'] = admin.username
            flask.session.permanent = True
            flask.session.pop('login_attempts', None)
            flask.session.pop('login_lockout_until', None)
            logger.info(f'Admin {admin.username} logged in')
            flask.flash('Login successful!', 'success')
            return flask.redirect(flask.url_for('dashboard'))

        attempts = flask.session.get('login_attempts', 0) + 1
        flask.session['login_attempts'] = attempts

        if attempts >= LOCKOUT_THRESHOLD:
            lockout_until_dt = datetime.utcnow() + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
            flask.session['login_lockout_until'] = lockout_until_dt.isoformat()
            flask.flash(
                'Too many failed login attempts. Please try again later.',
                'danger'
            )
        else:
            logger.warning(f'Failed login attempt for username: {form.username.data}')
            flask.flash('Invalid username or password', 'danger')

    return flask.render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Admin registration (first admin only for security)"""
    # Registration allowed only if no admin exists, or explicitly enabled
    allow_registration = app.config.get('ALLOW_REGISTRATION', False)
    if Admin.query.first() is not None and not allow_registration:
        flask.flash('Registration is closed', 'warning')
        return flask.redirect(flask.url_for('login'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            admin = Admin(username=form.username.data)
            admin.set_password(form.password.data)
            
            db.session.add(admin)
            db.session.commit()
            
            logger.info(f'New admin registered: {admin.username}')
            flask.flash('Registration successful! Please login.', 'success')
            return flask.redirect(flask.url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flask.flash('Username already exists', 'danger')
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error during registration: {str(e)}')
            flask.flash('Error during registration', 'danger')
    
    return flask.render_template('register.html', form=form)

@app.route('/logout')
def logout():
    """Admin logout"""
    flask.session.clear()
    flask.flash('You have been logged out', 'info')
    return flask.redirect(flask.url_for('index'))

@app.route('/admin')
def admin_root():
    """Redirect /admin to the dashboard or login page"""
    if 'admin_id' in flask.session:
        return flask.redirect(flask.url_for('dashboard'))
    return flask.redirect(flask.url_for('login'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    return flask.redirect(flask.url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard - view all tickets"""
    page = flask.request.args.get('page', 1, type=int)
    status_filter = flask.request.args.get('status', '', type=str)
    search_query = flask.request.args.get('search', '', type=str)
    
    # Build query
    query = Ticket.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    if search_query:
        query = query.filter(
            (Ticket.subject.ilike(f'%{search_query}%')) |
            (Ticket.customer_name.ilike(f'%{search_query}%')) |
            (Ticket.email.ilike(f'%{search_query}%'))
        )
    
    # Sort by date (newest first)
    tickets = query.order_by(Ticket.created_date.desc()).paginate(
        page=page,
        per_page=app.config['TICKETS_PER_PAGE']
    )

    total_services = ServiceItem.query.count()
    total_posts = BlogPost.query.count()
    total_events = EventTimeline.query.count()
    total_photos = GalleryItem.query.count()
    total_feedback = Feedback.query.count()
    unread_messages = ContactMessage.query.filter_by(is_read=False).count()
    
    return flask.render_template(
        'dashboard.html',
        tickets=tickets,
        status_filter=status_filter,
        search_query=search_query,
        total_services=total_services,
        total_posts=total_posts,
        total_events=total_events,
        total_photos=total_photos,
        total_feedback=total_feedback,
        unread_messages=unread_messages
    )

@app.route('/admin/services')
@login_required
def admin_services():
    items = ServiceItem.query.order_by(ServiceItem.created_date.desc()).all()
    return flask.render_template('admin_services.html', services=items)

@app.route('/admin/service/new', methods=['GET', 'POST'])
@login_required
def admin_service_new():
    form = ContentItemForm()
    if form.validate_on_submit():
        item = ServiceItem(
            title=sanitize_text(form.title.data),
            description=sanitize_text(form.description.data),
            icon=sanitize_text(form.icon.data),
            active=True
        )
        db.session.add(item)
        db.session.commit()
        flask.flash('Service added successfully', 'success')
        return flask.redirect(flask.url_for('admin_services'))
    return flask.render_template('admin_service_form.html', form=form, page_title='New Service')

@app.route('/admin/service/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_service_edit(item_id):
    item = ServiceItem.query.get_or_404(item_id)
    form = ContentItemForm(obj=item)
    if form.validate_on_submit():
        item.title = form.title.data
        item.description = form.description.data
        item.icon = form.icon.data
        db.session.commit()
        flask.flash('Service updated successfully', 'success')
        return flask.redirect(flask.url_for('admin_services'))
    return flask.render_template('admin_service_form.html', form=form, page_title='Edit Service')

@app.route('/admin/blog')
@login_required
def admin_blog():
    posts = BlogPost.query.order_by(BlogPost.published_date.desc()).all()
    return flask.render_template('admin_blog.html', posts=posts)

@app.route('/admin/blog/new', methods=['GET', 'POST'])
@login_required
def admin_blog_new():
    form = ContentItemForm()
    if form.validate_on_submit():
        post = BlogPost(
            title=sanitize_text(form.title.data),
            excerpt=sanitize_text(form.description.data),
            body=sanitize_text(form.description.data),
            image_url=sanitize_text(form.image_url.data),
            active=True
        )
        db.session.add(post)
        db.session.commit()
        flask.flash('Blog post added successfully', 'success')
        return flask.redirect(flask.url_for('admin_blog'))
    return flask.render_template('admin_blog_form.html', form=form, page_title='New Blog Post')

@app.route('/admin/blog/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_blog_edit(post_id):
    post = BlogPost.query.get_or_404(post_id)
    form = ContentItemForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.excerpt = form.description.data
        post.body = form.description.data
        post.image_url = form.image_url.data
        db.session.commit()
        flask.flash('Blog post updated successfully', 'success')
        return flask.redirect(flask.url_for('admin_blog'))
    return flask.render_template('admin_blog_form.html', form=form, page_title='Edit Blog Post')

@app.route('/admin/events')
@login_required
def admin_events():
    timeline = EventTimeline.query.order_by(EventTimeline.event_date.asc()).all()
    return flask.render_template('admin_events.html', timeline=timeline)

@app.route('/admin/event/new', methods=['GET', 'POST'])
@login_required
def admin_event_new():
    form = EventForm()
    if form.validate_on_submit():
        event = EventTimeline(
            title=form.title.data,
            description=form.description.data,
            event_date=datetime.fromisoformat(form.event_date.data),
            active=True
        )
        db.session.add(event)
        db.session.commit()
        flask.flash('Event added successfully', 'success')
        return flask.redirect(flask.url_for('admin_events'))
    return flask.render_template('admin_event_form.html', form=form, page_title='New Timeline Event')

@app.route('/admin/event/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_event_edit(event_id):
    event = EventTimeline.query.get_or_404(event_id)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.event_date = datetime.fromisoformat(form.event_date.data)
        db.session.commit()
        flask.flash('Event updated successfully', 'success')
        return flask.redirect(flask.url_for('admin_events'))
    return flask.render_template('admin_event_form.html', form=form, page_title='Edit Timeline Event')

@app.route('/admin/gallery')
@login_required
def admin_gallery():
    photos = GalleryItem.query.order_by(GalleryItem.created_date.desc()).all()
    return flask.render_template('admin_gallery.html', photos=photos)

@app.route('/admin/gallery/new', methods=['GET', 'POST'])
@login_required
def admin_gallery_new():
    form = ContentItemForm()
    if form.validate_on_submit():
        photo = GalleryItem(
            title=sanitize_text(form.title.data),
            caption=sanitize_text(form.description.data),
            image_url=sanitize_text(form.image_url.data),
            active=True
        )
        db.session.add(photo)
        db.session.commit()
        flask.flash('Gallery item added successfully', 'success')
        return flask.redirect(flask.url_for('admin_gallery'))
    return flask.render_template('admin_gallery_form.html', form=form, page_title='New Gallery Item')

@app.route('/admin/gallery/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_gallery_edit(item_id):
    photo = GalleryItem.query.get_or_404(item_id)
    form = ContentItemForm(obj=photo)
    if form.validate_on_submit():
        photo.title = form.title.data
        photo.caption = form.description.data
        photo.image_url = form.image_url.data
        db.session.commit()
        flask.flash('Gallery item updated successfully', 'success')
        return flask.redirect(flask.url_for('admin_gallery'))
    return flask.render_template('admin_gallery_form.html', form=form, page_title='Edit Gallery Item')

@app.route('/admin/feedback')
@login_required
def admin_feedback():
    reviews = Feedback.query.order_by(Feedback.created_date.desc()).all()
    return flask.render_template('admin_feedback.html', feedback=reviews)

@app.route('/admin/contact-messages')
@login_required
def admin_contact_messages():
    messages = ContactMessage.query.order_by(ContactMessage.created_date.desc()).all()
    return flask.render_template('admin_contact_messages.html', messages=messages)

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    settings = SiteSetting.query.first()
    if not settings:
        settings = SiteSetting()
        db.session.add(settings)
        db.session.commit()
    form = SiteSettingsForm(obj=settings)
    if form.validate_on_submit():
        settings.site_name = sanitize_text(form.site_name.data)
        settings.logo_url = sanitize_text(form.logo_url.data)
        settings.timezone = sanitize_text(form.timezone.data)
        settings.contact_email = sanitize_text(form.contact_email.data)
        settings.contact_phone = sanitize_text(form.contact_phone.data)
        settings.hero_tagline = sanitize_text(form.hero_tagline.data)
        db.session.commit()
        flask.flash('Site settings updated successfully', 'success')
        return flask.redirect(flask.url_for('admin_settings'))
    return flask.render_template('admin_settings.html', form=form)


@app.route('/admin/change-password', methods=['GET', 'POST'])
@login_required
def admin_change_password():
    admin = Admin.query.get_or_404(flask.session['admin_id'])
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not admin.check_password(form.current_password.data):
            form.current_password.errors.append('Current password is incorrect')
        else:
            admin.set_password(form.new_password.data)
            db.session.commit()
            flask.flash('Your password has been updated successfully.', 'success')
            return flask.redirect(flask.url_for('admin_settings'))
    return flask.render_template('admin_change_password.html', form=form)


@app.route('/ticket/<int:ticket_id>')
@login_required
def ticket_details(ticket_id):
    """View ticket details"""
    ticket = Ticket.query.get_or_404(ticket_id)
    return flask.render_template('ticket_details.html', ticket=ticket)

@app.route('/update-status/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def update_status(ticket_id):
    """Update ticket status"""
    ticket = Ticket.query.get_or_404(ticket_id)
    form = UpdateStatusForm()
    
    if form.validate_on_submit():
        try:
            ticket.status = form.status.data
            ticket.admin_id = flask.session['admin_id']
            db.session.commit()
            
            logger.info(f'Ticket #{ticket_id} status updated to {form.status.data}')
            flask.flash('Ticket status updated successfully', 'success')
            return flask.redirect(flask.url_for('ticket_details', ticket_id=ticket.id))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error updating ticket status: {str(e)}')
            flask.flash('Error updating status', 'danger')
    else:
        form.status.data = ticket.status
    
    return flask.render_template('update_status.html', ticket=ticket, form=form)

# ==================== API ENDPOINTS ====================

@app.route('/api/tickets/stats')
@login_required
def api_tickets_stats():
    """Get ticket statistics"""
    total = Ticket.query.count()
    open_count = Ticket.query.filter_by(status='Open').count()
    in_progress = Ticket.query.filter_by(status='In Progress').count()
    closed = Ticket.query.filter_by(status='Closed').count()
    urgent = Ticket.query.filter_by(priority='Urgent').count()
    
    return flask.jsonify({
        'total': total,
        'open': open_count,
        'in_progress': in_progress,
        'closed': closed,
        'urgent': urgent
    })

@app.route('/api/tickets/sentiment')
@login_required
def api_tickets_sentiment():
    """Get sentiment distribution"""
    positive = Ticket.query.filter_by(sentiment='Positive').count()
    neutral = Ticket.query.filter_by(sentiment='Neutral').count()
    negative = Ticket.query.filter_by(sentiment='Negative').count()
    
    return flask.jsonify({
        'positive': positive,
        'neutral': neutral,
        'negative': negative
    })

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return flask.render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f'Server error: {str(error)}')
    return flask.render_template('500.html'), 500


@app.after_request
def set_security_headers(response):
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "img-src 'self' data: https:; "
        "style-src 'self' 'unsafe-inline' https:; "
        "script-src 'self' 'unsafe-inline' https:;"
    )
    response.headers['Permissions-Policy'] = 'geolocation=()'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response


# ==================== CONTEXT PROCESSORS ====================

@app.context_processor
def inject_user():
    """Make user data available in templates"""
    settings = SiteSetting.query.first()
    return {
        'is_logged_in': 'admin_id' in flask.session,
        'username': flask.session.get('username', ''),
        'current_year': datetime.now().year,
        'site_name': settings.site_name if settings else 'HelpdeskAI',
        'hero_tagline': settings.hero_tagline if settings else 'AI-Powered Customer Helpdesk System'
    }

# ==================== MAIN ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
