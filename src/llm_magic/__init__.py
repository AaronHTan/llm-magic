"""
LLM Magic - Custom Jupyter magic for LLM integration
"""

from .magic import LLMMagic
from .clients import LLMClientBase, OpenAIClient, ClaudeClient
from .bridge import IPythonBridge

__version__ = "0.1.0"
__all__ = ["LLMMagic", "LLMClientBase", "OpenAIClient", "ClaudeClient", "IPythonBridge"]

def load_ipython_extension(ipython):
    """Load the LLM magic extension in IPython/Jupyter."""
    ipython.register_magics(LLMMagic)