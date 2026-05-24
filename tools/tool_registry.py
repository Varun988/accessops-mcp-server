from tools.access_request_tool import (
    get_access_request_status,
    TOOL_METADATA as ACCESS_REQUEST_TOOL_METADATA,
    get_pending_approvers,
    PENDING_APPROVERS_TOOL_METADATA,
    diagnose_access_request,
    DIAGNOSE_TOOL_METADATA,
)

from tools.retry_tool import (
    prepare_provisioning_retry,
    PREPARE_PROVISIONING_RETRY_METADATA,
    submit_provisioning_retry_after_confirmation,
    SUBMIT_PROVISIONING_RETRY_METADATA,
)

from tools.ticket_tool import (
    prepare_ticket_creation,
    PREPARE_TICKET_CREATION_METADATA,
    submit_ticket_creation_after_confirmation,
    SUBMIT_TICKET_CREATION_METADATA,
    prepare_ticket_closure,
    PREPARE_TICKET_CLOSURE_METADATA,
    submit_ticket_closure_after_confirmation,
    SUBMIT_TICKET_CLOSURE_METADATA,
)

from tools.access_request_tool import (
    get_access_request_status,
    TOOL_METADATA as ACCESS_REQUEST_TOOL_METADATA,
    get_pending_approvers,
    PENDING_APPROVERS_TOOL_METADATA,
    diagnose_access_request,
    DIAGNOSE_TOOL_METADATA,
)

from tools.retry_tool import (
    prepare_provisioning_retry,
    PREPARE_PROVISIONING_RETRY_METADATA,
    submit_provisioning_retry_after_confirmation,
    SUBMIT_PROVISIONING_RETRY_METADATA,
)

from tools.ticket_tool import (
    prepare_ticket_creation,
    PREPARE_TICKET_CREATION_METADATA,
    submit_ticket_creation_after_confirmation,
    SUBMIT_TICKET_CREATION_METADATA,
)

from tools.notification_tool import (
    prepare_notification,
    PREPARE_NOTIFICATION_METADATA,
    send_notification_after_confirmation,
    SEND_NOTIFICATION_METADATA,
)

class ToolRegistry:
    """Registry to manage all MCP tools."""

    def __init__(self):
        self.tools = {}

        self.register_tool(
            ACCESS_REQUEST_TOOL_METADATA["name"],
            get_access_request_status,
            ACCESS_REQUEST_TOOL_METADATA,
        )

        self.register_tool(
            PENDING_APPROVERS_TOOL_METADATA["name"],
            get_pending_approvers,
            PENDING_APPROVERS_TOOL_METADATA,
        )

        self.register_tool(
            DIAGNOSE_TOOL_METADATA["name"],
            diagnose_access_request,
            DIAGNOSE_TOOL_METADATA,
        )

        self.register_tool(
            PREPARE_PROVISIONING_RETRY_METADATA["name"],
            prepare_provisioning_retry,
            PREPARE_PROVISIONING_RETRY_METADATA,
        )

        self.register_tool(
            SUBMIT_PROVISIONING_RETRY_METADATA["name"],
            submit_provisioning_retry_after_confirmation,
            SUBMIT_PROVISIONING_RETRY_METADATA,
        )

        self.register_tool(
            PREPARE_TICKET_CREATION_METADATA["name"],
            prepare_ticket_creation,
            PREPARE_TICKET_CREATION_METADATA,
        )

        self.register_tool(
            SUBMIT_TICKET_CREATION_METADATA["name"],
            submit_ticket_creation_after_confirmation,
            SUBMIT_TICKET_CREATION_METADATA,
        )

        self.register_tool(
            PREPARE_NOTIFICATION_METADATA["name"],
            prepare_notification,
            PREPARE_NOTIFICATION_METADATA,
        )

        self.register_tool(
            SEND_NOTIFICATION_METADATA["name"],
            send_notification_after_confirmation,
            SEND_NOTIFICATION_METADATA,
        )

        self.register_tool(
            PREPARE_TICKET_CLOSURE_METADATA["name"],
            prepare_ticket_closure,
            PREPARE_TICKET_CLOSURE_METADATA,
        )

        self.register_tool(
            SUBMIT_TICKET_CLOSURE_METADATA["name"],
            submit_ticket_closure_after_confirmation,
            SUBMIT_TICKET_CLOSURE_METADATA,
        )


    def register_tool(self, name: str, function, metadata: dict) -> None:
        self.tools[name] = {
            "function": function,
            "metadata": metadata,
        }

    def list_tools(self) -> list[dict]:
        """Simulates ListToolsRequest."""
        return [tool["metadata"] for tool in self.tools.values()]

    def execute_tool(self, name: str, **kwargs) -> dict:
        """Simulates CallToolRequest."""
        tool = self.tools.get(name)

        if not tool:
            return {
                "success": False,
                "error": f"Tool '{name}' not found",
            }

        return tool["function"](**kwargs)