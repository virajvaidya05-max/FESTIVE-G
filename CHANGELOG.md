# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup
- Core features

### Fixed
- Minor bugs

### Changed
- Performance improvements

### Deprecated
- None yet

### Removed
- None yet

### Security
- None yet

---

## [1.0.0] - 2024-09-25

### Added
- Welcome page with festival overview
- Festival listing with navigation tabs
- Festival detail pages with full content
- User greeting submission form
  - Email address validation
  - Form validation (required fields, length limits)
  - HTML escaping to prevent XSS
- Admin dashboard
  - Secure login with session management
  - View all submissions in table format
  - Festival management interface
  - Edit festival content and descriptions
- Email integration
  - SMTP configuration via environment variables
  - Email sending on greeting submission
  - Email status tracking in submissions
- Data persistence
  - Festival data in JSON format
  - Submission logging in CSV format
  - Auto-initialization of data files
- Static file serving
  - CSS styling
  - Image hosting
- Security features
  - Session-based authentication
  - HttpOnly + SameSite cookies
  - CSRF protection in login form
  - Path traversal protection
  - Input sanitization
- Documentation
  - README with quick start guide
  - Architecture documentation
  - API reference
  - Contributing guidelines
  - Changelog

### Security
- HTML escaping on all user input
- Secure password comparison with `secrets.compare_digest()`
- Path traversal protection in static file serving
- HttpOnly and SameSite cookie flags for sessions

---

## Version Format

Versions follow Semantic Versioning:
- **MAJOR** version when you make incompatible API changes
- **MINOR** version when you add functionality in a backward compatible manner
- **PATCH** version when you make backward compatible bug fixes

---

## How to Contribute Changes

When making changes for a new release:

1. Add an `[Unreleased]` section at the top if not present
2. Document your changes under appropriate headers:
   - **Added** for new features
   - **Changed** for changes in existing functionality
   - **Deprecated** for soon-to-be removed features
   - **Removed** for now removed features
   - **Fixed** for any bug fixes
   - **Security** for security vulnerability fixes
3. When ready to release:
   - Create a new section with the version and date
   - Move items from [Unreleased] to the new version
   - Update the [Unreleased] section to be empty

---

## Unreleased Template

Copy this to the top of the file when starting a new development cycle:

```markdown
## [Unreleased]

### Added
- 

### Changed
- 

### Deprecated
- 

### Removed
- 

### Fixed
- 

### Security
- 
```

---

## Release Example

When releasing version 1.1.0:

```markdown
## [1.1.0] - 2024-10-15

### Added
- Database migration to SQLite
- User authentication system
- Email scheduling feature

### Changed
- Improved festival search performance
- Updated admin dashboard UI

### Fixed
- Session timeout not working correctly
- CSV file corrupted on concurrent writes

### Security
- Added rate limiting to prevent brute force attacks
```

---

## Links

- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)

---

For more information on FESTIVE G, see:
- [README](README.md) - Project overview
- [ARCHITECTURE](ARCHITECTURE.md) - Technical details
- [CONTRIBUTING](CONTRIBUTING.md) - How to contribute
