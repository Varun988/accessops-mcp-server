from services.request_service import RequestService
from utils.error_utils import ErrorUtils
from utils.audit_logger import AuditLogger

request_service = RequestService()

TOOL_METADATA = {
    "name": "get_access_request_status",
    "description": "Get status and details of an access request using request ID.",
    "input_schema": {
        "type": "object",
        "properties": {
            "request_id": {
                "type": "string",
                "description": "Access request ID (e.g., REQ-1001)"
            }
        },
        "required": ["request_id"]
    }
}

PENDING_APPROVERS_TOOL_METADATA = {
    "name": "get_pending_approvers",
    "description": "Get list of users or teams who need to approve the access request.",
    "input_schema": {
        "type": "object",
        "properties": {
            "request_id": {
                "type": "string",
                "description": "Access request ID (e.g., REQ-1001)"
            }
        },
        "required": ["request_id"]
    }
}

DIAGNOSE_TOOL_METADATA = {
    "name": "diagnose_access_request",
    "description": "Explain why an access request is pending, in progress, or failed.",
    "input_schema": {
        "type": "object",
        "properties": {
            "request_id": {
                "type": "string",
                "description": "Access request ID"
            }
        },
        "required": ["request_id"]
    }
}

PREPARE_PROVISIONING_RETRY_METADATA = {
    "name": "prepare_provisioning_retry",
    "description": (
        "Prepare a provisioning retry for a failed access request. "
        "This does not execute the retry and requires explicit confirmation."
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
                "description": "Retry draft ID, for example RETRY-1",
            },
            "approved_by": {
                "type": "string",
                "description": "User ID of the person approving the retry",
            },
        },
        "required": ["retry_id", "approved_by"],
    },
}



def get_access_request_status(request_id: str) -> dict:
    """
    MCP Tool: Get access request status.

    Description:
        Use this tool when you need to check the current status of an access request.
        It returns details such as status, current stage, requester, and last update time.

    Args:
        request_id (str): Unique identifier of the access request (e.g., REQ-1001)

    Returns:
        dict: Structured response containing request details or error
    """
    try:
        request = request_service.get_request_by_id(request_id)

        AuditLogger.log_tool_call(
            tool_name="access_request_status",
            request_id=request_id,
            status="success",
        )

        return {
            "success": True,
            "data": request.to_dict()
        }

    except ValueError:
        AuditLogger.log_tool_call(
            tool_name="access_request_status",
            request_id=request_id,
            status="failure",
        )
        return ErrorUtils.access_request_not_found(request_id)

    except Exception as e:
        AuditLogger.log_tool_call(
            tool_name="access_request_status",
            request_id=request_id,
            status="failure",
        )
        return ErrorUtils.generic_error(str(e))


def get_pending_approvers(request_id: str) -> dict:
    """
    MCP Tool: Get pending approvers for an access request.

    Description:
        Use this tool to find out which users or teams need to approve
        a given access request.

    Args:
        request_id (str): Unique identifier of the access request

    Returns:
        dict: List of approvers or error
    """
    try:
        approvers = request_service.get_pending_approvers(request_id)

        AuditLogger.log_tool_call(
            tool_name="pending_approvers",
            request_id=request_id,
            status="success",
        )

        return {
            "success": True,
            "data": {
                "request_id": request_id,
                "pending_approvers": approvers
            }
        }

    except ValueError:
        AuditLogger.log_tool_call(
            tool_name="pending_approvers",
            request_id=request_id,
            status="failure",
        )
        return ErrorUtils.approvers_not_found(request_id)

    except Exception as e:
        AuditLogger.log_tool_call(
            tool_name="pending_approvers",
            request_id=request_id,
            status="failure",
        )
        return ErrorUtils.generic_error(str(e))

