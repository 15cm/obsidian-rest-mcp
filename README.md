# Obsidian REST MCP

An MCP (Model Context Protocol) server that wraps the [Obsidian Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api) plugin, enabling AI assistants to interact with your Obsidian vault.

Built with [FastMCP](https://gofastmcp.com/) - automatically generates tools from the OpenAPI specification.

## Prerequisites

1. [Obsidian](https://obsidian.md/) with the [Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api) plugin installed and enabled
2. Docker

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

Add to your VS Code MCP settings (`.vscode/mcp.json`):

```json
{
	"servers": {
		"obsidian": {
			"type": "stdio",
			"command": "docker",
			"args": [
				"run",
				"-i",
				"--rm",
				"--network=host",
				"-e",
				"OBSIDIAN_API_KEY",
				"ghcr.io/alexweichart/obsidian-rest-mcp:latest"
			],
			"env": {
				"OBSIDIAN_API_KEY": "${input:obsidian-api-key}"
			}
		}
	},
	"inputs": [
		{
			"id": "obsidian-api-key",
			"type": "promptString",
			"description": "Obsidian Local REST API Key",
			"password": true
		}
	]
}
```

> **Note:** `--network=host` is required so the container can access the Obsidian REST API running on localhost.

### With Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
	"mcpServers": {
		"obsidian": {
			"command": "docker",
			"args": [
				"run",
				"-i",
				"--rm",
				"--network=host",
				"-e",
				"OBSIDIAN_API_KEY=your_api_key_here",
				"ghcr.io/alexweichart/obsidian-rest-mcp:latest"
			]
		}
	}
}
```

### Docker CLI

```bash
docker run -i --rm \
  --network=host \
  -e OBSIDIAN_API_KEY=your_api_key_here \
  ghcr.io/alexweichart/obsidian-rest-mcp:latest
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
# Clone the repository
git clone https://github.com/alexweichart/obsidian-rest-mcp.git
cd obsidian-rest-mcp

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install in development mode
pip install -e ".[dev]"

# Run locally
export OBSIDIAN_API_KEY=your_api_key_here
python -m obsidian_rest_mcp
```

### Building the Docker Image Locally

```bash
docker build -t obsidian-rest-mcp .
```

## License

MIT
