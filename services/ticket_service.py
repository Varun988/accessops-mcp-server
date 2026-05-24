from datetime import datetime
from uuid import uuid4

from data.mock_data import MOCK_TICKET_DRAFTS, MOCK_CREATED_TICKETS
from models.ticket_model import TicketCreationDraft
from services.request_service import RequestService


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