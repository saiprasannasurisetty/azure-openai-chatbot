"""
Unit tests for Azure OpenAI Chatbot API

Tests cover:
- Authentication (API key validation)
- Rate limiting
- Input validation
- API endpoints
- Session management
"""

import pytest
import os
import sys
import tempfile
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture
def test_db():
    """Create temporary test database"""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def client(test_db):
    """Create test Flask client with isolated database"""
    # Patch database path before importing
    with patch('app.DB_PATH', test_db):
        from app import app, init_database, rate_limits, active_tokens
        
        app.config['TESTING'] = True
        init_database()
        
        with app.test_client() as test_client:
            yield test_client
        
        rate_limits.clear()
        active_tokens.clear()


@pytest.fixture(autouse=True)
def reset_caches():
    """Reset rate limits and token cache"""
    from app import rate_limits, active_tokens
    rate_limits.clear()
    active_tokens.clear()
    yield
    rate_limits.clear()
    active_tokens.clear()


# ============== HEALTH & AUTH TESTS ==============

class TestHealth:
    """Test health endpoint"""
    
    def test_health_check(self, client):
        """Health endpoint should return status"""
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json['status'] == 'ok'


class TestAuthentication:
    """Test API key authentication"""
    
    def test_generate_api_key(self, client):
        """Should generate valid API key"""
        response = client.post('/auth/generate-key')
        assert response.status_code == 201
        assert 'api_key' in response.json
        assert len(response.json['api_key']) > 20
    
    def test_missing_auth_header(self, client):
        """Protected endpoints require auth"""
        response = client.post('/chat', json={'prompt': 'test'})
        assert response.status_code == 401
    
    def test_invalid_bearer_token(self, client):
        """Invalid bearer token should fail"""
        response = client.post(
            '/chat',
            json={'prompt': 'test'},
            headers={'Authorization': 'Bearer invalid_token'}
        )
        assert response.status_code == 401
    
    def test_valid_api_key_works(self, client):
        """Valid API key should authenticate"""
        # Generate key
        key_resp = client.post('/auth/generate-key')
        api_key = key_resp.json['api_key']
        
        # Use key in request
        response = client.post(
            '/chat',
            json={'prompt': 'test prompt'},
            headers={'Authorization': f'Bearer {api_key}'}
        )
        # Should not get auth error (might get other errors)
        assert response.status_code != 401


# ============== INPUT VALIDATION ==============

class TestInputValidation:
    """Test prompt validation"""
    
    def test_empty_prompt_rejected(self):
        """Empty prompts should be rejected"""
        from app import validate_prompt
        result, error = validate_prompt("")
        assert result is None
        assert "empty" in error.lower()
    
    def test_whitespace_prompt_rejected(self):
        """Whitespace-only prompts should be rejected"""
        from app import validate_prompt
        result, error = validate_prompt("   \n   ")
        assert result is None
    
    def test_long_prompt_rejected(self):
        """Prompts > 2000 chars should be rejected"""
        from app import validate_prompt
        result, error = validate_prompt("x" * 2001)
        assert result is None
        assert "2000" in error
    
    def test_valid_prompt_accepted(self):
        """Valid prompts should pass"""
        from app import validate_prompt
        result, error = validate_prompt("Valid prompt here")
        assert error is None
        assert result == "Valid prompt here"
    
    def test_whitespace_stripped(self):
        """Prompt whitespace should be stripped"""
        from app import validate_prompt
        result, error = validate_prompt("  test  \n")
        assert error is None
        assert result == "test"


# ============== CRYPTOGRAPHY ==============

class TestCryptography:
    """Test API key hashing"""
    
    def test_hash_deterministic(self):
        """Same input produces same hash"""
        from app import hash_api_key
        key = "test_key_123"
        h1 = hash_api_key(key)
        h2 = hash_api_key(key)
        assert h1 == h2
    
    def test_different_keys_different_hash(self):
        """Different keys produce different hashes"""
        from app import hash_api_key
        assert hash_api_key("key1") != hash_api_key("key2")
    
    def test_sha256_length(self):
        """Hash should be SHA256 (64 hex chars)"""
        from app import hash_api_key
        h = hash_api_key("test")
        assert len(h) == 64


# ============== RATE LIMITING ==============

