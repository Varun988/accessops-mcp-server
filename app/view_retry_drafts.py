from database.db_initializer import DatabaseInitializer
from database.db_connection import DatabaseConnection


def view_retry_drafts() -> None:
    """Print recent retry drafts from the SQLite database."""
    DatabaseInitializer.initialize()

    with DatabaseConnection.get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                retry_id,
                request_id,
                action,
                risk_level,
                requires_confirmation,
                status,
                summary,
                created_at,
                approved_by,
                submitted_at
            FROM retry_drafts
            ORDER BY created_at DESC
            LIMIT 20
            """
        )

        rows = cursor.fetchall()

        print("\n=== RECENT RETRY DRAFTS ===")

        if not rows:
            print("No retry drafts found.")
            return

        for row in rows:
            print(
                {
                    "retry_id": row["retry_id"],
                    "request_id": row["request_id"],
                    "action": row["action"],
                    "risk_level": row["risk_level"],
                    "requires_confirmation": bool(row["requires_confirmation"]),
                    "status": row["status"],
                    "summary": row["summary"],
                    "created_at": row["created_at"],
                    "approved_by": row["approved_by"],
                    "submitted_at": row["submitted_at"],
                }
            )


if __name__ == "__main__":
    view_retry_drafts()
    