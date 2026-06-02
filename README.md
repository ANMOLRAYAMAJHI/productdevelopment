# AI-Powered Customer Helpdesk System

## Project Overview

A Flask-based customer support helpdesk system with AI-powered sentiment analysis. The system automatically analyzes customer inquiries to determine sentiment and priority level, helping support teams efficiently manage tickets.

## Features

### Customer Features
- **Submit Support Tickets**: Customers can submit inquiries with category selection
- **Ticket Tracking**: Receive unique ticket ID for tracking
- **Real-time Feedback**: Immediate submission confirmation with ticket details

### Admin Features
- **Secure Login**: Protected admin panel with credential-based authentication
- **Dashboard**: Comprehensive view of all tickets with statistics
- **Ticket Management**: 
  - View ticket details
  - Update ticket status (Open → In Progress → Closed)
  - Search and filter functionality
- **AI Insights**: 
  - Sentiment analysis results per ticket
  - Automatic urgency detection
  - Priority visualization

### AI Features
- **Sentiment Analysis**: Automatically detects ticket sentiment (Positive/Neutral/Negative)
- **Automatic Priority Assignment**: Negative sentiment tickets are automatically marked as Urgent
- **Visual Indicators**: Color-coded priority levels for quick identification

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | Flask 2.3.3 |
| Frontend | HTML5, CSS3 (Bootstrap 5), JavaScript |
| Database | SQLite3 |
| AI/NLP | TextBlob |
| Forms | Flask-WTF |
| Server | Gunicorn (Production) |

## Project Structure

```
helpdesk_system/
├── app.py                 # Main Flask application
├── models.py              # Database models (Admin, Ticket)
├── forms.py               # WTForms form definitions
├── sentiment.py           # Sentiment analysis module
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── tests.py               # Unit and integration tests
│
├── static/
│   ├── css/
│   │   └── style.css      # Main stylesheet
│   ├── js/
│   │   └── main.js        # Client-side JavaScript
│   └── images/            # Image assets
│
├── templates/
│   ├── base.html          # Base template
│   ├── index.html         # Home page
│   ├── submit.html        # Submit ticket form
│   ├── success.html       # Success confirmation
│   ├── login.html         # Admin login
│   ├── register.html      # Admin registration
│   ├── dashboard.html     # Admin dashboard
│   ├── ticket_details.html # Ticket detail view
│   ├── update_status.html # Status update form
│   ├── 404.html           # 404 error page
│   └── 500.html           # 500 error page
│
└── database/
    └── helpdesk.db        # SQLite database (created on first run)
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd helpdesk_system
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
```bash
python app.py
```
The database will be created automatically on first run.

### Step 5: Run Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage Guide

### For Customers

1. **Submit a Ticket**:
   - Navigate to "Submit Ticket" page
   - Fill in your information and issue description
   - Select appropriate category
   - Submit the form
   - Receive confirmation with ticket ID

2. **Track Ticket Status**:
   - Use the ticket ID to reference your issue
   - Check email for updates (feature ready for email integration)

### For Admins

1. **First Time Setup**:
   - Navigate to `/register`
   - Create admin account (only available for first admin)
   - Login with credentials

2. **Dashboard Usage**:
   - View all tickets with status and sentiment
   - **Search**: Find tickets by name, email, or subject
   - **Filter**: Sort by status (Open, In Progress, Closed)
   - **Priority Color Coding**:
     - 🔴 Red: Urgent (Negative sentiment)
     - 🔵 Blue: Normal priority

3. **Manage Tickets**:
   - Click "View" to see full ticket details
   - Review AI sentiment analysis
   - Click "Change Status" to update ticket progress
   - Update customer via email (integration needed)

## Database Schema

### Admin Table
```sql
CREATE TABLE admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Ticket Table
```sql
CREATE TABLE ticket (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    subject VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    sentiment VARCHAR(20) DEFAULT 'Neutral',
    priority VARCHAR(20) DEFAULT 'Normal',
    status VARCHAR(20) DEFAULT 'Open',
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    admin_id INTEGER,
    FOREIGN KEY (admin_id) REFERENCES admin(id)
);
```

## API Endpoints

### Customer Routes
| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page |
| `/submit` | GET/POST | Submit ticket form |
| `/success` | GET | Submission confirmation |

### Admin Routes
| Route | Method | Description |
|-------|--------|-------------|
| `/login` | GET/POST | Admin login |
| `/register` | GET/POST | Register first admin |
| `/logout` | GET | Admin logout |
| `/dashboard` | GET | View all tickets |
| `/ticket/<id>` | GET | View ticket details |
| `/update-status/<id>` | GET/POST | Update ticket status |

### API Endpoints
| Route | Method | Description |
|-------|--------|-------------|
| `/api/tickets/stats` | GET | Get ticket statistics |
| `/api/tickets/sentiment` | GET | Get sentiment distribution |

## Testing

Run the test suite:
```bash
python -m pytest tests.py -v
# or
python -m unittest tests.py -v
```

### Test Coverage

**Unit Tests** (15+ test cases):
- Admin model and password hashing
- Ticket CRUD operations
- Sentiment analysis accuracy
- Form validation
- Database operations

**Integration Tests** (10+ test cases):
- Route accessibility
- Form submission and validation
- Admin authentication
- Ticket workflow
- Error handling

**User Acceptance Tests** (5+ scenarios):
- Complete customer ticket submission
- Admin ticket management workflow
- Sentiment-based priority assignment
- Dashboard functionality
- Search and filter operations

## Configuration

### Development Configuration
```python
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///database/helpdesk.db'
```

### Production Configuration
```python
DEBUG = False
SESSION_COOKIE_SECURE = True
```

Change configuration in `config.py` and set environment variable:
```bash
export FLASK_ENV=production
```

## Security Features

- ✅ Password hashing with SHA-256
- ✅ CSRF protection with Flask-WTF
- ✅ Session-based authentication
- ✅ Secure form validation
- ✅ SQL injection prevention via SQLAlchemy ORM
- ✅ XSS protection via Jinja2 templating

## Future Enhancements

1. **Email Integration**: Automated email notifications
2. **Advanced Analytics**: Ticket trends and performance metrics
3. **Multi-language Support**: Sentiment analysis in multiple languages
4. **Ticket Attachments**: File upload capability
5. **Real-time Chat**: Live support chat feature
6. **Mobile App**: Dedicated mobile application
7. **OAuth Integration**: Single sign-on support
8. **Database Migration**: Oracle/PostgreSQL support
9. **Advanced NLP**: Deep learning-based sentiment analysis
10. **Reporting**: Exportable reports and analytics

## Troubleshooting

### Database Not Found
```bash
# Delete the old database and restart
rm database/helpdesk.db
python app.py
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Port Already in Use
```bash
# Change port in app.py
app.run(debug=True, port=5001)
```

## Contributing

1. Create a feature branch
2. Make changes
3. Run tests
4. Submit pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please contact the development team or open an issue in the repository.

---

**Last Updated**: June 2026
**Version**: 1.0.0
