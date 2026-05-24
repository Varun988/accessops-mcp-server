from datetime import datetime


class NotificationDraft:
    """Model representing a prepared notification action."""

    def __init__(
        self,
        notification_draft_id: str,
        request_id: str,
        recipient: str,
        channel: str,
        subject: str,
        message: str,
        status: str,
        requires_confirmation: bool,
        created_at: datetime,
        approved_by: str | None = None,
        sent_at: datetime | None = None,
        notification_id: str | None = None,
    ):
        self.notification_draft_id = notification_draft_id
        self.request_id = request_id
        self.recipient = recipient
        self.channel = channel
        self.subject = subject
        self.message = message
        self.status = status
        self.requires_confirmation = requires_confirmation
        self.created_at = created_at
        self.approved_by = approved_by
        self.sent_at = sent_at
        self.notification_id = notification_id

    def to_dict(self) -> dict:
        """Convert notification draft to dictionary."""
        return {
            "notification_draft_id": self.notification_draft_id,
            "request_id": self.request_id,
            "recipient": self.recipient,
            "channel": self.channel,
            "subject": self.subject,
            "message": self.message,
            "status": self.status,
            "requires_confirmation": self.requires_confirmation,
            "created_at": self.created_at.isoformat(),
            "approved_by": self.approved_by,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
            "notification_id": self.notification_id,
        }