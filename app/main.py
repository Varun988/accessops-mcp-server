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

    print_section("TEST 10: PREPARE TICKET CREATION")
    result10 = registry.execute_tool(
        "prepare_ticket_creation",
        request_id="REQ-1003",
        title="Access provisioning failure for REQ-1003",
        priority="High",
    )
    print(result10)

    ticket_draft_id = None
    if result10.get("success"):
        ticket_draft_id = result10["data"]["ticket_draft_id"]

    print_section("TEST 11: SUBMIT TICKET AFTER CONFIRMATION")
    if ticket_draft_id:
        result11 = registry.execute_tool(
            "submit_ticket_creation_after_confirmation",
            ticket_draft_id=ticket_draft_id,
            approved_by="varun.kumar",
        )
        print(result11)
    else:
        print("Skipping ticket submission because ticket draft creation failed.")

    print_section("TEST 11A: SUBMIT SAME TICKET DRAFT AGAIN")
    if ticket_draft_id:
        result11a = registry.execute_tool(
            "submit_ticket_creation_after_confirmation",
            ticket_draft_id=ticket_draft_id,
            approved_by="varun.kumar",
        )
        print(result11a)
    else:
        print("Skipping duplicate ticket submission because ticket draft creation failed.")

    print_section("TEST 12: PREPARE TICKET FOR INVALID REQUEST")
    result12 = registry.execute_tool(
        "prepare_ticket_creation",
        request_id="REQ-9999",
        title="Invalid request ticket",
        priority="Medium",
    )
    print(result12)

    print_section("TEST 13: SUBMIT NON-EXISTING TICKET DRAFT")
    result13 = registry.execute_tool(
        "submit_ticket_creation_after_confirmation",
        ticket_draft_id="TICKET-DRAFT-9999",
        approved_by="varun.kumar",
    )
    print(result13)

    print_section("TEST 14: SUBMIT TICKET WITHOUT APPROVAL")
    result14_prepare = registry.execute_tool(
        "prepare_ticket_creation",
        request_id="REQ-1002",
    )
    print(result14_prepare)

    if result14_prepare.get("success"):
        approval_test_draft_id = result14_prepare["data"]["ticket_draft_id"]

        result14 = registry.execute_tool(
            "submit_ticket_creation_after_confirmation",
            ticket_draft_id=approval_test_draft_id,
            approved_by="",
        )
        print(result14)
    else:
        print("Skipping approval-required test because ticket draft creation failed.")


    print_section("TEST 15: PREPARE NOTIFICATION")
    result15 = registry.execute_tool(
        "prepare_notification",
        request_id="REQ-1003",
        recipient="identity_ops_team",
        channel="teams",
        subject="Provisioning failure requires attention",
        message="Access request REQ-1003 failed during provisioning. Please review and take necessary action.",
    )
    print(result15)

    notification_draft_id = None
    if result15.get("success"):
        notification_draft_id = result15["data"]["notification_draft_id"]

    print_section("TEST 16: SEND NOTIFICATION AFTER CONFIRMATION")
    if notification_draft_id:
        result16 = registry.execute_tool(
            "send_notification_after_confirmation",
            notification_draft_id=notification_draft_id,
            approved_by="varun.kumar",
        )
        print(result16)
    else:
        print("Skipping notification send because notification draft preparation failed.")

    print_section("TEST 16A: SEND SAME NOTIFICATION AGAIN")
    if notification_draft_id:
        result16a = registry.execute_tool(
            "send_notification_after_confirmation",
            notification_draft_id=notification_draft_id,
            approved_by="varun.kumar",
        )
        print(result16a)
    else:
        print("Skipping duplicate notification send because notification draft preparation failed.")

    print_section("TEST 17: PREPARE NOTIFICATION FOR INVALID REQUEST")
    result17 = registry.execute_tool(
        "prepare_notification",
        request_id="REQ-9999",
        recipient="identity_ops_team",
        channel="email",
    )
    print(result17)

    print_section("TEST 18: SEND NON-EXISTING NOTIFICATION DRAFT")
    result18 = registry.execute_tool(
        "send_notification_after_confirmation",
        notification_draft_id="NOTIFICATION-DRAFT-9999",
        approved_by="varun.kumar",
    )
    print(result18)

    print_section("TEST 19: SEND NOTIFICATION WITHOUT APPROVAL")
    result19_prepare = registry.execute_tool(
        "prepare_notification",
        request_id="REQ-1001",
    )
    print(result19_prepare)

    if result19_prepare.get("success"):
        approval_test_notification_id = result19_prepare["data"]["notification_draft_id"]

        result19 = registry.execute_tool(
            "send_notification_after_confirmation",
            notification_draft_id=approval_test_notification_id,
            approved_by="",
        )
        print(result19)
    else:
        print("Skipping notification approval-required test because draft preparation failed.")

if __name__ == "__main__":
    run_test()