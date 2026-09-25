# FESTIVE G - API Reference

Complete documentation of all endpoints, functions, and data structures.

## HTTP Endpoints

### Public Routes

#### GET `/` or `/welcome`
Home page with festival overview.

**Response:** HTML page

**Example:**
```bash
curl http://127.0.0.1:4173/
```

---

#### GET `/festivals`
List all festivals with navigation tabs.

**Response:** HTML page with festival tabs

**Example:**
```bash
curl http://127.0.0.1:4173/festivals
```

---

#### GET `/festival/{slug}`
Display detailed information for a specific festival.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| slug | URL path | Yes | Festival identifier (e.g., "diwali", "holi") |

**Response:** HTML page with festival details

**Status Codes:**
- `200` - Festival found and displayed
- `404` - Festival not found

**Available Slugs:**
```
diwali, holi, navratri, dussehra-vijayadashami, janmashtami,
ganesh-chaturthi, maha-shivaratri, ram-navami, janma-divas,
makar-sankranti
```

**Example:**
```bash
curl http://127.0.0.1:4173/festival/diwali
```

---

#### GET `/user-info`
Display the greeting submission form.

**Response:** HTML form with fields for user input

**Example:**
```bash
curl http://127.0.0.1:4173/user-info
```

---

#### POST `/user-info`
Submit a greeting to send to a recipient.

**Form Parameters:**
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| sender_name | string | Yes | Max 80 characters |
| sender_email | string | Yes | Valid email format |
| receiver_name | string | Yes | Max 80 characters |
| receiver_email | string | Yes | Valid email format |
| receiver_address | string | Yes | 10-300 characters |

**Request Body:**
```html
POST /user-info
Content-Type: application/x-www-form-urlencoded

sender_name=John+Doe&sender_email=john@example.com&receiver_name=Jane+Doe&receiver_email=jane@example.com&receiver_address=123+Main+St+City+State+12345
```

**Response:**
- `200` - Greeting submitted and saved successfully
- `400` - Validation error (missing fields, invalid format, etc.)

**Response Body:**
```html
Thank you page with submission confirmation
```

**Errors Returned:**
```
"Sender's name is required."
"Sender's email must be a valid email address."
"Receiver's address must be at least 10 characters."
"Receiver's address must be 300 characters or fewer."
```

**Example:**
```bash
curl -X POST http://127.0.0.1:4173/user-info \
  -d "sender_name=John&sender_email=john@example.com&receiver_name=Jane&receiver_email=jane@example.com&receiver_address=123+Main+Street+City"
```

---

#### GET `/static/styles.css`
Stylesheet for the application.

**Response:** CSS file

---

#### GET `/static/images/{filename}`
Static images directory.

**Parameters:**
| Name | Type | Required |
|------|------|----------|
| filename | URL path | Yes |

**Response:** Image file (JPEG, PNG, SVG, etc.)

**Security:** Path traversal protection enabled

---

### Admin Routes

All admin routes require authentication. Unauthenticated requests redirect to login.

#### GET `/admin`
Admin authentication page or redirect.

**Behavior:**
- If authenticated: Redirects to `/admin/submissions`
- If not authenticated: Shows login form

**Response:** 
- `200` - Login form
- `303` - Redirect to submissions (if authenticated)

**Example:**
```bash
curl http://127.0.0.1:4173/admin
```

---

#### POST `/admin/login`
Authenticate as admin.

**Form Parameters:**
| Field | Type | Required |
|-------|------|----------|
| username | string | Yes |
| password | string | Yes |

**Credentials:**
- Default username: `admin`
- Default password: `admin123` (override with `FESTIVE_G_ADMIN_PASSWORD` env var)

**Response:**
- `200` - Login form (invalid credentials)
- `303` - Redirect to submissions (success)

**Response Headers (Success):**
```
Set-Cookie: festiveg_session=<token>; Path=/; HttpOnly; SameSite=Lax
Location: /admin/submissions
```

