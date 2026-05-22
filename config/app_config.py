import os


class AppConfig:
    """Application configuration for AccessOps MCP Server."""

    MCP_SERVER_URL = os.getenv(
        "MCP_SERVER_URL",
        "http://127.0.0.1:8000/mcp"
    )