"""
LLM client implementations for various providers.
"""

import os
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import requests
import json


class LLMClientBase(ABC):
    """Abstract base class for LLM clients."""
    
    @abstractmethod
    def call_model(self, prompt: str, **kwargs) -> str:
        """Call the LLM with the given prompt and return the response."""
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """Return the name of the model being used."""
        pass


class OpenAIClient(LLMClientBase):
    """OpenAI API client implementation."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.base_url = "https://api.openai.com/v1"
        
        if not self.api_key:
            raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY environment variable.")
    
    def call_model(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.7, **kwargs) -> str:
        """Call OpenAI's API with the given prompt."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenAI API error: {e}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Unexpected OpenAI API response format: {e}")
    
    def get_model_name(self) -> str:
        return f"openai/{self.model}"


class ClaudeClient(LLMClientBase):
    """Anthropic Claude API client implementation."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-sonnet-20240229"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self.base_url = "https://api.anthropic.com/v1"
        
        if not self.api_key:
            raise ValueError("Anthropic API key not provided. Set ANTHROPIC_API_KEY environment variable.")
    
    def call_model(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.7, **kwargs) -> str:
        """Call Anthropic's API with the given prompt."""
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/messages",
                headers=headers,
                json=data,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            return result["content"][0]["text"].strip()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Anthropic API error: {e}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Unexpected Anthropic API response format: {e}")
    
    def get_model_name(self) -> str:
        return f"claude/{self.model}"


class ClientFactory:
    """Factory for creating LLM clients."""
    
    @staticmethod
    def create_client(provider: str, **kwargs) -> LLMClientBase:
        """Create an LLM client for the specified provider."""
        if provider.lower() == "openai":
            return OpenAIClient(**kwargs)
        elif provider.lower() == "claude":
            return ClaudeClient(**kwargs)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    
    @staticmethod
    def get_available_providers() -> list:
        """Get list of available LLM providers."""
        return ["openai", "claude"]