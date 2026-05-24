from models.error_model import ErrorResponse


class ErrorUtils:
    """Utility class for building standardized error responses."""

    @staticmethod
    def access_request_not_found(request_id: str) -> dict:
        return {
            "success": False,
            "error": ErrorResponse(
                code="ACCESS_REQUEST_NOT_FOUND",
                message=f"Access request '{request_id}' was not found.",
                retryable=False,
                suggested_action="Verify the request ID and try again.",
            ).to_dict(),
        }

    @staticmethod
    def approvers_not_found(request_id: str) -> dict:
        return {
            "success": False,
            "error": ErrorResponse(
                code="APPROVERS_NOT_FOUND",
                message=f"No pending approvers were found for request '{request_id}'.",
                retryable=False,
                suggested_action="Verify whether the request is valid or already completed.",
            ).to_dict(),
        }

    @staticmethod
    def generic_error(message: str) -> dict:
        return {
            "success": False,
            "error": ErrorResponse(
                code="INTERNAL_ERROR",
                message=message,
                retryable=True,
                suggested_action="Retry the operation. If the issue persists, contact support.",
            ).to_dict(),
        }

    @staticmethod
    def retry_not_allowed(request_id: str, reason: str) -> dict:
        return {
            "success": False,
            "error": ErrorResponse(
                code="RETRY_NOT_ALLOWED",
                message=f"Provisioning retry is not allowed for request '{request_id}'. {reason}",
                retryable=False,
                suggested_action="Retry can be prepared only for access requests in Failed status.",
            ).to_dict(),
        }

    @staticmethod
    def retry_draft_not_found(retry_id: str) -> dict:
        return {
            "success": False,
            "error": ErrorResponse(
                code="RETRY_DRAFT_NOT_FOUND",
                message=f"Retry draft '{retry_id}' was not found.",
                retryable=False,
                suggested_action="Prepare a provisioning retry first, then submit it after confirmation.",
            ).to_dict(),
        }
    @staticmethod
    def retry_already_processed(retry_id: str) -> dict:
        return {
            "success": False,
            "error": ErrorResponse(
                code="RETRY_ALREADY_PROCESSED",
                message=f"Retry draft '{retry_id}' has already been processed.",
                retryable=False,
                suggested_action="Prepare a new provisioning retry draft if another retry is required.",
            ).to_dict(),
        }
        
    @staticmethod
    def approval_required() -> dict:
        return {
            "success": False,
            "error": ErrorResponse(
                code="APPROVAL_REQUIRED",
                message="Human approval is required before submitting the provisioning retry.",
                retryable=False,
                suggested_action="Provide the approving user or operator before submitting the retry.",
            ).to_dict(),
        }

    @staticmethod
    def ticket_draft_not_found(ticket_draft_id: str) -> dict:
        return {
            "success": False,
            "error": ErrorResponse(
                code="TICKET_DRAFT_NOT_FOUND",
                message=f"Ticket draft '{ticket_draft_id}' was not found.",
                retryable=False,
                suggested_action="Prepare a ticket creation draft first, then submit it after confirmation.",
            ).to_dict(),
        }

    @staticmethod
    def ticket_already_processed(ticket_draft_id: str) -> dict:
        return {
            "success": False,
            "error": ErrorResponse(
                code="TICKET_ALREADY_PROCESSED",
                message=f"Ticket draft '{ticket_draft_id}' has already been processed.",
                retryable=False,
                suggested_action="Prepare a new ticket creation draft if another ticket is required.",
            ).to_dict(),
        }

    @staticmethod
    def ticket_approval_required() -> dict:
        return {
            "success": False,
            "error": ErrorResponse(
                code="TICKET_APPROVAL_REQUIRED",
                message="Human approval is required before creating the ticket.",
                retryable=False,
                suggested_action="Provide the approving user or operator before submitting ticket creation.",
            ).to_dict(),
        }
    @staticmethod
    def notification_draft_not_found(notification_draft_id: str) -> dict:
        return {
            "success": False,
            "error": ErrorResponse(
                code="NOTIFICATION_DRAFT_NOT_FOUND",
                message=f"Notification draft '{notification_draft_id}' was not found.",
                retryable=False,
                suggested_action="Prepare a notification draft first, then send it after confirmation.",
            ).to_dict(),
        }

    @staticmethod
    def notification_already_processed(notification_draft_id: str) -> dict:
        return {
            "success": False,
            "error": ErrorResponse(
                code="NOTIFICATION_ALREADY_PROCESSED",
                message=f"Notification draft '{notification_draft_id}' has already been processed.",
                retryable=False,
                suggested_action="Prepare a new notification draft if another notification is required.",
            ).to_dict(),
        }

    @staticmethod
    def notification_approval_required() -> dict:
        return {
            "success": False,
            "error": ErrorResponse(
                code="NOTIFICATION_APPROVAL_REQUIRED",
                message="Human approval is required before sending the notification.",
                retryable=False,
                suggested_action="Provide the approving user or operator before sending the notification.",
            ).to_dict(),
        }
