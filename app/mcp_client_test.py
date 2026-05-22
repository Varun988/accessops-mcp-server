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


if __name__ == "__main__":
    asyncio.run(main())