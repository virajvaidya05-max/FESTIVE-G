import csv
import html
import json
import os
import re
import secrets
import smtplib
from datetime import datetime
from email.message import EmailMessage
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from mimetypes import guess_type
from urllib.parse import parse_qs, unquote, urlparse


BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
DATA_DIR = BASE_DIR / "data"
FESTIVALS_FILE = DATA_DIR / "festivals.json"
SUBMISSIONS_FILE = DATA_DIR / "submissions.csv"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = os.environ.get("FESTIVE_G_ADMIN_PASSWORD", "admin123")
SESSIONS = {}

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

DEFAULT_FESTIVALS = [
    {"slug": "diwali", "title": "Diwali", "content": "Add detailed information about Diwali here."},
    {"slug": "holi", "title": "Holi", "content": "Add detailed information about Holi here."},
    {"slug": "navratri", "title": "Navratri", "content": "Add detailed information about Navratri here."},
    {
        "slug": "dussehra-vijayadashami",
        "title": "Dussehra (Vijayadashami)",
        "content": "Add detailed information about Dussehra (Vijayadashami) here.",
    },
    {
        "slug": "janmashtami",
        "title": "Janmashtami",
        "content": "Add detailed information about Janmashtami here.",
    },
    {
        "slug": "ganesh-chaturthi",
        "title": "Ganesh Chaturthi",
        "content": "Add detailed information about Ganesh Chaturthi here.",
    },
    {
        "slug": "maha-shivaratri",
        "title": "Maha Shivaratri",
        "content": "Add detailed information about Maha Shivaratri here.",
    },
    {
        "slug": "ram-navami",
        "title": "Ram Navami",
        "content": "Add detailed information about Ram Navami here.",
    },
    {
        "slug": "janma-divas",
        "title": "Janma Divas",
        "content": "Add detailed information about Janma Divas here.",
    },
    {
        "slug": "makar-sankranti",
        "title": "Makar Sankranti",
        "content": "Add detailed information about Makar Sankranti here.",
    },
]

SUBMISSION_FIELDS = [
    "submitted_at",
    "sender_name",
    "sender_email",
    "receiver_name",
    "receiver_email",
    "receiver_address",
    "email_status",
]


def escape(value):
    return html.escape(str(value), quote=True)


def read_template(name):
    return (TEMPLATE_DIR / name).read_text(encoding="utf-8")


def render_page(template_name, **values):
    page = read_template(template_name)
    for key, value in values.items():
        page = page.replace("{{ " + key + " }}", str(value))
    return page


def send_html(handler, page, status=200, headers=None):
    body = page.encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "text/html; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    if headers:
        for key, value in headers.items():
            handler.send_header(key, value)
    handler.end_headers()
    handler.wfile.write(body)


def redirect(handler, location):
    handler.send_response(303)
    handler.send_header("Location", location)
    handler.end_headers()


def ensure_data_files():
    DATA_DIR.mkdir(exist_ok=True)

    if not FESTIVALS_FILE.exists():
        save_festivals(DEFAULT_FESTIVALS)

    if not SUBMISSIONS_FILE.exists():
        with SUBMISSIONS_FILE.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=SUBMISSION_FIELDS)
            writer.writeheader()


def load_festivals():
    ensure_data_files()
    return json.loads(FESTIVALS_FILE.read_text(encoding="utf-8"))


def save_festivals(festivals):
    DATA_DIR.mkdir(exist_ok=True)
    FESTIVALS_FILE.write_text(
        json.dumps(festivals, indent=2, ensure_ascii=True),
        encoding="utf-8",
    )


def find_festival(slug):
    for festival in load_festivals():
        if festival["slug"] == slug:
            return festival
    return None


def content_to_html(content):
    paragraphs = []
    for paragraph in content.splitlines():
        paragraph = paragraph.strip()
        if paragraph:
            paragraphs.append(f"<p>{escape(paragraph)}</p>")

    if not paragraphs:
        return "<p>No festival information has been added yet.</p>"

    return "\n".join(paragraphs)


