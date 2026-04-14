"""Obsidian Local REST API MCP Server using FastMCP."""

import json
import ssl
from typing import Any

import httpx
import yaml
from fastmcp import FastMCP
from fastmcp.server.openapi import (
    OpenAPITool,
    OpenAPIResource,
    OpenAPIResourceTemplate,
)
from fastmcp.utilities.openapi import HTTPRoute


async def set_content_type(request: httpx.Request) -> None:
    """Set Content-Type for POST/PATCH requests if not already set.

    Detects JSON bodies and sets application/json; falls back to text/markdown.
    """
    if request.method in ("POST", "PATCH") and "content-type" not in request.headers:
        body = request.content
        if body:
            try:
                json.loads(body)
                request.headers["content-type"] = "application/json"
            except (json.JSONDecodeError, ValueError):
                request.headers["content-type"] = "text/markdown"


def create_ssl_context() -> ssl.SSLContext:
    """Create an SSL context that doesn't verify certificates.

    The Obsidian Local REST API uses a self-signed certificate,
    so we need to disable certificate verification.
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def fetch_openapi_spec(
    base_url: str, openapi_path: str, api_key: str
) -> dict[str, Any]:
    """Fetch the OpenAPI specification from the Obsidian Local REST API.

    Args:
        base_url: The base URL of the Obsidian REST API (e.g., https://127.0.0.1:27124)
        openapi_path: Path to the OpenAPI spec (e.g., /openapi.yaml)
        api_key: The API key for authentication

    Returns:
        The parsed OpenAPI specification as a dictionary
    """
    url = f"{base_url.rstrip('/')}/{openapi_path.lstrip('/')}"

    with httpx.Client(
        verify=create_ssl_context(),
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=30.0,
    ) as client:
        response = client.get(url)
        response.raise_for_status()
        return yaml.safe_load(response.text)


def create_server(
    base_url: str = "https://127.0.0.1:27124",
    openapi_path: str = "/openapi.yaml",
    api_key: str | None = None,
) -> FastMCP:
    """Create a FastMCP server from the Obsidian Local REST API OpenAPI spec.

    Args:
        base_url: The base URL of the Obsidian REST API
        openapi_path: Path to the OpenAPI spec relative to base_url
        api_key: The API key for authentication (required)

    Returns:
        A FastMCP server instance with tools generated from the OpenAPI spec

    Raises:
        ValueError: If api_key is not provided
        httpx.HTTPError: If the OpenAPI spec cannot be fetched
    """
    if not api_key:
        raise ValueError(
            "API key is required. Get it from Obsidian Settings > Local REST API."
        )

    # Fetch the OpenAPI specification
    openapi_spec = fetch_openapi_spec(base_url, openapi_path, api_key)

    # Create an HTTP client with authentication for making API requests
    api_client = httpx.AsyncClient(
        base_url=base_url,
        headers={"Authorization": f"Bearer {api_key}"},
        verify=create_ssl_context(),
        timeout=30.0,
        event_hooks={"request": [set_content_type]},
    )

    def disable_output_schema(
        route: HTTPRoute,
        component: OpenAPITool | OpenAPIResource | OpenAPIResourceTemplate,
    ) -> None:
        """Disable output schema for tools.

        The Obsidian REST API returns various content types (text/markdown,
        application/json, etc.). When an outputSchema is defined but the
        response is plain text, FastMCP raises an error. Disabling output
        schemas allows all response types to work correctly.
        """
        if isinstance(component, OpenAPITool):
            component.output_schema = None

    # Create the MCP server from the OpenAPI spec
    mcp = FastMCP.from_openapi(
        openapi_spec=openapi_spec,
        client=api_client,
        name="Obsidian REST API",
        mcp_component_fn=disable_output_schema,
    )

    return mcp
