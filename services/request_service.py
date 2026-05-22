from data.mock_data import MOCK_ACCESS_REQUESTS
from models.request_model import AccessRequest
from data.mock_data import MOCK_APPROVERS


class RequestService:
    """Service layer for handling access request operations"""

    @staticmethod
    def get_request_by_id(request_id: str) -> AccessRequest:
        """
        Fetch an access request by ID.

        Raises:
            ValueError: If request is not found
        """
        request = MOCK_ACCESS_REQUESTS.get(request_id)

        if not request:
            raise ValueError(f"Access request '{request_id}' not found")

        return request

    @staticmethod
    def get_pending_approvers(request_id: str) -> list:
        """
        Fetch pending approvers for a request.

        Raises:
            ValueError: If request is not found
        """
        if request_id not in MOCK_APPROVERS:
            raise ValueError(f"No approvers found for request '{request_id}'")

        return MOCK_APPROVERS[request_id]