def festival_tabs(active_slug=None):
    links = []
    for festival in load_festivals():
        active = " active" if festival["slug"] == active_slug else ""
        links.append(
            '<a class="tab{active}" href="/festival/{slug}">{title}</a>'.format(
                active=active,
                slug=escape(festival["slug"]),
                title=escape(festival["title"]),
            )
        )
    return "\n".join(links)


def append_submission(data):
    ensure_data_files()
    with SUBMISSIONS_FILE.open("a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=SUBMISSION_FIELDS)
        writer.writerow(data)


def load_submissions():
    ensure_data_files()
    with SUBMISSIONS_FILE.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def error_list(errors):
    if not errors:
        return ""

    items = "".join(f"<li>{escape(error)}</li>" for error in errors)
    return f'<ul class="message error">{items}</ul>'


def success_message(message):
    if not message:
        return ""

    return f'<p class="message success">{escape(message)}</p>'


def validate_user_form(form):
    errors = []
    required_fields = {
        "sender_name": "Sender's name",
        "sender_email": "Sender's email",
        "receiver_name": "Receiver's name",
        "receiver_email": "Receiver's email",
        "receiver_address": "Receiver's address",
    }

    for field, label in required_fields.items():
        if not form.get(field, "").strip():
            errors.append(f"{label} is required.")

    for field, label in (
        ("sender_email", "Sender's email"),
        ("receiver_email", "Receiver's email"),
    ):
        value = form.get(field, "").strip()
        if value and not EMAIL_PATTERN.match(value):
            errors.append(f"{label} must be a valid email address.")

    for field, label in (
        ("sender_name", "Sender's name"),
        ("receiver_name", "Receiver's name"),
    ):
        if len(form.get(field, "")) > 80:
            errors.append(f"{label} must be 80 characters or fewer.")

    address = form.get("receiver_address", "").strip()
    if address and len(address) < 10:
        errors.append("Receiver's address must be at least 10 characters.")
    if len(address) > 300:
        errors.append("Receiver's address must be 300 characters or fewer.")

    return errors


def send_greeting_email(data):
    host = os.environ.get("FESTIVE_G_SMTP_HOST", "").strip()
    if not host:
        return "Email not sent: SMTP settings are not configured."

    port = int(os.environ.get("FESTIVE_G_SMTP_PORT", "587"))
    username = os.environ.get("FESTIVE_G_SMTP_USER", "").strip()
    password = os.environ.get("FESTIVE_G_SMTP_PASSWORD", "")
    sender = os.environ.get("FESTIVE_G_EMAIL_FROM", username or data["sender_email"])
    use_tls = os.environ.get("FESTIVE_G_SMTP_TLS", "true").lower() != "false"

    message = EmailMessage()
    message["Subject"] = f"Festival wishes from {data['sender_name']}"
    message["From"] = sender
    message["To"] = data["receiver_email"]
    message["Reply-To"] = data["sender_email"]
    message.set_content(
        "Hello {receiver_name},\n\n"
        "{sender_name} has sent you festive wishes through FESTIVE G.\n\n"
        "Receiver address saved:\n{receiver_address}\n\n"
        "THANK YOU!\n".format(**data)
    )

    try:
        with smtplib.SMTP(host, port, timeout=10) as smtp:
            if use_tls:
                smtp.starttls()
            if username and password:
                smtp.login(username, password)
            smtp.send_message(message)
        return "Email sent successfully."
    except Exception as exc:
        return f"Email not sent: {exc}"


def form_values(form):
    fields = [
        "sender_name",
        "sender_email",
        "receiver_name",
        "receiver_email",
        "receiver_address",
    ]
    return {field: escape(form.get(field, "")) for field in fields}


def get_cookie(headers, name):
    cookie_header = headers.get("Cookie", "")
    cookies = {}
    for part in cookie_header.split(";"):
        if "=" in part:
            key, value = part.strip().split("=", 1)
            cookies[key] = value
    return cookies.get(name)


def is_admin(handler):
    token = get_cookie(handler.headers, "festiveg_session")
    return bool(token and SESSIONS.get(token) == ADMIN_USERNAME)


def require_admin(handler):
    if is_admin(handler):
        return True

    redirect(handler, "/admin")
    return False


def parse_form(handler):
    content_length = int(handler.headers.get("Content-Length", 0))
    raw_body = handler.rfile.read(content_length).decode("utf-8")
    parsed = parse_qs(raw_body, keep_blank_values=True)
    return {key: values[0].strip() for key, values in parsed.items()}


def render_user_info(form=None, errors=None, thank_you="", email_status=""):
    form = form or {}
    values = form_values(form)
    return render_page(
        "user_info.html",
        errors=error_list(errors or []),
        thank_you=thank_you,
        email_status=success_message(email_status),
        **values,
    )


def render_admin_login(error=""):
    return render_page("admin_login.html", errors=error_list([error] if error else []))


def render_admin_submissions():
    rows = []
    for submission in reversed(load_submissions()):
        rows.append(
            """
            <tr>
                <td>{submitted_at}</td>
                <td>{sender_name}</td>
                <td>{sender_email}</td>
                <td>{receiver_name}</td>
                <td>{receiver_email}</td>
                <td>{receiver_address}</td>
                <td>{email_status}</td>
            </tr>
            """.format(
                submitted_at=escape(submission.get("submitted_at", "")),
                sender_name=escape(submission.get("sender_name", "")),
                sender_email=escape(submission.get("sender_email", "")),
                receiver_name=escape(submission.get("receiver_name", "")),
                receiver_email=escape(submission.get("receiver_email", "")),
                receiver_address=escape(submission.get("receiver_address", "")),
                email_status=escape(submission.get("email_status", "")),
            )
        )

    if not rows:
        rows.append('<tr><td colspan="7">No submissions yet.</td></tr>')

    return render_page("admin_submissions.html", rows="\n".join(rows))


def render_admin_festivals(message=""):
    rows = []
    for festival in load_festivals():
        rows.append(
            """
            <tr>
                <td>{title}</td>
                <td><a href="/festival/{slug}">View</a></td>
                <td><a href="/admin/festival/{slug}/edit">Edit</a></td>
            </tr>
            """.format(
                title=escape(festival["title"]),
                slug=escape(festival["slug"]),
            )
        )

    return render_page(
        "admin_festivals.html",
        rows="\n".join(rows),
        message=success_message(message),
    )


class FestiveGHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/" or path == "/welcome":
            send_html(self, render_page("welcome.html"))
            return

        if path == "/festivals":
            send_html(self, render_page("festivals.html", tabs=festival_tabs()))
            return

        if path.startswith("/festival/"):
            slug = unquote(path.removeprefix("/festival/")).strip("/")
            festival = find_festival(slug)
            if not festival:
                self.send_error(404, "Festival not found")
                return

            send_html(
                self,
                render_page(
                    "festival_detail.html",
                    title=escape(festival["title"]),
                    content=content_to_html(festival["content"]),
                    tabs=festival_tabs(festival["slug"]),
                ),
            )
            return

        if path == "/user-info":
            send_html(self, render_user_info())
            return

        if path == "/admin":
            if is_admin(self):
                redirect(self, "/admin/submissions")
                return
            send_html(self, render_admin_login())
            return

        if path == "/admin/submissions":
            if not require_admin(self):
                return
            send_html(self, render_admin_submissions())
            return

        if path == "/admin/festivals":
            if not require_admin(self):
                return
            send_html(self, render_admin_festivals())
            return

        if path.startswith("/admin/festival/") and path.endswith("/edit"):
            if not require_admin(self):
                return

            slug = unquote(path.removeprefix("/admin/festival/").removesuffix("/edit")).strip("/")
            festival = find_festival(slug)
            if not festival:
                self.send_error(404, "Festival not found")
                return

            send_html(
                self,
                render_page(
                    "admin_festival_edit.html",
                    title=escape(festival["title"]),
                    slug=escape(festival["slug"]),
                    content=escape(festival["content"]),
                    message="",
                    errors="",
                ),
            )
            return

        if path == "/static/styles.css":
            self.serve_static("styles.css", "text/css; charset=utf-8")
            return

        if path.startswith("/static/images/"):
            filename = unquote(path.removeprefix("/static/"))
            self.serve_static(filename)
            return

        self.send_error(404, "Page not found")

    def do_POST(self):
        path = urlparse(self.path).path

        if path == "/user-info":
            form = parse_form(self)
            errors = validate_user_form(form)
            if errors:
                send_html(self, render_user_info(form=form, errors=errors), status=400)
                return

            submission = {
                "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "sender_name": form["sender_name"],
                "sender_email": form["sender_email"],
                "receiver_name": form["receiver_name"],
                "receiver_email": form["receiver_email"],
                "receiver_address": form["receiver_address"],
                "email_status": "",
            }
            submission["email_status"] = send_greeting_email(submission)
            append_submission(submission)

            thank_you = (
                '<p class="thank-you">THANK YOU, {name}! Your festive greeting details '
                "have been saved.</p>"
            ).format(name=escape(submission["receiver_name"]))
            send_html(
                self,
                render_user_info(
                    form={},
                    thank_you=thank_you,
                    email_status=submission["email_status"],
                ),
            )
            return

        if path == "/admin/login":
            form = parse_form(self)
            username = form.get("username", "")
            password = form.get("password", "")
            if username == ADMIN_USERNAME and secrets.compare_digest(password, ADMIN_PASSWORD):
                token = secrets.token_urlsafe(32)
                SESSIONS[token] = ADMIN_USERNAME
                send_html(
                    self,
                    "<!doctype html><html><body>Logged in.</body></html>",
                    status=303,
                    headers={
                        "Location": "/admin/submissions",
                        "Set-Cookie": (
                            f"festiveg_session={token}; Path=/; HttpOnly; SameSite=Lax"
                        ),
                    },
                )
                return

            send_html(self, render_admin_login("Invalid admin username or password."), status=401)
            return

        if path == "/admin/logout":
            token = get_cookie(self.headers, "festiveg_session")
            if token:
                SESSIONS.pop(token, None)
            send_html(
                self,
                "<!doctype html><html><body>Logged out.</body></html>",
                status=303,
                headers={
                    "Location": "/admin",
                    "Set-Cookie": (
                        "festiveg_session=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax"
                    ),
                },
            )
            return

        if path.startswith("/admin/festival/") and path.endswith("/edit"):
            if not require_admin(self):
                return

            slug = unquote(path.removeprefix("/admin/festival/").removesuffix("/edit")).strip("/")
            form = parse_form(self)
            content = form.get("content", "")
            errors = []
            if len(content) > 5000:
                errors.append("Festival information must be 5000 characters or fewer.")

            festivals = load_festivals()
            festival = next((item for item in festivals if item["slug"] == slug), None)
            if not festival:
                self.send_error(404, "Festival not found")
                return

            if errors:
                send_html(
                    self,
                    render_page(
                        "admin_festival_edit.html",
                        title=escape(festival["title"]),
                        slug=escape(festival["slug"]),
                        content=escape(content),
                        message="",
                        errors=error_list(errors),
                    ),
                    status=400,
                )
                return

            festival["content"] = content
            save_festivals(festivals)
            send_html(
                self,
                render_page(
                    "admin_festival_edit.html",
                    title=escape(festival["title"]),
                    slug=escape(festival["slug"]),
                    content=escape(content),
                    message=success_message("Festival information saved."),
                    errors="",
                ),
            )
            return

        self.send_error(404, "Page not found")

    def serve_static(self, filename, content_type=None):
        path = STATIC_DIR / filename
        try:
            resolved_path = path.resolve()
            resolved_static = STATIC_DIR.resolve()
        except OSError:
            self.send_error(404, "File not found")
            return

        if not resolved_path.is_relative_to(resolved_static) or not resolved_path.exists():
            self.send_error(404, "File not found")
            return

        body = resolved_path.read_bytes()
        self.send_response(200)
        self.send_header(
            "Content-Type",
            content_type or guess_type(str(resolved_path))[0] or "application/octet-stream",
        )
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")


if __name__ == "__main__":
    ensure_data_files()
    host = "127.0.0.1"
    port = 4173
    server = ThreadingHTTPServer((host, port), FestiveGHandler)
    print(f"FESTIVE G is running at http://{host}:{port}")
    print("Admin login: http://127.0.0.1:4173/admin")
    print("Default admin: admin / admin123")
    server.serve_forever()
