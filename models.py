"""
Database models for the Helpdesk System
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib

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
        self.password = hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password):
        """Verify password"""
        return self.password == hashlib.sha256(password.encode()).hexdigest()
    
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
