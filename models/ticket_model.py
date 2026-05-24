from datetime import datetime


class TicketCreationDraft:
    """Model representing a prepared ticket creation action."""

    def __init__(
        self,
        ticket_draft_id: str,
        request_id: str,
        title: str,
        description: str,
        priority: str,
        category: str,
        status: str,
        requires_confirmation: bool,
        created_at: datetime,
        approved_by: str | None = None,
        submitted_at: datetime | None = None,
        ticket_id: str | None = None,
    ):
        self.ticket_draft_id = ticket_draft_id
        self.request_id = request_id
        self.title = title
        self.description = description
        self.priority = priority
        self.category = category
        self.status = status
        self.requires_confirmation = requires_confirmation
        self.created_at = created_at
        self.approved_by = approved_by
        self.submitted_at = submitted_at
        self.ticket_id = ticket_id

    def to_dict(self) -> dict:
        """Convert ticket draft to dictionary."""
        return {
            "ticket_draft_id": self.ticket_draft_id,
            "request_id": self.request_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "category": self.category,
            "status": self.status,
            "requires_confirmation": self.requires_confirmation,
            "created_at": self.created_at.isoformat(),
            "approved_by": self.approved_by,
            "submitted_at": self.submitted_at.isoformat() if self.submitted_at else None,
            "ticket_id": self.ticket_id,
        }

class TicketClosureDraft:
    """Model representing a prepared ticket closure action."""

    def __init__(
        self,
        closure_draft_id: str,
        ticket_id: str,
        request_id: str,
        closure_reason: str,
        resolution_summary: str,
        status: str,
        requires_confirmation: bool,
        created_at: datetime,
        approved_by: str | None = None,
        submitted_at: datetime | None = None,
    ):
        self.closure_draft_id = closure_draft_id
        self.ticket_id = ticket_id
        self.request_id = request_id
        self.closure_reason = closure_reason
        self.resolution_summary = resolution_summary
        self.status = status
        self.requires_confirmation = requires_confirmation
        self.created_at = created_at
        self.approved_by = approved_by
        self.submitted_at = submitted_at

    def to_dict(self) -> dict:
        """Convert ticket closure draft to dictionary."""
        return {
            "closure_draft_id": self.closure_draft_id,
            "ticket_id": self.ticket_id,
            "request_id": self.request_id,
            "closure_reason": self.closure_reason,
            "resolution_summary": self.resolution_summary,
            "status": self.status,
            "requires_confirmation": self.requires_confirmation,
            "created_at": self.created_at.isoformat(),
            "approved_by": self.approved_by,
            "submitted_at": self.submitted_at.isoformat() if self.submitted_at else None,
        }