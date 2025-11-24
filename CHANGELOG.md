# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-24

### Added
- **Message Persistence** - SQLite database stores conversations across sessions
- **API Authentication** - Bearer token-based security with hashed API keys
- **Rate Limiting** - 100 requests/hour per API key to prevent abuse
- **Session Management** - Track multiple independent conversations
- **Input Validation** - Comprehensive prompt validation and error handling
- **Local Fallback Mode** - Test without Azure credentials using mock responses
- Professional README with badges and complete documentation
- QUICKSTART.md for quick reference
- FEATURES.md with complete API documentation
- IMPLEMENTATION.md with technical architecture
- PowerShell test script (test_api.ps1)
- Professional project structure with organized directories

### Changed
- Reorganized project into enterprise-standard folder structure:
  - `/src` - Source code
  - `/tests` - Test files
  - `/docs` - Documentation
  - `/config` - Configuration
  - `/data` - Data files
  - `/scripts` - Utility scripts

### Fixed
- Proper error handling for missing environment variables
- Input validation for prompts (max 2000 characters)

### Security
- API keys hashed using SHA256 before storage
- Bearer token authentication on all protected endpoints
- Rate limiting per API key
- Environment variables for sensitive configuration

## [0.1.0] - Initial Release

### Added
- Basic Flask API server
- Azure OpenAI integration
- Mock response mode for local testing
- Health check endpoint

---

## Unreleased

### Planned Features
- [ ] User management dashboard
- [ ] Analytics and usage metrics
- [ ] WebSocket support for real-time chat
- [ ] Message search and filtering
- [ ] Conversation export (JSON, PDF, CSV)
- [ ] Multi-region support
- [ ] GraphQL API
- [ ] Message formatting (markdown, syntax highlighting)
- [ ] Conversation templates
- [ ] Cost tracking per API key
- [ ] Webhook notifications
- [ ] Multi-language support
- [ ] Custom system prompts per session
- [ ] Vector embeddings for semantic search
- [ ] Conversation branching

### Known Issues
- In-memory token cache resets on server restart
- SQLite suitable for development only (consider PostgreSQL for production)

---

## Versioning

This project follows semantic versioning:
- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes

---

## How to Read This File

- `[YYYY-MM-DD]` format for dates
- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` for vulnerability fixes
