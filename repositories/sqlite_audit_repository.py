from database.db_connection import DatabaseConnection
from repositories.audit_repository import AuditRepository


class SQLiteAuditRepository(AuditRepository):
    """SQLite implementation of audit event persistence."""

    def save_audit_event(self, audit_event: dict) -> None:
        """
        Save an audit event to the SQLite database.

        Args:
            audit_event (dict): Audit event data
        """
        with DatabaseConnection.get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO audit_events (
                    timestamp,
                    event_type,
                    tool_name,
                    request_id,
                    status,
                    correlation_id
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    audit_event["timestamp"],
                    audit_event["event_type"],
                    audit_event["tool_name"],
                    audit_event.get("request_id"),
                    audit_event["status"],
                    audit_event["correlation_id"],
                ),
            )

            connection.commit()