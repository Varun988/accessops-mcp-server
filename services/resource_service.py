from data.resource_data import (
    ACCESS_APPROVAL_RULES,
    PROVISIONING_FAILURE_RUNBOOK,
    ACCESS_STATUS_CODES,
)


class ResourceService:
    """Service layer for managing MCP resource content."""

    RESOURCE_MAP = {
        "policy://access/approval-rules": ACCESS_APPROVAL_RULES,
        "runbook://identity/provisioning-failure": PROVISIONING_FAILURE_RUNBOOK,
        "schema://access-request/status-codes": ACCESS_STATUS_CODES,
    }

    @classmethod
    def get_resource(cls, uri: str) -> str:
        """
        Retrieve resource content by URI.

        Args:
            uri (str): Resource URI

        Returns:
            str: Resource content

        Raises:
            ValueError: If resource URI is not found
        """
        resource = cls.RESOURCE_MAP.get(uri)

        if not resource:
            raise ValueError(f"Resource '{uri}' not found")

        return resource