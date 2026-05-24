# Mock role-to-permission mapping for AccessOps MCP Server

ROLE_PERMISSIONS = {
    "identity_operator": [
        "provisioning:retry",
        "notification:send",
    ],
    "support_engineer": [
        "ticket:create",
        "ticket:close",
        "notification:send",
    ],
    "access_manager": [
        "provisioning:retry",
        "ticket:create",
        "ticket:close",
        "notification:send",
    ],
    "admin": [
        "provisioning:retry",
        "ticket:create",
        "ticket:close",
        "notification:send",
        "access:approve",
        "access:revoke",
    ],
}


# Mock user-to-role mapping
USER_ROLES = {
    "varun.kumar": ["admin"],
    "identity.operator": ["identity_operator"],
    "support.engineer": ["support_engineer"],
    "access.manager": ["access_manager"],
    "readonly.user": [],
}