"""
Custom IPython magic for LLM integration.
"""

import argparse
import os
from typing import Optional, Dict, Any
from IPython.core.magic import Magics, magics_class, cell_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from .clients import ClientFactory, LLMClientBase
from .bridge import IPythonBridge
from .config import ConfigManager


@magics_class
class LLMMagic(Magics):
    """Custom magic class for LLM integration in Jupyter notebooks."""
    
    def __init__(self, shell=None):
        super().__init__(shell)
        self.bridge = IPythonBridge(shell)
        self.config = ConfigManager()
        self.console = Console()
        self._clients: Dict[str, LLMClientBase] = {}
    
    def _get_client(self, provider: str, model: Optional[str] = None) -> LLMClientBase:
        """Get or create an LLM client for the specified provider."""
        client_key = f"{provider}:{model or 'default'}"
        
        if client_key not in self._clients:
            kwargs = {}
            if model:
                kwargs['model'] = model
            
            self._clients[client_key] = ClientFactory.create_client(provider, **kwargs)
        
        return self._clients[client_key]
    
    @cell_magic
    @magic_arguments()
    @argument('--provider', '-p', default='openai', 
              help='LLM provider (openai, claude)')
    @argument('--model', '-m', default=None,
              help='Specific model to use')
    @argument('--context', '-c', type=int, default=3,
              help='Number of previous cells to include as context')
    @argument('--exec', action='store_true', dest='execute',
              help='Execute the returned code automatically')
    @argument('--inject', action='store_true',
              help='Inject response into a new cell')
    @argument('--no-variables', action='store_true',
              help='Exclude variable context from prompt')
    @argument('--temperature', '-t', type=float, default=0.7,
              help='Temperature for response generation (0.0-2.0)')
    @argument('--max-tokens', type=int, default=2000,
              help='Maximum tokens in response')
    @argument('--raw', action='store_true',
              help='Return raw response without formatting')
    def llm(self, line: str, cell: str):
        """
        %%llm magic command for LLM integration.
        
        Usage examples:
        %%llm
        Explain this code
        
        %%llm --provider claude --exec
        Write a function to calculate fibonacci numbers
        
        %%llm --context 5 --inject
        Refactor the above code for better performance
        """
        try:
            # Parse arguments
            args = parse_argstring(self.llm, line)
            
            # Validate provider
            if args.provider not in ClientFactory.get_available_providers():
                available = ", ".join(ClientFactory.get_available_providers())
                raise ValueError(f"Invalid provider '{args.provider}'. Available: {available}")
            
            # Get or create client
            client = self._get_client(args.provider, args.model)
            
            # Build context prompt
            include_variables = not args.no_variables
            full_prompt = self.bridge.build_context_prompt(
                cell, 
                context_cells=args.context,
                include_variables=include_variables
            )
            
            # Display what we're sending to the LLM (in debug mode)
            if self.config.get('debug', False):
                self.console.print(Panel(
                    full_prompt,
                    title=f"Prompt to {client.get_model_name()}",
                    border_style="blue"
                ))
            
            # Call the LLM
            self.console.print(f"🤖 Calling {client.get_model_name()}...")
            
            response = client.call_model(
                full_prompt,
                temperature=args.temperature,
                max_tokens=args.max_tokens
            )
            
            # Handle the response based on flags
            if args.execute:
                self._execute_response(response)
            elif args.inject:
                self._inject_response(response)
            elif args.raw:
                print(response)
            else:
                self._display_formatted_response(response, client.get_model_name())
                
        except Exception as e:
            self.console.print(f"❌ Error: {e}", style="red")
    
    def _execute_response(self, response: str) -> None:
        """Execute the LLM response as code."""
        try:
            # Extract code blocks if the response contains markdown
            code_to_execute = self._extract_code_blocks(response)
            
            if not code_to_execute:
                code_to_execute = response
            
            self.console.print("🔄 Executing LLM response...")
            result = self.bridge.run_code(code_to_execute)
            
            if result and hasattr(result, 'error_before_exec') and result.error_before_exec:
                self.console.print(f"❌ Execution error: {result.error_before_exec}", style="red")
            elif result and hasattr(result, 'error_in_exec') and result.error_in_exec:
                self.console.print(f"❌ Runtime error: {result.error_in_exec}", style="red")
            else:
                self.console.print("✅ Code executed successfully", style="green")
                
        except Exception as e:
            self.console.print(f"❌ Execution error: {e}", style="red")
    
    def _inject_response(self, response: str) -> None:
        """Inject the LLM response into a new cell."""
        try:
            # Extract code blocks if the response contains markdown
            code_to_inject = self._extract_code_blocks(response)
            
            if not code_to_inject:
                code_to_inject = response
            
            self.bridge.inject_new_cell(code_to_inject)
            self.console.print("✅ Response injected into new cell", style="green")
            
        except Exception as e:
            self.console.print(f"❌ Injection error: {e}", style="red")
            # Fallback: display the response
            self._display_formatted_response(response, "LLM Response")
    
    def _display_formatted_response(self, response: str, model_name: str) -> None:
        """Display the LLM response with rich formatting."""
        try:
            # Try to detect if the response contains code
            if self._contains_code_blocks(response):
                # Display as syntax-highlighted markdown
                syntax = Syntax(response, "markdown", theme="github-dark", line_numbers=False)
                self.console.print(Panel(
                    syntax,
                    title=f"Response from {model_name}",
                    border_style="green"
                ))
            else:
                # Display as plain text
                self.console.print(Panel(
                    response,
                    title=f"Response from {model_name}",
                    border_style="green"
                ))
                
        except Exception:
            # Fallback to simple display
            print(f"\n--- Response from {model_name} ---")
            print(response)
            print("--- End Response ---\n")
    
    def _extract_code_blocks(self, text: str) -> str:
        """Extract code blocks from markdown-formatted text."""
        import re
        
        # Find code blocks (```language\ncode\n```)
        code_pattern = r'```(?:\w+)?\n(.*?)\n```'
        matches = re.findall(code_pattern, text, re.DOTALL)
        
        if matches:
            return '\n\n'.join(matches)
        
        # If no code blocks found, look for inline code
        inline_pattern = r'`([^`]+)`'
        inline_matches = re.findall(inline_pattern, text)
        
        if inline_matches and len(inline_matches) == 1:
            return inline_matches[0]
        
        return ""
    
    def _contains_code_blocks(self, text: str) -> bool:
        """Check if text contains code blocks."""
        return '```' in text or text.count('`') >= 2
    
    @cell_magic
    def llm_config(self, line: str, cell: str):
        """
        %%llm_config magic for setting configuration.
        
        Usage:
        %%llm_config
        debug: true
        default_provider: claude
        """
        try:
            import yaml
            config_data = yaml.safe_load(cell)
            
            for key, value in config_data.items():
                self.config.set(key, value)
            
            self.console.print("✅ Configuration updated", style="green")
            self.console.print("Current config:", style="blue")
            for key, value in config_data.items():
                self.console.print(f"  {key}: {value}")
                
        except Exception as e:
            self.console.print(f"❌ Configuration error: {e}", style="red")


def load_ipython_extension(ipython):
    """Load the LLM magic extension."""
    ipython.register_magics(LLMMagic)