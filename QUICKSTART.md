# Quick Start Guide

Get the AI-Powered Customer Helpdesk System running in 5 minutes!

## Prerequisites

- **Python 3.8+** installed ([Download](https://www.python.org/downloads/))
- **Git** installed ([Download](https://git-scm.com/))
- **Command line** access (Terminal on macOS/Linux, CMD/PowerShell on Windows)

---

## 5-Minute Setup

### Step 1: Clone Project (30 seconds)

```bash
git clone <repository-url>
cd helpdesk_system
```

Or download and extract the ZIP file.

### Step 2: Create Virtual Environment (1 minute)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies (2 minutes)

```bash
pip install -r requirements.txt
```

### Step 4: Start Application (1 minute)

```bash
python app.py
```

You should see:
```
 * Running on http://localhost:5000 (Press CTRL+C to quit)
```

### Step 5: Access Application (30 seconds)

1. Open browser
2. Go to: **http://localhost:5000**
3. You're done! 🎉

---

## First Test

### Test 1: Submit a Customer Ticket

1. Click "Submit Ticket"
2. Fill in the form:
   - **Name**: John Doe
   - **Email**: john@example.com
   - **Category**: Technical Support
   - **Subject**: Test Ticket
   - **Message**: This is a test message for testing the helpdesk system.
3. Click "Submit Ticket"
4. You'll see confirmation with Ticket ID

**✅ Customer feature works!**

### Test 2: Admin Dashboard

1. Go to http://localhost:5000/register
2. Create admin account:
   - **Username**: admin
   - **Password**: password123
   - **Confirm**: password123
3. Click "Register"
4. Go to http://localhost:5000/login
5. Login with credentials
6. You'll see dashboard with your ticket

**✅ Admin feature works!**

---

## Common Tasks

### View Ticket Details

1. From dashboard, click "View" on any ticket
2. See full details and AI sentiment analysis
3. Change status if needed

### Search Tickets

1. Enter search term (name, email, or subject)
2. Select status filter
3. Click "Search"

### Update Ticket Status

1. View ticket details
2. Click "Change Status"
3. Select new status
4. Click "Update Status"

### Logout

1. Click "Logout" button in top right
2. You'll be redirected to home page

---

## Troubleshooting

### "Port 5000 already in use"

```bash
# Change port in app.py
app.run(debug=True, port=5001)

# Then access: http://localhost:5001
```

### "ModuleNotFoundError"

```bash
# Make sure virtual environment is activated
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Then run:
pip install -r requirements.txt
```

### "Database locked" error

```bash
# Delete the database and restart
rm database/helpdesk.db
python app.py
```

---

## Project Structure at a Glance

```
helpdesk_system/
├── app.py                 ← Main application
├── models.py              ← Database models
├── forms.py               ← Forms
├── sentiment.py           ← AI sentiment analysis
├── config.py              ← Settings
├── tests.py               ← Tests
├── requirements.txt       ← Dependencies
├── templates/             ← HTML pages
│   ├── base.html
│   ├── index.html
│   ├── submit.html
│   ├── login.html
│   ├── dashboard.html
│   └── ...
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── images/
└── database/              ← SQLite database (created on first run)
```

---

## Next Steps

### Learn More

- **Full Installation Guide**: See [INSTALLATION.md](INSTALLATION.md)
- **User Guide**: See [USER_GUIDE.md](USER_GUIDE.md)
- **API Reference**: See [API.md](API.md)
- **Project Overview**: See [README.md](README.md)

### Run Tests

```bash
python -m unittest tests.py -v
```

### Deploy to Production

See [DEPLOYMENT.md](DEPLOYMENT.md)

---

## Tips & Tricks

### Faster Development

1. Use `flask --app app run` for auto-reload
2. Enable debug mode in `config.py`
3. Use `flask shell` for interactive debugging

### Testing Different Sentiments

Create tickets with different messages to test AI analysis:

| Message | Expected Sentiment | Priority |
|---------|-------------------|----------|
| "This is amazing!" | Positive | Normal |
| "The system is broken" | Negative | Urgent |
| "It works fine" | Neutral | Normal |

### Database Backup

```bash
# Copy database
cp database/helpdesk.db database/helpdesk_backup.db

# Delete to reset
rm database/helpdesk.db
python app.py  # Creates new database
```

---

## Key Features Explained

### 🎫 Ticket Submission
Customers submit inquiries with category, subject, and detailed message.

### 🤖 AI Sentiment Analysis
Automatically detects sentiment (Positive/Neutral/Negative) of each ticket.

### 🚨 Auto Priority Assignment
Negative sentiment tickets automatically marked as URGENT in red.

### 📊 Admin Dashboard
View all tickets with search, filter, and statistics.

### 🔐 Secure Authentication
Admin login with hashed passwords.

### 📱 Mobile Responsive
Works on desktop, tablet, and mobile devices.

---

## Performance

**Typical response times:**
- Home page: < 500ms
- Submit ticket: < 1s
- Dashboard load: < 1s
- Search/filter: < 500ms

---

## Support

### Documentation
- [README.md](README.md) - Project overview
- [USER_GUIDE.md](USER_GUIDE.md) - How to use
- [API.md](API.md) - API endpoints
- [TESTING.md](TESTING.md) - Testing guide

### Troubleshooting
- Check [INSTALLATION.md](INSTALLATION.md#troubleshooting) for common issues
- See [README.md](README.md#troubleshooting) for FAQs

### Contact
- GitHub Issues: Report bugs and feature requests
- Email: support@helpdesk-system.com

---

## Next Steps After Running

1. ✅ **Test the application** - Submit a ticket and manage it
2. 📖 **Read documentation** - Understand features and usage
3. ✏️ **Customize** - Modify colors, text, categories
4. 🧪 **Run tests** - Verify functionality with `python -m unittest tests.py`
5. 🚀 **Deploy** - Follow [DEPLOYMENT.md](DEPLOYMENT.md) for production setup

---

## Quick Reference

| Task | Command |
|------|---------|
| Start app | `python app.py` |
| Run tests | `python -m unittest tests.py -v` |
| Reset database | `rm database/helpdesk.db` |
| Activate venv (Windows) | `venv\Scripts\activate` |
| Activate venv (Mac/Linux) | `source venv/bin/activate` |
| Install dependencies | `pip install -r requirements.txt` |
| Exit app | `CTRL+C` |

---

**Happy coding! 🚀**

**Last Updated**: June 2026
