# Obsidian REST MCP

An MCP (Model Context Protocol) server that wraps the [Obsidian Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api) plugin, enabling AI assistants to interact with your Obsidian vault.

Built with [FastMCP](https://gofastmcp.com/) - automatically generates tools from the OpenAPI specification.

## Why this server

Most MCP wrappers for REST APIs are maintained by manually re-implementing each endpoint as a bespoke tool. That approach tends to drift over time: when the underlying REST API adds/renames/changes endpoints, the MCP server needs a code update (and a new release) to catch up.

This server is different: it **dynamically generates tools directly from the Obsidian Local REST API OpenAPI spec**.

- **Stays in sync with the REST API**: when the plugin’s OpenAPI spec changes, this server’s tool surface updates automatically (no hand-updating dozens of wrappers).
- **Less breakage / less maintenance**: fewer places for the MCP implementation to get out of date compared to the plugin.
- **Full coverage**: you get the complete set of documented endpoints exposed as tools.

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

> **Note:** On macOS/Windows, containers can usually reach services on your machine via `https://host.docker.internal:27124`.
> On Linux, you may need `--network=host` (or an equivalent host gateway setup) for the container to reach the Obsidian REST API.

## Available Tools

This server exposes all endpoints from the Obsidian Local REST API.

Documentation (Swagger): https://coddingtonbear.github.io/obsidian-local-rest-api/

## License

MIT
