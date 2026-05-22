from data.mock_data import MOCK_ACCESS_REQUESTS, MOCK_APPROVERS
from models.request_model import AccessRequest
from repositories.request_repository import RequestRepository


class MockRequestRepository(RequestRepository):
    """Mock repository implementation for access request data."""

    def get_request_by_id(self, request_id: str) -> AccessRequest:
        """
        Fetch an access request from mock data.

        Args:
            request_id (str): Access request ID

        Returns:
            AccessRequest: Matching access request

        Raises:
            ValueError: If request is not found
        """
        request = MOCK_ACCESS_REQUESTS.get(request_id)

        if not request:
            raise ValueError(f"Access request '{request_id}' not found")

        return request

    def get_pending_approvers(self, request_id: str) -> list:
        """
        Fetch pending approvers from mock data.

        Args:
            request_id (str): Access request ID

        Returns:
            list[str]: Pending approvers

        Raises:
            ValueError: If approvers are not found
        """
        approvers = MOCK_APPROVERS.get(request_id)

        if approvers is None:
            raise ValueError(f"No approvers found for request '{request_id}'")

        return approvers