**Example:**
```bash
curl -X POST http://127.0.0.1:4173/admin/login \
  -d "username=admin&password=admin123" \
  -c cookies.txt
```

---

#### POST `/admin/logout`
Clear admin session and logout.

**Response:**
- `303` - Redirect to login page

**Response Headers:**
```
Set-Cookie: festiveg_session=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax
Location: /admin
```

**Example:**
```bash
curl -X POST http://127.0.0.1:4173/admin/logout \
  -b "festiveg_session=<token>"
```

---

#### GET `/admin/submissions`
View all greeting submissions.

**Authentication:** Required

**Response:** HTML table with submissions

**Table Columns:**
- Submitted At
- Sender Name
- Sender Email
- Receiver Name
- Receiver Email
- Receiver Address
- Email Status

**Example:**
```bash
curl http://127.0.0.1:4173/admin/submissions \
  -b "festiveg_session=<token>"
```

---

#### GET `/admin/festivals`
Manage festivals.

**Authentication:** Required

**Response:** HTML page with festival list and links to edit each

**Example:**
```bash
curl http://127.0.0.1:4173/admin/festivals \
  -b "festiveg_session=<token>"
```

---

#### GET `/admin/festival/{slug}/edit`
Edit form for a specific festival.

**Authentication:** Required

**Parameters:**
| Name | Type | Required |
|------|------|----------|
| slug | URL path | Yes |

**Response:** HTML form with festival content editor

**Status Codes:**
- `200` - Edit form displayed
- `404` - Festival not found

**Example:**
```bash
curl http://127.0.0.1:4173/admin/festival/diwali/edit \
  -b "festiveg_session=<token>"
```

---

#### POST `/admin/festival/{slug}/edit`
Update festival content.

**Authentication:** Required

**Parameters:**
| Name | Type | Required |
|------|------|----------|
| slug | URL path | Yes |
| content | form | Yes |

**Form Parameters:**
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| content | string | Yes | Max 5000 characters |

**Response:**
- `200` - Success message, edit form redisplayed
- `400` - Validation error (content too long)
- `404` - Festival not found

**Example:**
```bash
curl -X POST http://127.0.0.1:4173/admin/festival/diwali/edit \
  -b "festiveg_session=<token>" \
  -d "content=Diwali+is+the+festival+of+lights..."
```

---

## Python Functions

### Data Management

#### `load_festivals() -> list[dict]`
Load all festivals from JSON file.

**Returns:**
```python
[
    {
        "slug": "diwali",
        "title": "Diwali",
        "content": "Festival information..."
    },
    ...
]
```

**Raises:**
- `FileNotFoundError` - If data not initialized
- `json.JSONDecodeError` - If JSON is corrupted

---

#### `save_festivals(festivals: list[dict]) -> None`
Save festivals to JSON file.

**Parameters:**
```python
festivals = [
    {
        "slug": "diwali",
        "title": "Diwali",
        "content": "Updated content..."
    }
]
save_festivals(festivals)
```

---

#### `find_festival(slug: str) -> dict | None`
Find a festival by slug.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| slug | str | Festival identifier |

**Returns:**
```python
# Found
{
    "slug": "diwali",
    "title": "Diwali",
    "content": "..."
}

# Not found
None
```

---

#### `append_submission(data: dict) -> None`
Log a submission to CSV.

**Parameters:**
```python
submission = {
    "submitted_at": "2024-09-25 10:30:00",
    "sender_name": "John Doe",
    "sender_email": "john@example.com",
    "receiver_name": "Jane Doe",
    "receiver_email": "jane@example.com",
    "receiver_address": "123 Main St",
    "email_status": "Sent successfully"
}
append_submission(submission)
```

---

#### `load_submissions() -> list[dict]`
Load all submissions from CSV.

**Returns:**
```python
[
    {
        "submitted_at": "2024-09-25 10:30:00",
        "sender_name": "John Doe",
        "sender_email": "john@example.com",
        ...
    },
    ...
]
```

