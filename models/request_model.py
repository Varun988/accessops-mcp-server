from datetime import datetime


class AccessRequest:
    def __init__(
        self,
        request_id: str,
        requester: str,
        target_system: str,
        role: str,
        status: str,
        current_stage: str,
        requested_at: datetime,
        last_updated: datetime,
    ):
        self.request_id = request_id
        self.requester = requester
        self.target_system = target_system
        self.role = role
        self.status = status
        self.current_stage = current_stage
        self.requested_at = requested_at
        self.last_updated = last_updated

    def to_dict(self) -> dict:
        """Convert object to dictionary (useful for tool output)"""
        return {
            "request_id": self.request_id,
            "requester": self.requester,
            "target_system": self.target_system,
            "role": self.role,
            "status": self.status,
            "current_stage": self.current_stage,
            "requested_at": self.requested_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
        }