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

PREPARE_TICKET_CLOSURE_METADATA = {
    "name": "prepare_ticket_closure",
    "description": (
        "Prepare a ticket closure draft. "
        "This does not close the ticket and requires explicit human confirmation."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "ticket_id": {
                "type": "string",
                "description": "Ticket ID to close, for example INC-12345678",
            },
            "closure_reason": {
                "type": "string",
                "description": "Optional reason for closing the ticket",
            },
            "resolution_summary": {
                "type": "string",
                "description": "Optional resolution summary for the ticket",
            },
        },
        "required": ["ticket_id"],
    },
}


SUBMIT_TICKET_CLOSURE_METADATA = {
    "name": "submit_ticket_closure_after_confirmation",
    "description": (
        "Close a ticket from a prepared closure draft after explicit human confirmation."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "closure_draft_id": {
                "type": "string",
                "description": "Closure draft ID returned by prepare_ticket_closure",
            },
            "approved_by": {
                "type": "string",
                "description": "User/operator who approved ticket closure",
            },
        },
        "required": ["closure_draft_id", "approved_by"],
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
        
    except PermissionError:
        AuditLogger.log_tool_call(
            tool_name="submit_ticket_creation_after_confirmation",
            request_id=ticket_draft_id,
            status="failure",
        )

        return ErrorUtils.authorization_failed(
            user_id=approved_by,
            permission="ticket:create",
        )

    except Exception as e:
        AuditLogger.log_tool_call(
            tool_name="submit_ticket_creation_after_confirmation",
            request_id=ticket_draft_id,
            status="failure",
        )

        return ErrorUtils.generic_error(str(e))

def prepare_ticket_closure(
    ticket_id: str,
    closure_reason: str | None = None,
    resolution_summary: str | None = None,
) -> dict:
    """
    MCP Tool: Prepare ticket closure draft.

    Description:
        Use this tool when a user wants to close an existing ticket.
        This tool does not close the ticket immediately. It prepares a
        closure draft and requires human confirmation.

    Args:
        ticket_id (str): Ticket ID
        closure_reason (str | None): Optional closure reason
        resolution_summary (str | None): Optional resolution summary

    Returns:
        dict: Prepared ticket closure draft or structured error
    """
    try:
        closure_draft = ticket_service.prepare_ticket_closure(
            ticket_id=ticket_id,
            closure_reason=closure_reason,
            resolution_summary=resolution_summary,
        )

        AuditLogger.log_tool_call(
            tool_name="prepare_ticket_closure",
            request_id=ticket_id,
            status="success",
        )

        return {
            "success": True,
            "data": closure_draft.to_dict(),
        }

    except ValueError as e:
        AuditLogger.log_tool_call(
            tool_name="prepare_ticket_closure",
            request_id=ticket_id,
            status="failure",
        )

        error_message = str(e).lower()

        if "not found" in error_message:
            return ErrorUtils.ticket_not_found(ticket_id)

        if "already closed" in error_message:
            return ErrorUtils.ticket_already_closed(ticket_id)

        return ErrorUtils.generic_error(str(e))

    except Exception as e:
        AuditLogger.log_tool_call(
            tool_name="prepare_ticket_closure",
            request_id=ticket_id,
            status="failure",
        )

        return ErrorUtils.generic_error(str(e))

def submit_ticket_closure_after_confirmation(
    closure_draft_id: str,
    approved_by: str,
) -> dict:
    """
    MCP Tool: Submit ticket closure after human confirmation.

    Description:
        Use this tool only after a closure draft has been prepared and
        the user/operator has explicitly approved ticket closure.

    Args:
        closure_draft_id (str): Ticket closure draft ID
        approved_by (str): User/operator who approved ticket closure

    Returns:
        dict: Closed ticket details or structured error
    """
    try:
        result = ticket_service.submit_ticket_closure_after_confirmation(
            closure_draft_id=closure_draft_id,
            approved_by=approved_by,
        )

        AuditLogger.log_tool_call(
            tool_name="submit_ticket_closure_after_confirmation",
            request_id=result["ticket_id"],
            status="success",
        )

        return {
            "success": True,
            "data": result,
        }

    except ValueError as e:
        error_message = str(e).lower()

        AuditLogger.log_tool_call(
            tool_name="submit_ticket_closure_after_confirmation",
            request_id=closure_draft_id,
            status="failure",
        )

        if "closure draft" in error_message and "not found" in error_message:
            return ErrorUtils.ticket_closure_draft_not_found(closure_draft_id)

        if "approval is required" in error_message:
            return ErrorUtils.ticket_closure_approval_required()

        if "already been processed" in error_message:
            return ErrorUtils.ticket_closure_already_processed(closure_draft_id)

        if "already closed" in error_message:
            return ErrorUtils.ticket_already_closed(closure_draft_id)

        if "ticket" in error_message and "not found" in error_message:
            return ErrorUtils.ticket_not_found(closure_draft_id)

        return ErrorUtils.generic_error(str(e))

    except Exception as e:
        AuditLogger.log_tool_call(
            tool_name="submit_ticket_closure_after_confirmation",
            request_id=closure_draft_id,
            status="failure",
        )

        return ErrorUtils.generic_error(str(e))