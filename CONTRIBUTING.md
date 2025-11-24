# Contributing to Azure OpenAI Chatbot

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person

## Getting Started

1. **Fork** the repository
2. **Clone** your fork
   ```bash
   git clone https://github.com/YOUR-USERNAME/azure-openai-chatbot.git
   cd azure-openai-chatbot
   ```
3. **Create** a virtual environment
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```
4. **Install** dependencies
   ```bash
   pip install -r config/requirements.txt
   ```
5. **Create** a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Making Changes

1. Make your changes in the `/src` directory
2. Write tests in `/tests` directory
3. Update documentation in `/docs` if needed
4. Test your changes:
   ```bash
   python src/app.py
   # In another terminal:
   tests/test_api.ps1
   ```

### Commit Guidelines

Use meaningful commit messages:

```bash
git commit -m "feat: Add new feature description"
git commit -m "fix: Fix bug description"
git commit -m "docs: Update documentation"
git commit -m "refactor: Refactor code section"
```

**Commit Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance

### Pushing Changes

```bash
git push origin feature/your-feature-name
```

## Creating a Pull Request

1. **Go** to GitHub and click "Compare & pull request"
2. **Fill** in the PR description:
   - What changes you made
   - Why you made them
   - How to test
   - Any related issues
3. **Link** related issues (if any)
4. **Wait** for review and address feedback

### PR Title Format
```
[TYPE] Brief description

Detailed description here
```

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## How to Test
Steps to verify the changes

## Checklist
- [ ] Code follows project style
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No new warnings
```

## Coding Standards

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

Example:
```python
def validate_api_key(api_key):
    """
    Validate API key from Authorization header.
    
    Args:
        api_key (str): The API key to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not api_key:
        return False
    # ... validation logic
    return True
```

### File Organization

```
src/
├── __init__.py
├── app.py                 # Main application
├── models/                # Data models
├── services/              # Business logic
├── utils/                 # Utility functions
└── config.py              # Configuration
```

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage
- Use descriptive test names

## Documentation

- Update README.md if adding features
- Add docstrings to all functions
- Update FEATURES.md for user-facing changes
- Add technical details to IMPLEMENTATION.md

## Reporting Issues

### Bug Reports

Include:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Python version and OS
- Error messages/stack traces

### Feature Requests

Include:
- Description of the feature
- Use case and benefits
- Possible implementation approach
- Related issues (if any)

## Questions?

- Check existing issues and discussions
- Read the documentation in `/docs`
- Open an issue with the `question` label

## Recognition

Contributors will be:
- Added to the project contributors list
- Mentioned in release notes
- Credited in commits

---

Thank you for contributing to making this project better! 🎉
