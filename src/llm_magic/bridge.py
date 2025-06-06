"""
IPython bridge for interacting with Jupyter notebook environment.
"""

import json
from typing import List, Dict, Any, Optional
from IPython.display import display, HTML, Javascript
from IPython.core.interactiveshell import InteractiveShell


class IPythonBridge:
    """Bridge for interacting with IPython/Jupyter environment."""
    
    def __init__(self, shell: Optional[InteractiveShell] = None):
        self.shell = shell or InteractiveShell.instance()
    
    def get_previous_cells(self, count: int = 3) -> List[str]:
        """Get the content of the last N input cells."""
        try:
            # Get input history from IPython
            in_history = self.shell.user_ns.get("In", [])
            if len(in_history) <= 1:  # Only the current cell exists
                return []
            
            # Return last 'count' cells, excluding the current one
            start_idx = max(1, len(in_history) - count - 1)
            return in_history[start_idx:-1]  # Exclude current cell
        except Exception:
            return []
    
    def get_previous_outputs(self, count: int = 3) -> List[Any]:
        """Get the output of the last N executed cells."""
        try:
            out_history = self.shell.user_ns.get("Out", {})
            if not out_history:
                return []
            
            # Get the last 'count' outputs
            out_keys = sorted(out_history.keys())[-count:]
            return [out_history[key] for key in out_keys]
        except Exception:
            return []
    
    def get_globals(self) -> Dict[str, Any]:
        """Get current global variables from the notebook."""
        try:
            # Filter out IPython internals and large objects
            filtered_globals = {}
            for key, value in self.shell.user_ns.items():
                if (not key.startswith('_') and 
                    not callable(value) and 
                    not hasattr(value, '__module__')):
                    try:
                        # Try to serialize to check if it's a simple type
                        json.dumps(value, default=str)
                        filtered_globals[key] = value
                    except (TypeError, ValueError):
                        # For complex objects, just store their type and string representation
                        filtered_globals[key] = f"{type(value).__name__}: {str(value)[:100]}..."
            
            return filtered_globals
        except Exception:
            return {}
    
    def get_variable_summary(self, max_vars: int = 10) -> str:
        """Get a summary of current variables for context."""
        globals_dict = self.get_globals()
        if not globals_dict:
            return "No variables defined."
        
        # Limit to most recent variables
        var_items = list(globals_dict.items())[-max_vars:]
        
        summary_lines = ["Current variables:"]
        for key, value in var_items:
            if isinstance(value, (int, float, str, bool)):
                summary_lines.append(f"  {key} = {repr(value)}")
            else:
                summary_lines.append(f"  {key} = {type(value).__name__}")
        
        return "\n".join(summary_lines)
    
    def run_code(self, code: str) -> Any:
        """Execute code in the current notebook context."""
        try:
            return self.shell.run_cell(code)
        except Exception as e:
            raise Exception(f"Error executing code: {e}")
    
    def inject_new_cell(self, content: str, cell_type: str = "code") -> None:
        """Inject a new cell below the current one."""
        # JavaScript to create a new cell
        js_code = f"""
        var cell = Jupyter.notebook.insert_cell_below('{cell_type}');
        cell.set_text({json.dumps(content)});
        cell.focus_cell();
        """
        
        try:
            display(Javascript(js_code))
        except Exception as e:
            # Fallback: just display the content
            print(f"Could not inject cell, displaying content instead:\n{content}")
    
    def display_formatted_output(self, content: str, title: str = "LLM Response") -> None:
        """Display formatted output in the notebook."""
        html_content = f"""
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin: 10px 0; background-color: #f9f9f9;">
            <h4 style="color: #333; margin-top: 0;">{title}</h4>
            <pre style="white-space: pre-wrap; font-family: 'Courier New', monospace; background-color: white; padding: 10px; border-radius: 4px;">{content}</pre>
        </div>
        """
        display(HTML(html_content))
    
    def build_context_prompt(self, user_prompt: str, context_cells: int = 3, include_variables: bool = True) -> str:
        """Build a comprehensive prompt including context from the notebook."""
        context_parts = []
        
        # Add previous cells context
        if context_cells > 0:
            prev_cells = self.get_previous_cells(context_cells)
            if prev_cells:
                context_parts.append("Previous notebook cells:")
                for i, cell in enumerate(prev_cells, 1):
                    context_parts.append(f"Cell {i}:\n{cell}")
                context_parts.append("")
        
        # Add variable context
        if include_variables:
            var_summary = self.get_variable_summary()
            if var_summary != "No variables defined.":
                context_parts.append(var_summary)
                context_parts.append("")
        
        # Add the main prompt
        context_parts.append("Current request:")
        context_parts.append(user_prompt)
        
        return "\n".join(context_parts)
    
    def get_cell_execution_count(self) -> Optional[int]:
        """Get the execution count of the current cell."""
        try:
            return self.shell.execution_count
        except Exception:
            return None