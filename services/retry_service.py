from datetime import datetime
from uuid import uuid4

from data.mock_data import MOCK_RETRY_DRAFTS
from models.retry_model import ProvisioningRetryDraft
from services.request_service import RequestService
from services.authorization_service import AuthorizationService


class RetryService:
    """Service layer for preparing and submitting provisioning retry actions."""

    def __init__(self, request_service: RequestService | None = None):
        """
        Initialize retry service.

        Args:
            request_service (RequestService | None): Optional request service dependency.
        """
        self.request_service = request_service or RequestService()

    def prepare_provisioning_retry(self, request_id: str) -> ProvisioningRetryDraft:
        """
        Prepare a provisioning retry draft for a failed access request.

        Args:
            request_id (str): Access request ID

        Returns:
            ProvisioningRetryDraft: Prepared retry draft

        Raises:
            ValueError: If request is not found or retry is not allowed
        """
        access_request = self.request_service.get_request_by_id(request_id)

        if access_request.status != "Failed":
            raise ValueError(
                f"Provisioning retry is allowed only for failed requests. "
                f"Current status is '{access_request.status}'."
            )

        retry_id = f"RETRY-{request_id}-{str(uuid4())[:8]}"

        retry_draft = ProvisioningRetryDraft(
            retry_id=retry_id,
            request_id=request_id,
            action="Retry provisioning",
            risk_level="Medium",
            requires_confirmation=True,
            status="Prepared",
            summary=(
                f"Provisioning retry prepared for access request {request_id}. "
                f"The request failed during '{access_request.current_stage}'. "
                "User confirmation is required before execution."
            ),
            created_at=datetime.utcnow(),
        )

        MOCK_RETRY_DRAFTS[retry_id] = retry_draft

        return retry_draft

    def submit_provisioning_retry_after_confirmation(
        self,
        retry_id: str,
        approved_by: str,
    ) -> dict:
        """
        Submit a prepared provisioning retry after human confirmation.

        Args:
            retry_id (str): Retry draft ID
            approved_by (str): User/operator who approved the retry

        Returns:
            dict: Retry execution result

        Raises:
            ValueError: If retry draft is not found, already processed, or approval is missing
        """
        retry_draft = MOCK_RETRY_DRAFTS.get(retry_id)

        if not retry_draft:
            raise ValueError(f"Retry draft '{retry_id}' not found")

        if not approved_by or not approved_by.strip():
            raise ValueError("Approval is required before submitting provisioning retry")

        AuthorizationService.require_permission(
            user_id=approved_by,
            permission="provisioning:retry",
        )

        if retry_draft.status != "Prepared":
            raise ValueError(f"Retry draft '{retry_id}' has already been processed")

        retry_draft.status = "Submitted"
        retry_draft.requires_confirmation = False
        retry_draft.approved_by = approved_by
        retry_draft.submitted_at = datetime.utcnow()

        return {
            "retry_id": retry_id,
            "request_id": retry_draft.request_id,
            "action": retry_draft.action,
            "risk_level": retry_draft.risk_level,
            "status": retry_draft.status,
            "requires_confirmation": retry_draft.requires_confirmation,
            "approved_by": retry_draft.approved_by,
            "submitted_at": retry_draft.submitted_at.isoformat(),
            "message": (
                f"Provisioning retry for request {retry_draft.request_id} "
                f"has been submitted after approval by {approved_by}."
            ),
        }