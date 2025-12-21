FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/alexweichart/obsidian-rest-mcp"
LABEL org.opencontainers.image.description="MCP server for Obsidian Local REST API"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

# Install dependencies first for better caching
COPY pyproject.toml README.md ./
COPY src/ ./src/

RUN pip install --no-cache-dir .

ENTRYPOINT ["obsidian-rest-mcp"]
