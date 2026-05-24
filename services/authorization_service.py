from data.mock_auth_data import ROLE_PERMISSIONS, USER_ROLES


class AuthorizationService:
    """Service layer for role-based access control checks."""

    @staticmethod
    def get_user_roles(user_id: str) -> list[str]:
        """
        Get roles assigned to a user.

        Args:
            user_id (str): User/operator ID

        Returns:
            list[str]: Assigned roles
        """
        return USER_ROLES.get(user_id, [])

    @staticmethod
    def get_permissions_for_user(user_id: str) -> set[str]:
        """
        Get effective permissions for a user based on assigned roles.

        Args:
            user_id (str): User/operator ID

        Returns:
            set[str]: Effective permission set
        """
        roles = AuthorizationService.get_user_roles(user_id)
        permissions = set()

        for role in roles:
            permissions.update(ROLE_PERMISSIONS.get(role, []))

        return permissions

    @staticmethod
    def has_permission(user_id: str, permission: str) -> bool:
        """
        Check whether a user has a specific permission.

        Args:
            user_id (str): User/operator ID
            permission (str): Required permission

        Returns:
            bool: True if allowed, False otherwise
        """
        return permission in AuthorizationService.get_permissions_for_user(user_id)

    @staticmethod
    def require_permission(user_id: str, permission: str) -> None:
        """
        Enforce that a user has a specific permission.

        Args:
            user_id (str): User/operator ID
            permission (str): Required permission

        Raises:
            PermissionError: If user does not have the required permission
        """
        if not AuthorizationService.has_permission(user_id, permission):
            raise PermissionError(
                f"User '{user_id}' does not have required permission '{permission}'."
            )