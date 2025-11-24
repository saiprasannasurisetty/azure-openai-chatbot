# Project Structure

```
azure-openai-chatbot/
├── .github/                    # GitHub configuration
│   └── workflows/              # CI/CD workflows (future)
├── src/                        # Source code
│   └── app.py                  # Main Flask application
├── tests/                      # Test files
│   ├── __init__.py
│   └── test_api.ps1            # PowerShell API tests
├── docs/                       # Documentation
│   ├── FEATURES.md            # Feature documentation
│   ├── IMPLEMENTATION.md       # Technical implementation
│   └── QUICKSTART.md           # Quick start guide
├── config/                     # Configuration files
│   ├── .env                    # Environment variables (local)
│   ├── .env.example            # Example environment variables
│   └── requirements.txt        # Python dependencies
├── data/                       # Data files
│   └── chatbot_data.db        # SQLite database
├── scripts/                    # Utility scripts
│   └── setup.sh (coming)       # Setup script
├── .gitignore                  # Git ignore rules
├── README.md                   # Main documentation
├── LICENSE                     # License file
├── setup.py (coming)           # Package setup
└── docker-compose.yml (coming) # Docker configuration
```

## Directory Purposes

### `/src`
- Main application source code
- Python modules and core logic
- Entry point: `app.py`

### `/tests`
- Test scripts and utilities
- API testing tools
- Unit tests and integration tests

### `/docs`
- Feature documentation
- Technical guides
- Quick start guides
- Architecture documentation

### `/config`
- Environment configuration
- Dependencies definition
- Example configurations

### `/data`
- SQLite database files
- Data persistence layer
- Can be gitignored for local-only data

### `/scripts`
- Setup and utility scripts
- Deployment helpers
- Database migration tools

### `/.github`
- GitHub Actions workflows
- Issue templates
- Pull request templates
- Contributing guidelines

## Key Files

| File | Purpose |
|------|---------|
| `README.md` | Main project documentation |
| `LICENSE` | MIT License |
| `.gitignore` | Git exclusion rules |
| `setup.py` | Package setup (coming soon) |
| `docker-compose.yml` | Docker orchestration (coming soon) |
| `Dockerfile` | Container definition (coming soon) |

## Development Workflow

```
1. Clone repository
   ↓
2. Copy config/requirements.txt → Install dependencies
   ↓
3. Copy config/.env.example → config/.env
   ↓
4. Edit config/.env with credentials
   ↓
5. Run: python src/app.py
   ↓
6. Test with: tests/test_api.ps1
```

## Adding New Modules

When adding new features:
- Place Python modules in `/src`
- Add tests in `/tests`
- Document in `/docs`
- Update requirements in `/config/requirements.txt`

