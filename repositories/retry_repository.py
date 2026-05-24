from abc import ABC, abstractmethod

from models.retry_model import ProvisioningRetryDraft


class RetryRepository(ABC):
    """Repository interface for provisioning retry draft persistence."""

    @abstractmethod
    def save_retry_draft(self, retry_draft: ProvisioningRetryDraft) -> None:
        """
        Save a provisioning retry draft.

        Args:
            retry_draft (ProvisioningRetryDraft): Retry draft to persist
        """
        pass

    @abstractmethod
    def get_retry_draft_by_id(self, retry_id: str) -> ProvisioningRetryDraft | None:
        """
        Fetch a provisioning retry draft by retry ID.

        Args:
            retry_id (str): Retry draft ID

        Returns:
            ProvisioningRetryDraft | None: Matching retry draft if found
        """
        pass

    @abstractmethod
    def update_retry_draft(self, retry_draft: ProvisioningRetryDraft) -> None:
        """
        Update an existing provisioning retry draft.

        Args:
            retry_draft (ProvisioningRetryDraft): Retry draft to update
        """
        pass
        