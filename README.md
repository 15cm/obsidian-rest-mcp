# Obsidian REST MCP

An MCP (Model Context Protocol) server that wraps the [Obsidian Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api) plugin, enabling AI assistants to interact with your Obsidian vault.

Built with [FastMCP](https://gofastmcp.com/) - automatically generates tools from the OpenAPI specification.

## Prerequisites

1. [Obsidian](https://obsidian.md/) with the [Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api) plugin installed and enabled
2. Python 3.10+

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/obsidian-rest-mcp.git
cd obsidian-rest-mcp

# Install dependencies
pip install -e .
```

## Configuration

Get your API key from **Obsidian Settings → Local REST API**.

### Environment Variables

| Variable                | Description                                 | Default                   |
| ----------------------- | ------------------------------------------- | ------------------------- |
| `OBSIDIAN_API_KEY`      | API key from Obsidian Local REST API plugin | (required)                |
| `OBSIDIAN_REST_URL`     | Base URL of the REST API                    | `https://127.0.0.1:27124` |
| `OBSIDIAN_OPENAPI_PATH` | Path to OpenAPI spec                        | `/openapi.yaml`           |

## Usage

### VS Code (MCP)

This repo includes a ready-to-use VS Code workspace MCP configuration example: [mcp.json](mcp.json).

### As a CLI

```bash
# Using environment variables
export OBSIDIAN_API_KEY=your_api_key_here
python -m obsidian_rest_mcp

# Or with command line arguments
python -m obsidian_rest_mcp --api-key your_api_key_here
```

### With Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
	"mcpServers": {
		"obsidian": {
			"command": "python",
			"args": ["-m", "obsidian_rest_mcp"],
			"env": {
				"OBSIDIAN_API_KEY": "your_api_key_here"
			}
		}
	}
}
```

### Programmatic Usage

```python
from obsidian_rest_mcp import create_server

mcp = create_server(
    base_url="https://127.0.0.1:27124",
    api_key="your_api_key_here",
)
mcp.run()
```

## Available Tools

The server automatically exposes all endpoints from the Obsidian Local REST API:

- **Active File**: Read, update, append, or delete the currently active file
- **Vault Files**: CRUD operations on any file in your vault
- **Vault Directories**: List directory contents
- **Commands**: List and execute Obsidian commands
- **Search**: Full-text and simple search across your vault
- **Periodic Notes**: Access daily/weekly/monthly notes
- **Open**: Open files in Obsidian's UI

## Development

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install in development mode
pip install -e ".[dev]"
```

## License

MIT
