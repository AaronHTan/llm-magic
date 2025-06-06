"""
Logging functionality for LLM Magic.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, Optional
from pathlib import Path


class LLMLogger:
    """Logger for LLM requests and responses."""
    
    def __init__(self, log_file: Optional[str] = None, enabled: bool = True):
        self.enabled = enabled
        self.log_file = log_file or self._get_default_log_path()
        self._ensure_log_directory()
    
    def _get_default_log_path(self) -> str:
        """Get the default log file path."""
        home_dir = Path.home()
        log_dir = home_dir / ".llm_magic" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create timestamped log file
        timestamp = datetime.now().strftime("%Y%m%d")
        return str(log_dir / f"llm_requests_{timestamp}.json")
    
    def _ensure_log_directory(self) -> None:
        """Ensure the log directory exists."""
        if self.log_file:
            log_dir = Path(self.log_file).parent
            log_dir.mkdir(parents=True, exist_ok=True)
    
    def log_request(self, 
                   provider: str,
                   model: str,
                   prompt: str,
                   response: str,
                   metadata: Optional[Dict[str, Any]] = None) -> None:
        """Log an LLM request and response."""
        if not self.enabled:
            return
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "provider": provider,
            "model": model,
            "prompt_length": len(prompt),
            "response_length": len(response),
            "prompt": prompt[:1000] + "..." if len(prompt) > 1000 else prompt,
            "response": response[:1000] + "..." if len(response) > 1000 else response,
            "metadata": metadata or {}
        }
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f"Warning: Could not write to log file: {e}")
    
    def get_recent_logs(self, count: int = 10) -> list:
        """Get recent log entries."""
        if not os.path.exists(self.log_file):
            return []
        
        try:
            logs = []
            with open(self.log_file, 'r') as f:
                for line in f:
                    if line.strip():
                        logs.append(json.loads(line))
            
            return logs[-count:] if logs else []
        except Exception as e:
            print(f"Warning: Could not read log file: {e}")
            return []
    
    def clear_logs(self) -> None:
        """Clear all log entries."""
        try:
            if os.path.exists(self.log_file):
                os.remove(self.log_file)
        except Exception as e:
            print(f"Warning: Could not clear log file: {e}")


class SecurityValidator:
    """Validates and sanitizes inputs for security."""
    
    @staticmethod
    def sanitize_prompt(prompt: str) -> str:
        """Sanitize prompt to remove potential security issues."""
        # Remove potential command injection patterns
        dangerous_patterns = [
            'rm -rf',
            'sudo',
            'chmod',
            'eval(',
            'exec(',
            '__import__',
        ]
        
        sanitized = prompt
        for pattern in dangerous_patterns:
            if pattern in sanitized.lower():
                print(f"Warning: Potentially dangerous pattern '{pattern}' detected in prompt")
        
        return sanitized
    
    @staticmethod
    def validate_api_key(api_key: str, provider: str) -> bool:
        """Validate API key format."""
        if not api_key:
            return False
        
        if provider == 'openai':
            return api_key.startswith('sk-') and len(api_key) > 20
        elif provider == 'claude':
            return len(api_key) > 20
        
        return True
    
    @staticmethod
    def sanitize_code_execution(code: str) -> str:
        """Sanitize code before execution."""
        # Remove potentially dangerous operations
        dangerous_operations = [
            'os.system',
            'subprocess.call',
            'subprocess.run',
            'eval(',
            'exec(',
            '__import__',
            'open(',
            'file(',
        ]
        
        for operation in dangerous_operations:
            if operation in code:
                print(f"Warning: Potentially dangerous operation '{operation}' detected in code")
        
        return code