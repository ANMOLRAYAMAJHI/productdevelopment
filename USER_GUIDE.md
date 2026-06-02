# User Guide

## For Customers

### Submitting a Support Ticket

#### Step 1: Navigate to Submit Ticket
- Click "Submit Ticket" from the home page navigation menu
- Or go directly to `/submit`

#### Step 2: Fill in Your Information

| Field | Requirements | Example |
|-------|--------------|---------|
| **Full Name** | 2-100 characters, required | John Doe |
| **Email Address** | Valid email format, required | john@example.com |
| **Category** | Select one from dropdown | Technical Support |
| **Subject** | 5-200 characters, required | Cannot login to account |
| **Message** | 10-5000 characters, required | I've been unable to login for 2 days... |

#### Step 3: Select Category

Available categories:
- 🔧 **Technical Support**: Issues with account, login, or features
- 💰 **Billing Issue**: Payment, refund, or subscription problems
- 📝 **General Inquiry**: General questions
- 💬 **Feedback**: Suggestions and comments
- ❓ **Other**: Anything else

#### Step 4: Submit Form

- Review your information
- Click "Submit Ticket" button
- You will be redirected to confirmation page

#### Step 5: Save Your Ticket ID

**Important**: Save the ticket ID displayed on the confirmation page. You'll need it to track your issue.

Example: **Ticket #12345**

### Understanding Your Ticket Status

| Status | Meaning | Timeline |
|--------|---------|----------|
| 🔵 **Open** | Your ticket received, waiting for review | 0-24 hours |
| 🟡 **In Progress** | Support team is working on your issue | 24-72 hours |
| 🟢 **Closed** | Issue resolved, check email for details | Completed |

### Tracking Your Ticket

#### Option 1: Email Notification
- You'll receive email updates at the address provided
- Updates include status changes and responses

#### Option 2: Using Ticket ID
- Use your ticket ID to reference your issue in follow-up communications
- Example: "Regarding Ticket #12345..."

### FAQ - Customer

**Q: How long does it take to get a response?**
A: Our average response time is 2 hours. Urgent tickets (marked based on sentiment) are prioritized.

**Q: Can I edit my ticket after submission?**
A: Contact support with your ticket ID to request modifications.

**Q: What if I forgot my ticket ID?**
A: Check your email confirmation. Your ticket ID is at the top of the confirmation page.

**Q: How do I know if my issue is urgent?**
A: Our AI system automatically marks negative or urgent-sounding issues as priority. You'll see this in your confirmation.

---

## For Admins

### Logging In

#### First Time Setup
1. Go to `/register`
2. Create admin account (only available for the first admin)
3. Username: Choose something memorable (3-50 characters)
4. Password: Use a strong password (minimum 6 characters)

#### Subsequent Logins
1. Go to `/login`
2. Enter username and password
3. Click "Login"
4. You'll be directed to the Dashboard

**Security Note**: Always log out after your session ends.

### Dashboard Overview

The admin dashboard shows:

#### Statistics Cards (Top of Dashboard)
- **Total Tickets**: All tickets in system
- **Open**: Waiting for review
- **In Progress**: Currently being worked on
- **Urgent**: Marked as urgent (high priority)

#### Search and Filter Section

**Search by:**
- Customer name
- Email address
- Subject or message keywords

**Filter by Status:**
- All Status (default)
- Open
- In Progress
- Closed

Example workflow:
1. Type "billing" in search box
2. Select "Open" from status filter
3. Click "Search"
4. View all open billing-related tickets

#### Tickets Table

| Column | Information |
|--------|-------------|
| **ID** | Unique ticket number |
| **Customer** | Customer name |
| **Subject** | Issue subject (truncated) |
| **Category** | Category selected |
| **Status** | Current status badge |
| **Priority** | Urgent or Normal |
| **Sentiment** | AI-detected sentiment |
| **Created** | Date ticket submitted |
| **Action** | "View" button |

### Ticket Management

#### Viewing Ticket Details

1. Click "View" button on any ticket
2. You'll see:
   - Full ticket information
   - Customer details and email
   - Complete message
   - AI sentiment analysis
   - Current status and priority

#### Changing Ticket Status

1. From ticket details page, click "Change Status"
2. Select new status from dropdown:
   - Open → In Progress (start working)
   - In Progress → Closed (resolved)
   - Or any status as needed
3. Click "Update Status"
4. Status will be updated immediately

**Workflow Example:**
```
Customer submits ticket (Open)
    ↓
Admin reviews ticket (Change to: In Progress)
    ↓
Admin resolves issue (Change to: Closed)
```

#### Understanding AI Analysis

On each ticket, you'll see:

**Sentiment Analysis:**
- 🟢 **Positive**: Customer is happy or satisfied
- 🟡 **Neutral**: Standard issue, no strong emotion
- 🔴 **Negative**: Customer is upset or frustrated

**Priority Assignment:**
- 🔴 **Urgent**: Automatically assigned for negative sentiment
- 🔵 **Normal**: Standard priority

**Tips:**
- Focus on Urgent tickets first
- Negative sentiment usually means faster response needed
- Use sentiment to gauge customer frustration level

### Pagination

If you have many tickets:
- Use "Next" / "Previous" buttons at bottom
- Or click specific page number
- Filters are maintained across pages

### Best Practices

#### For Efficient Ticket Management

1. **Start with Urgent**: 
   - Filter for Urgent priority first
   - Address negative sentiment tickets quickly

2. **Group by Status**:
   - View Open tickets to find new assignments
   - Check In Progress to follow up

3. **Use Search**:
   - Search for customer name if follow-up needed
   - Search for keywords to find related tickets

4. **Update Status Regularly**:
   - Keep ticket status current
   - Helps track what's being worked on

5. **Save Important Notes**:
   - Add personal notes before closing
   - Helps with future reference

### FAQ - Admin

**Q: How do I create additional admin accounts?**
A: Currently, only the first admin can be created at `/register`. Future versions will have admin management features.

**Q: Can I delete tickets?**
A: No, tickets are permanent records. You can only change status. This maintains audit trail.

**Q: How is sentiment determined?**
A: AI analyzes the message text using natural language processing. Words, tone, and context determine if sentiment is positive, neutral, or negative.

**Q: Why are some tickets marked Urgent?**
A: Tickets with negative sentiment are automatically marked Urgent by the AI system.

**Q: How do I contact a customer?**
A: Use the email address in the ticket to respond directly to the customer.

**Q: Can I export tickets?**
A: Export functionality is available in the production version. Currently, you can view and print individual tickets.

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + L` | Go to login page |
| `Ctrl + H` | Go to home page |
| `Ctrl + /` | Open help menu |

## Tips & Tricks

### For Customers
- Use clear subject lines (helps admin prioritization)
- Include specific details in message (helps faster resolution)
- Don't forget to save ticket ID
- Check spam folder for email updates

### For Admins
- Sort by sentiment to prioritize work
- Use date filters to find old tickets
- Maintain consistent status updates
- Check urgent tickets regularly

---

## Support

For additional help:
- Contact: support@helpdeskapp.com
- Documentation: See README.md
- API Reference: See API.md

**Last Updated**: June 2026
