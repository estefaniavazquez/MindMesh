# MindMesh 🧠

A standalone Python application with beautiful UI and LLM integration for personalized learning experiences.

## Features

- 🎨 **Beautiful UI Options**: Tkinter GUI, CLI, and extensible UI framework
- 🤖 **LLM Integration**: Support for OpenAI, Anthropic, and custom LLM providers
- 🎯 **Personalized Learning**: Adapts to user's learning style and preferences
- ⚙️ **Configurable**: Extensive configuration options and user preferences
- 🔧 **Extensible**: Plugin-friendly architecture for custom components
- 🌐 **Cross-platform**: Works on Windows, macOS, and Linux

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/estefaniavazquez/MindMesh.git
cd MindMesh

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### Basic Usage

```bash
# Start with GUI interface
python -m mindmesh.main

# Start with CLI interface
python -m mindmesh.main --ui cli

# Show help
python -m mindmesh.main --help
```

### Configuration

Create a `.env` file for API keys:
```bash
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

## Learning Styles

MindMesh adapts to different learning preferences:

- **Visual**: Uses descriptions, diagrams, and visual examples
- **Auditory**: Focuses on explanations that work well when spoken
- **Kinesthetic**: Includes hands-on activities and practical examples
- **Reading/Writing**: Provides detailed written explanations and notes
- **Multimodal**: Combines multiple learning approaches

## Architecture

```
mindmesh/
├── config.py          # Configuration management
├── app.py             # Main application class
├── main.py            # Entry point
├── llm/               # LLM integration
│   ├── base.py        # Abstract LLM provider
│   ├── openai_provider.py
│   ├── anthropic_provider.py
│   └── factory.py     # LLM provider factory
└── ui/                # User interfaces
    ├── base.py        # Abstract UI interface
    ├── tkinter_ui.py  # GUI implementation
    ├── cli_ui.py      # CLI implementation
    └── factory.py     # UI factory
```

## Examples

See `examples.py` for comprehensive usage examples:

```python
from mindmesh import MindMeshApp, Config
from mindmesh.config import LearningStyle

# Create custom configuration
config = Config()
config.user_preferences.learning_style = LearningStyle.VISUAL
config.user_preferences.difficulty_level = "advanced"

# Create and run app
app = MindMeshApp(config=config, ui_type="tkinter")
app.run()
```

## Extending MindMesh

### Custom LLM Provider

```python
from mindmesh.llm.base import BaseLLMProvider
from mindmesh.llm.factory import LLMFactory

class MyCustomProvider(BaseLLMProvider):
    async def generate_response(self, messages, learning_context=None):
        # Your custom implementation
        return "Custom response"
    
    def test_connection(self):
        return True

# Register your provider
LLMFactory.register_provider("mycustom", MyCustomProvider)
```

### Custom UI

```python
from mindmesh.ui.base import BaseUI
from mindmesh.ui.factory import UIFactory

class MyCustomUI(BaseUI):
    def initialize(self):
        # Initialize your UI
        pass
    
    def run(self):
        # Run your UI main loop
        return 0

# Register your UI
UIFactory.register_ui_type("myui", MyCustomUI)
```

## Configuration Options

MindMesh offers extensive configuration through `config.json`:

```json
{
  "debug": false,
  "log_level": "INFO",
  "llm": {
    "provider": "openai",
    "model": "gpt-3.5-turbo",
    "max_tokens": 1000,
    "temperature": 0.7
  },
  "user_preferences": {
    "learning_style": "multimodal",
    "difficulty_level": "intermediate",
    "session_duration": 30,
    "ui_theme": "system",
    "font_size": 12
  }
}
```

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements.txt

# Install in editable mode
pip install -e .

# Run examples
python examples.py

# Run with different configurations
python -m mindmesh.main --debug --ui cli
```

### Testing

```bash
# Run tests (when available)
pytest

# Run type checking
mypy src/mindmesh

# Run linting
black src/mindmesh
flake8 src/mindmesh
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

- 📧 Email: [maintainer email]
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions