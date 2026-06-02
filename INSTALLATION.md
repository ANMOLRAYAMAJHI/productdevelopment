# Installation Guide

## System Requirements

- **Python**: 3.8 or higher
- **RAM**: 2GB minimum
- **Storage**: 500MB free space
- **OS**: Windows, macOS, or Linux

## Step-by-Step Installation

### 1. Install Python

**Windows:**
- Download from [python.org](https://www.python.org/downloads/)
- Run installer
- ✅ Check "Add Python to PATH"
- Click "Install Now"

**macOS:**
```bash
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3 python3-pip
```

### 2. Clone or Download Project

```bash
git clone <repository-url>
cd helpdesk_system
```

Or download and extract the ZIP file.

### 3. Create Virtual Environment

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

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask 2.3.3
- Flask-SQLAlchemy 3.0.5
- Flask-WTF 1.1.1
- TextBlob 0.17.1
- And more...

### 5. Initialize Database

```bash
python app.py
```

The database will be created automatically. You should see:
```
 * Running on http://localhost:5000
```

### 6. Access Application

Open browser and go to: **http://localhost:5000**

## Configuration

### Environment Variables (Optional)

Create `.env` file in root directory:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

Load variables in `app.py`:

```python
from dotenv import load_dotenv
load_dotenv()
```

## First-Time Admin Setup

1. Go to http://localhost:5000/register
2. Create admin account (only first admin can register)
3. Login with credentials
4. Access dashboard at http://localhost:5000/dashboard

## Testing Installation

```bash
# Run tests
python -m unittest tests.py -v

# Run specific test
python -m unittest tests.TestModels -v
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `pip: command not found` | Python not added to PATH, reinstall Python |
| `ModuleNotFoundError` | Activate virtual environment and reinstall requirements |
| `Port 5000 already in use` | Change port in `app.py`: `app.run(port=5001)` |
| `Database locked` | Delete `database/helpdesk.db` and restart |
| `Permission denied` | Run terminal as administrator (Windows) or use `sudo` (Linux/Mac) |

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Using Docker

```dockerfile
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w 4", "-b 0.0.0.0:8000", "app:app"]
```

Build and run:
```bash
docker build -t helpdesk .
docker run -p 8000:8000 helpdesk
```

## Updating Dependencies

```bash
pip install --upgrade -r requirements.txt
```

## Uninstalling

```bash
# Deactivate virtual environment
deactivate

# Delete virtual environment folder
rm -rf venv  # macOS/Linux
rmdir venv   # Windows
```
