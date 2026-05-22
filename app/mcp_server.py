from mcp.server.fastmcp import FastMCP

from tools.access_request_tool import (
    get_access_request_status,
    get_pending_approvers,
    diagnose_access_request,
)


mcp = FastMCP("AccessOps MCP Server")


@mcp.tool()
def access_request_status(request_id: str) -> dict:
    """
    Get status and details of an access request using request ID.

    Use this tool when the user asks for the current status, requester,
    target system, role, current stage, or last update of an access request.
    """
    return get_access_request_status(request_id)


@mcp.tool()
def pending_approvers(request_id: str) -> dict:
    """
    Get list of users or teams who need to approve the access request.

    Use this tool when the user asks who is currently responsible for approving
    or moving the access request forward.
    """
    return get_pending_approvers(request_id)


@mcp.tool()
def diagnose_request(request_id: str) -> dict:
    """
    Explain why an access request is pending, in progress, or failed.

    Use this tool when the user asks why an access request is stuck, delayed,
    pending, in progress, or failed.
    """
    return diagnose_access_request(request_id)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")