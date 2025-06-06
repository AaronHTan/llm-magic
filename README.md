# LLM Magic 🪄

A custom Jupyter magic command that seamlessly integrates Large Language Models (LLMs) into your notebook workflow. Send cell content to OpenAI, Claude, or other LLM providers with context from your notebook environment.

## Features

- **Easy Integration**: Simple `%%llm` magic command in Jupyter notebooks
- **Multiple Providers**: Support for OpenAI GPT models and Anthropic Claude
- **Context Awareness**: Automatically includes previous cells and variables as context
- **Flexible Output**: Display, execute, or inject LLM responses into new cells
- **Rich Formatting**: Beautiful syntax highlighting and formatted output
- **Configuration**: Customizable settings and logging
- **Security**: Input sanitization and validation

## Installation

```bash
# Clone the repository
git clone https://github.com/AaronHTan/llm-magic.git
cd llm-magic

# Install the package
pip install -e .

# Or install from requirements
pip install -r requirements.txt
```

## Quick Start

### 1. Set up API Keys

Create a `.env` file or set environment variables:

```bash
export OPENAI_API_KEY="your_openai_api_key"
export ANTHROPIC_API_KEY="your_anthropic_api_key"
```

### 2. Load the Extension

In your Jupyter notebook:

```python
%load_ext llm_magic
```

### 3. Start Using

```python
%%llm
Explain what machine learning is and give me a simple example in Python.
```

## Usage Examples

### Basic Usage

```python
%%llm
Write a function to calculate the factorial of a number.
```

### Execute Code Automatically

```python
%%llm --exec
Create a simple plot showing a sine wave using matplotlib.
```

### Inject into New Cell

```python
%%llm --inject
Write a class for a simple calculator with basic operations.
```

### Use Different Providers

```python
%%llm --provider claude
Explain the differences between Python lists and tuples.
```

```python
%%llm --provider openai --model gpt-3.5-turbo
Generate test cases for a sorting function.
```

### Include Context

```python
# Cell 1: Create some data
data = [1, 2, 3, 4, 5]

# Cell 2: Ask LLM to analyze it
%%llm --context 1
Analyze this data and suggest what kind of analysis would be appropriate.
```

### Configuration

```python
%%llm_config
debug: true
default_provider: claude
temperature: 0.3
max_tokens: 1500
```

## Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--provider` | `-p` | LLM provider (`openai`, `claude`) |
| `--model` | `-m` | Specific model to use |
| `--context` | `-c` | Number of previous cells to include (default: 3) |
| `--exec` | | Execute the returned code automatically |
| `--inject` | | Inject response into a new cell |
| `--no-variables` | | Exclude variable context from prompt |
| `--temperature` | `-t` | Temperature for response generation (0.0-2.0) |
| `--max-tokens` | | Maximum tokens in response |
| `--raw` | | Return raw response without formatting |

## Configuration

### Global Configuration

Create `~/.llm_magic/config.yaml`:

```yaml
debug: false
default_provider: openai
default_openai_model: gpt-4
default_claude_model: claude-3-sonnet-20240229
max_context_cells: 10
max_tokens: 2000
temperature: 0.7
log_requests: false
```

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `LLM_MAGIC_DEBUG`: Enable debug mode
- `LLM_MAGIC_DEFAULT_PROVIDER`: Default LLM provider
- `LLM_MAGIC_LOG_REQUESTS`: Enable request logging

## Advanced Features

### Context Management

The magic automatically includes:
- Previous notebook cells (configurable number)
- Current variable values and types
- Execution history

### Security Features

- API key validation
- Input sanitization
- Code execution warnings for dangerous operations
- Configurable logging and audit trails

### Logging

All LLM requests can be logged for analysis:

```python
%%llm_config
log_requests: true
log_file: /path/to/logfile.json
```

## Development

### Project Structure

```
llm_magic/
├── src/llm_magic/
│   ├── __init__.py       # Main package
│   ├── magic.py          # IPython magic implementation
│   ├── clients.py        # LLM client implementations
│   ├── bridge.py         # IPython/Jupyter integration
│   ├── config.py         # Configuration management
│   └── logging.py        # Logging and security
├── examples/
│   └── demo_notebook.ipynb
├── tests/
├── requirements.txt
└── setup.py
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# Run with coverage
pytest --cov=llm_magic tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Examples

Check out the `examples/demo_notebook.ipynb` for comprehensive usage examples.

## Troubleshooting

### Common Issues

1. **API Key Not Found**
   - Ensure environment variables are set correctly
   - Check `.env` file location and format

2. **Module Not Found**
   - Verify installation: `pip list | grep llm-magic`
   - Try reinstalling: `pip install -e .`

3. **JavaScript Injection Not Working**
   - Ensure you're running in a Jupyter notebook (not JupyterLab console)
   - Check browser console for errors

### Debug Mode

Enable debug mode to see detailed information:

```python
%%llm_config
debug: true
```

This will show:
- Full prompts sent to LLMs
- API response details
- Context information

## Repository

🔗 **GitHub**: https://github.com/AaronHTan/llm-magic

This project implements a comprehensive solution following the blueprint from your implementation requirements. The repository contains all source code, documentation, examples, and tests for the LLM Magic Jupyter extension.

## License

MIT License - see LICENSE file for details.

## Changelog

### v0.1.0
- Initial release
- Support for OpenAI and Claude
- Basic magic command functionality
- Context awareness
- Configuration system
