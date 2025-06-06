"""
Configuration management for LLM Magic.
"""

import os
import yaml
from typing import Any, Dict, Optional
from pathlib import Path


class ConfigManager:
    """Manages configuration for LLM Magic."""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or self._get_default_config_path()
        self._config: Dict[str, Any] = {}
        self._load_config()
    
    def _get_default_config_path(self) -> str:
        """Get the default configuration file path."""
        home_dir = Path.home()
        config_dir = home_dir / ".llm_magic"
        config_dir.mkdir(exist_ok=True)
        return str(config_dir / "config.yaml")
    
    def _load_config(self) -> None:
        """Load configuration from file and environment variables."""
        # Default configuration
        self._config = {
            'debug': False,
            'default_provider': 'openai',
            'default_openai_model': 'gpt-4',
            'default_claude_model': 'claude-3-sonnet-20240229',
            'max_context_cells': 10,
            'max_tokens': 2000,
            'temperature': 0.7,
            'log_requests': False,
            'log_file': None
        }
        
        # Load from file if it exists
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    file_config = yaml.safe_load(f) or {}
                self._config.update(file_config)
            except Exception as e:
                print(f"Warning: Could not load config file {self.config_file}: {e}")
        
        # Override with environment variables
        env_mappings = {
            'LLM_MAGIC_DEBUG': 'debug',
            'LLM_MAGIC_DEFAULT_PROVIDER': 'default_provider',
            'LLM_MAGIC_LOG_REQUESTS': 'log_requests',
            'LLM_MAGIC_LOG_FILE': 'log_file'
        }
        
        for env_var, config_key in env_mappings.items():
            if os.getenv(env_var):
                value = os.getenv(env_var)
                # Convert string boolean values
                if value.lower() in ('true', 'false'):
                    value = value.lower() == 'true'
                self._config[config_key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self._config[key] = value
    
    def save(self) -> None:
        """Save configuration to file."""
        try:
            config_dir = Path(self.config_file).parent
            config_dir.mkdir(exist_ok=True)
            
            with open(self.config_file, 'w') as f:
                yaml.dump(self._config, f, default_flow_style=False)
        except Exception as e:
            print(f"Warning: Could not save config file {self.config_file}: {e}")
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values."""
        return self._config.copy()
    
    def reset(self) -> None:
        """Reset configuration to defaults."""
        self._config = {
            'debug': False,
            'default_provider': 'openai',
            'default_openai_model': 'gpt-4',
            'default_claude_model': 'claude-3-sonnet-20240229',
            'max_context_cells': 10,
            'max_tokens': 2000,
            'temperature': 0.7,
            'log_requests': False,
            'log_file': None
        }