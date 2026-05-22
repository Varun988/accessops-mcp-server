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