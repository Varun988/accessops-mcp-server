from mcp.server.fastmcp import FastMCP

from tools.access_request_tool import (
    get_access_request_status,
    get_pending_approvers,
    diagnose_access_request,
)

from services.resource_service import ResourceService
from services.prompt_service import PromptService

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

@mcp.resource("policy://access/approval-rules")
def access_approval_rules() -> str:
    """
    Access approval policy rules.

    Provides enterprise approval rules for access requests, including
    manager approval, security approval, compliance approval, escalation,
    and least-privilege guidance.
    """
    return ResourceService.get_resource("policy://access/approval-rules")


@mcp.resource("runbook://identity/provisioning-failure")
def provisioning_failure_runbook() -> str:
    """
    Identity provisioning failure runbook.

    Provides troubleshooting steps for access requests that are approved
    but fail during provisioning.
    """
    return ResourceService.get_resource("runbook://identity/provisioning-failure")


@mcp.resource("schema://access-request/status-codes")
def access_request_status_codes() -> str:
    """
    Access request status code reference.

    Explains meanings of access request statuses such as Pending,
    In Progress, Failed, Completed, and Rejected.
    """
    return ResourceService.get_resource("schema://access-request/status-codes")

@mcp.prompt()
def troubleshoot_access_request(request_id: str) -> str:
    """
    Generate a structured troubleshooting workflow for an access request.

    Use this prompt when the user asks why an access request is stuck,
    delayed, pending, in progress, or failed.
    """
    return PromptService.troubleshoot_access_request(request_id)


@mcp.prompt()
def generate_requester_response(request_id: str) -> str:
    """
    Generate a requester-facing response for an access request.

    Use this prompt when the user wants to draft a professional update
    for the person who submitted the access request.
    """
    return PromptService.generate_requester_response(request_id)


@mcp.prompt()
def prepare_support_summary(request_id: str) -> str:
    """
    Generate a support engineer summary for an access request.

    Use this prompt when the user wants an operations-focused summary
    for troubleshooting, escalation, or handover.
    """
    return PromptService.prepare_support_summary(request_id)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
