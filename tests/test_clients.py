"""
Tests for LLM client implementations.
"""

import pytest
from unittest.mock import Mock, patch
from llm_magic.clients import LLMClientBase, OpenAIClient, ClaudeClient, ClientFactory


class TestLLMClientBase:
    """Test the abstract base class."""
    
    def test_abstract_methods(self):
        """Test that abstract methods raise NotImplementedError."""
        with pytest.raises(TypeError):
            LLMClientBase()


class TestOpenAIClient:
    """Test OpenAI client implementation."""
    
    def test_init_with_api_key(self):
        """Test initialization with API key."""
        client = OpenAIClient(api_key="test-key")
        assert client.api_key == "test-key"
        assert client.model == "gpt-4"
    
    def test_init_without_api_key(self):
        """Test initialization without API key raises error."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="OpenAI API key not provided"):
                OpenAIClient()
    
    @patch('llm_magic.clients.requests.post')
    def test_call_model_success(self, mock_post):
        """Test successful API call."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Hello, world!"}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        client = OpenAIClient(api_key="test-key")
        result = client.call_model("Test prompt")
        
        assert result == "Hello, world!"
        mock_post.assert_called_once()
    
    @patch('llm_magic.clients.requests.post')
    def test_call_model_api_error(self, mock_post):
        """Test API error handling."""
        mock_post.side_effect = Exception("API Error")
        
        client = OpenAIClient(api_key="test-key")
        
        with pytest.raises(Exception, match="OpenAI API error"):
            client.call_model("Test prompt")
    
    def test_get_model_name(self):
        """Test model name generation."""
        client = OpenAIClient(api_key="test-key", model="gpt-3.5-turbo")
        assert client.get_model_name() == "openai/gpt-3.5-turbo"


class TestClaudeClient:
    """Test Claude client implementation."""
    
    def test_init_with_api_key(self):
        """Test initialization with API key."""
        client = ClaudeClient(api_key="test-key")
        assert client.api_key == "test-key"
        assert client.model == "claude-3-sonnet-20240229"
    
    def test_init_without_api_key(self):
        """Test initialization without API key raises error."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="Anthropic API key not provided"):
                ClaudeClient()
    
    @patch('llm_magic.clients.requests.post')
    def test_call_model_success(self, mock_post):
        """Test successful API call."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "content": [{"text": "Hello from Claude!"}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        client = ClaudeClient(api_key="test-key")
        result = client.call_model("Test prompt")
        
        assert result == "Hello from Claude!"
        mock_post.assert_called_once()
    
    def test_get_model_name(self):
        """Test model name generation."""
        client = ClaudeClient(api_key="test-key", model="claude-3-opus-20240229")
        assert client.get_model_name() == "claude/claude-3-opus-20240229"


class TestClientFactory:
    """Test the client factory."""
    
    def test_create_openai_client(self):
        """Test creating OpenAI client."""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            client = ClientFactory.create_client("openai")
            assert isinstance(client, OpenAIClient)
    
    def test_create_claude_client(self):
        """Test creating Claude client."""
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            client = ClientFactory.create_client("claude")
            assert isinstance(client, ClaudeClient)
    
    def test_invalid_provider(self):
        """Test invalid provider raises error."""
        with pytest.raises(ValueError, match="Unsupported LLM provider"):
            ClientFactory.create_client("invalid")
    
    def test_get_available_providers(self):
        """Test getting available providers."""
        providers = ClientFactory.get_available_providers()
        assert "openai" in providers
        assert "claude" in providers