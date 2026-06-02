# API Documentation

## Overview

This document describes all API endpoints available in the AI-Powered Customer Helpdesk System.

## Base URL

```
http://localhost:5000
```

## Authentication

Most endpoints require admin authentication via Flask sessions. The admin must be logged in and have an active session.

## Response Format

All responses are in JSON format (except HTML template responses).

### Success Response
```json
{
    "status": "success",
    "data": { ... },
    "message": "Operation completed"
}
```

### Error Response
```json
{
    "status": "error",
    "message": "Description of error"
}
```

---

## Customer API

### 1. Submit Ticket

**Endpoint**: `POST /submit`

**Description**: Submit a new support ticket

**Request Headers**:
```
Content-Type: application/x-www-form-urlencoded
```

**Request Body**:
```json
{
    "customer_name": "John Doe",
    "email": "john@example.com",
    "category": "technical",
    "subject": "Cannot login",
    "message": "I cannot access my account..."
}
```

**Parameters**:

| Name | Type | Required | Validation |
|------|------|----------|-----------|
| customer_name | string | Yes | 2-100 chars |
| email | string | Yes | Valid email |
| category | string | Yes | One of: general, technical, billing, feedback, other |
| subject | string | Yes | 5-200 chars |
| message | string | Yes | 10-5000 chars |

**Success Response** (Redirect to /success):
```
Status: 302 Found
Location: /success
```

**Error Response**:
```
Status: 200 OK
Returns form with validation errors
```

**Example**:
```bash
curl -X POST http://localhost:5000/submit \
  -d "customer_name=John Doe" \
  -d "email=john@example.com" \
  -d "category=technical" \
  -d "subject=Login Issue" \
  -d "message=I cannot login to my account"
```

---

### 2. Success Page

**Endpoint**: `GET /success`

**Description**: Display ticket submission confirmation

**Parameters**: None (uses session variable)

**Response**:
```
Status: 200 OK
HTML page with ticket ID and details
```

---

## Admin API

### 1. Admin Login

**Endpoint**: `POST /login`

**Description**: Authenticate admin user

**Request Body**:
```json
{
    "username": "admin",
    "password": "password123"
}
```

**Success Response** (Redirect to dashboard):
```
Status: 302 Found
Location: /dashboard
Sets session cookie
```

**Error Response**:
```
Status: 200 OK
Returns login form with error message
```

**Example**:
```bash
curl -X POST http://localhost:5000/login \
  -d "username=admin" \
  -d "password=password123"
```

---

### 2. Admin Logout

**Endpoint**: `GET /logout`

**Description**: Logout current admin user

**Parameters**: None

**Response**:
```
Status: 302 Found
Location: /
Clears session cookie
```

---

### 3. Register Admin

**Endpoint**: `POST /register`

**Description**: Create first admin account (only available when no admins exist)

**Request Body**:
```json
{
    "username": "admin",
    "password": "password123",
    "password_confirm": "password123"
}
```

**Success Response**:
```
Status: 302 Found
Location: /login
```

**Error Response**:
```
Status: 200 OK
Returns register form with validation errors
```

---

### 4. View Dashboard

**Endpoint**: `GET /dashboard`

**Description**: Get admin dashboard with tickets list

**Parameters** (Query String):
```
?page=1
&status=Open
&search=keyword
```

| Name | Type | Default | Options |
|------|------|---------|---------|
| page | integer | 1 | 1+ |
| status | string | All | Open, In Progress, Closed |
| search | string | Empty | Any keyword |

**Response**:
```
Status: 200 OK
HTML page with tickets table and statistics
```

**Authentication**: Required (session admin_id)

**Example**:
```bash
curl -X GET "http://localhost:5000/dashboard?status=Open&page=1" \
  -H "Cookie: session=<session_id>"
```

---

### 5. View Ticket Details

**Endpoint**: `GET /ticket/<ticket_id>`

**Description**: Get detailed information about a specific ticket

**URL Parameters**:

| Name | Type | Description |
|------|------|-------------|
| ticket_id | integer | Ticket ID (required) |

**Response**:
```
Status: 200 OK
HTML page with ticket details and AI analysis
```

**Error Response**:
```
Status: 404 Not Found
If ticket doesn't exist
```

**Authentication**: Required

