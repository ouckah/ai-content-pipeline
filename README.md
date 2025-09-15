# AI Content Pipeline Agent

A flexible and extensible AI agent framework designed for content creation and pipeline management. This boilerplate provides a solid foundation for building AI agents with tool integration, conversation management, and modular architecture.

## Features

- **Modular Tool System**: Easy-to-extend tool framework with built-in file system and web search capabilities
- **Conversation Management**: Persistent conversation history with context management
- **Async Architecture**: Built with Python asyncio for efficient concurrent operations
- **Extensible Design**: Abstract base classes for easy customization and extension
- **Logging & Error Handling**: Comprehensive logging and robust error handling
- **JSON Schema Support**: Structured tool parameter validation
- **Interactive Mode**: Built-in interactive chat interface

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-content-pipeline
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (optional):
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Basic Usage

```python
import asyncio
from agent import AIAgent

async def main():
    # Create an agent instance
    agent = AIAgent(
        name="My Content Agent",
        system_prompt="You are a helpful content creation assistant."
    )
    
    # Process a single message
    response = await agent.process_message("Help me organize my files")
    print(response)
    
    # Run in interactive mode
    await agent.run_interactive()

if __name__ == "__main__":
    asyncio.run(main())
```

## Architecture

### Core Components

#### 1. AIAgent
The main orchestrator class that manages tools, conversation, and AI model integration.

```python
agent = AIAgent(
    name="Content Pipeline Agent",
    model_name="gpt-4",
    api_key="your-key",
    system_prompt="Custom system prompt"
)
```

#### 2. Tool System
Extensible tool framework with abstract base class:

```python
class CustomTool(Tool):
    def __init__(self):
        super().__init__(
            name="custom_tool",
            description="Description of what this tool does"
        )
    
    async def execute(self, parameters: Dict[str, Any]) -> ToolResult:
        # Tool implementation
        return ToolResult(call_id="", success=True, result="result")
    
    def get_schema(self) -> Dict[str, Any]:
        # Return JSON schema for parameters
        return {...}

# Register with agent
agent.register_tool(CustomTool())
```

#### 3. Conversation Management
Handles message history and context:

```python
# Save conversation
agent.save_conversation("conversation.json")

# Load conversation
agent.load_conversation("conversation.json")

# Clear history
agent.conversation.clear_history()
```

### Built-in Tools

#### FileSystemTool
Handles file and directory operations:
- `read`: Read file contents
- `write`: Write content to files
- `list`: List directory contents

#### WebSearchTool
Placeholder for web search functionality (integrate with your preferred search API).

## Customization

### Adding Custom Tools

1. Create a new tool class inheriting from `Tool`:

```python
class DatabaseTool(Tool):
    def __init__(self, connection_string: str):
        super().__init__(
            name="database",
            description="Execute database queries"
        )
        self.connection_string = connection_string
    
    async def execute(self, parameters: Dict[str, Any]) -> ToolResult:
        query = parameters.get("query")
        # Execute database query
        return ToolResult(call_id="", success=True, result=results)
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "SQL query to execute"
                }
            },
            "required": ["query"]
        }
```

2. Register the tool with your agent:

```python
agent.register_tool(DatabaseTool("sqlite:///database.db"))
```

### Integrating AI Models

The `_generate_response` method in `AIAgent` is where you integrate with your chosen AI model:

```python
async def _generate_response(self, user_input: str) -> str:
    # Example OpenAI integration
    import openai
    
    messages = [
        {"role": "system", "content": self.system_prompt}
    ] + self.conversation.get_context()
    
    response = await openai.ChatCompletion.acreate(
        model=self.model_name,
        messages=messages,
        tools=self.get_available_tools()
    )
    
    return response.choices[0].message.content
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: OpenAI API key for GPT models
- `ANTHROPIC_API_KEY`: Anthropic API key for Claude models

### Agent Configuration

```python
agent = AIAgent(
    name="Custom Agent Name",
    model_name="gpt-4",  # or "claude-3", etc.
    system_prompt="Custom system prompt",
    api_key="your-api-key"  # or use environment variable
)

# Adjust conversation history limit
agent.conversation.max_history = 50
```

## Examples

### Content Creation Pipeline

```python
async def content_pipeline_example():
    agent = AIAgent(
        name="Content Creator",
        system_prompt="""You are a content creation specialist. 
        Help users create, edit, and organize content efficiently."""
    )
    
    # Process content creation request
    response = await agent.process_message(
        "Create a blog post about AI agents and save it to blog_post.md"
    )
    print(response)

asyncio.run(content_pipeline_example())
```

### File Management Assistant

```python
async def file_manager_example():
    agent = AIAgent(
        name="File Manager",
        system_prompt="You are a file management assistant."
    )
    
    # Interactive file management
    await agent.run_interactive()

asyncio.run(file_manager_example())
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black agent.py
flake8 agent.py
```

### Adding New Features

1. Create feature branch
2. Implement changes with tests
3. Update documentation
4. Submit pull request

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Update documentation
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Roadmap

- [ ] Integration with popular AI model APIs (OpenAI, Anthropic, etc.)
- [ ] Web interface for agent interaction
- [ ] Plugin system for third-party tools
- [ ] Advanced conversation management features
- [ ] Multi-agent coordination capabilities
- [ ] Performance monitoring and analytics

## Support

For questions, issues, or contributions, please open an issue on GitHub or contact the maintainers.
