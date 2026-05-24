import sqlite3
from config.app_config import AppConfig


class DatabaseConnection:
    """Utility class for creating SQLite database connections."""

    @staticmethod
    def get_connection() -> sqlite3.Connection:
        """
        Create and return a SQLite database connection.

        Returns:
            sqlite3.Connection: SQLite database connection
        """
        connection = sqlite3.connect(AppConfig.DATABASE_PATH)
        connection.row_factory = sqlite3.Row
        return connection