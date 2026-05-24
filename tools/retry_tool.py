from services.retry_service import RetryService
from utils.audit_logger import AuditLogger
from utils.error_utils import ErrorUtils


retry_service = RetryService()


PREPARE_PROVISIONING_RETRY_METADATA = {
    "name": "prepare_provisioning_retry",
    "description": (
        "Prepare a provisioning retry for a failed access request. "
        "This does not execute the retry and requires explicit human confirmation."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "request_id": {
                "type": "string",
                "description": "Access request ID, for example REQ-1003",
            }
        },
        "required": ["request_id"],
    },
}


SUBMIT_PROVISIONING_RETRY_METADATA = {
    "name": "submit_provisioning_retry_after_confirmation",
    "description": (
        "Execute a prepared provisioning retry after explicit human confirmation."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "retry_id": {
                "type": "string",
                "description": "Retry draft ID returned by prepare_provisioning_retry",
            },
            "approved_by": {
                "type": "string",
                "description": "User/operator who approved the retry",
            },
        },
        "required": ["retry_id", "approved_by"],
    },
}


def prepare_provisioning_retry(request_id: str) -> dict:
    """
    MCP Tool: Prepare a provisioning retry draft.

    Description:
        Use this tool when a user asks whether provisioning can be retried
        for a failed access request. This tool does not execute the retry.
        It only prepares a retry draft and requires human confirmation before submission.

    Args:
        request_id (str): Access request ID

    Returns:
        dict: Prepared retry draft or structured error
    """
    try:
        retry_draft = retry_service.prepare_provisioning_retry(request_id)

        AuditLogger.log_tool_call(
            tool_name="prepare_provisioning_retry",
            request_id=request_id,
            status="success",
        )

        return {
            "success": True,
            "data": retry_draft.to_dict(),
        }

    except ValueError as e:
        AuditLogger.log_tool_call(
            tool_name="prepare_provisioning_retry",
            request_id=request_id,
            status="failure",
        )

        error_message = str(e)

        if "only for failed requests" in error_message.lower():
            return ErrorUtils.retry_not_allowed(request_id, error_message)

        if "not found" in error_message.lower():
            return ErrorUtils.access_request_not_found(request_id)

        return ErrorUtils.generic_error(error_message)

    except Exception as e:
        AuditLogger.log_tool_call(
            tool_name="prepare_provisioning_retry",
            request_id=request_id,
            status="failure",
        )

        return ErrorUtils.generic_error(str(e))


def submit_provisioning_retry_after_confirmation(
    retry_id: str,
    approved_by: str,
) -> dict:
    """
    MCP Tool: Submit provisioning retry after human confirmation.

    Description:
        Use this tool only after a retry draft has been prepared and the user/operator
        has explicitly approved the retry action.

    Args:
        retry_id (str): Retry draft ID
        approved_by (str): User/operator who approved the retry

    Returns:
        dict: Retry submission result or structured error
    """
    try:
        result = retry_service.submit_provisioning_retry_after_confirmation(
            retry_id=retry_id,
            approved_by=approved_by,
        )

        AuditLogger.log_tool_call(
            tool_name="submit_provisioning_retry_after_confirmation",
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
            tool_name="submit_provisioning_retry_after_confirmation",
            request_id=retry_id,
            status="failure",
        )

        if "not found" in error_message.lower():
            return ErrorUtils.retry_draft_not_found(retry_id)

        if "approval is required" in error_message.lower():
            return ErrorUtils.approval_required()

        if "already been processed" in error_message.lower():
            return ErrorUtils.retry_already_processed(retry_id)

        return ErrorUtils.generic_error(error_message)
    
    except PermissionError:
        AuditLogger.log_tool_call(
            tool_name="submit_provisioning_retry_after_confirmation",
            request_id=retry_id,
            status="failure",
        )

        return ErrorUtils.authorization_failed(
            user_id=approved_by,
            permission="provisioning:retry",
        )

    except Exception as e:
        AuditLogger.log_tool_call(
            tool_name="submit_provisioning_retry_after_confirmation",
            request_id=retry_id,
            status="failure",
        )

        return ErrorUtils.generic_error(str(e))