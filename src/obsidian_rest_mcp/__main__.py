"""Entry point for running the Obsidian REST MCP server."""

import argparse
import os
import sys


def main() -> None:
    """Main entry point for the Obsidian REST MCP server."""
    parser = argparse.ArgumentParser(
        description="MCP server for Obsidian Local REST API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment variables:
  OBSIDIAN_REST_URL      Base URL of the Obsidian REST API
  OBSIDIAN_API_KEY       API key for authentication (required)
  OBSIDIAN_OPENAPI_PATH  Path to the OpenAPI spec
  OBSIDIAN_MCP_TRANSPORT Transport to use: stdio (default), http, or sse
  OBSIDIAN_MCP_HOST      Host for http/sse transport (default: 127.0.0.1)
  OBSIDIAN_MCP_PORT      Port for http/sse transport (default: 8000)
  OBSIDIAN_MCP_PATH      Path for http/sse transport (default: /mcp/)

Examples:
  # Using command line arguments
  python -m obsidian_rest_mcp --api-key YOUR_API_KEY

  # Using environment variables
  export OBSIDIAN_API_KEY=YOUR_API_KEY
  python -m obsidian_rest_mcp

  # HTTP transport
  OBSIDIAN_MCP_TRANSPORT=http OBSIDIAN_API_KEY=YOUR_API_KEY python -m obsidian_rest_mcp
        """,
    )

    parser.add_argument(
        "--url",
        default=os.environ.get("OBSIDIAN_REST_URL", "https://127.0.0.1:27124"),
        help="Base URL of the Obsidian REST API (default: https://127.0.0.1:27124)",
    )

    parser.add_argument(
        "--api-key",
        default=os.environ.get("OBSIDIAN_API_KEY"),
        help="API key for authentication (or set OBSIDIAN_API_KEY env var)",
    )

    parser.add_argument(
        "--openapi-path",
        default=os.environ.get("OBSIDIAN_OPENAPI_PATH", "/openapi.yaml"),
        help="Path to the OpenAPI spec (default: /openapi.yaml)",
    )

    parser.add_argument(
        "--transport",
        default=os.environ.get("OBSIDIAN_MCP_TRANSPORT", "stdio"),
        choices=["stdio", "http", "sse"],
        help="Transport to use (default: stdio)",
    )

    parser.add_argument(
        "--host",
        default=os.environ.get("OBSIDIAN_MCP_HOST", "127.0.0.1"),
        help="Host for http/sse transport (default: 127.0.0.1)",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("OBSIDIAN_MCP_PORT", "8000")),
        help="Port for http/sse transport (default: 8000)",
    )

    parser.add_argument(
        "--path",
        default=os.environ.get("OBSIDIAN_MCP_PATH", "/mcp/"),
        help="Path for http/sse transport (default: /mcp/)",
    )

    args = parser.parse_args()

    if not args.api_key:
        print("Error: API key is required.", file=sys.stderr)
        print(
            "Set it via --api-key or OBSIDIAN_API_KEY environment variable.",
            file=sys.stderr,
        )
        print(
            "Get the API key from Obsidian Settings > Local REST API.", file=sys.stderr
        )
        sys.exit(1)

    # Import here to avoid import errors if dependencies are missing
    from .server import create_server

    try:
        mcp = create_server(
            base_url=args.url,
            openapi_path=args.openapi_path,
            api_key=args.api_key,
        )
        if args.transport == "stdio":
            mcp.run(transport="stdio")
        else:
            mcp.run(transport=args.transport, host=args.host, port=args.port, path=args.path)
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