---

#### `ensure_data_files() -> None`
Create data directory and initialize files if missing.

**Side Effects:**
- Creates `data/` directory if it doesn't exist
- Creates `festivals.json` with defaults if missing
- Creates `submissions.csv` with headers if missing

---

### Rendering

#### `render_page(template_name: str, **values: str) -> str`
Render a template with variable substitution.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| template_name | str | HTML file in templates/ |
| **values | str | Template variables |

**Returns:** Rendered HTML string

**Example:**
```python
html = render_page("festival_detail.html", 
                   title="Diwali",
                   content="<p>Festival info</p>")
```

**Template Syntax:**
```html
<h1>{{ title }}</h1>
<div>{{ content }}</div>
```

---

#### `send_html(handler, page: str, status=200, headers=None) -> None`
Send HTML response to client.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| handler | BaseHTTPRequestHandler | Request handler |
| page | str | HTML content |
| status | int | HTTP status code (default: 200) |
| headers | dict | Additional headers (optional) |

**Example:**
```python
send_html(self, render_page("welcome.html"), status=200)
send_html(self, error_html, status=400)
```

---

#### `redirect(handler, location: str) -> None`
Send 303 redirect response.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| handler | BaseHTTPRequestHandler | Request handler |
| location | str | Redirect URL |

**Example:**
```python
redirect(self, "/admin/submissions")
```

---

### Validation

#### `validate_user_form(form: dict) -> list[str]`
Validate greeting submission form.

**Parameters:**
```python
form = {
    "sender_name": "John Doe",
    "sender_email": "john@example.com",
    "receiver_name": "Jane Doe",
    "receiver_email": "jane@example.com",
    "receiver_address": "123 Main Street City"
}
errors = validate_user_form(form)
```

**Returns:** List of error messages (empty if valid)

**Validations:**
- All required fields present and not empty
- Email format valid (basic regex)
- Sender name ≤ 80 characters
- Receiver name ≤ 80 characters
- Receiver address between 10-300 characters

**Example Errors:**
```python
[
    "Sender's name is required.",
    "Sender's email must be a valid email address.",
    "Receiver's address must be at least 10 characters."
]
```

---

### Email

#### `send_greeting_email(data: dict) -> str`
Send greeting email to recipient.

**Parameters:**
```python
data = {
    "sender_name": "John Doe",
    "sender_email": "john@example.com",
    "receiver_name": "Jane Doe",
    "receiver_email": "jane@example.com",
    "receiver_address": "123 Main Street"
}
status = send_greeting_email(data)
```

**Returns:** Status message string

**Success Example:**
```
"Email sent to jane@example.com"
```

**Error Examples:**
```
"Email not sent: SMTP settings are not configured."
"Email not sent: Error connecting to SMTP server"
```

**Configuration (Environment Variables):**
| Variable | Default | Required |
|----------|---------|----------|
| FESTIVE_G_SMTP_HOST | - | Yes (to send emails) |
| FESTIVE_G_SMTP_PORT | 587 | No |
| FESTIVE_G_SMTP_USER | - | No |
| FESTIVE_G_SMTP_PASSWORD | - | No |
| FESTIVE_G_EMAIL_FROM | sender_email | No |
| FESTIVE_G_SMTP_TLS | true | No |

---

### Utility Functions

#### `escape(value: any) -> str`
HTML escape a value to prevent XSS.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| value | any | Value to escape |

**Returns:** Escaped string safe for HTML

**Example:**
```python
escape("<script>alert('xss')</script>")
# Returns: "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;"
```

---

#### `content_to_html(content: str) -> str`
Convert line-separated text to HTML paragraphs.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| content | str | Multi-line text |

**Returns:** HTML with `<p>` tags

**Example:**
```python
content_to_html("Line 1\nLine 2\nLine 3")
# Returns: "<p>Line 1</p>\n<p>Line 2</p>\n<p>Line 3</p>"
```