**Example**:
```bash
curl -X GET "http://localhost:5000/ticket/123" \
  -H "Cookie: session=<session_id>"
```

---

### 6. Update Ticket Status

**Endpoint**: `POST /update-status/<ticket_id>`

**Description**: Update status of a specific ticket

**URL Parameters**:

| Name | Type | Description |
|------|------|-------------|
| ticket_id | integer | Ticket ID (required) |

**Request Body**:
```json
{
    "status": "In Progress"
}
```

**Status Options**:
- Open
- In Progress
- Closed

**Success Response**:
```
Status: 302 Found
Location: /ticket/<ticket_id>
```

**Error Response**:
```
Status: 400 Bad Request
{
    "error": "Invalid status value"
}
```

**Authentication**: Required

**Example**:
```bash
curl -X POST "http://localhost:5000/update-status/123" \
  -d "status=In Progress" \
  -H "Cookie: session=<session_id>"
```

---

## Data API

### 1. Get Ticket Statistics

**Endpoint**: `GET /api/tickets/stats`

**Description**: Get ticket count statistics

**Response**:
```json
{
    "total": 45,
    "open": 12,
    "in_progress": 8,
    "closed": 25,
    "urgent": 5
}
```

**Status Code**: 200 OK

**Authentication**: Required

**Example**:
```bash
curl -X GET "http://localhost:5000/api/tickets/stats" \
  -H "Accept: application/json" \
  -H "Cookie: session=<session_id>"
```

---

### 2. Get Sentiment Distribution

**Endpoint**: `GET /api/tickets/sentiment`

**Description**: Get sentiment analysis statistics

**Response**:
```json
{
    "positive": 8,
    "neutral": 22,
    "negative": 15
}
```

**Status Code**: 200 OK

**Authentication**: Required

**Example**:
```bash
curl -X GET "http://localhost:5000/api/tickets/sentiment" \
  -H "Accept: application/json" \
  -H "Cookie: session=<session_id>"
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 302 | Found - Redirect (login, etc.) |
| 400 | Bad Request - Invalid data |
| 401 | Unauthorized - Login required |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

---

## Rate Limiting

Currently no rate limiting is implemented. In production, implement:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

---

## Data Models

### Ticket Object

```json
{
    "id": 1,
    "customer_name": "John Doe",
    "email": "john@example.com",
    "category": "technical",
    "subject": "Cannot login",
    "message": "I cannot access my account...",
    "sentiment": "Negative",
    "priority": "Urgent",
    "status": "Open",
    "created_date": "2024-06-01 14:30:00",
    "updated_date": "2024-06-01 14:30:00"
}
```

### Admin Object

```json
{
    "id": 1,
    "username": "admin",
    "created_date": "2024-06-01 10:00:00"
}
```

---

## Code Examples

### JavaScript/Fetch

```javascript
// Get statistics
fetch('/api/tickets/stats')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));

// Update ticket status
fetch('/update-status/123', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: 'status=In Progress'
})
.then(response => {
    if (response.redirected) {
        window.location.href = response.url;
    }
})
.catch(error => console.error('Error:', error));
```

### Python/Requests

```python
import requests

# Login
session = requests.Session()
login_data = {
    'username': 'admin',
    'password': 'password123'
}
response = session.post('http://localhost:5000/login', data=login_data)

# Get statistics
response = session.get('http://localhost:5000/api/tickets/stats')
stats = response.json()
print(f"Total tickets: {stats['total']}")
print(f"Urgent tickets: {stats['urgent']}")
```

### cURL

```bash
# Login
curl -c cookies.txt -X POST http://localhost:5000/login \
  -d "username=admin&password=password123"

# Get stats
curl -b cookies.txt http://localhost:5000/api/tickets/stats

# Submit ticket
curl -X POST http://localhost:5000/submit \
  -d "customer_name=John&email=john@example.com&category=technical&subject=Test&message=Test message"
```

---

## Future API Enhancements

- [ ] RESTful API for all operations
- [ ] JWT authentication
- [ ] Rate limiting
- [ ] Pagination with cursors
- [ ] Bulk operations
- [ ] Webhook support
- [ ] GraphQL endpoint
- [ ] API versioning
- [ ] OpenAPI/Swagger documentation

---

**Last Updated**: June 2026
**API Version**: 1.0.0
