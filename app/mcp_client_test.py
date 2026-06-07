import asyncio
import json

from config.app_config import AppConfig
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

def extract_tool_payload(tool_result) -> dict:
    """
    Extract JSON payload from an MCP tool result.

    The MCP SDK may return tool output either as structuredContent
    or as text content. This helper safely handles both cases.
    """
    if tool_result.structuredContent:
        return tool_result.structuredContent

    if tool_result.content and len(tool_result.content) > 0:
        first_content = tool_result.content[0]

        if hasattr(first_content, "text"):
            return json.loads(first_content.text)

    raise ValueError(f"Unable to extract payload from MCP tool result: {tool_result}")



async def main():
    server_url = AppConfig.MCP_SERVER_URL

    async with streamablehttp_client(server_url) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            print("=== AVAILABLE TOOLS ===")
            tools = await session.list_tools()
            print(tools)

            print("\n=== AVAILABLE RESOURCES ===")
            resources = await session.list_resources()
            print(resources)

            print("\n=== READ RESOURCE: policy://access/approval-rules ===")
            approval_policy = await session.read_resource(
                "policy://access/approval-rules"
            )
            print(approval_policy)

            print("\n=== READ RESOURCE: runbook://identity/provisioning-failure ===")
            runbook = await session.read_resource(
                "runbook://identity/provisioning-failure"
            )

            print("\n=== AVAILABLE PROMPTS ===")
            prompts = await session.list_prompts()
            print(prompts)

            print("\n=== GET PROMPT: troubleshoot_access_request ===")
            troubleshoot_prompt = await session.get_prompt(
                "troubleshoot_access_request",
                {
                    "request_id": "REQ-1001"
                }
            )
            print(troubleshoot_prompt)

            print("\n=== GET PROMPT: generate_requester_response ===")
            requester_prompt = await session.get_prompt(
                "generate_requester_response",
                {
                    "request_id": "REQ-1001"
                }
            )
            print(requester_prompt)

            print(runbook)
            print("\n=== CALL TOOL: get_access_request_status ===")
            result = await session.call_tool(
                "access_request_status",
                {
                    "request_id": "REQ-1001"
                }
            )
            print(result)

            print("\n=== CALL TOOL: diagnose_access_request ===")
            diagnosis = await session.call_tool(
                "diagnose_request",
                {
                    "request_id": "REQ-1001"
                }
            )
            print(diagnosis)

            print("\n=== CALL TOOL: access_request_status INVALID REQUEST ===")
            invalid_result = await session.call_tool(
                "access_request_status",
                {
                    "request_id": "REQ-9999"
                }
            )
            print(invalid_result)

            print("\n=== CALL TOOL: prepare_provisioning_retry VALID FAILED REQUEST ===")
            prepare_retry_result = await session.call_tool(
                "prepare_provisioning_retry",
                {
                    "request_id": "REQ-1003"
                }
            )
            print(prepare_retry_result)

            print("\n=== CALL TOOL: prepare_provisioning_retry NOT ALLOWED ===")
            prepare_retry_not_allowed = await session.call_tool(
                "prepare_provisioning_retry",
                {
                    "request_id": "REQ-1001"
                }
            )
            print(prepare_retry_not_allowed)

            print("\n=== CALL TOOL: submit_provisioning_retry_after_confirmation ===")

            prepare_retry_payload = extract_tool_payload(prepare_retry_result)

            if not prepare_retry_payload.get("success"):
                print("Cannot submit retry because prepare retry failed:")
                print(prepare_retry_payload)
            else:
                retry_id = prepare_retry_payload["data"]["retry_id"]

                submit_retry_result = await session.call_tool(
                    "submit_provisioning_retry_after_confirmation",
                    {
                        "retry_id": retry_id,
                        "approved_by": "varun.kumar"
                    }
                )
                print(submit_retry_result)

            print("\n=== CALL TOOL: submit_provisioning_retry_after_confirmation INVALID RETRY ===")
            invalid_submit_retry = await session.call_tool(
                "submit_provisioning_retry_after_confirmation",
                {
                    "retry_id": "RETRY-INVALID-001",
                    "approved_by": "varun.kumar"
                }
            )
            print(invalid_submit_retry)

            print("\n=== CALL TOOL: prepare_ticket_creation ===")
            prepare_ticket_result = await session.call_tool(
                "prepare_ticket_creation",
                {
                    "request_id": "REQ-1003",
                    "title": "MCP ticket creation test for REQ-1003",
                    "priority": "High",
                }
            )
            print(prepare_ticket_result)

            prepare_ticket_payload = extract_tool_payload(prepare_ticket_result)

            created_ticket_id = None

            if prepare_ticket_payload.get("success"):
                ticket_draft_id = prepare_ticket_payload["data"]["ticket_draft_id"]

                print("\n=== CALL TOOL: submit_ticket_creation_after_confirmation ===")
                submit_ticket_result = await session.call_tool(
                    "submit_ticket_creation_after_confirmation",
                    {
                        "ticket_draft_id": ticket_draft_id,
                        "approved_by": "varun.kumar",
                    }
                )
                print(submit_ticket_result)

                submit_ticket_payload = extract_tool_payload(submit_ticket_result)

                if submit_ticket_payload.get("success"):
                    created_ticket_id = submit_ticket_payload["data"]["ticket_id"]
            else:
                print("Skipping ticket submission because ticket preparation failed.")


            print("\n=== CALL TOOL: prepare_notification ===")
            prepare_notification_result = await session.call_tool(
                "prepare_notification",
                {
                    "request_id": "REQ-1003",
                    "recipient": "identity_ops_team",
                    "channel": "teams",
                    "subject": "MCP notification test",
                    "message": "Testing notification workflow through MCP client.",
                }
            )
            print(prepare_notification_result)

            prepare_notification_payload = extract_tool_payload(prepare_notification_result)

            if prepare_notification_payload.get("success"):
                notification_draft_id = prepare_notification_payload["data"]["notification_draft_id"]

                print("\n=== CALL TOOL: send_notification_after_confirmation ===")
                send_notification_result = await session.call_tool(
                    "send_notification_after_confirmation",
                    {
                        "notification_draft_id": notification_draft_id,
                        "approved_by": "varun.kumar",
                    }
                )
                print(send_notification_result)
            else:
                print("Skipping notification send because notification preparation failed.")


            print("\n=== CALL TOOL: prepare_ticket_closure ===")
            if created_ticket_id:
                prepare_closure_result = await session.call_tool(
                    "prepare_ticket_closure",
                    {
                        "ticket_id": created_ticket_id,
                        "closure_reason": "MCP test completed",
                        "resolution_summary": "Ticket was created and closed through MCP client test.",
                    }
                )
                print(prepare_closure_result)

                prepare_closure_payload = extract_tool_payload(prepare_closure_result)

                if prepare_closure_payload.get("success"):
                    closure_draft_id = prepare_closure_payload["data"]["closure_draft_id"]

                    print("\n=== CALL TOOL: submit_ticket_closure_after_confirmation ===")
                    submit_closure_result = await session.call_tool(
                        "submit_ticket_closure_after_confirmation",
                        {
                            "closure_draft_id": closure_draft_id,
                            "approved_by": "varun.kumar",
                        }
                    )
                    print(submit_closure_result)
            else:
                print("Skipping ticket closure because ticket creation failed.")


            print("\n=== CALL TOOL: submit_ticket_closure_after_confirmation UNAUTHORIZED ===")
            unauthorized_ticket_result = await session.call_tool(
                "prepare_ticket_creation",
                {
                    "request_id": "REQ-1002",
                    "title": "MCP unauthorized closure test",
                    "priority": "Low",
                }
            )
            print(unauthorized_ticket_result)

            unauthorized_ticket_payload = extract_tool_payload(unauthorized_ticket_result)

            if unauthorized_ticket_payload.get("success"):
                unauthorized_ticket_submit = await session.call_tool(
                    "submit_ticket_creation_after_confirmation",
                    {
                        "ticket_draft_id": unauthorized_ticket_payload["data"]["ticket_draft_id"],
                        "approved_by": "varun.kumar",
                    }
                )
                print(unauthorized_ticket_submit)

                unauthorized_ticket_submit_payload = extract_tool_payload(unauthorized_ticket_submit)

                if unauthorized_ticket_submit_payload.get("success"):
                    unauthorized_created_ticket_id = unauthorized_ticket_submit_payload["data"]["ticket_id"]

                    unauthorized_closure_prepare = await session.call_tool(
                        "prepare_ticket_closure",
                        {
                            "ticket_id": unauthorized_created_ticket_id,
                        }
                    )
                    print(unauthorized_closure_prepare)

                    unauthorized_closure_prepare_payload = extract_tool_payload(
                        unauthorized_closure_prepare
                    )

                    if unauthorized_closure_prepare_payload.get("success"):
                        unauthorized_closure_submit = await session.call_tool(
                            "submit_ticket_closure_after_confirmation",
                            {
                                "closure_draft_id": unauthorized_closure_prepare_payload["data"]["closure_draft_id"],
                                "approved_by": "readonly.user",
                            }
                        )
                        print(unauthorized_closure_submit)

if __name__ == "__main__":
    asyncio.run(main())