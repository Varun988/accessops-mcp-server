from datetime import datetime
from uuid import uuid4

from data.mock_data import MOCK_NOTIFICATION_DRAFTS, MOCK_SENT_NOTIFICATIONS
from models.notification_model import NotificationDraft
from services.request_service import RequestService


class NotificationService:
    """Service layer for preparing and sending notification actions."""

    def __init__(self, request_service: RequestService | None = None):
        """
        Initialize notification service.

        Args:
            request_service (RequestService | None): Optional request service dependency.
        """
        self.request_service = request_service or RequestService()

    def prepare_notification(
        self,
        request_id: str,
        recipient: str | None = None,
        channel: str | None = None,
        subject: str | None = None,
        message: str | None = None,
    ) -> NotificationDraft:
        """
        Prepare a notification draft for an access request.

        This method does not send the notification immediately. It only creates
        a notification draft that requires explicit human confirmation.

        Args:
            request_id (str): Access request ID
            recipient (str | None): Optional notification recipient
            channel (str | None): Optional notification channel
            subject (str | None): Optional notification subject
            message (str | None): Optional notification message

        Returns:
            NotificationDraft: Prepared notification draft

        Raises:
            ValueError: If access request is not found
        """
        access_request = self.request_service.get_request_by_id(request_id)

        notification_draft_id = f"NOTIFICATION-DRAFT-{request_id}-{str(uuid4())[:8]}"

        resolved_recipient = recipient or access_request.requester
        resolved_channel = channel or "email"

        resolved_subject = subject or self._build_default_subject(
            request_id=request_id,
            status=access_request.status,
        )

        resolved_message = message or self._build_default_message(
            request_id=request_id,
            requester=access_request.requester,
            target_system=access_request.target_system,
            role=access_request.role,
            status=access_request.status,
            current_stage=access_request.current_stage,
        )

        notification_draft = NotificationDraft(
            notification_draft_id=notification_draft_id,
            request_id=request_id,
            recipient=resolved_recipient,
            channel=resolved_channel,
            subject=resolved_subject,
            message=resolved_message,
            status="Prepared",
            requires_confirmation=True,
            created_at=datetime.utcnow(),
        )

        MOCK_NOTIFICATION_DRAFTS[notification_draft_id] = notification_draft

        return notification_draft

    def send_notification_after_confirmation(
        self,
        notification_draft_id: str,
        approved_by: str,
    ) -> dict:
        """
        Send a prepared notification after human confirmation.

        Args:
            notification_draft_id (str): Notification draft ID
            approved_by (str): User/operator who approved notification sending

        Returns:
            dict: Sent notification details

        Raises:
            ValueError: If draft is not found, approval is missing, or draft is already processed
        """
        notification_draft = MOCK_NOTIFICATION_DRAFTS.get(notification_draft_id)

        if not notification_draft:
            raise ValueError(f"Notification draft '{notification_draft_id}' not found")

        if not approved_by or not approved_by.strip():
            raise ValueError("Approval is required before sending notification")

        if notification_draft.status != "Prepared":
            raise ValueError(
                f"Notification draft '{notification_draft_id}' has already been processed"
            )

        notification_id = f"NOTIF-{str(uuid4())[:8].upper()}"

        notification_draft.status = "Sent"
        notification_draft.requires_confirmation = False
        notification_draft.approved_by = approved_by
        notification_draft.sent_at = datetime.utcnow()
        notification_draft.notification_id = notification_id

        sent_notification = {
            "notification_id": notification_id,
            "notification_draft_id": notification_draft_id,
            "request_id": notification_draft.request_id,
            "recipient": notification_draft.recipient,
            "channel": notification_draft.channel,
            "subject": notification_draft.subject,
            "message": notification_draft.message,
            "status": notification_draft.status,
            "requires_confirmation": notification_draft.requires_confirmation,
            "approved_by": notification_draft.approved_by,
            "sent_at": notification_draft.sent_at.isoformat(),
            "delivery_status": "Simulated",
            "delivery_note": (
                "Notification sending is simulated using mock storage. "
                "In production, this would call an email, chat, or enterprise notification API."
            ),
        }

        MOCK_SENT_NOTIFICATIONS[notification_id] = sent_notification

        return sent_notification

    @staticmethod
    def _build_default_subject(request_id: str, status: str) -> str:
        """
        Build a default notification subject.

        Args:
            request_id (str): Access request ID
            status (str): Access request status

        Returns:
            str: Notification subject
        """
        return f"Update on access request {request_id} - {status}"

    @staticmethod
    def _build_default_message(
        request_id: str,
        requester: str,
        target_system: str,
        role: str,
        status: str,
        current_stage: str,
    ) -> str:
        """
        Build a default notification message.

        Args:
            request_id (str): Access request ID
            requester (str): Requester user ID
            target_system (str): Target system
            role (str): Requested role
            status (str): Current request status
            current_stage (str): Current workflow stage

        Returns:
            str: Notification message
        """
        return (
            f"Hello {requester},\n\n"
            f"This is an update for your access request {request_id}.\n\n"
            f"Target system: {target_system}\n"
            f"Requested role: {role}\n"
            f"Current status: {status}\n"
            f"Current stage: {current_stage}\n\n"
            "This notification was prepared by AccessOps MCP Server and requires "
            "human confirmation before sending."
        )