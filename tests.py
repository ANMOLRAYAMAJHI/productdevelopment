"""
Unit Tests for the Helpdesk System
Tests for models and core functionality
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from models import Admin, Ticket
from sentiment import SentimentAnalyzer
from config import TestingConfig

class TestModels(unittest.TestCase):
    """Test database models"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_admin_password_hashing(self):
        """Test that admin passwords are hashed"""
        admin = Admin(username='testadmin')
        admin.set_password('password123')
        
        self.assertNotEqual(admin.password, 'password123')
        self.assertTrue(admin.check_password('password123'))
        self.assertFalse(admin.check_password('wrongpassword'))
    
    def test_ticket_creation(self):
        """Test creating a ticket"""
        ticket = Ticket(
            customer_name='John Doe',
            email='john@example.com',
            category='technical',
            subject='Cannot login',
            message='I cannot login to my account',
            sentiment='Negative',
            priority='Urgent',
            status='Open'
        )
        
        db.session.add(ticket)
        db.session.commit()
        
        self.assertEqual(ticket.id, 1)
        self.assertEqual(ticket.customer_name, 'John Doe')
        self.assertEqual(ticket.status, 'Open')
    
    def test_ticket_to_dict(self):
        """Test converting ticket to dictionary"""
        ticket = Ticket(
            customer_name='Jane Doe',
            email='jane@example.com',
            category='billing',
            subject='Refund request',
            message='I need a refund',
            sentiment='Positive',
            priority='Normal',
            status='Closed'
        )
        
        ticket_dict = ticket.to_dict()
        
        self.assertEqual(ticket_dict['customer_name'], 'Jane Doe')
        self.assertEqual(ticket_dict['email'], 'jane@example.com')
        self.assertIn('created_date', ticket_dict)

class TestSentimentAnalysis(unittest.TestCase):
    """Test sentiment analysis functionality"""
    
    def test_positive_sentiment(self):
        """Test detection of positive sentiment"""
        result = SentimentAnalyzer.analyze('This is amazing! I love it!')
        self.assertEqual(result['sentiment'], 'Positive')
    
    def test_negative_sentiment(self):
        """Test detection of negative sentiment"""
        result = SentimentAnalyzer.analyze('This is terrible! I hate it!')
        self.assertEqual(result['sentiment'], 'Negative')
    
    def test_neutral_sentiment(self):
        """Test detection of neutral sentiment"""
        result = SentimentAnalyzer.analyze('The service was okay.')
        self.assertEqual(result['sentiment'], 'Neutral')
    
    def test_empty_text(self):
        """Test handling of empty text"""
        result = SentimentAnalyzer.analyze('')
        self.assertEqual(result['sentiment'], 'Neutral')
    
    def test_priority_from_sentiment(self):
        """Test priority assignment based on sentiment"""
        urgent = SentimentAnalyzer.get_priority('Negative')
        normal = SentimentAnalyzer.get_priority('Positive')
        
        self.assertEqual(urgent, 'Urgent')
        self.assertEqual(normal, 'Normal')

class TestRoutes(unittest.TestCase):
    """Test Flask routes and views"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_index_page(self):
        """Test home page loads"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)
    
    def test_submit_ticket_page(self):
        """Test submit ticket page loads"""
        response = self.client.get('/submit')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Support Ticket', response.data)
    
    def test_login_page(self):
        """Test login page loads"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
    
    def test_submit_valid_ticket(self):
        """Test submitting a valid ticket"""
        data = {
            'customer_name': 'Test User',
            'email': 'test@example.com',
            'category': 'technical',
            'subject': 'Test Subject',
            'message': 'This is a test message for testing purposes'
        }
        
        response = self.client.post('/submit', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Check that ticket was created
        ticket = Ticket.query.first()
        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.customer_name, 'Test User')
    
    def test_submit_invalid_ticket(self):
        """Test submitting invalid ticket data"""
        data = {
            'customer_name': '',  # Invalid - required
            'email': 'invalid-email',  # Invalid - bad format
            'category': 'technical',
            'subject': 'Test',  # Too short
            'message': 'Short'  # Too short
        }
        
        response = self.client.post('/submit', data=data)
        self.assertEqual(response.status_code, 200)
        
        # Check that no ticket was created
        ticket = Ticket.query.first()
        self.assertIsNone(ticket)
    
    def test_404_page(self):
        """Test 404 error page"""
        response = self.client.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
