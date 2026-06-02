# Development Guidelines

## Code Style Guide

### Python Code Style (PEP 8)

#### Naming Conventions

```python
# Classes: PascalCase
class AdminUser:
    pass

# Functions/Methods: snake_case
def get_ticket_count():
    pass

# Constants: UPPER_CASE
DATABASE_URL = 'sqlite:///helpdesk.db'

# Variables: snake_case
customer_email = 'john@example.com'

# Private methods: Leading underscore
def _internal_helper():
    pass
```

#### Line Length

- Maximum 100 characters
- 88 characters preferred for better readability
- Break long lines logically

```python
# Good
ticket = Ticket.query.filter_by(
    status='Open',
    priority='Urgent'
).first()

# Avoid
ticket = Ticket.query.filter_by(status='Open', priority='Urgent').first()
```

#### Imports

```python
# Standard library imports
import os
import sys
from datetime import datetime

# Third-party imports
from flask import Flask, render_template, request

# Local imports
from models import db, Admin, Ticket
from forms import TicketForm
from sentiment import SentimentAnalyzer
```

#### Docstrings

```python
def get_ticket_stats(status=None):
    """
    Get ticket statistics.
    
    Args:
        status (str, optional): Filter by status. Defaults to None.
        
    Returns:
        dict: Dictionary with ticket counts.
        
    Raises:
        ValueError: If status is invalid.
        
    Example:
        >>> stats = get_ticket_stats('Open')
        >>> print(stats['total'])
    """
    pass
```

#### Comments

```python
# Use comments sparingly - code should be self-documenting
# Good comment explains WHY, not WHAT

# Bad: Increment counter
counter += 1

# Good: Skip urgent tickets as they're processed separately
counter += 1
```

---

## Project Structure

### Folder Organization

```
helpdesk_system/
├── core/                      # Core application logic
│   ├── models.py
│   ├── forms.py
│   ├── sentiment.py
│   └── errors.py             # Custom exceptions
│
├── admin/                     # Admin routes
│   ├── routes.py
│   ├── utils.py
│   └── decorators.py
│
├── customer/                  # Customer routes
│   ├── routes.py
│   └── utils.py
│
├── api/                       # API endpoints
│   └── routes.py
│
├── static/                    # Static files
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/                 # Jinja2 templates
│   ├── base.html
│   ├── admin/
│   └── customer/
│
├── tests/                     # Test files
│   ├── test_models.py
│   ├── test_forms.py
│   ├── test_sentiment.py
│   └── test_routes.py
│
├── config.py                  # Configuration
├── app.py                     # Application factory
└── requirements.txt           # Dependencies
```

---

## Git Workflow

### Branch Naming

```
feature/feature-name           # New feature
bugfix/issue-description       # Bug fix
hotfix/critical-issue          # Critical production fix
release/version-number         # Release branch
docs/documentation-update      # Documentation
```

### Commit Messages

```
# Format: [TYPE] Short description (50 chars max)
# 
# Longer explanation if needed (72 chars per line)

# Good
[FEATURE] Add sentiment analysis to tickets
[BUGFIX] Fix password hashing in admin login
[DOCS] Update installation guide

# Bad
fixed stuff
updated code
changes
```

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing done

## Checklist
- [ ] Code follows style guide
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No new warnings generated
```

---

## Testing Guidelines

### Test Organization

```python
class TestTicketModel(unittest.TestCase):
    """Tests for Ticket model"""
    
    def setUp(self):
        """Set up test fixtures"""
        pass
    
    def tearDown(self):
        """Clean up after test"""
        pass
    
    def test_ticket_creation(self):
        """Test creating a ticket"""
        pass
    
    def test_invalid_ticket_data(self):
        """Test with invalid data"""
        pass
```

### Test Naming

```python
# Format: test_[method_name]_[condition]_[expected_result]

# Good
def test_admin_password_hashing_valid_password_returns_hashed():
    pass

def test_ticket_submission_missing_email_returns_validation_error():
    pass

# Bad
def test_password():
    pass

def test_form():
    pass
```

### Coverage Goals

| Module | Target |
|--------|--------|
| Models | 95% |
| Forms | 90% |
| Sentiment | 100% |
| Routes | 85% |
| Overall | 85% |

---

## Database Guidelines

### Migrations

```python
# Use Flask-Migrate for production
from flask_migrate import Migrate, init_db, migrate, upgrade

# For development (current):
with app.app_context():
    db.create_all()
```

### Query Best Practices

```python
# Good: Use ORM for queries
ticket = Ticket.query.filter_by(id=1).first()

# Avoid: Raw SQL
ticket = db.session.execute('SELECT * FROM ticket WHERE id=1')

