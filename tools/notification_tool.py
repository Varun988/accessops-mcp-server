from services.notification_service import NotificationService
from utils.audit_logger import AuditLogger
from utils.error_utils import ErrorUtils


notification_service = NotificationService()


PREPARE_NOTIFICATION_METADATA = {
    "name": "prepare_notification",
    "description": (
        "Prepare a notification draft for an access request. "
        "This does not send the notification and requires explicit human confirmation."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "request_id": {
                "type": "string",
                "description": "Access request ID, for example REQ-1003",
            },
            "recipient": {
                "type": "string",
                "description": "Optional notification recipient. Defaults to the requester.",
            },
            "channel": {
                "type": "string",
                "description": "Optional notification channel such as email, teams, or slack.",
            },
            "subject": {
                "type": "string",
                "description": "Optional notification subject.",
            },
            "message": {
                "type": "string",
                "description": "Optional notification message.",
            },
        },
        "required": ["request_id"],
    },
}


SEND_NOTIFICATION_METADATA = {
    "name": "send_notification_after_confirmation",
    "description": (
        "Send a prepared notification after explicit human confirmation."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "notification_draft_id": {
                "type": "string",
                "description": "Notification draft ID returned by prepare_notification.",
            },
            "approved_by": {
                "type": "string",
                "description": "User/operator who approved sending the notification.",
            },
        },
        "required": ["notification_draft_id", "approved_by"],
    },
}


def prepare_notification(
    request_id: str,
    recipient: str | None = None,
    channel: str | None = None,
    subject: str | None = None,
    message: str | None = None,
) -> dict:
    """
    MCP Tool: Prepare notification draft.

    Description:
        Use this tool when a user wants to notify a requester, approver,
        or operations team about an access request. This tool does not send
        the notification immediately. It prepares a draft and requires human
        confirmation.

    Args:
        request_id (str): Access request ID
        recipient (str | None): Optional notification recipient
        channel (str | None): Optional notification channel
        subject (str | None): Optional notification subject
        message (str | None): Optional notification message

    Returns:
        dict: Prepared notification draft or structured error
    """
    try:
        notification_draft = notification_service.prepare_notification(
            request_id=request_id,
            recipient=recipient,
            channel=channel,
            subject=subject,
            message=message,
        )

        AuditLogger.log_tool_call(
            tool_name="prepare_notification",
            request_id=request_id,
            status="success",
        )

        return {
            "success": True,
            "data": notification_draft.to_dict(),
        }

    except ValueError as e:
        AuditLogger.log_tool_call(
            tool_name="prepare_notification",
            request_id=request_id,
            status="failure",
        )

        error_message = str(e)

        if "not found" in error_message.lower():
            return ErrorUtils.access_request_not_found(request_id)

        return ErrorUtils.generic_error(error_message)

    except Exception as e:
        AuditLogger.log_tool_call(
            tool_name="prepare_notification",
            request_id=request_id,
            status="failure",
        )

        return ErrorUtils.generic_error(str(e))


def send_notification_after_confirmation(
    notification_draft_id: str,
    approved_by: str,
) -> dict:
    """
    MCP Tool: Send notification after human confirmation.

    Description:
        Use this tool only after a notification draft has been prepared and
        the user/operator has explicitly approved sending the notification.

    Args:
        notification_draft_id (str): Notification draft ID
        approved_by (str): User/operator who approved sending

    Returns:
        dict: Sent notification details or structured error
    """
    try:
        result = notification_service.send_notification_after_confirmation(
            notification_draft_id=notification_draft_id,
            approved_by=approved_by,
        )

        AuditLogger.log_tool_call(
            tool_name="send_notification_after_confirmation",
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
            tool_name="send_notification_after_confirmation",
            request_id=notification_draft_id,
            status="failure",
        )

        if "not found" in error_message.lower():
            return ErrorUtils.notification_draft_not_found(notification_draft_id)

        if "approval is required" in error_message.lower():
            return ErrorUtils.notification_approval_required()

        if "already been processed" in error_message.lower():
            return ErrorUtils.notification_already_processed(notification_draft_id)

        return ErrorUtils.generic_error(error_message)

    except Exception as e:
        AuditLogger.log_tool_call(
            tool_name="send_notification_after_confirmation",
            request_id=notification_draft_id,
            status="failure",
        )

        return ErrorUtils.generic_error(str(e))