---

#### `error_list(errors: list[str]) -> str`
Format error messages as HTML.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| errors | list | List of error messages |

**Returns:** HTML error list or empty string

**Example:**
```python
error_list(["Field required", "Invalid format"])
# Returns: '<ul class="message error"><li>Field required</li><li>Invalid format</li></ul>'

error_list([])
# Returns: ""
```

---

#### `success_message(message: str) -> str`
Format success message as HTML.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| message | str | Success message text |

**Returns:** HTML success message or empty string

**Example:**
```python
success_message("Changes saved!")
# Returns: '<p class="message success">Changes saved!</p>'
```

---

### Authentication

#### `is_admin(handler) -> bool`
Check if request is from authenticated admin.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| handler | BaseHTTPRequestHandler | Request handler |

**Returns:** `True` if admin session valid, `False` otherwise

---

#### `require_admin(handler) -> bool`
Require admin authentication, redirect to login if not.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| handler | BaseHTTPRequestHandler | Request handler |

**Returns:** `True` if admin, `False` if not (and redirects)

---

## Data Structures

### Festival Object
```python
{
    "slug": str,           # URL-friendly identifier
    "title": str,          # Display name
    "content": str         # Festival description (multi-line)
}
```

### Submission Object
```python
{
    "submitted_at": str,       # ISO datetime "YYYY-MM-DD HH:MM:SS"
    "sender_name": str,        # Greeting sender's name
    "sender_email": str,       # Sender's email address
    "receiver_name": str,      # Recipient's name
    "receiver_email": str,     # Recipient's email
    "receiver_address": str,   # Recipient's address
    "email_status": str        # "Sent", error message, or empty
}
```

---

## Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful request |
| 303 | See Other | Redirect after POST |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | Invalid login credentials |
| 404 | Not Found | Page/resource doesn't exist |
| 500 | Server Error | Unexpected error |

---

## Examples

### Using the Python API

```python
import app

# Load festivals
festivals = app.load_festivals()
print(f"Total festivals: {len(festivals)}")

# Find a specific festival
diwali = app.find_festival("diwali")
print(diwali["title"])

# Load submissions
submissions = app.load_submissions()
print(f"Total submissions: {len(submissions)}")

# Create and save submission
submission = {
    "submitted_at": "2024-09-25 14:30:00",
    "sender_name": "John",
    "sender_email": "john@example.com",
    "receiver_name": "Jane",
    "receiver_email": "jane@example.com",
    "receiver_address": "123 Main Street",
    "email_status": ""
}
app.append_submission(submission)
```

### cURL Examples

```bash
# Get festivals
curl http://127.0.0.1:4173/festivals

# Submit greeting
curl -X POST http://127.0.0.1:4173/user-info \
  -d "sender_name=John&sender_email=john@example.com&receiver_name=Jane&receiver_email=jane@example.com&receiver_address=123+Main+St"

# Login to admin
curl -X POST http://127.0.0.1:4173/admin/login \
  -d "username=admin&password=admin123" \
  -c cookies.txt

# View submissions
curl http://127.0.0.1:4173/admin/submissions \
  -b cookies.txt

# Edit festival
curl -X POST http://127.0.0.1:4173/admin/festival/diwali/edit \
  -b cookies.txt \
  -d "content=New+festival+content"
```

---

## Rate Limiting

Currently no rate limiting. Implement using:
- Nginx `limit_req` module
- Python middleware
- Reverse proxy protection

---

## Error Handling

All errors should be caught and returned as HTML pages with appropriate status codes. 

**Example Error Response:**
```html
400 Bad Request

<html>
<body>
<ul class="message error">
  <li>Sender's email is required.</li>
  <li>Receiver's address must be at least 10 characters.</li>
</ul>
</body>
</html>
```

---

For more information, see [ARCHITECTURE.md](ARCHITECTURE.md) and [README.md](README.md)
