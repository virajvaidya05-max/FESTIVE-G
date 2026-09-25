# Contributing to FESTIVE G

Thank you for your interest in contributing! This guide will help you get started.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## Getting Started

### 1. Fork & Clone
```bash
git clone https://github.com/yourusername/festive-g.git
cd festive-g
```

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 3. Make Changes
- Keep changes focused and atomic
- Write clear commit messages
- Test your changes locally

### 4. Submit a Pull Request
- Describe what your PR does
- Reference any related issues
- Be responsive to feedback

## Code Style

### Python Style Guide
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4 spaces for indentation (not tabs)
- Maximum line length: 100 characters

### Type Hints
While type hints aren't currently used, they're encouraged for new code:

```python
def render_page(template_name: str, **values: str) -> str:
    """Render a template with given values."""
    pass
```

### Docstrings
Follow the Google docstring format:

```python
def validate_user_form(form: dict) -> list:
    """Validate user greeting form submission.
    
    Args:
        form: Dictionary of form fields from user submission
        
    Returns:
        List of error messages (empty if valid)
        
    Raises:
        ValueError: If form structure is invalid
        
    Example:
        >>> errors = validate_user_form({"sender_name": "John"})
        >>> len(errors) > 0  # Missing required fields
        True
    """
    pass
```

### Variable Naming
- Use descriptive names: `submission_data` not `sd`
- Constants in UPPER_CASE: `ADMIN_PASSWORD`
- Functions/variables in snake_case: `get_submission()`
- Avoid single letters except in loops: `for submission in submissions:`

### HTML in Python
Minimize HTML in Python code. Keep template strings separate:

```python
# Good
error_html = f'<ul class="error">{error_list}</ul>'
send_html(handler, error_html)

# Avoid complex HTML in Python
html = f'<div><ul>{"".join(f"<li>{e}</li>" for e in errors)}</ul></div>'
```

## File Organization

### New Features
1. **Core logic** in `app.py`
2. **HTML templates** in `templates/`
3. **Styles** in `static/styles.css`
4. **Data** in `data/` (auto-created)

### Directory Structure
```
feature-name/
├── feature_handler()     # In app.py
├── template_name.html    # In templates/
└── Relevant constants    # In app.py
```

## Testing

### Manual Testing
While automated tests aren't currently in place, test manually:

```bash
# Start the server
python app.py

# Test in browser
# 1. Visit http://127.0.0.1:4173
# 2. Submit a greeting (check validation works)
# 3. Check data/submissions.csv was updated
# 4. Login to admin and verify
```

### Recommended Test Cases for New Features
- **Happy path:** Feature works as intended
- **Error cases:** Invalid input handled gracefully
- **Edge cases:** Empty inputs, max lengths, special characters
- **Security:** XSS prevention, path traversal protection

### Testing Checklist
- [ ] Feature works locally
- [ ] Error messages are helpful
- [ ] Input is HTML-escaped
- [ ] Data is saved correctly
- [ ] Admin can view/manage data
- [ ] No console errors

## Commit Messages

Use clear, descriptive commit messages:

### Format
```
<type>: <subject>

<body (optional)>
```

### Types
- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code restructuring
- `docs:` Documentation
- `style:` Formatting, variable names
- `test:` Test additions/changes
- `chore:` Dependencies, build config

### Examples

Good:
```
feat: add festival search functionality

Users can now search festivals by name or date.
Implements case-insensitive full-text search.
```

```
fix: prevent XSS in festival content display

Ensure all user-provided festival content is
properly HTML-escaped before rendering.
```

```
docs: expand ARCHITECTURE.md with data flow diagrams
```

Avoid:
```
fixed stuff
update
changes
```

## Security Considerations

### Input Validation
- ✅ Validate all user inputs
- ✅ Escape HTML: `escape(value)`
- ✅ Check email format
- ✅ Validate string lengths

### Path Security
- ✅ Use `is_relative_to()` for file paths
- ✅ Prevent directory traversal
- ✅ Don't trust user-provided file paths

### Authentication
- ✅ Use `secrets.compare_digest()` for password comparison
- ✅ HttpOnly + SameSite cookies
- ✅ Protect against CSRF

### Never
- ❌ Hardcode secrets in code
- ❌ Trust user input without validation
- ❌ Use simple string comparison for passwords
- ❌ Send sensitive data in URLs

## Documentation

### When to Update Docs
- New features → Update README.md
- Architecture changes → Update ARCHITECTURE.md
- New endpoints → Update API reference in README
- Deployment changes → Update deployment section

### Comment Guidelines
- Comment *why*, not *what*
- Keep comments up-to-date with code
- Use single `#` for inline comments
- Use triple-quotes for docstrings

```python
# Good
# Skip validation for test submissions to speed up testing
if is_test_mode:
    return []

# Avoid
# This function validates the form
def validate_form():
    pass
```

## Pull Request Checklist

Before submitting, ensure:

- [ ] Code follows PEP 8 style guide
- [ ] Docstrings added/updated
- [ ] HTML input is escaped with `escape()`
- [ ] Tested locally (happy path + edge cases)
- [ ] No hardcoded secrets or credentials
- [ ] Commit messages follow format
- [ ] README/docs updated if needed
- [ ] No unrelated changes included

## Common Tasks

### Adding a New Festival Route

1. **Add template** in `templates/your_festival.html`
2. **Add handler** in `FestiveGHandler.do_GET()`:
   ```python
   if path == "/your-route":
       send_html(self, render_page("your_festival.html"))
       return
   ```
3. **Add to data** (festivals.json or DEFAULT_FESTIVALS)
4. **Test** locally

### Adding Admin Functionality

1. **Add route** in `do_GET()` and/or `do_POST()`
2. **Check admin** with `require_admin(self)`
3. **Load/save data** with functions in data layer
4. **Create template** in `templates/admin_*.html`
5. **Test** login and access control

### Adding Validation

1. **Add validation** in `validate_user_form()` or create new function
2. **Return error messages** in a list
3. **Display errors** using `error_list(errors)`
4. **Test** with invalid inputs

## Troubleshooting

### "Where do I put code?"
- Logic → `app.py`
- HTML → `templates/` folder
- Styles → `static/styles.css`
- Images → `static/images/` folder
- Data → `data/` folder (auto-created)

### "How do I test my changes?"
```bash
python app.py
# Visit http://127.0.0.1:4173 in browser
# Test your feature
# Check data/ folder for new files
```

### "Can I change the database?"
Yes! See ARCHITECTURE.md "Extension Points" section. JSON/CSV can be replaced with SQLite/PostgreSQL.

### "How do I handle errors?"
```python
errors = []
if condition:
    errors.append("Error message for user")

if errors:
    send_html(self, render_page("template.html", errors=error_list(errors)))
    return
```

## Questions?

- 📖 Read [ARCHITECTURE.md](ARCHITECTURE.md) for project overview
- 📧 Email: [your-email@example.com]
- 🐛 Open an issue for bugs or questions

## Additional Resources

- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [Python Naming Conventions](https://www.python.org/dev/peps/pep-0008/#naming-conventions)
- [HTTP Status Codes](https://httpwg.org/specs/rfc7231.html#status.codes)
- [HTML Security](https://owasp.org/www-community/attacks/xss/)

Thank you for contributing! 🎉
