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

See the checked-in VS Code MCP configuration at `.vscode/mcp.json`.

> **Note:** `--network=host` is required so the container can access the Obsidian REST API running on localhost.

## Available Tools

This server exposes all endpoints from the Obsidian Local REST API.

Documentation (Swagger): https://coddingtonbear.github.io/obsidian-local-rest-api/

## License

MIT
