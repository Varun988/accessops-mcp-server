# AccessOps MCP Server

AccessOps MCP Server is a production-style Model Context Protocol (MCP) server for enterprise access request troubleshooting.

It exposes MCP tools, resources, and prompts that allow AI assistants to safely retrieve access request status, identify pending approvers, diagnose stuck requests, read policy/runbook context, and follow standardized troubleshooting workflows.

## Project Purpose

Enterprise support and identity operations teams often spend time investigating why access requests are pending, delayed, or failed.

This project demonstrates how MCP can provide an AI assistant with structured, safe, and auditable access to enterprise access-operation capabilities.

## Key Features

- Real MCP server implementation using Python
- Streamable HTTP transport
- MCP tool discovery and invocation
- MCP resource discovery and reading
- MCP prompt discovery and retrieval
- Modular architecture with models, services, tools, and data layers
- Mock enterprise data layer designed to be replaceable with real systems
- Composite diagnostic tool for access request troubleshooting
- Clean separation between MCP wrapper and business logic

## MCP Capabilities

### Tools

The server exposes the following MCP tools:

- `access_request_status`
  - Retrieves status and details of an access request.

- `pending_approvers`
  - Returns users or teams currently responsible for approving the request.

- `diagnose_request`
  - Provides a business-level diagnosis for pending, in-progress, or failed access requests.

### Resources

The server exposes the following MCP resources:

- `policy://access/approval-rules`
  - Access approval policy rules.

- `runbook://identity/provisioning-failure`
  - Troubleshooting runbook for provisioning failures.

- `schema://access-request/status-codes`
  - Reference for access request status meanings.

### Prompts

The server exposes the following MCP prompts:

- `troubleshoot_access_request`
  - Standard workflow for diagnosing access request issues.

- `generate_requester_response`
  - Template for drafting a requester-facing response.

- `prepare_support_summary`
  - Template for creating an operations/support summary.

## Architecture

```text
MCP Client
   ↓
Streamable HTTP Transport
   ↓
AccessOps MCP Server
   ├── MCP Tool Wrappers
   ├── MCP Resource Wrappers
   ├── MCP Prompt Wrappers
   ↓
Internal Tool Layer
   ↓
Service Layer
   ↓
Model Layer
   ↓
Mock Enterprise Data Layer
```

## Project Structure

```text
accessops-mcp-server/
├── app/
│   ├── main.py
│   ├── mcp_server.py
│   └── mcp_client_test.py
├── data/
│   ├── mock_data.py
│   └── resource_data.py
├── models/
│   └── request_model.py
├── services/
│   ├── request_service.py
│   ├── resource_service.py
│   └── prompt_service.py
├── tools/
│   ├── access_request_tool.py
│   └── tool_registry.py
├── README.md
└── .gitignore
```

## Setup

Install dependencies:

```bash
pip install mcp
```

## Run the MCP Server

Start the MCP server:

```bash
python -m app.mcp_server
```

The server runs using Streamable HTTP transport.

Default endpoint:

```text
http://127.0.0.1:8000/mcp
```

## Run MCP Client Test

In another terminal, run:

```bash
python -m app.mcp_client_test
```

The client test validates:

- Tool discovery
- Tool invocation
- Resource discovery
- Resource reading
- Prompt discovery
- Prompt retrieval

## Example Tool Call

Tool:

```text
access_request_status
```

Input:

```json
{
  "request_id": "REQ-1001"
}
```

Example response:

```json
{
  "success": true,
  "data": {
    "request_id": "REQ-1001",
    "requester": "varun.kumar",
    "target_system": "SAP_FINANCE",
    "role": "FIN_DISPLAY",
    "status": "Pending",
    "current_stage": "Manager Approval"
  }
}
```

## Production Design Direction

The current version uses mock data for learning and demonstration.

The architecture is designed so the mock layer can later be replaced with:

- SAP IDM or IGA platform APIs
- ServiceNow or Jira workflows
- PostgreSQL or enterprise databases
- Splunk or Elasticsearch logs
- SharePoint, Confluence, or Git-based knowledge repositories

Planned production enhancements:

- Repository abstraction layer
- Structured error model
- Audit logging
- Role-based authorization
- Human-in-the-loop approval actions
- Safe write-action tools
- Observability and metrics
- Deployment on SAP BTP or cloud platform

## Interview Explanation

AccessOps MCP Server demonstrates how MCP can connect AI assistants to enterprise access management workflows.

The project exposes domain-specific tools, resources, and prompts rather than generic backend APIs. This allows an AI assistant to safely discover capabilities, retrieve structured access request data, read policy context, follow approved troubleshooting workflows, and produce consistent support responses.

The architecture separates MCP protocol concerns from business logic using tool wrappers, services, models, and data layers. This makes the project easier to test, maintain, and extend toward real enterprise integrations.

## Status

Current version:

```text
MCP tools: complete
MCP resources: complete
MCP prompts: complete
Real MCP client-server test: complete
Production hardening: in progress
```
