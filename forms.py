"""
Form definitions for the Helpdesk System
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo
from models import Admin

class TicketForm(FlaskForm):
    """Form for submitting a support ticket"""
    customer_name = StringField(
        'Full Name',
        validators=[
            DataRequired(message='Name is required'),
            Length(min=2, max=100, message='Name must be 2-100 characters')
        ]
    )
    email = StringField(
        'Email Address',
        validators=[
            DataRequired(message='Email is required'),
            Email(message='Invalid email address')
        ]
    )
    category = SelectField(
        'Category',
        choices=[
            ('general', 'General Inquiry'),
            ('technical', 'Technical Support'),
            ('billing', 'Billing Issue'),
            ('feedback', 'Feedback'),
            ('other', 'Other')
        ],
        validators=[DataRequired(message='Please select a category')]
    )
    subject = StringField(
        'Subject',
        validators=[
            DataRequired(message='Subject is required'),
            Length(min=5, max=200, message='Subject must be 5-200 characters')
        ]
    )
    message = TextAreaField(
        'Message',
        validators=[
            DataRequired(message='Message is required'),
            Length(min=10, max=5000, message='Message must be 10-5000 characters')
        ]
    )
    submit = SubmitField('Submit Ticket')

class LoginForm(FlaskForm):
    """Form for admin login"""
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required'),
            Length(min=3, max=50, message='Username must be 3-50 characters')
        ]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message='Password is required')]
    )
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    """Form for admin registration"""
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required'),
            Length(min=3, max=50, message='Username must be 3-50 characters')
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required'),
            Length(min=6, message='Password must be at least 6 characters')
        ]
    )
    password_confirm = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message='Please confirm password'),
            EqualTo('password', message='Passwords must match')
        ]
    )
    submit = SubmitField('Register')
    
    def validate_username(self, field):
        """Check if username already exists"""
        if Admin.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')

class UpdateStatusForm(FlaskForm):
    """Form for updating ticket status"""
    status = SelectField(
        'Status',
        choices=[
            ('Open', 'Open'),
            ('In Progress', 'In Progress'),
            ('Closed', 'Closed')
        ],
        validators=[DataRequired(message='Status is required')]
    )
    submit = SubmitField('Update Status')
