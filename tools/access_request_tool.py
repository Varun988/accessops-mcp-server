from services.request_service import RequestService

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
        request = RequestService.get_request_by_id(request_id)

        return {
            "success": True,
            "data": request.to_dict()
        }

    except ValueError as e:
        return {
            "success": False,
            "error": str(e)
        }

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
        approvers = RequestService.get_pending_approvers(request_id)

        return {
            "success": True,
            "data": {
                "request_id": request_id,
                "pending_approvers": approvers
            }
        }

    except ValueError as e:
        return {
            "success": False,
            "error": str(e)
        }

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
        # Step 1: Get request status
        request = RequestService.get_request_by_id(request_id)

        # Step 2: Get pending approvers
        try:
            approvers = RequestService.get_pending_approvers(request_id)
        except ValueError:
            approvers = []

        # Step 3: Basic reasoning logic
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

        return {
            "success": True,
            "data": {
                "request_id": request_id,
                "status": request.status,
                "current_stage": request.current_stage,
                "diagnosis": diagnosis
            }
        }

    except ValueError as e:
        return {
            "success": False,
            "error": str(e)
        }