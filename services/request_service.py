from models.request_model import AccessRequest
from repositories.mock_request_repository import MockRequestRepository
from repositories.request_repository import RequestRepository


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