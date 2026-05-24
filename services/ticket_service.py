from datetime import datetime
from uuid import uuid4

from data.mock_data import (
    MOCK_TICKET_DRAFTS,
    MOCK_CREATED_TICKETS,
    MOCK_TICKET_CLOSURE_DRAFTS,
)
from models.ticket_model import TicketCreationDraft, TicketClosureDraft
from services.request_service import RequestService
from services.authorization_service import AuthorizationService

class TicketService:
    """Service layer for preparing and submitting ticket creation actions."""

    def __init__(self, request_service: RequestService | None = None):
        """
        Initialize ticket service.

        Args:
            request_service (RequestService | None): Optional request service dependency.
        """
        self.request_service = request_service or RequestService()

    def prepare_ticket_creation(
        self,
        request_id: str,
        title: str | None = None,
        priority: str | None = None,
    ) -> TicketCreationDraft:
        """
        Prepare a ticket creation draft for an access request.

        This method does not create the ticket immediately. It only creates
        a ticket draft that requires explicit human confirmation.

        Args:
            request_id (str): Access request ID
            title (str | None): Optional ticket title
            priority (str | None): Optional ticket priority

        Returns:
            TicketCreationDraft: Prepared ticket draft

        Raises:
            ValueError: If access request is not found
        """
        access_request = self.request_service.get_request_by_id(request_id)

        ticket_draft_id = f"TICKET-DRAFT-{request_id}-{str(uuid4())[:8]}"

        resolved_title = title or (
            f"Access request issue for {request_id}"
        )

        resolved_priority = priority or self._derive_priority_from_request_status(
            access_request.status
        )

        description = (
            f"Access request {request_id} requires support attention.\n\n"
            f"Requester: {access_request.requester}\n"
            f"Target system: {access_request.target_system}\n"
            f"Requested role: {access_request.role}\n"
            f"Current status: {access_request.status}\n"
            f"Current stage: {access_request.current_stage}\n"
            f"Last updated: {access_request.last_updated.isoformat()}\n\n"
            "This ticket was prepared by AccessOps MCP Server and requires "
            "human confirmation before creation."
        )

        ticket_draft = TicketCreationDraft(
            ticket_draft_id=ticket_draft_id,
            request_id=request_id,
            title=resolved_title,
            description=description,
            priority=resolved_priority,
            category="Access Management",
            status="Prepared",
            requires_confirmation=True,
            created_at=datetime.utcnow(),
        )

        MOCK_TICKET_DRAFTS[ticket_draft_id] = ticket_draft

        return ticket_draft

    def submit_ticket_creation_after_confirmation(
        self,
        ticket_draft_id: str,
        approved_by: str,
    ) -> dict:
        """
        Submit a prepared ticket creation draft after human confirmation.

        Args:
            ticket_draft_id (str): Ticket draft ID
            approved_by (str): User/operator who approved ticket creation

        Returns:
            dict: Created ticket details

        Raises:
            ValueError: If draft is not found, approval is missing, or draft is already processed
        """
        ticket_draft = MOCK_TICKET_DRAFTS.get(ticket_draft_id)

        if not ticket_draft:
            raise ValueError(f"Ticket draft '{ticket_draft_id}' not found")

        if not approved_by or not approved_by.strip():
            raise ValueError("Approval is required before creating ticket")

        AuthorizationService.require_permission(
            user_id=approved_by,
            permission="ticket:create",
        )

        if ticket_draft.status != "Prepared":
            raise ValueError(f"Ticket draft '{ticket_draft_id}' has already been processed")

        ticket_id = f"INC-{str(uuid4())[:8].upper()}"

        ticket_draft.status = "Created"
        ticket_draft.requires_confirmation = False
        ticket_draft.approved_by = approved_by
        ticket_draft.submitted_at = datetime.utcnow()
        ticket_draft.ticket_id = ticket_id

        created_ticket = {
            "ticket_id": ticket_id,
            "ticket_draft_id": ticket_draft_id,
            "request_id": ticket_draft.request_id,
            "title": ticket_draft.title,
            "description": ticket_draft.description,
            "priority": ticket_draft.priority,
            "category": ticket_draft.category,
            "status": ticket_draft.status,
            "requires_confirmation": ticket_draft.requires_confirmation,
            "approved_by": ticket_draft.approved_by,
            "submitted_at": ticket_draft.submitted_at.isoformat(),
            "message": (
                f"Ticket {ticket_id} has been created for access request "
                f"{ticket_draft.request_id} after approval by {approved_by}."
            ),
        }

        MOCK_CREATED_TICKETS[ticket_id] = created_ticket

        return created_ticket

    @staticmethod
    def _derive_priority_from_request_status(status: str) -> str:
        """
        Derive ticket priority based on access request status.

        Args:
            status (str): Access request status

        Returns:
            str: Ticket priority
        """
        if status == "Failed":
            return "High"

        if status == "Pending":
            return "Medium"

        return "Low"
    
    def prepare_ticket_closure(
        self,
        ticket_id: str,
        closure_reason: str | None = None,
        resolution_summary: str | None = None,
    ) -> TicketClosureDraft:
        """
        Prepare a ticket closure draft.

        This method does not close the ticket immediately. It only creates
        a closure draft that requires explicit human confirmation.

        Args:
            ticket_id (str): Ticket ID to close
            closure_reason (str | None): Optional closure reason
            resolution_summary (str | None): Optional resolution summary

        Returns:
            TicketClosureDraft: Prepared ticket closure draft

        Raises:
            ValueError: If ticket is not found or ticket is already closed
        """
        ticket = MOCK_CREATED_TICKETS.get(ticket_id)

        if not ticket:
            raise ValueError(f"Ticket '{ticket_id}' not found")

        if ticket.get("status") == "Closed":
            raise ValueError(f"Ticket '{ticket_id}' is already closed")

        closure_draft_id = f"CLOSURE-DRAFT-{ticket_id}-{str(uuid4())[:8]}"

        resolved_closure_reason = closure_reason or "Issue resolved"
        resolved_resolution_summary = resolution_summary or (
            f"Ticket {ticket_id} is ready for closure. "
            f"Access request {ticket['request_id']} has been reviewed and no further action is pending."
        )

        closure_draft = TicketClosureDraft(
            closure_draft_id=closure_draft_id,
            ticket_id=ticket_id,
            request_id=ticket["request_id"],
            closure_reason=resolved_closure_reason,
            resolution_summary=resolved_resolution_summary,
            status="Prepared",
            requires_confirmation=True,
            created_at=datetime.utcnow(),
        )

        MOCK_TICKET_CLOSURE_DRAFTS[closure_draft_id] = closure_draft

        return closure_draft

    def submit_ticket_closure_after_confirmation(
        self,
        closure_draft_id: str,
        approved_by: str,
    ) -> dict:
        """
        Close a ticket after human confirmation.

        Args:
            closure_draft_id (str): Ticket closure draft ID
            approved_by (str): User/operator who approved ticket closure

        Returns:
            dict: Closed ticket details

        Raises:
            ValueError: If closure draft is not found, approval is missing,
                draft is already processed, or ticket is not found
        """
        closure_draft = MOCK_TICKET_CLOSURE_DRAFTS.get(closure_draft_id)

        if not closure_draft:
            raise ValueError(f"Ticket closure draft '{closure_draft_id}' not found")

        if not approved_by or not approved_by.strip():
            raise ValueError("Approval is required before closing ticket")

        if closure_draft.status != "Prepared":
            raise ValueError(
                f"Ticket closure draft '{closure_draft_id}' has already been processed"
            )

        ticket = MOCK_CREATED_TICKETS.get(closure_draft.ticket_id)

        if not ticket:
            raise ValueError(f"Ticket '{closure_draft.ticket_id}' not found")

        if ticket.get("status") == "Closed":
            raise ValueError(f"Ticket '{closure_draft.ticket_id}' is already closed")

        closure_draft.status = "Closed"
        closure_draft.requires_confirmation = False
        closure_draft.approved_by = approved_by
        closure_draft.submitted_at = datetime.utcnow()

        ticket["status"] = "Closed"
        ticket["closure_reason"] = closure_draft.closure_reason
        ticket["resolution_summary"] = closure_draft.resolution_summary
        ticket["closed_by"] = approved_by
        ticket["closed_at"] = closure_draft.submitted_at.isoformat()

        return {
            "closure_draft_id": closure_draft_id,
            "ticket_id": closure_draft.ticket_id,
            "request_id": closure_draft.request_id,
            "status": ticket["status"],
            "closure_reason": closure_draft.closure_reason,
            "resolution_summary": closure_draft.resolution_summary,
            "requires_confirmation": closure_draft.requires_confirmation,
            "approved_by": closure_draft.approved_by,
            "closed_at": ticket["closed_at"],
            "message": (
                f"Ticket {closure_draft.ticket_id} has been closed after approval by "
                f"{approved_by}."
            ),
        }