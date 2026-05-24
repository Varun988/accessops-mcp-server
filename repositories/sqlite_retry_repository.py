from datetime import datetime

from database.db_connection import DatabaseConnection
from models.retry_model import ProvisioningRetryDraft
from repositories.retry_repository import RetryRepository


class SQLiteRetryRepository(RetryRepository):
    """SQLite implementation of provisioning retry draft persistence."""

    def save_retry_draft(self, retry_draft: ProvisioningRetryDraft) -> None:
        """
        Save a provisioning retry draft to SQLite.

        Args:
            retry_draft (ProvisioningRetryDraft): Retry draft to persist
        """
        with DatabaseConnection.get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO retry_drafts (
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
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    retry_draft.retry_id,
                    retry_draft.request_id,
                    retry_draft.action,
                    retry_draft.risk_level,
                    1 if retry_draft.requires_confirmation else 0,
                    retry_draft.status,
                    retry_draft.summary,
                    retry_draft.created_at.isoformat(),
                    retry_draft.approved_by,
                    retry_draft.submitted_at.isoformat()
                    if retry_draft.submitted_at
                    else None,
                ),
            )

            connection.commit()

    def get_retry_draft_by_id(self, retry_id: str) -> ProvisioningRetryDraft | None:
        """
        Fetch a provisioning retry draft by retry ID.

        Args:
            retry_id (str): Retry draft ID

        Returns:
            ProvisioningRetryDraft | None: Matching retry draft if found
        """
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
                WHERE retry_id = ?
                """,
                (retry_id,),
            )

            row = cursor.fetchone()

            if not row:
                return None

            return self._row_to_retry_draft(row)

    def update_retry_draft(self, retry_draft: ProvisioningRetryDraft) -> None:
        """
        Update an existing provisioning retry draft in SQLite.

        Args:
            retry_draft (ProvisioningRetryDraft): Retry draft to update
        """
        with DatabaseConnection.get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE retry_drafts
                SET
                    request_id = ?,
                    action = ?,
                    risk_level = ?,
                    requires_confirmation = ?,
                    status = ?,
                    summary = ?,
                    created_at = ?,
                    approved_by = ?,
                    submitted_at = ?
                WHERE retry_id = ?
                """,
                (
                    retry_draft.request_id,
                    retry_draft.action,
                    retry_draft.risk_level,
                    1 if retry_draft.requires_confirmation else 0,
                    retry_draft.status,
                    retry_draft.summary,
                    retry_draft.created_at.isoformat(),
                    retry_draft.approved_by,
                    retry_draft.submitted_at.isoformat()
                    if retry_draft.submitted_at
                    else None,
                    retry_draft.retry_id,
                ),
            )

            connection.commit()

    @staticmethod
    def _row_to_retry_draft(row) -> ProvisioningRetryDraft:
        """
        Convert a SQLite row into a ProvisioningRetryDraft model.

        Args:
            row: SQLite row

        Returns:
            ProvisioningRetryDraft: Retry draft model
        """
        return ProvisioningRetryDraft(
            retry_id=row["retry_id"],
            request_id=row["request_id"],
            action=row["action"],
            risk_level=row["risk_level"],
            requires_confirmation=bool(row["requires_confirmation"]),
            status=row["status"],
            summary=row["summary"],
            created_at=datetime.fromisoformat(row["created_at"]),
            approved_by=row["approved_by"],
            submitted_at=(
                datetime.fromisoformat(row["submitted_at"])
                if row["submitted_at"]
                else None
            ),
        )