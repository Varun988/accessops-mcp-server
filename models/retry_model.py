from datetime import datetime


class ProvisioningRetryDraft:
    """Model representing a prepared provisioning retry action."""

    def __init__(
        self,
        retry_id: str,
        request_id: str,
        action: str,
        risk_level: str,
        requires_confirmation: bool,
        status: str,
        summary: str,
        created_at: datetime,
        approved_by: str | None = None,
        submitted_at: datetime | None = None,
    ):
        self.retry_id = retry_id
        self.request_id = request_id
        self.action = action
        self.risk_level = risk_level
        self.requires_confirmation = requires_confirmation
        self.status = status
        self.summary = summary
        self.created_at = created_at
        self.approved_by = approved_by
        self.submitted_at = submitted_at

    def to_dict(self) -> dict:
        """Convert retry draft to dictionary."""
        return {
            "retry_id": self.retry_id,
            "request_id": self.request_id,
            "action": self.action,
            "risk_level": self.risk_level,
            "requires_confirmation": self.requires_confirmation,
            "status": self.status,
            "summary": self.summary,
            "created_at": self.created_at.isoformat(),
            "approved_by": self.approved_by,
            "submitted_at": self.submitted_at.isoformat() if self.submitted_at else None,
        }