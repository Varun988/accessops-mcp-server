import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def main():
    server_url = "http://127.0.0.1:8000/mcp"

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


if __name__ == "__main__":
    asyncio.run(main())