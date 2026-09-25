# FESTIVE G - Architecture Documentation

## Overview

FESTIVE G is a lightweight web application for sending personalized festival greetings. Users can browse festivals, submit recipient details, and the system handles email delivery and admin management. The application is built with Python's built-in HTTP server and requires no external web framework dependencies.

## Project Structure

```
festive-g/
├── app.py                 # Main application (HTTP server + all logic)
├── templates/             # HTML templates for rendering pages
│   ├── welcome.html       # Home page
│   ├── festivals.html     # Festival listing page
│   ├── festival_detail.html
│   ├── user_info.html     # User greeting form
│   ├── admin_login.html   # Admin login
│   ├── admin_submissions.html
│   ├── admin_festival_edit.html
│   └── admin_festivals.html
├── static/                # Static assets
│   ├── styles.css         # Styling
│   └── images/            # Festival images
├── data/                  # Data storage (auto-created)
│   ├── festivals.json     # Festival definitions
│   └── submissions.csv    # Greeting submissions log
├── requirements.txt       # Dependencies (if any)
├── README.md              # Project overview
└── .env.example           # Environment variables template
```

## Core Components

### 1. **Data Management Layer**

#### Festival Storage (JSON-based)
```
load_festivals()      → Reads festivals.json, initializes defaults if missing
save_festivals(list)  → Persists festival data to JSON
find_festival(slug)   → Searches for festival by slug identifier
ensure_data_files()   → Creates data/ directory and initializes files
```

**Data Structure:**
```json
{
  "slug": "diwali",
  "title": "Diwali",
  "content": "Detailed festival information..."
}
```

**Includes 10 default Indian festivals:** Diwali, Holi, Navratri, Dussehra, Janmashtami, Ganesh Chaturthi, Maha Shivaratri, Ram Navami, Janma Divas, Makar Sankranti

#### Submission Storage (CSV-based)
```
append_submission(dict) → Logs user submissions to CSV
load_submissions()      → Reads all submissions from CSV
```

**Fields Tracked:** submitted_at, sender_name, sender_email, receiver_name, receiver_email, receiver_address, email_status

### 2. **HTTP Request Handler (FestiveGHandler)**

The main request router that extends `BaseHTTPRequestHandler`:

#### GET Routes
| Route | Handler | Purpose |
|-------|---------|---------|
| `/` `/welcome` | `do_GET` | Home page |
| `/festivals` | Lists all festivals in tab navigation |
| `/festival/{slug}` | Shows festival detail page with content |
| `/user-info` | Greeting submission form |
| `/admin` | Admin login page (redirects if authenticated) |
| `/admin/submissions` | Admin dashboard - view all submissions |
| `/admin/festivals` | Admin dashboard - manage festivals |
| `/admin/festival/{slug}/edit` | Edit individual festival content |
| `/static/*` | Serves CSS and images |

#### POST Routes
| Route | Purpose |
|-------|---------|
| `/user-info` | Process greeting submission → validate → email → save |
| `/admin/login` | Authenticate and create session cookie |
| `/admin/logout` | Clear session |
| `/admin/festival/{slug}/edit` | Update festival content |

### 3. **Rendering & Templating**

Simple string replacement system:
```python
render_page("welcome.html", tabs=festival_tabs())
# Replaces {{ tabs }} with actual content
```

Key rendering functions:
- `render_page(template_name, **kwargs)` - Basic templating
- `render_user_info()` - Greeting form with error/success messages
- `render_admin_login()` - Admin authentication form
- `render_admin_submissions()` - Submission table
- `render_admin_festivals()` - Festival management interface
- `festival_tabs(active_slug)` - Navigation tabs with active highlighting

### 4. **Validation & Security**

#### User Form Validation
```
validate_user_form(form)
├── Required fields: sender_name, sender_email, receiver_name, 
│                    receiver_email, receiver_address
├── Email validation: RFC-like pattern matching
├── Length limits: Names (≤80 chars), Address (10-300 chars)
└── Returns: List of error messages (empty if valid)
```

#### Admin Authentication
- Session-based using secure HTTP-only cookies
- Credentials: `ADMIN_USERNAME` & `ADMIN_PASSWORD` (env vars)
- Token storage: In-memory dictionary (lost on server restart)
- Secure password comparison using `secrets.compare_digest()`

#### Input Sanitization
- `escape()` - HTML escapes all user input
- Path traversal protection in static file serving (`is_relative_to()`)

### 5. **Email Integration**

```
send_greeting_email(submission_data)
├── Configuration: 5 environment variables
│   ├── FESTIVE_G_SMTP_HOST (required)
│   ├── FESTIVE_G_SMTP_PORT (default: 587)
│   ├── FESTIVE_G_SMTP_USER
│   ├── FESTIVE_G_SMTP_PASSWORD
│   └── FESTIVE_G_EMAIL_FROM (defaults to sender email)
├── TLS Support: FESTIVE_G_SMTP_TLS (default: true)
└── Returns: Status message (success or configuration error)
```

**Email Flow:**
1. User submits greeting form
2. Form validates (required fields, length, format)
3. Email sends (if SMTP configured)
4. Submission logged to CSV with email status
5. User sees thank you message

### 6. **Utility Functions**

