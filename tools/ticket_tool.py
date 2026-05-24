from services.ticket_service import TicketService
from utils.audit_logger import AuditLogger
from utils.error_utils import ErrorUtils


ticket_service = TicketService()


PREPARE_TICKET_CREATION_METADATA = {
    "name": "prepare_ticket_creation",
    "description": (
        "Prepare a ticket creation draft for an access request. "
        "This does not create the ticket and requires explicit human confirmation."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "request_id": {
                "type": "string",
                "description": "Access request ID, for example REQ-1003",
            },
            "title": {
                "type": "string",
                "description": "Optional ticket title",
            },
            "priority": {
                "type": "string",
                "description": "Optional priority such as High, Medium, or Low",
            },
        },
        "required": ["request_id"],
    },
}


SUBMIT_TICKET_CREATION_METADATA = {
    "name": "submit_ticket_creation_after_confirmation",
    "description": (
        "Create a ticket from a prepared ticket draft after explicit human confirmation."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "ticket_draft_id": {
                "type": "string",
                "description": "Ticket draft ID returned by prepare_ticket_creation",
            },
            "approved_by": {
                "type": "string",
                "description": "User/operator who approved ticket creation",
            },
        },
        "required": ["ticket_draft_id", "approved_by"],
    },
}


def prepare_ticket_creation(
    request_id: str,
    title: str | None = None,
    priority: str | None = None,
) -> dict:
    """
    MCP Tool: Prepare ticket creation draft.

    Description:
        Use this tool when a user wants to create a support/incident ticket
        for an access request. This tool does not create the ticket immediately.
        It prepares a draft and requires human confirmation.

    Args:
        request_id (str): Access request ID
        title (str | None): Optional ticket title
        priority (str | None): Optional ticket priority

    Returns:
        dict: Prepared ticket draft or structured error
    """
    try:
        ticket_draft = ticket_service.prepare_ticket_creation(
            request_id=request_id,
            title=title,
            priority=priority,
        )

        AuditLogger.log_tool_call(
            tool_name="prepare_ticket_creation",
            request_id=request_id,
            status="success",
        )

        return {
            "success": True,
            "data": ticket_draft.to_dict(),
        }

    except ValueError as e:
        AuditLogger.log_tool_call(
            tool_name="prepare_ticket_creation",
            request_id=request_id,
            status="failure",
        )

        error_message = str(e)

        if "not found" in error_message.lower():
            return ErrorUtils.access_request_not_found(request_id)

        return ErrorUtils.generic_error(error_message)

    except Exception as e:
        AuditLogger.log_tool_call(
            tool_name="prepare_ticket_creation",
            request_id=request_id,
            status="failure",
        )

        return ErrorUtils.generic_error(str(e))


def submit_ticket_creation_after_confirmation(
    ticket_draft_id: str,
    approved_by: str,
) -> dict:
    """
    MCP Tool: Submit ticket creation after human confirmation.

    Description:
        Use this tool only after a ticket draft has been prepared and
        the user/operator has explicitly approved the ticket creation.

    Args:
        ticket_draft_id (str): Ticket draft ID
        approved_by (str): User/operator who approved ticket creation

    Returns:
        dict: Created ticket details or structured error
    """
    try:
        result = ticket_service.submit_ticket_creation_after_confirmation(
            ticket_draft_id=ticket_draft_id,
            approved_by=approved_by,
        )

        AuditLogger.log_tool_call(
            tool_name="submit_ticket_creation_after_confirmation",
            request_id=result["request_id"],
            status="success",
        )

        return {
            "success": True,
            "data": result,
        }

    except ValueError as e:
        error_message = str(e)

        AuditLogger.log_tool_call(
            tool_name="submit_ticket_creation_after_confirmation",
            request_id=ticket_draft_id,
            status="failure",
        )

        if "not found" in error_message.lower():
            return ErrorUtils.ticket_draft_not_found(ticket_draft_id)

        if "approval is required" in error_message.lower():
            return ErrorUtils.ticket_approval_required()

        if "already been processed" in error_message.lower():
            return ErrorUtils.ticket_already_processed(ticket_draft_id)

        return ErrorUtils.generic_error(error_message)

    except Exception as e:
        AuditLogger.log_tool_call(
            tool_name="submit_ticket_creation_after_confirmation",
            request_id=ticket_draft_id,
            status="failure",
        )

        return ErrorUtils.generic_error(str(e))