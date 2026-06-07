from mcp.server.fastmcp import FastMCP
from config.version import APP_NAME, APP_VERSION
from tools.access_request_tool import (
    get_access_request_status,
    get_pending_approvers,
    diagnose_access_request,
)

from tools.retry_tool import (
    prepare_provisioning_retry as prepare_retry_tool,
    submit_provisioning_retry_after_confirmation as submit_retry_tool,
)

from tools.ticket_tool import (
    prepare_ticket_creation as prepare_ticket_creation_tool,
    submit_ticket_creation_after_confirmation as submit_ticket_creation_tool,
    prepare_ticket_closure as prepare_ticket_closure_tool,
    submit_ticket_closure_after_confirmation as submit_ticket_closure_tool,
)

from tools.notification_tool import (
    prepare_notification as prepare_notification_tool,
    send_notification_after_confirmation as send_notification_tool,
)

from services.resource_service import ResourceService
from services.prompt_service import PromptService

mcp = FastMCP(f"{APP_NAME} v{APP_VERSION}")

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

@mcp.tool()
def prepare_provisioning_retry(request_id: str) -> dict:
    """
    Prepare a provisioning retry draft for a failed access request.

    Use this tool when the user asks whether provisioning can be retried
    for a failed access request. This tool does not execute the retry.
    It creates a retry draft and requires human confirmation before submission.
    """
    return prepare_retry_tool(request_id)
   
@mcp.tool()
def submit_provisioning_retry_after_confirmation(
    retry_id: str,
    approved_by: str,
) -> dict:
    """
    Submit a provisioning retry after explicit human confirmation.

    Use this tool only after a retry draft has been prepared and the user/operator
    has explicitly approved the retry action.
    """
    return submit_retry_tool(
        retry_id=retry_id,
        approved_by=approved_by,
    )

@mcp.tool()
def prepare_ticket_creation(
    request_id: str,
    title: str | None = None,
    priority: str | None = None,
) -> dict:
    """
    Prepare a ticket creation draft for an access request.

    Use this tool when the user wants to create a support or incident ticket
    for an access request. This tool does not create the ticket immediately.
    It creates a draft and requires human confirmation before submission.
    """
    return prepare_ticket_creation_tool(
        request_id=request_id,
        title=title,
        priority=priority,
    )


@mcp.tool()
def submit_ticket_creation_after_confirmation(
    ticket_draft_id: str,
    approved_by: str,
) -> dict:
    """
    Create a ticket from a prepared ticket draft after explicit human confirmation.

    Use this tool only after a ticket draft has been prepared and the
    user/operator has explicitly approved ticket creation.
    """
    return submit_ticket_creation_tool(
        ticket_draft_id=ticket_draft_id,
        approved_by=approved_by,
    )


@mcp.tool()
def prepare_notification(
    request_id: str,
    recipient: str | None = None,
    channel: str | None = None,
    subject: str | None = None,
    message: str | None = None,
) -> dict:
    """
    Prepare a notification draft for an access request.

    Use this tool when the user wants to notify a requester, approver,
    or operations team. This tool does not send the notification immediately.
    It creates a draft and requires human confirmation before sending.
    """
    return prepare_notification_tool(
        request_id=request_id,
        recipient=recipient,
        channel=channel,
        subject=subject,
        message=message,
    )


@mcp.tool()
def send_notification_after_confirmation(
    notification_draft_id: str,
    approved_by: str,
) -> dict:
    """
    Send a prepared notification after explicit human confirmation.

    Use this tool only after a notification draft has been prepared and
    the user/operator has explicitly approved sending the notification.
    """
    return send_notification_tool(
        notification_draft_id=notification_draft_id,
        approved_by=approved_by,
    )


@mcp.tool()
def prepare_ticket_closure(
    ticket_id: str,
    closure_reason: str | None = None,
    resolution_summary: str | None = None,
) -> dict:
    """
    Prepare a ticket closure draft.

    Use this tool when the user wants to close an existing ticket.
    This tool does not close the ticket immediately. It creates a closure
    draft and requires human confirmation before closure.
    """
    return prepare_ticket_closure_tool(
        ticket_id=ticket_id,
        closure_reason=closure_reason,
        resolution_summary=resolution_summary,
    )


@mcp.tool()
def submit_ticket_closure_after_confirmation(
    closure_draft_id: str,
    approved_by: str,
) -> dict:
    """
    Close a ticket from a prepared closure draft after explicit human confirmation.

    Use this tool only after a closure draft has been prepared and the
    user/operator has explicitly approved ticket closure.
    """
    return submit_ticket_closure_tool(
        closure_draft_id=closure_draft_id,
        approved_by=approved_by,
    )

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
