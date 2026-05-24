from abc import ABC, abstractmethod


class AuditRepository(ABC):
    """Repository interface for audit event persistence."""

    @abstractmethod
    def save_audit_event(self, audit_event: dict) -> None:
        """
        Persist an audit event.

        Args:
            audit_event (dict): Audit event data
        """
        pass