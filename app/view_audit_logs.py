from database.db_initializer import DatabaseInitializer
from database.db_connection import DatabaseConnection


def view_audit_logs() -> None:
    """Print recent audit events from the SQLite database."""
    DatabaseInitializer.initialize()

    with DatabaseConnection.get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                timestamp,
                event_type,
                tool_name,
                request_id,
                status,
                correlation_id
            FROM audit_events
            ORDER BY id DESC
            LIMIT 20
            """
        )

        rows = cursor.fetchall()

        print("\n=== RECENT AUDIT EVENTS ===")

        if not rows:
            print("No audit events found.")
            return

        for row in rows:
            print(
                {
                    "id": row["id"],
                    "timestamp": row["timestamp"],
                    "event_type": row["event_type"],
                    "tool_name": row["tool_name"],
                    "request_id": row["request_id"],
                    "status": row["status"],
                    "correlation_id": row["correlation_id"],
                }
            )


if __name__ == "__main__":
    view_audit_logs()