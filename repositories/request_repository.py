from abc import ABC, abstractmethod
from models.request_model import AccessRequest


class RequestRepository(ABC):
    """Abstract repository contract for access request data sources."""

    @abstractmethod
    def get_request_by_id(self, request_id: str) -> AccessRequest:
        """
        Fetch an access request by request ID.

        Args:
            request_id (str): Access request ID

        Returns:
            AccessRequest: Matching access request

        Raises:
            ValueError: If request is not found
        """
        pass

    @abstractmethod
    def get_pending_approvers(self, request_id: str) -> list[str]:
        """
        Fetch pending approvers for an access request.

        Args:
            request_id (str): Access request ID

        Returns:
            list[str]: Pending approvers

        Raises:
            ValueError: If approvers are not found
        """
        pass