class TestRateLimiting:
    """Test rate limiting logic"""
    
    def test_under_limit_allowed(self):
        """Requests under limit should be allowed"""
        from app import check_rate_limit, rate_limits
        rate_limits.clear()
        
        for i in range(50):
            assert check_rate_limit("user1") is True
    
    def test_over_limit_rejected(self):
        """Requests over limit should be rejected"""
        from app import check_rate_limit, rate_limits
        rate_limits.clear()
        
        # Fill limit
        for i in range(100):
            check_rate_limit("user1")
        
        # Next should fail
        assert check_rate_limit("user1") is False
    
    def test_per_user_limits(self):
        """Rate limits are per user"""
        from app import check_rate_limit, rate_limits
        rate_limits.clear()
        
        # User 1 at limit
        for i in range(100):
            check_rate_limit("user1")
        
        # User 2 should not be affected
        assert check_rate_limit("user2") is True


# ============== API ENDPOINTS ==============

class TestChatEndpoint:
    """Test /chat endpoint"""
    
    def test_chat_requires_auth(self, client):
        """Chat endpoint requires authentication"""
        response = client.post('/chat', json={'prompt': 'test'})
        assert response.status_code == 401
    
    def test_chat_with_valid_key(self, client):
        """Chat should work with valid key"""
        key_resp = client.post('/auth/generate-key')
        api_key = key_resp.json['api_key']
        
        response = client.post(
            '/chat',
            json={'prompt': 'Hello?'},
            headers={'Authorization': f'Bearer {api_key}'}
        )
        
        assert response.status_code == 200
        assert 'response' in response.json
        assert 'session_id' in response.json
    
    def test_chat_empty_prompt_fails(self, client):
        """Empty prompt should fail"""
        key_resp = client.post('/auth/generate-key')
        api_key = key_resp.json['api_key']
        
        response = client.post(
            '/chat',
            json={'prompt': ''},
            headers={'Authorization': f'Bearer {api_key}'}
        )
        
        assert response.status_code == 400


class TestHistoryEndpoint:
    """Test /history endpoint"""
    
    def test_history_requires_auth(self, client):
        """History endpoint requires authentication"""
        response = client.get('/history')
        assert response.status_code == 401
    
    def test_history_retrieval(self, client):
        """Should retrieve message history"""
        key_resp = client.post('/auth/generate-key')
        api_key = key_resp.json['api_key']
        headers = {'Authorization': f'Bearer {api_key}'}
        
        # Send a message
        client.post(
            '/chat',
            json={'prompt': 'test message'},
            headers=headers
        )
        
        # Get history
        response = client.get('/history', headers=headers)
        
        assert response.status_code == 200
        assert 'history' in response.json
        assert response.json['total_messages'] > 0


# ============== INTEGRATION ==============

class TestIntegration:
    """End-to-end tests"""
    
    def test_full_flow(self, client):
        """Test complete user workflow"""
        # 1. Generate key
        key_resp = client.post('/auth/generate-key')
        assert key_resp.status_code == 201
        api_key = key_resp.json['api_key']
        
        # 2. Chat with key
        headers = {'Authorization': f'Bearer {api_key}'}
        chat_resp = client.post(
            '/chat',
            json={'prompt': 'test'},
            headers=headers
        )
        assert chat_resp.status_code == 200
        
        # 3. Get history
        hist_resp = client.get('/history', headers=headers)
        assert hist_resp.status_code == 200
        assert len(hist_resp.json['history']) > 0
    
    def test_sessions_isolated(self, client):
        """Sessions should be isolated"""
        key_resp = client.post('/auth/generate-key')
        api_key = key_resp.json['api_key']
        headers_base = {'Authorization': f'Bearer {api_key}'}
        
        # Session A
        headers_a = {**headers_base, 'X-Session-ID': 'session_a'}
        client.post(
            '/chat',
            json={'prompt': 'message_a'},
            headers=headers_a
        )
        
        # Session B
        headers_b = {**headers_base, 'X-Session-ID': 'session_b'}
        client.post(
            '/chat',
            json={'prompt': 'message_b'},
            headers=headers_b
        )
        
        # Get histories
        hist_a = client.get('/history', headers=headers_a).json['history']
        hist_b = client.get('/history', headers=headers_b).json['history']
        
        # Both should have content
        assert len(hist_a) > 0
        assert len(hist_b) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
