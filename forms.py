"""
Form definitions for the Helpdesk System
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo, URL
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


class ChangePasswordForm(FlaskForm):
    """Form to allow an admin to update their password"""
    current_password = PasswordField(
        'Current Password',
        validators=[DataRequired(message='Current password is required')]
    )
    new_password = PasswordField(
        'New Password',
        validators=[
            DataRequired(message='New password is required'),
            Length(min=6, message='New password must be at least 6 characters')
        ]
    )
    confirm_password = PasswordField(
        'Confirm New Password',
        validators=[
            DataRequired(message='Please confirm your new password'),
            EqualTo('new_password', message='Passwords must match')
        ]
    )
    submit = SubmitField('Change Password')


class ContentItemForm(FlaskForm):
    """Generic form for services, blog posts, and gallery items"""
    title = StringField(
        'Title',
        validators=[DataRequired(message='Title is required'), Length(min=3, max=150)]
    )
    description = TextAreaField(
        'Description',
        validators=[DataRequired(message='Description is required'), Length(min=10, max=3000)]
    )
    image_url = StringField(
        'Image URL',
        validators=[Length(max=255), URL(require_tld=False, message='Invalid image URL')]
    )
    icon = StringField(
        'Icon',
        validators=[Length(max=100)]
    )
    submit = SubmitField('Save')


class EventForm(FlaskForm):
    """Form for timeline events"""
    title = StringField(
        'Title',
        validators=[DataRequired(message='Title is required'), Length(min=3, max=150)]
    )
    description = TextAreaField(
        'Description',
        validators=[DataRequired(message='Description is required'), Length(min=10, max=2000)]
    )
    event_date = StringField(
        'Event date',
        validators=[DataRequired(message='Event date is required')]
    )
    submit = SubmitField('Save Event')

    def validate_event_date(self, field):
        from datetime import datetime
        try:
            datetime.fromisoformat(field.data)
        except Exception:
            raise ValidationError('Event date must use ISO format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS')


class FeedbackForm(FlaskForm):
    """Form for customer feedback/testimonial"""
    name = StringField(
        'Name',
        validators=[DataRequired(message='Name is required'), Length(min=2, max=120)]
    )
    role = StringField(
        'Role', validators=[Length(max=120)])
    message = TextAreaField(
        'Feedback',
        validators=[DataRequired(message='Feedback is required'), Length(min=10, max=2000)]
    )
    rating = SelectField(
        'Rating',
        choices=[('5','5'), ('4','4'), ('3','3'), ('2','2'), ('1','1')],
        validators=[DataRequired(message='Rating is required')]
    )
    submit = SubmitField('Save Feedback')


class ContactForm(FlaskForm):
    """Form for website contact page"""
    name = StringField(
        'Name',
        validators=[DataRequired(message='Name is required'), Length(min=2, max=120)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(message='Email is required'), Email(message='Invalid email address')]
    )
    subject = StringField(
        'Subject',
        validators=[DataRequired(message='Subject is required'), Length(min=5, max=200)]
    )
    message = TextAreaField(
        'Message',
        validators=[DataRequired(message='Message is required'), Length(min=10, max=2500)]
    )
    submit = SubmitField('Send Message')


class SiteSettingsForm(FlaskForm):
    """Form for site basic control settings"""
    site_name = StringField(
        'Site name',
        validators=[DataRequired(message='Site name is required'), Length(min=2, max=120)]
    )
    logo_url = StringField(
        'Logo URL', validators=[Length(max=255), URL(require_tld=False, message='Invalid logo URL')])
    timezone = StringField(
        'Timezone', validators=[Length(max=80)])
    contact_email = StringField(
        'Contact email', validators=[Email(message='Invalid email address'), Length(max=120)])
    contact_phone = StringField(
        'Contact phone', validators=[Length(max=80)])
    hero_tagline = StringField(
        'Hero tagline', validators=[Length(max=220)])
    submit = SubmitField('Save Settings')
