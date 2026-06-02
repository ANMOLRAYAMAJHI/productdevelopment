"""
Main Flask application for AI-Powered Customer Helpdesk System
"""
import os
import logging
import flask
from functools import wraps
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from config import config
from models import db, Admin, Ticket
from forms import TicketForm, LoginForm, RegisterForm, UpdateStatusForm
from sentiment import SentimentAnalyzer
import oracle_sync

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app(config_name='development'):
    """Application factory"""
    app = flask.Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config[config_name])
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        # Initialize Oracle sync
        oracle_sync.init_oracle_sync(app)
    
    return app

# Create application instance
app = create_app(os.environ.get('FLASK_ENV', 'development'))

# ==================== DECORATORS ====================

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
    
    if form.validate_on_submit():
        try:
            # Analyze sentiment
            analysis = SentimentAnalyzer.analyze(form.message.data)
            sentiment = analysis['sentiment']
            priority = SentimentAnalyzer.get_priority(sentiment)
            
            # Create ticket
            ticket = Ticket(
                customer_name=form.customer_name.data,
                email=form.email.data,
                category=form.category.data,
                subject=form.subject.data,
                message=form.message.data,
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

# ==================== ADMIN ROUTES ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login"""
    if 'admin_id' in flask.session:
        return flask.redirect(flask.url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        
        if admin and admin.check_password(form.password.data):
            flask.session['admin_id'] = admin.id
            flask.session['username'] = admin.username
            flask.session.permanent = True
            logger.info(f'Admin {admin.username} logged in')
            flask.flash('Login successful!', 'success')
            return flask.redirect(flask.url_for('dashboard'))
        else:
            logger.warning(f'Failed login attempt for username: {form.username.data}')
            flask.flash('Invalid username or password', 'danger')
    
    return flask.render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Admin registration (first admin only for security)"""
    # Check if any admin exists
    if Admin.query.first() is not None:
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
    
    return flask.render_template(
        'dashboard.html',
        tickets=tickets,
        status_filter=status_filter,
        search_query=search_query
    )

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

# ==================== CONTEXT PROCESSORS ====================

@app.context_processor
def inject_user():
    """Make user data available in templates"""
    return {
        'is_logged_in': 'admin_id' in flask.session,
        'username': flask.session.get('username', ''),
        'current_year': datetime.now().year
    }

# ==================== MAIN ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
