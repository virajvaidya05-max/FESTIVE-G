# FESTIVE G - Documentation Index

Quick reference for finding the right documentation.

## 📖 Start Here

**New to FESTIVE G?**
→ Read [README.md](README.md) first for overview and quick start

**Want to understand how it works?**
→ Read [ARCHITECTURE.md](ARCHITECTURE.md) for technical design

**Need to know what endpoints/functions do?**
→ Read [API.md](API.md) for complete reference

**Want to contribute?**
→ Read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines

**Want to see what changed?**
→ Read [CHANGELOG.md](CHANGELOG.md) for version history

---

## 📚 Documentation Files

### Core Documentation

| File | Purpose | Audience |
|------|---------|----------|
| **README.md** | Overview, features, quick start, FAQ | Everyone |
| **ARCHITECTURE.md** | Technical design, components, data flow | Developers |
| **API.md** | Endpoints, functions, parameters, examples | Developers, API users |
| **CONTRIBUTING.md** | Code style, testing, commit format | Contributors |
| **CHANGELOG.md** | Version history, what changed | Everyone |

### Configuration Files

| File | Purpose |
|------|---------|
| **.env.example** | Environment variables template |
| **.gitignore** | Git ignore rules |
| **setup.py** | Python package configuration |
| **requirements.txt** | Python dependencies (none required) |

### Project Structure

```
festive-g/
├── app.py                    # Main application
├── README.md                 # Start here
├── ARCHITECTURE.md           # How it works
├── API.md                    # Functions & endpoints
├── CONTRIBUTING.md           # How to contribute
├── CHANGELOG.md              # Version history
├── DOCS_INDEX.md             # This file
├── setup.py                  # Package config
├── requirements.txt          # Dependencies
├── .env.example              # Config template
├── .gitignore                # Git rules
├── templates/                # HTML templates
├── static/                   # CSS & images
└── data/                     # Auto-created data
    ├── festivals.json
    └── submissions.csv
```

---

## 🎯 Find What You Need

### "How do I...?"

