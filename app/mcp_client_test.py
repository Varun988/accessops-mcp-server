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


if __name__ == "__main__":
    asyncio.run(main())