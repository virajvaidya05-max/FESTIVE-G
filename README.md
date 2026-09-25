# FESTIVE G 🎉

Send personalized festival greetings to your loved ones with a beautiful web interface.

![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)
![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)
![Status: Active](https://img.shields.io/badge/status-active-brightgreen.svg)

## Features

✨ **Festival Management**
- Browse 10+ Indian festivals (Diwali, Holi, Navratri, and more)
- View detailed festival information
- Admin panel to edit festival content

📧 **Greeting Submissions**
- User-friendly form to submit greetings
- Automatic email sending to recipients (SMTP configurable)
- Track submission history with email delivery status
- Input validation and error handling

🔐 **Admin Dashboard**
- Secure login with session management
- View all submissions in a table
- Edit festival descriptions
- Email status tracking

🚀 **Simple & Lightweight**
- No external web framework required
- Uses Python's built-in `http.server`
- Quick setup and deployment
- Minimal dependencies

## Quick Start

### Requirements
- Python 3.8 or higher
- No pip packages required (uses stdlib only)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/festive-g.git
cd festive-g

# Run the server
python app.py
```

The application will start at `http://127.0.0.1:4173`

### Default Admin Credentials
```
URL: http://127.0.0.1:4173/admin
Username: admin
Password: admin123
```

⚠️ **Change the default password in production!**

## Configuration

### Environment Variables

Configure the app by setting environment variables:

```bash
# Admin password (REQUIRED for production)
export FESTIVE_G_ADMIN_PASSWORD="your_super_secure_password"

# Email delivery (optional - if not set, emails won't send)
export FESTIVE_G_SMTP_HOST="smtp.gmail.com"
export FESTIVE_G_SMTP_PORT="587"
export FESTIVE_G_SMTP_USER="your_email@gmail.com"
export FESTIVE_G_SMTP_PASSWORD="your_app_password"
export FESTIVE_G_EMAIL_FROM="no-reply@festive-g.com"  # Optional
export FESTIVE_G_SMTP_TLS="true"
```

### Example: Gmail SMTP

```bash
export FESTIVE_G_SMTP_HOST="smtp.gmail.com"
export FESTIVE_G_SMTP_PORT="587"
export FESTIVE_G_SMTP_USER="your_email@gmail.com"
export FESTIVE_G_SMTP_PASSWORD="your_16_char_app_password"  # Use app password, not account password
export FESTIVE_G_EMAIL_FROM="Your Name <your_email@gmail.com>"
```

### `.env` File

Create a `.env` file to avoid setting variables each time:

```env
FESTIVE_G_ADMIN_PASSWORD=your_secure_password
FESTIVE_G_SMTP_HOST=smtp.gmail.com
FESTIVE_G_SMTP_PORT=587
FESTIVE_G_SMTP_USER=your_email@gmail.com
FESTIVE_G_SMTP_PASSWORD=your_app_password
FESTIVE_G_EMAIL_FROM=no-reply@festive-g.com
```

Then load it:
```bash
export $(cat .env | xargs)
python app.py
```

## Usage

### User Flow: Send a Greeting

1. **Visit** http://127.0.0.1:4173/user-info
2. **Fill the form:**
   - Your name
   - Your email
   - Recipient's name
   - Recipient's email
   - Recipient's address
3. **Submit** - greeting is recorded and email sent (if configured)
4. **Confirmation** - you'll see a thank you message

### Admin Flow: Manage Festivals

1. **Log in** at http://127.0.0.1:4173/admin
2. **View Submissions** - see all greeting submissions
3. **Manage Festivals** - click a festival to edit its description
4. **Log out** when done

## Project Structure

```
festive-g/
├── app.py                      # Main application
├── templates/                  # HTML templates
│   ├── welcome.html
│   ├── festivals.html
│   ├── festival_detail.html
│   ├── user_info.html
│   ├── admin_login.html
│   ├── admin_submissions.html
│   ├── admin_festivals.html
│   └── admin_festival_edit.html
├── static/                     # CSS and images
│   ├── styles.css
│   └── images/
├── data/                       # Data storage (auto-created)
│   ├── festivals.json
│   └── submissions.csv
├── README.md                   # This file
└── requirements.txt            # Dependencies (if needed)
```

## Architecture Overview

For detailed technical information, see [ARCHITECTURE.md](ARCHITECTURE.md)

**Key Components:**
- **Data Layer:** JSON (festivals), CSV (submissions)
- **HTTP Server:** Python's `ThreadingHTTPServer`
- **Templates:** Simple string-based rendering
- **Admin:** Session-based authentication
- **Email:** SMTP integration (optional)

## API Endpoints

### Public Routes
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Home page |
| `/festivals` | GET | Festival listing |
| `/festival/{slug}` | GET | Festival details |
| `/user-info` | GET | Greeting form |
| `/user-info` | POST | Submit greeting |
| `/static/*` | GET | Static files (CSS, images) |

### Admin Routes (Require Login)
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/admin` | GET | Login page |
| `/admin/login` | POST | Authenticate |
| `/admin/logout` | POST | Logout |
| `/admin/submissions` | GET | View submissions |
| `/admin/festivals` | GET | Manage festivals |
| `/admin/festival/{slug}/edit` | GET | Edit festival form |
| `/admin/festival/{slug}/edit` | POST | Save changes |

## Deployment

### Local Development
```bash
python app.py
```

### Production Deployment

Use a reverse proxy (nginx, Apache) in front:

1. **Change binding address:**
   Edit `app.py` line 626: `host = "0.0.0.0"` (instead of 127.0.0.1)

2. **Use a process manager:**
   ```bash
   # Using systemd
   [Service]
   ExecStart=/usr/bin/python3 /path/to/app.py
   Restart=always
   ```

3. **Use HTTPS:**
   Configure nginx/Apache to handle SSL/TLS

4. **Scale:** Behind nginx with multiple instances

5. **Persistent Sessions:**
   Replace in-memory sessions with Redis (see extension points)

6. **Database:**
   Consider SQLite or PostgreSQL instead of JSON/CSV

## Troubleshooting

### Server won't start
```
Address already in use
```
→ Port 4173 is in use. Change port in `app.py` line 627

### Emails not sending
```
Email not sent: SMTP settings are not configured.
```
→ Set `FESTIVE_G_SMTP_HOST` environment variable

### Admin login fails
```
Invalid admin username or password.
```
→ Default is `admin` / `admin123` or check `FESTIVE_G_ADMIN_PASSWORD` env var

### Submissions not saving
```
Check data/ folder permissions - must be readable/writable
```
→ Ensure write permissions: `chmod 755 data/`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Code style
- Testing
- Pull requests
- Commit messages

## Roadmap

- [ ] Database backend (SQLite/PostgreSQL)
- [ ] Persistent sessions (Redis)
- [ ] Email scheduling/queue
- [ ] Multi-admin users
- [ ] Rate limiting
- [ ] Analytics dashboard
- [ ] Custom email templates
- [ ] Festival date tracking

## FAQ

**Q: Can I customize festivals?**
A: Yes! Edit festival content in admin panel or edit `DEFAULT_FESTIVALS` in `app.py`

**Q: Is this secure for production?**
A: No. Use HTTPS, environment variables for secrets, and consider a proper web framework for production use.

**Q: Can I use a database?**
A: Currently uses JSON/CSV. See ARCHITECTURE.md for extension points.

**Q: Will sessions persist after restart?**
A: No, sessions are in-memory. Use Redis for persistence in production.

**Q: Can multiple users/admins use this?**
A: Currently only one admin account. Extend authentication for multiple users.

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

- 📧 Email: [your-email@example.com]
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/festive-g/issues)
- 📖 Documentation: [ARCHITECTURE.md](ARCHITECTURE.md)

---

Made with 🎉 for festival lovers everywhere
