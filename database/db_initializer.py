from database.db_connection import DatabaseConnection


class DatabaseInitializer:
    """Initializes database tables required by AccessOps MCP Server."""

    @staticmethod
    def initialize() -> None:
        """
        Create required database tables if they do not already exist.
        """
        with DatabaseConnection.get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS audit_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    tool_name TEXT NOT NULL,
                    request_id TEXT,
                    status TEXT NOT NULL,
                    correlation_id TEXT NOT NULL
                )
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS retry_drafts (
                    retry_id TEXT PRIMARY KEY,
                    request_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    risk_level TEXT NOT NULL,
                    requires_confirmation INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    approved_by TEXT,
                    submitted_at TEXT
                )
                """
            )

            connection.commit()