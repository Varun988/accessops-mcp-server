from datetime import datetime, timezone
from uuid import uuid4

from database.db_initializer import DatabaseInitializer
from repositories.sqlite_audit_repository import SQLiteAuditRepository


class AuditLogger:
    """Utility class for writing audit events."""

    audit_repository = SQLiteAuditRepository()

    @staticmethod
    def log_tool_call(
        tool_name: str,
        request_id: str,
        status: str,
        event_type: str = "MCP_TOOL_CALL",
        correlation_id: str | None = None,
    ) -> str:
        """
        Log an MCP tool call audit event.

        Args:
            tool_name (str): Name of the MCP tool.
            request_id (str): Access request ID or related entity ID.
            status (str): Execution status such as success or failure.
            event_type (str): Type of audit event.
            correlation_id (str | None): Optional correlation ID.

        Returns:
            str: Correlation ID used for this audit event.
        """
        DatabaseInitializer.initialize()

        correlation_id = correlation_id or str(uuid4())

        audit_event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "tool_name": tool_name,
            "request_id": request_id,
            "status": status,
            "correlation_id": correlation_id,
        }

        print(f"AUDIT_EVENT: {audit_event}")

        AuditLogger.audit_repository.save_audit_event(audit_event)

        return correlation_id