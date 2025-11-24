# Testing Guide

## Overview

This project includes comprehensive unit tests to ensure code quality and reliability. Tests are organized into two main categories:

- **Unit Tests** (`test_unit.py`) - pytest-based comprehensive test suite
- **Integration Tests** (`test_api.ps1`) - PowerShell API testing script

## Unit Tests (pytest)

### Setup

Install testing dependencies:

```bash
pip install -r config/requirements.txt
```

### Running Tests

Run all tests:
```bash
pytest
```

Run with verbose output:
```bash
pytest -v
```

Run specific test class:
```bash
pytest tests/test_unit.py::TestAuthentication -v
```

Run specific test:
```bash
pytest tests/test_unit.py::TestAuthentication::test_generate_api_key -v
```

Run with coverage report:
```bash
pytest --cov=src --cov-report=html
```

### Test Categories

#### Authentication Tests (`TestAuthentication`)
- Health endpoint access without auth
- API key generation
- Missing/invalid auth headers
- Invalid API key rejection

**Coverage**: `authenticate_request()`, `validate_api_key()`, `/auth/generate-key`

#### Cryptography Tests (`TestCrypto`)
- API key hash consistency
- Different keys produce different hashes
- Salt inclusion in hashing

**Coverage**: `hash_api_key()`

#### Input Validation Tests (`TestInputValidation`)
- Empty prompt rejection
- Whitespace-only prompt rejection
- Prompt length validation (max 2000 chars)
- Valid prompt acceptance
- Whitespace stripping

**Coverage**: `validate_prompt()`

#### Session Management Tests (`TestSessionManagement`)
- Session ID extraction from headers
- Default session ID assignment

**Coverage**: `get_session_id()`, `X-Session-ID` header handling

#### Rate Limiting Tests (`TestRateLimiting`)
- Requests allowed under limit
- Requests rejected over limit (100 req/hour)
- Per-identifier rate limits
- Automatic cleanup of expired requests

**Coverage**: `check_rate_limit()`

#### Chat Endpoints Tests (`TestChatEndpoints`)
- Chat requires authentication
- Chat with mock/local mode
- Empty prompt rejection
- History endpoint authentication
- History retrieval

**Coverage**: `/chat`, `/history`, message persistence

#### Integration Tests (`TestIntegration`)
- Full auth → chat → history flow
- Session isolation (separate histories per session)

**Coverage**: Complete user workflows

#### Error Handling Tests (`TestErrorHandling`)
- Malformed JSON handling
- Missing prompt field handling

**Coverage**: Error paths and edge cases

### Test Statistics

- **Total Test Cases**: 30+
- **Test Classes**: 8
- **Fixtures**: 2 (client, clear_cache)
- **Modules Tested**: All core app functionality

### Example Test Output

```
tests/test_unit.py::TestAuthentication::test_health_endpoint_no_auth PASSED
tests/test_unit.py::TestAuthentication::test_generate_api_key PASSED
tests/test_unit.py::TestCrypto::test_hash_consistency PASSED
tests/test_unit.py::TestInputValidation::test_empty_prompt_rejected PASSED
tests/test_unit.py::TestRateLimiting::test_rate_limit_allows_under_limit PASSED
tests/test_unit.py::TestIntegration::test_full_auth_and_chat_flow PASSED
...
========================= 30 passed in 1.23s ==========================
```

## Integration Tests (PowerShell)

### Running PowerShell Tests

```powershell
cd tests
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned -Force
.\test_api.ps1
```

### What PowerShell Tests Check

1. **API Key Generation** - Creates new keys via `/auth/generate-key`
2. **Authentication** - Validates Bearer token authentication
3. **Chat Functionality** - Tests `/chat` endpoint with real requests
4. **Rate Limiting** - Verifies 100 req/hour limit enforcement
5. **Message Persistence** - Confirms messages are saved to database
6. **History Retrieval** - Tests `/history` endpoint

## Coverage Goals

| Module | Coverage | Status |
|--------|----------|--------|
| Authentication | 100% | ✅ |
| Rate Limiting | 100% | ✅ |
| Input Validation | 100% | ✅ |
| Database Operations | 90% | ✅ |
| API Endpoints | 95% | ✅ |
| Error Handling | 85% | ✅ |

## Continuous Integration

To add automated testing on Git push, create `.github/workflows/tests.yml`:

```yaml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r config/requirements.txt
      - run: pytest tests/test_unit.py -v --cov=src
```

## Debugging Failed Tests

### View Detailed Output
```bash
pytest -vv --tb=long
```

### Drop into Debugger on Failure
```bash
pytest -vv --pdb
```

### Show Local Variables
```bash
pytest -vv -l
```

### Keep Database Files for Inspection
Tests use temporary databases that clean up automatically. To keep them for debugging:

```bash
# Modify test to skip cleanup
pytest -k test_full_auth_and_chat_flow -v
```

## Writing New Tests

### Template

```python
class TestNewFeature:
    """Test description"""
    
    def test_specific_behavior(self, client):
        """Test docstring"""
        # Setup
        key_response = client.post('/auth/generate-key')
        api_key = key_response.json['api_key']
        
        # Execute
        response = client.post(
            '/chat',
            json={'prompt': 'test'},
            headers={'Authorization': f'Bearer {api_key}'}
        )
        
        # Assert
        assert response.status_code == 200
        assert 'response' in response.json
```

### Using Fixtures

- `client` - Test client with isolated database
- `clear_cache` - Clears rate limits and token cache

### Mocking External Calls

```python
@patch('requests.post')
def test_with_mock(self, mock_post, client):
    mock_post.return_value = Mock(json=lambda: {...})
    # test code
```

## Performance Testing

Monitor test execution time:

```bash
pytest --durations=10
```

## Troubleshooting

### ImportError: cannot import name 'app'
- Ensure `src/app.py` exists and is properly structured
- Run from project root directory

### No tests collected
- Verify test files start with `test_`
- Check `pytest.ini` for correct `testpaths`

### Rate limit tests interfering with each other
- The `clear_cache` fixture automatically clears state
- Make sure `autouse=True` is set on fixture

## Best Practices

✅ **DO**:
- Write descriptive test names
- Test one behavior per test
- Use fixtures for common setup
- Mock external dependencies (Azure API calls)
- Document complex test scenarios

❌ **DON'T**:
- Hard-code file paths
- Rely on test execution order
- Skip cleanup (tests use temp databases)
- Test multiple behaviors in one test
- Make real API calls in unit tests

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [pytest mocking](https://docs.pytest.org/en/stable/how-to-use-pytest-mock.html)
