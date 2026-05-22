from tools.access_request_tool import (
    get_access_request_status,
    TOOL_METADATA as ACCESS_REQUEST_TOOL_METADATA,
    get_pending_approvers,
    PENDING_APPROVERS_TOOL_METADATA,
    diagnose_access_request,
    DIAGNOSE_TOOL_METADATA
)



class ToolRegistry:
    """Registry to manage all MCP tools"""

    def __init__(self):
        self.tools = {}

        # Register tools here
        self.register_tool(

            DIAGNOSE_TOOL_METADATA["name"],
            diagnose_access_request,
            DIAGNOSE_TOOL_METADATA

        )

    def register_tool(self, name: str, function, metadata: dict):
        self.tools[name] = {
            "function": function,
            "metadata": metadata
        }

    def list_tools(self):
        """Simulates ListToolsRequest"""
        return [tool["metadata"] for tool in self.tools.values()]

    def execute_tool(self, name: str, **kwargs):
        """Simulates CallToolRequest"""
        tool = self.tools.get(name)

        if not tool:
            return {
                "success": False,
                "error": f"Tool '{name}' not found"
            }

        return tool["function"](**kwargs)