| Function | Purpose |
|----------|---------|
| `escape(value)` | HTML entity escaping |
| `read_template(name)` | Load HTML template file |
| `send_html(handler, page, status, headers)` | Send HTML response |
| `redirect(handler, location)` | Send 303 redirect |
| `parse_form(handler)` | Parse multipart form data |
| `get_cookie(headers, name)` | Extract cookie value |
| `content_to_html(text)` | Convert line breaks to `<p>` tags |
| `error_list(errors)` | Format errors for HTML display |
| `success_message(msg)` | Format success message for HTML |

## Data Flow Diagram

```
User Submission Flow:
┌─────────────────────────────────┐
│ User visits /user-info          │
└────────────┬────────────────────┘
             │
             ├─→ render_user_info() → display form
             │
    ┌────────▼─────────────┐
    │ User submits form    │
    └────────┬─────────────┘
             │
    ┌────────▼──────────────────────┐
    │ validate_user_form()          │
    │ - Check required fields       │
    │ - Validate emails & lengths   │
    └────────┬──────────────────────┘
             │
        ┌────┴────┐
        │          │
       NO         YES (valid)
        │          │
        │    ┌─────▼──────────────────┐
    Return  │ send_greeting_email()   │
    Error   │ (if SMTP configured)    │
            └────────┬─────────────────┘
                     │
                ┌────▼─────────────────┐
                │ append_submission()  │
                │ (save to CSV)        │
                └────┬────────────────┘
                     │
            ┌────────▼──────────────┐
            │ Render thank you page │
            └───────────────────────┘
```

```
Festival Management Flow:
┌─────────────────────┐
│ Admin logs in       │
│ (/admin/login)      │
└────────┬────────────┘
         │
    ┌────▼──────────────────────┐
    │ Verify credentials        │
    │ Create session token      │
    │ Set HttpOnly cookie       │
    └────┬───────────────────────┘
         │
    ┌────▼──────────────────────┐
    │ Access admin dashboard    │
    │ /admin/submissions        │
    │ /admin/festivals          │
    └────┬───────────────────────┘
         │
    ┌────▼──────────────────────┐
    │ Edit festival content     │
    │ POST to /festival/X/edit  │
    │ save_festivals()          │
    └───────────────────────────┘
```

## Configuration

### Environment Variables
```bash
# Admin credentials
FESTIVE_G_ADMIN_PASSWORD=your_secure_password    # Required

# SMTP for email sending (optional)
FESTIVE_G_SMTP_HOST=smtp.gmail.com              # Required to send emails
FESTIVE_G_SMTP_PORT=587                         # Default: 587
FESTIVE_G_SMTP_USER=your_email@gmail.com
FESTIVE_G_SMTP_PASSWORD=your_app_password
FESTIVE_G_EMAIL_FROM=no-reply@festive-g.com    # Defaults to sender email
FESTIVE_G_SMTP_TLS=true                         # Default: true
```

### Default Settings
- **Host:** 127.0.0.1 (localhost only)
- **Port:** 4173
- **Default Admin:** admin / admin123 (override with env var)
- **Session Storage:** In-memory (NOT persistent)

## Key Design Decisions

1. **No External Framework:** Uses Python stdlib `http.server` for maximum portability
2. **Simple Templating:** Basic string replacement avoids Jinja2 dependency
3. **File-based Storage:** JSON for semi-structured data (festivals), CSV for logs
4. **In-memory Sessions:** Fast but reset on server restart
5. **Environment Configuration:** 12-factor app principles for secrets
6. **Multi-threaded:** `ThreadingHTTPServer` for concurrent requests
7. **HTML Escaping:** All user input escaped to prevent XSS

## Limitations & Known Issues

- ⚠️ Sessions lost on server restart (consider Redis in production)
- ⚠️ CSV is append-only (no built-in way to delete submissions)
- ⚠️ Single admin account (consider user management in production)
- ⚠️ No HTTPS (use reverse proxy like nginx in production)
- ⚠️ Localhost-only binding (configure if deploying)

## Performance Considerations

- **Concurrency:** `ThreadingHTTPServer` handles multiple requests
- **File I/O:** Blocking reads/writes (acceptable for small deployments)
- **Session lookup:** O(1) in-memory dictionary
- **Festival search:** O(n) linear scan (acceptable for ~10 festivals)
- **CSV append:** Single file write per submission

## Security Notes

- ✅ Password comparison uses `secrets.compare_digest()` (timing attack safe)
- ✅ CSRF token in login form
- ✅ Path traversal protection in static file serving
- ✅ HTML escaping on all user input
- ✅ HttpOnly + SameSite cookies
- ⚠️ No rate limiting (implement reverse proxy protection)
- ⚠️ SMTP password in environment (use CI/CD secrets)

## Extension Points

To extend FESTIVE G:

1. **Add new festivals:** Edit `DEFAULT_FESTIVALS` constant
2. **Custom email template:** Modify `send_greeting_email()` message body
3. **Database backend:** Replace JSON/CSV with SQLite/PostgreSQL
4. **User authentication:** Implement proper user registration in `do_POST("/admin/login")`
5. **Email scheduling:** Queue submissions and process asynchronously
6. **Analytics:** Parse submissions.csv with pandas
