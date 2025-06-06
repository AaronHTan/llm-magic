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

## Repository

🔗 **GitHub**: https://github.com/AaronHTan/llm-magic

This project implements a comprehensive solution following the blueprint from your implementation requirements. The repository contains all source code, documentation, examples, and tests for the LLM Magic Jupyter extension.

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request