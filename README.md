# AccessOps MCP Server

AccessOps MCP Server is a production-style Model Context Protocol (MCP) server for enterprise access request troubleshooting.

It exposes MCP tools, resources, and prompts that allow AI assistants to safely retrieve access request status, identify pending approvers, diagnose stuck requests, read policy/runbook context, follow standardized troubleshooting workflows, and execute sensitive actions only through human-approved workflows.

## Project Purpose

Enterprise support and identity operations teams often spend significant time investigating why access requests are pending, delayed, or failed.

This project demonstrates how MCP can provide an AI assistant with structured, safe, auditable, and extensible access to enterprise access-operation capabilities.

The project is designed as a resume-worthy, production-oriented MCP implementation with modular architecture, repository abstraction, structured error handling, audit logging, and human-in-the-loop action controls.

## Key Features

- Real MCP server implementation using Python
- Streamable HTTP transport
- MCP tool discovery and invocation
- MCP resource discovery and reading
- MCP prompt discovery and retrieval
- Modular architecture with MCP wrapper, tool, service, repository, model, utility, and data layers
- Repository abstraction pattern for replacing mock data with real enterprise systems
- Composite diagnostic tool for access request troubleshooting
- Structured error model with error codes, retryability, and suggested actions
- Audit logging with correlation IDs for tool execution traceability
- Human-in-the-loop provisioning retry workflow for safe action execution
- Clean separation between MCP protocol layer and business logic

## MCP Capabilities

### Tools

The server exposes the following MCP tools:

- `access_request_status`
  - Retrieves status and details of an access request.

- `pending_approvers`
  - Returns users or teams currently responsible for approving the request.

- `diagnose_request`
  - Provides a business-level diagnosis for pending, in-progress, or failed access requests.

- `prepare_provisioning_retry`
  - Creates a retry draft for a failed provisioning request.
  - Does not execute the retry.
  - Marks the action as requiring human confirmation.

- `submit_provisioning_retry_after_confirmation`
  - Submits a prepared provisioning retry only after explicit human/operator approval.
  - Requires a valid `retry_id` and `approved_by` value.
  - Emits audit logs for action traceability.

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

## Human-in-the-loop Action Workflow

The server supports a safe two-step action pattern for provisioning retry.

### 1. Prepare Retry

Tool:

```text
prepare_provisioning_retry
```

This tool:

- Validates that the access request is in `Failed` status.
- Creates a retry draft.
- Marks the draft as requiring confirmation.
- Does not execute the provisioning retry.
- Returns a `retry_id` for the next step.

Example output:

```json
{
  "success": true,
  "data": {
    "retry_id": "RETRY-REQ-1003-abc12345",
    "request_id": "REQ-1003",
    "action": "Retry provisioning",
    "risk_level": "Medium",
    "requires_confirmation": true,
    "status": "Prepared",
    "summary": "Provisioning retry prepared for access request REQ-1003. User confirmation is required before execution."
  }
}
```

### 2. Submit Retry After Confirmation

Tool:

```text
submit_provisioning_retry_after_confirmation
```

This tool:

- Requires a valid `retry_id`.
- Requires an `approved_by` value.
- Submits the retry only after explicit approval.
- Updates the retry draft status to `Submitted`.
- Emits an audit event.

Example input:

```json
{
  "retry_id": "RETRY-REQ-1003-abc12345",
  "approved_by": "operator.user"
}
```

Example output:

```json
{
  "success": true,
  "data": {
    "retry_id": "RETRY-REQ-1003-abc12345",
    "request_id": "REQ-1003",
    "action": "Retry provisioning",
    "status": "Submitted",
    "approved_by": "operator.user",
    "message": "Provisioning retry for request REQ-1003 has been submitted after approval by operator.user."
  }
}
```

This pattern prevents autonomous execution of sensitive actions and demonstrates enterprise-safe AI automation.

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
Repository Interface
   ↓
Repository Implementation
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
│   ├── error_model.py
│   ├── request_model.py
│   └── retry_model.py
├── repositories/
│   ├── request_repository.py
│   └── mock_request_repository.py
├── services/
│   ├── prompt_service.py
│   ├── request_service.py
│   ├── resource_service.py
│   └── retry_service.py
├── tools/
│   ├── access_request_tool.py
│   ├── retry_tool.py
│   └── tool_registry.py
├── utils/
│   ├── audit_logger.py
│   └── error_utils.py
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
- Structured error responses
- Human-in-the-loop retry preparation
- Human-approved retry submission

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

## Structured Error Example

Invalid request input returns a structured error response:

```json
{
  "success": false,
  "error": {
    "code": "ACCESS_REQUEST_NOT_FOUND",
    "message": "Access request 'REQ-9999' was not found.",
    "retryable": false,
    "suggested_action": "Verify the request ID and try again."
  }
}
```

Retry-specific errors include:

- `RETRY_NOT_ALLOWED`
- `RETRY_DRAFT_NOT_FOUND`
- `APPROVAL_REQUIRED`

## Audit Logging

The server emits audit events for MCP tool execution.

Example audit event:

```json
{
  "timestamp": "2026-05-22T18:30:00Z",
  "event_type": "MCP_TOOL_CALL",
  "tool_name": "access_request_status",
  "request_id": "REQ-1001",
  "status": "success",
  "correlation_id": "generated-correlation-id"
}
```

Audit logging currently prints events to the server console. The design can later be extended to centralized logging systems such as Splunk, ELK, SAP BTP logging, Azure Application Insights, or cloud-native observability platforms.

## Production Design Direction

The current version uses mock data for learning and demonstration.

The architecture is designed so the mock layer can later be replaced with:

- SAP IDM or IGA platform APIs
- ServiceNow or Jira workflows
- PostgreSQL or enterprise databases
- Splunk or Elasticsearch logs
- SharePoint, Confluence, or Git-based knowledge repositories
- SAP BTP Destination service or enterprise API gateway

Planned production enhancements:

- Authentication and authorization
- Role-based access control
- Persistent retry draft storage
- Centralized audit logging
- Request tracing and observability metrics
- Rate limiting and timeout handling
- Deployment on SAP BTP or cloud platform
- Integration with real access management and workflow systems


## Status

Current version:

```text
MCP tools: complete
MCP resources: complete
MCP prompts: complete
Real MCP client-server test: complete
Repository abstraction: complete
Structured error model: complete
Audit logging: complete
Human-in-the-loop retry workflow: complete
Production hardening: in progress
```
