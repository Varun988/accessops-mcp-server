class ErrorResponse:
    """Standard error response model for MCP tool outputs."""

    def __init__(
        self,
        code: str,
        message: str,
        retryable: bool,
        suggested_action: str,
    ):
        self.code = code
        self.message = message
        self.retryable = retryable
        self.suggested_action = suggested_action

    def to_dict(self) -> dict:
        """Convert error response to dictionary."""
        return {
            "code": self.code,
            "message": self.message,
            "retryable": self.retryable,
            "suggested_action": self.suggested_action,
        }