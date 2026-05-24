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