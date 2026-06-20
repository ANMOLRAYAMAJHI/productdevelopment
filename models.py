"""
Database models for the Helpdesk System
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Admin(db.Model):
    """Admin user model"""
    __tablename__ = 'admin'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    tickets = db.relationship('Ticket', backref='admin', lazy=True)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<Admin {self.username}>'

class Ticket(db.Model):
    """Support ticket model"""
    __tablename__ = 'ticket'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(20), default='Neutral')  # Positive, Neutral, Negative
    priority = db.Column(db.String(20), default='Normal')    # Normal, Urgent
    status = db.Column(db.String(20), default='Open')        # Open, In Progress, Closed
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=True)
    
    def __repr__(self):
        return f'<Ticket {self.id} - {self.subject}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'email': self.email,
            'category': self.category,
            'subject': self.subject,
            'message': self.message,
            'sentiment': self.sentiment,
            'priority': self.priority,
            'status': self.status,
            'created_date': self.created_date.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_date': self.updated_date.strftime('%Y-%m-%d %H:%M:%S')
        }


class ServiceItem(db.Model):
    """Service portfolio item model"""
    __tablename__ = 'service_item'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(100), nullable=True)
    active = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ServiceItem {self.title}>'


class BlogPost(db.Model):
    """Blog post model"""
    __tablename__ = 'blog_post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    excerpt = db.Column(db.String(400), nullable=False)
    body = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    published_date = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<BlogPost {self.title}>'


class EventTimeline(db.Model):
    """Timeline event model"""
    __tablename__ = 'event_timeline'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    position = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<EventTimeline {self.title}>'


class GalleryItem(db.Model):
    """Photo gallery item model"""
    __tablename__ = 'gallery_item'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<GalleryItem {self.title}>'


class Feedback(db.Model):
    """Customer feedback / testimonial model"""
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=True)
    message = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)
    active = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Feedback {self.name}>'


class ContactMessage(db.Model):
    """Contact form submission"""
    __tablename__ = 'contact_message'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ContactMessage {self.subject}>'


class SiteSetting(db.Model):
    """Basic site settings"""
    __tablename__ = 'site_setting'

    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(120), nullable=False, default='HelpdeskAI')
    logo_url = db.Column(db.String(255), nullable=True)
    timezone = db.Column(db.String(80), nullable=True, default='UTC')
    contact_email = db.Column(db.String(120), nullable=True)
    contact_phone = db.Column(db.String(80), nullable=True)
    hero_tagline = db.Column(db.String(220), nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<SiteSetting {self.site_name}>'