# Good: Use relationships
tickets = admin.tickets  # Through relationship

# Avoid: N+1 queries
for ticket in Ticket.query.all():
    print(ticket.admin.username)  # N queries!

# Better: Use join
tickets = Ticket.query.join(Admin).all()
```

---

## API Development Guidelines

### Response Format

```python
def get_tickets():
    """Get all tickets"""
    tickets = Ticket.query.all()
    return jsonify({
        'status': 'success',
        'data': [t.to_dict() for t in tickets],
        'count': len(tickets)
    })
```

### Error Responses

```python
def update_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    
    if not ticket:
        return jsonify({
            'status': 'error',
            'message': 'Ticket not found'
        }), 404
    
    # Update logic...
    return jsonify({'status': 'success'}), 200
```

---

## Performance Guidelines

### Database Optimization

```python
# Use indexing for frequently queried fields
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    status = db.Column(db.String(20), index=True)
    created_date = db.Column(db.DateTime, index=True)

# Use pagination for large datasets
tickets = Ticket.query.paginate(page=1, per_page=10)

# Use eager loading to avoid N+1
tickets = Ticket.query.options(
    joinedload('admin')
).all()
```

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_ticket_stats():
    """Cache ticket statistics"""
    return {
        'total': Ticket.query.count(),
        'urgent': Ticket.query.filter_by(priority='Urgent').count()
    }
```

---

## Security Guidelines

### Input Validation

```python
# Always validate user input
from wtforms.validators import DataRequired, Email, Length

email = StringField('Email', validators=[
    DataRequired(),
    Email(message='Invalid email')
])
```

### Output Escaping

```python
# Jinja2 automatically escapes output
{{ ticket.message }}  # Safe: HTML entities escaped

# Use |safe only when necessary
{{ safe_html | safe }}
```

### CSRF Protection

```python
# All forms automatically protected by Flask-WTF
{{ form.hidden_tag() }}

# Verify token in API
from flask_wtf.csrf import csrf_token
csrf_token()
```

### Password Hashing

```python
# Use secure hashing algorithm
def set_password(self, password):
    # Instead of SHA256, consider bcrypt
    import bcrypt
    self.password = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    )
```

---

## Logging Guidelines

```python
import logging

logger = logging.getLogger(__name__)

# Log levels
logger.debug('Debug information')      # Development
logger.info('User action performed')   # General info
logger.warning('Unexpected behavior')  # Warnings
logger.error('Error occurred')         # Errors
logger.critical('Critical failure')    # Critical
```

---

## Documentation Guidelines

### Code Documentation

```python
"""Module docstring: High-level description"""

def function_name(param1, param2):
    """
    Brief description of function.
    
    Longer description if needed, explaining the
    purpose and behavior in detail.
    
    Args:
        param1 (str): Description of param1
        param2 (int): Description of param2
        
    Returns:
        bool: True if successful, False otherwise
        
    Raises:
        ValueError: If param1 is empty
        
    Example:
        >>> result = function_name('test', 42)
        >>> print(result)
        True
    """
    pass
```

### README Structure

```markdown
# Project Name

## Overview
Brief description

## Installation
Step-by-step setup

## Usage
How to use the application

## Architecture
System design overview

## API Documentation
Endpoint documentation

## Testing
How to run tests

## Troubleshooting
Common issues and solutions

## Contributing
How to contribute

## License
License information
```

---

## Debugging Tips

### Flask Debugging

```python
# Enable debug mode
app.run(debug=True)

# Add breakpoints
import pdb
pdb.set_trace()

# Use Flask shell
flask shell

# Check routes
for rule in app.url_map.iter_rules():
    print(rule)
```

### Database Debugging

```python
# Check database state
with app.app_context():
    tickets = Ticket.query.all()
    for ticket in tickets:
        print(ticket.to_dict())

# Monitor queries
from flask_sqlalchemy import get_debug_queries
print(get_debug_queries())
```

---

## Review Checklist

Before submitting code:

- [ ] Code follows PEP 8 style guide
- [ ] Variable names are descriptive
- [ ] Functions have docstrings
- [ ] Code is DRY (Don't Repeat Yourself)
- [ ] Error handling is implemented
- [ ] Tests are included and passing
- [ ] No debug prints or breakpoints
- [ ] Documentation is updated
- [ ] Security best practices followed
- [ ] Performance optimized
- [ ] No hard-coded values

---

## Tools & Setup

### Recommended IDE Extensions

- Python Linter (pylint)
- Code Formatter (black)
- Test Runner (pytest)
- Git extension

### Pre-commit Hooks

```bash
# Install
pip install pre-commit

# Create .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

---

**Last Updated**: June 2026