#### Get started?
→ [README.md - Quick Start](README.md#quick-start)

#### Deploy to production?
→ [README.md - Deployment](README.md#deployment)

#### Configure SMTP for emails?
→ [.env.example](.env.example) or [README.md - Configuration](README.md#configuration)

#### Understand the project structure?
→ [ARCHITECTURE.md - Project Structure](ARCHITECTURE.md#project-structure)

#### Find all API endpoints?
→ [API.md - HTTP Endpoints](API.md#http-endpoints)

#### Use Python functions?
→ [API.md - Python Functions](API.md#python-functions)

#### Add a new feature?
→ [CONTRIBUTING.md - Common Tasks](CONTRIBUTING.md#common-tasks)

#### Follow code style?
→ [CONTRIBUTING.md - Code Style](CONTRIBUTING.md#code-style)

#### Make a commit?
→ [CONTRIBUTING.md - Commit Messages](CONTRIBUTING.md#commit-messages)

#### Fix a security issue?
→ [ARCHITECTURE.md - Security Notes](ARCHITECTURE.md#security-notes) or [CONTRIBUTING.md - Security](CONTRIBUTING.md#security-considerations)

#### See what's new?
→ [CHANGELOG.md](CHANGELOG.md)

#### Troubleshoot problems?
→ [README.md - Troubleshooting](README.md#troubleshooting)

---

## 👥 By Role

### 👤 User
- Read [README.md](README.md) for overview
- Follow [README.md - Quick Start](README.md#quick-start) to set up
- Check [README.md - Usage](README.md#usage) for how to use
- See [README.md - FAQ](README.md#faq) for answers

### 💻 Developer (Non-contributor)
- Read [README.md](README.md)
- Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand design
- Read [API.md](API.md) for all functions and endpoints
- Use [API.md - Examples](API.md#examples) for integration

### 🔧 Contributor
- Read [README.md](README.md)
- Read [ARCHITECTURE.md](ARCHITECTURE.md)
- Follow [CONTRIBUTING.md](CONTRIBUTING.md) guidelines
- Check [CONTRIBUTING.md - Code Style](CONTRIBUTING.md#code-style)
- Use [CONTRIBUTING.md - Common Tasks](CONTRIBUTING.md#common-tasks) for reference

### 📊 Maintainer
- Review all documents
- Update [CHANGELOG.md](CHANGELOG.md) for releases
- Ensure [CONTRIBUTING.md](CONTRIBUTING.md) reflects actual process
- Keep [ARCHITECTURE.md](ARCHITECTURE.md) synchronized with code
- Monitor [API.md](API.md) for breaking changes

---

## 📋 Quick Links

### Installation & Setup
- [Quick Start](README.md#quick-start)
- [Configuration](README.md#configuration)
- [Environment Variables](.env.example)

### Features & Usage
- [Features](README.md#features)
- [Usage](README.md#usage)
- [API Endpoints](API.md#http-endpoints)

### Technical Information
- [Architecture Overview](ARCHITECTURE.md#overview)
- [Project Structure](ARCHITECTURE.md#project-structure)
- [Core Components](ARCHITECTURE.md#core-components)
- [Data Flow](ARCHITECTURE.md#data-flow-diagram)

### Development
- [Contributing Guidelines](CONTRIBUTING.md)
- [Code Style](CONTRIBUTING.md#code-style)
- [Testing](CONTRIBUTING.md#testing)
- [Common Tasks](CONTRIBUTING.md#common-tasks)

### Reference
- [API Functions](API.md#python-functions)
- [Endpoints Reference](API.md#http-endpoints)
- [Data Structures](API.md#data-structures)

### Troubleshooting
- [Troubleshooting](README.md#troubleshooting)
- [FAQ](README.md#faq)
- [Limitations](ARCHITECTURE.md#limitations--known-issues)

---

## 🔍 Search Guide

**If you want information about:**

| Topic | Look in |
|-------|----------|
| Emails | README.md (Configuration), .env.example, ARCHITECTURE.md (Email Integration) |
| Security | ARCHITECTURE.md (Security Notes), CONTRIBUTING.md (Security) |
| Admin panel | README.md (Usage), ARCHITECTURE.md (Core Components), API.md (Admin Routes) |
| Endpoints | API.md (HTTP Endpoints), README.md (API Endpoints) |
| Functions | API.md (Python Functions) |
| Data | ARCHITECTURE.md (Data Management), API.md (Data Structures) |
| Deployment | README.md (Deployment) |
| Testing | CONTRIBUTING.md (Testing) |
| Code style | CONTRIBUTING.md (Code Style) |
| Validation | API.md (validate_user_form) |
| Festivals | ARCHITECTURE.md (Festival Storage) |

---

## 📞 Need Help?

1. **Check the relevant section above** for documentation link
2. **Search this file** (Ctrl+F) for keywords
3. **Check FAQ** in [README.md](README.md#faq)
4. **Check Troubleshooting** in [README.md](README.md#troubleshooting)
5. **Open an issue** on GitHub

---

## 📝 Documentation Status

| File | Status | Last Updated |
|------|--------|--------------|
| README.md | ✅ Complete | 2024-09-25 |
| ARCHITECTURE.md | ✅ Complete | 2024-09-25 |
| API.md | ✅ Complete | 2024-09-25 |
| CONTRIBUTING.md | ✅ Complete | 2024-09-25 |
| CHANGELOG.md | ✅ Complete | 2024-09-25 |
| .env.example | ✅ Complete | 2024-09-25 |
| .gitignore | ✅ Complete | 2024-09-25 |
| setup.py | ✅ Complete | 2024-09-25 |
| requirements.txt | ✅ Complete | 2024-09-25 |

---

## 🎓 Learning Path

**Beginner:** README → Quick Start → Usage

**Intermediate:** README → ARCHITECTURE → API Reference

**Advanced:** All documents + code review + contribution

---

## 💡 Tips

- 📌 **Bookmark** README.md for quick reference
- 🔗 **Use links** to jump between related sections
- 🔍 **Search** (Ctrl+F) within documents
- 📖 **Skim** headings first to understand structure
- 💬 **Comment** code with references to these docs

---

Happy documenting! 🎉

For more information, visit the [main README](README.md).
