from tools.tool_registry import ToolRegistry


def print_section(title: str) -> None:
    """Print a formatted test section title."""
    print(f"\n=== {title} ===")


def run_test():
    registry = ToolRegistry()

    print_section("AVAILABLE TOOLS")
    tools = registry.list_tools()
    print(tools)

    print_section("TEST 1: VALID REQUEST")
    result1 = registry.execute_tool(
        "get_access_request_status",
        request_id="REQ-1001",
    )
    print(result1)

    print_section("TEST 2: INVALID REQUEST")
    result2 = registry.execute_tool(
        "get_access_request_status",
        request_id="REQ-9999",
    )
    print(result2)

    print_section("TEST 3: UNKNOWN TOOL")
    result3 = registry.execute_tool(
        "unknown_tool",
        request_id="REQ-1001",
    )
    print(result3)

    print_section("TEST 4: APPROVERS")
    result4 = registry.execute_tool(
        "get_pending_approvers",
        request_id="REQ-1001",
    )
    print(result4)

    print_section("TEST 5: DIAGNOSE REQUEST")
    result5 = registry.execute_tool(
        "diagnose_access_request",
        request_id="REQ-1001",
    )
    print(result5)

    print_section("TEST 6: PREPARE RETRY FOR FAILED REQUEST")
    result6 = registry.execute_tool(
        "prepare_provisioning_retry",
        request_id="REQ-1003",
    )
    print(result6)

    retry_id = None
    if result6.get("success"):
        retry_id = result6["data"]["retry_id"]

    print_section("TEST 7: SUBMIT RETRY AFTER CONFIRMATION")
    if retry_id:
        result7 = registry.execute_tool(
            "submit_provisioning_retry_after_confirmation",
            retry_id=retry_id,
            approved_by="varun.kumar",
        )
        print(result7)
    else:
        print("Skipping submit because retry preparation failed.")

    print_section("TEST 7A: SUBMIT SAME RETRY AGAIN")
    if retry_id:
        result7a = registry.execute_tool(
            "submit_provisioning_retry_after_confirmation",
            retry_id=retry_id,
            approved_by="varun.kumar",
        )
        print(result7a)
    else:
        print("Skipping duplicate submit because retry preparation failed.")

    print_section("TEST 8: RETRY NOT ALLOWED FOR NON-FAILED REQUEST")
    result8 = registry.execute_tool(
        "prepare_provisioning_retry",
        request_id="REQ-1001",
    )
    print(result8)

    print_section("TEST 9: SUBMIT NON-EXISTING RETRY DRAFT")
    result9 = registry.execute_tool(
        "submit_provisioning_retry_after_confirmation",
        retry_id="RETRY-9999",
        approved_by="varun.kumar",
    )
    print(result9)


if __name__ == "__main__":
    run_test()