def diagnose_access_request(request_id: str) -> dict:
    """
    MCP Tool: Diagnose why an access request is pending or failed.

    Description:
        Use this tool when the user asks why an access request is delayed,
        pending, or failed. It combines request status and approval details
        to provide a meaningful diagnosis.

    Args:
        request_id (str): Access request ID

    Returns:
        dict: Diagnosis summary
    """
    try:
        request = request_service.get_request_by_id(request_id)

        try:
            approvers = request_service.get_pending_approvers(request_id)
        except ValueError:
            approvers = []

        if request.status == "Pending":
            diagnosis = f"Request is pending at stage '{request.current_stage}'."
            if approvers:
                diagnosis += f" Awaiting approval from: {', '.join(approvers)}."

        elif request.status == "In Progress":
            diagnosis = f"Request is in progress at stage '{request.current_stage}'."

        elif request.status == "Failed":
            diagnosis = f"Request failed during '{request.current_stage}'. Needs investigation."

        else:
            diagnosis = f"Request is in status '{request.status}'."

        AuditLogger.log_tool_call(
            tool_name="diagnose_request",
            request_id=request_id,
            status="success",
        )

        return {
            "success": True,
            "data": {
                "request_id": request_id,
                "status": request.status,
                "current_stage": request.current_stage,
                "diagnosis": diagnosis
            }
        }

    except ValueError:
        AuditLogger.log_tool_call(
            tool_name="diagnose_request",
            request_id=request_id,
            status="failure",
        )
        return ErrorUtils.access_request_not_found(request_id)

    except Exception as e:
        AuditLogger.log_tool_call(
            tool_name="diagnose_request",
            request_id=request_id,
            status="failure",
        )
        return ErrorUtils.generic_error(str(e))


def prepare_provisioning_retry(request_id: str) -> dict:
    """
    MCP Tool: Prepare provisioning retry.

    Description:
        Use this tool to prepare a retry for a failed access request.
        This tool does not execute retry. It creates a retry draft and
        requires explicit human confirmation.

    Args:
        request_id (str): Access request ID

    Returns:
        dict: Retry draft details or structured error
    """
    try:
        retry_draft = request_service.prepare_provisioning_retry(request_id)

        AuditLogger.log_tool_call(
            tool_name="prepare_provisioning_retry",
            request_id=request_id,
            status="success",
        )

        return {
            "success": True,
            "data": {
                "retry_id": retry_draft["retry_id"],
                "request_id": retry_draft["request_id"],
                "target_system": retry_draft["target_system"],
                "role": retry_draft["role"],
                "status": retry_draft["status"],
                "requires_confirmation": retry_draft["requires_confirmation"],
                "summary": retry_draft["summary"],
                "message": "Retry draft created. Awaiting explicit confirmation.",
            },
        }

    except ValueError as e:
        AuditLogger.log_tool_call(
            tool_name="prepare_provisioning_retry",
            request_id=request_id,
            status="failure",
        )

        error_message = str(e)

        if "not found" in error_message.lower():
            return ErrorUtils.access_request_not_found(request_id)

        if "retry not allowed" in error_message.lower():
            return ErrorUtils.retry_not_allowed(
                request_id=request_id,
                reason=error_message,
            )

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
    MCP Tool: Submit provisioning retry after confirmation.

    Description:
        Use this tool only after explicit human confirmation.
        It executes a previously prepared provisioning retry draft.

    Args:
        retry_id (str): Retry draft ID
        approved_by (str): User who approved the action

    Returns:
        dict: Retry execution result or structured error
    """
    try:
        result = request_service.submit_provisioning_retry_after_confirmation(
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
            "data": {
                "retry_id": result["retry_id"],
                "request_id": result["request_id"],
                "status": result["status"],
                "approved_by": result["approved_by"],
                "requires_confirmation": result["requires_confirmation"],
                "message": "Provisioning retry executed successfully.",
            },
        }

    except ValueError as e:
        AuditLogger.log_tool_call(
            tool_name="submit_provisioning_retry_after_confirmation",
            request_id=retry_id,
            status="failure",
        )

        error_message = str(e)

        if "not found" in error_message.lower():
            return ErrorUtils.retry_draft_not_found(retry_id)

        if "already processed" in error_message.lower():
            return ErrorUtils.retry_already_processed(retry_id)

        return ErrorUtils.generic_error(error_message)

    except Exception as e:
        AuditLogger.log_tool_call(
            tool_name="submit_provisioning_retry_after_confirmation",
            request_id=retry_id,
            status="failure",
        )

        return ErrorUtils.generic_error(str(e))