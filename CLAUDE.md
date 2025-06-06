# LLM Magic - Claude Instructions

This project implements a custom Jupyter magic command `%%llm` that integrates Large Language Models into notebook workflows.

## Project Overview

**Purpose**: Enable seamless LLM integration in Jupyter notebooks with context awareness and flexible output handling.

**Key Components**:
1. **LLMClientBase**: Abstract base for LLM providers
2. **OpenAIClient/ClaudeClient**: Concrete implementations for API calls
3. **IPythonBridge**: Jupyter environment interaction
4. **LLMMagic**: The main magic command implementation
5. **ConfigManager**: Configuration and settings management

## Architecture

```
%%llm cell magic
     ↓
LLMMagic.llm() method
     ↓
IPythonBridge (context gathering)
     ↓
LLMClientBase.call_model()
     ↓
Response handling (display/execute/inject)
```

## Usage Patterns

### Basic Usage
```python
%%llm
Write a function to sort a list of dictionaries by a specific key.
```

### With Execution
```python
%%llm --exec
Create a plot showing the relationship between two variables in 'data'.
```

### Context Aware
```python
# Previous cell creates 'df' DataFrame
%%llm --context 2
Analyze this dataset and suggest appropriate visualizations.
```

## Implementation Details

### Security Considerations
- API keys stored in environment variables
- Input sanitization for dangerous operations
- Code execution warnings
- Configurable logging for audit trails

### Error Handling
- Graceful API failure handling
- Invalid parameter validation
- Network timeout management
- Fallback display methods

### Performance Features
- Client instance caching
- Configurable context limits
- Response size limits
- Async-ready architecture (future enhancement)

## Configuration

Default settings in `config.py`:
- `debug`: false
- `default_provider`: openai
- `max_context_cells`: 10
- `temperature`: 0.7
- `max_tokens`: 2000

Override via:
1. `~/.llm_magic/config.yaml`
2. Environment variables
3. `%%llm_config` magic

## Testing Strategy

Test coverage includes:
- Client API mocking
- Magic command parsing
- Context extraction
- Error scenarios
- Configuration management

## Future Enhancements

Planned features:
- More LLM providers (Google, etc.)
- Streaming responses
- Token usage tracking
- Prompt templates
- Variable injection control
- Session persistence

## Development Commands

```bash
# Setup development environment
pip install -e .

# Run tests
pytest tests/

# Install in Jupyter
pip install -e . && jupyter notebook

# Load extension
%load_ext llm_magic
```

## File Dependencies

Core files that must be maintained together:
- `magic.py` ↔ `bridge.py` (IPython integration)
- `clients.py` ↔ `config.py` (API configuration)
- `__init__.py` (extension loading)

## Important Notes

1. **API Keys**: Never commit API keys; always use environment variables
2. **Context Size**: Large context can hit token limits; monitor usage
3. **Execution Safety**: Code execution has security implications
4. **Error Messages**: Provide clear, actionable error messages to users
5. **Performance**: Cache clients and avoid redundant API calls