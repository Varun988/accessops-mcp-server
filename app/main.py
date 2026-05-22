from tools.tool_registry import ToolRegistry


def run_test():
    registry = ToolRegistry()

    print("=== AVAILABLE TOOLS ===")
    tools = registry.list_tools()
    print(tools)

    print("\n=== TEST 1: VALID REQUEST ===")
    result1 = registry.execute_tool(
        "get_access_request_status",
        request_id="REQ-1001"
    )
    print(result1)

    print("\n=== TEST 2: INVALID REQUEST ===")
    result2 = registry.execute_tool(
        "get_access_request_status",
        request_id="REQ-9999"
    )
    print(result2)

    print("\n=== TEST 3: UNKNOWN TOOL ===")
    result3 = registry.execute_tool(
        "unknown_tool",
        request_id="REQ-1001"
    )
    print(result3)

    print("\n=== TEST 4: APPROVERS ===")
    result4 = registry.execute_tool(
        "get_pending_approvers",
        request_id="REQ-1001"
    )
    print(result4)

    print("\n=== TEST 5: DIAGNOSE REQUEST ===")
    result5 = registry.execute_tool(
        "diagnose_access_request",
        request_id="REQ-1001"
    )
    print(result5)    

if __name__ == "__main__":
    run_test()
