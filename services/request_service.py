from datetime import datetime

from models.request_model import AccessRequest
from repositories.mock_request_repository import MockRequestRepository
from repositories.request_repository import RequestRepository
from data.mock_data import MOCK_RETRY_DRAFTS
import data.mock_data as mock_data


class RequestService:
    """Service layer for handling access request operations."""

    def __init__(self, repository: RequestRepository | None = None):
        """
        Initialize request service with a repository implementation.

        Args:
            repository (RequestRepository | None): Repository implementation.
                If not provided, MockRequestRepository is used by default.
        """
        self.repository = repository or MockRequestRepository()

    def get_request_by_id(self, request_id: str) -> AccessRequest:
        """
        Fetch an access request by ID.

        Args:
            request_id (str): Access request ID

        Returns:
            AccessRequest: Matching access request

        Raises:
            ValueError: If request is not found
        """
        return self.repository.get_request_by_id(request_id)

    def get_pending_approvers(self, request_id: str) -> list:
        """
        Fetch pending approvers for a request.

        Args:
            request_id (str): Access request ID

        Returns:
            list[str]: Pending approvers

        Raises:
            ValueError: If approvers are not found
        """
        return self.repository.get_pending_approvers(request_id)

    def prepare_provisioning_retry(self, request_id: str) -> dict:
        """
        Prepare a provisioning retry draft for a failed access request.

        This method does not execute retry. It only creates a retry draft
        that requires explicit human confirmation.

        Args:
            request_id (str): Access request ID

        Returns:
            dict: Retry draft details

        Raises:
            ValueError: If request does not exist or retry is not allowed
        """
        request = self.get_request_by_id(request_id)

        if request.status != "Failed":
            raise ValueError(
                f"Retry not allowed. Request '{request_id}' is not in Failed state."
            )

        retry_id = f"RETRY-{mock_data.RETRY_DRAFT_COUNTER}"
        mock_data.RETRY_DRAFT_COUNTER += 1

        retry_draft = {
            "retry_id": retry_id,
            "request_id": request_id,
            "target_system": request.target_system,
            "role": request.role,
            "status": "PENDING_CONFIRMATION",
            "requires_confirmation": True,
            "created_at": datetime.utcnow(),
            "approved_by": None,
            "executed_at": None,
            "summary": (
                f"Provisioning retry prepared for request '{request_id}' "
                f"on target system '{request.target_system}' for role '{request.role}'."
            ),
        }

        MOCK_RETRY_DRAFTS[retry_id] = retry_draft

        return retry_draft

    def submit_provisioning_retry_after_confirmation(
        self,
        retry_id: str,
        approved_by: str,
    ) -> dict:
        """
        Execute a prepared provisioning retry after explicit human confirmation.

        Args:
            retry_id (str): Retry draft ID
            approved_by (str): User who approved the retry execution

        Returns:
            dict: Retry execution result

        Raises:
            ValueError: If retry draft is not found or already processed
        """
        retry_draft = MOCK_RETRY_DRAFTS.get(retry_id)

        if not retry_draft:
            raise ValueError(f"Retry draft '{retry_id}' not found.")

        if retry_draft["status"] != "PENDING_CONFIRMATION":
            raise ValueError(f"Retry draft '{retry_id}' is already processed.")

        retry_draft["status"] = "COMPLETED"
        retry_draft["approved_by"] = approved_by
        retry_draft["executed_at"] = datetime.utcnow()
        retry_draft["requires_confirmation"] = False

        return retry_draft