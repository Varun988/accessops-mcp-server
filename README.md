# AccessOps MCP Server

A production-style **Model Context Protocol (MCP)** server for enterprise access request troubleshooting, approval analysis, operational runbooks, and safe human-approved write actions.

AccessOps MCP Server demonstrates how an AI assistant can securely interact with enterprise access-management workflows by using MCP tools, resources, and prompts. The project is intentionally designed as a beginner-friendly learning project and a resume-worthy implementation that shows real-world architecture patterns such as layered design, repository abstraction, structured errors, audit logging, and human-in-the-loop action control.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Why This Project Exists](#why-this-project-exists)
3. [What Is MCP?](#what-is-mcp)
4. [What This Project Demonstrates](#what-this-project-demonstrates)
5. [Real-World Use Case](#real-world-use-case)
6. [Current Capabilities](#current-capabilities)
7. [How the System Works](#how-the-system-works)
8. [Architecture](#architecture)
9. [Project Structure](#project-structure)
10. [Core Design Principles](#core-design-principles)
11. [MCP Tools](#mcp-tools)
12. [MCP Resources](#mcp-resources)
13. [MCP Prompts](#mcp-prompts)
14. [Human-in-the-Loop Write Workflow](#human-in-the-loop-write-workflow)
15. [Structured Error Handling](#structured-error-handling)
16. [Audit Logging](#audit-logging)
17. [Mock Data and Enterprise Replacement Strategy](#mock-data-and-enterprise-replacement-strategy)
18. [Setup Instructions](#setup-instructions)
19. [Running the Project](#running-the-project)
20. [Testing the MCP-Style Tool Registry](#testing-the-mcp-style-tool-registry)
21. [Running the Real MCP Server](#running-the-real-mcp-server)
22. [Running the MCP Client Test](#running-the-mcp-client-test)
23. [Example Outputs](#example-outputs)
24. [How This Project Was Developed](#how-this-project-was-developed)
25. [How to Extend This Project](#how-to-extend-this-project)
26. [Production Readiness Roadmap](#production-readiness-roadmap)
27. [Interview Explanation](#interview-explanation)
28. [Current Status](#current-status)

---

## Project Overview

**AccessOps MCP Server** is a Python-based MCP server that exposes access-operations capabilities to AI assistants.

The project focuses on a realistic enterprise problem:

> Users submit access requests, but those requests may get stuck in approval, fail during provisioning, or require manual operational follow-up.

This MCP server gives an AI assistant controlled access to:

- Access request status
- Pending approvers
- Request diagnosis
- Access approval policies
- Provisioning failure runbooks
- Standard troubleshooting prompts
- Safe write actions such as preparing and submitting a provisioning retry after human confirmation

The project currently uses mock enterprise data, but the architecture is designed so the mock layer can later be replaced with real enterprise systems such as identity governance platforms, workflow APIs, ticketing systems, databases, and logging platforms.

---

## Why This Project Exists

Enterprise identity and access-management teams often face questions such as:

```text
Why is my access request still pending?
Who needs to approve this request?
Did provisioning fail?
Can this failed provisioning step be retried?
What should I tell the requester?
What policy applies to this access request?
```

Without AI assistance, support engineers usually need to check multiple systems:

```text
Access request system
Approval workflow system
Provisioning logs
Policy documents
Runbooks
Ticketing systems
Audit logs
```

AccessOps MCP Server demonstrates how MCP can connect an AI assistant to those systems in a safe, structured, auditable, and extensible way.

---

## What Is MCP?

**MCP**, or **Model Context Protocol**, is a protocol that allows AI applications to connect with external tools, data sources, and workflows in a standardized way.

A simple mental model is:

```text
AI Assistant / MCP Host
        ↓
MCP Client
        ↓
MCP Server
        ↓
Enterprise System / API / Database / Files / Tools
```

In this project:

```text
AI Assistant
        ↓
MCP Client
        ↓
AccessOps MCP Server
        ↓
Access request data, approval data, retry workflow, policies, runbooks
```

MCP servers expose three important types of capabilities:

| MCP Primitive | Meaning | Example in This Project |
|---|---|---|
| Tools | Functions/actions the AI can call | Get request status, diagnose request, prepare retry |
| Resources | Read-only context the AI can read | Access policy, provisioning runbook, status code schema |
| Prompts | Reusable workflow templates | Troubleshoot access request, generate requester response |

---

## What This Project Demonstrates

This project demonstrates both MCP concepts and production-style backend design.

Key learning areas:

- MCP server implementation
- MCP tool discovery and invocation
- MCP resource discovery and reading
- MCP prompt discovery and retrieval
- Tool registry design
- Service layer design
- Repository abstraction pattern
- Mock-to-real backend replacement strategy
- Structured error handling
- Audit logging
- Human-in-the-loop write actions
- Modular code organization
- Safe enterprise automation design

---

## Real-World Use Case

### Scenario

A user asks an AI assistant:

```text
Why is access request REQ-1003 stuck?
```

The AI assistant can use the MCP server to:

1. Get the request status.
2. Check pending approvers.
3. Diagnose whether the request is pending, in progress, or failed.
4. Read policy or runbook resources.
5. If provisioning failed, prepare a retry draft.
6. Ask a human operator for confirmation.
7. Submit the retry only after approval.
8. Emit audit logs for traceability.

### Example Flow

```text
User asks question
        ↓
AI assistant chooses relevant MCP tools
        ↓
MCP server executes controlled business capabilities
        ↓
Service layer applies business rules
        ↓
Repository layer reads/writes backend data
        ↓
AI assistant explains result to user
```

---

## Current Capabilities

The current project supports:

```text
Read tools                     ✅
Composite diagnostic tool       ✅
MCP-style tool registry         ✅
Real MCP server wrapper         ✅
MCP resources                   ✅
MCP prompts                     ✅
Structured errors               ✅
Audit logging                   ✅
Human-approved retry workflow   ✅
Repository abstraction          ✅
Mock enterprise data            ✅
```

---

## How the System Works

At a high level, the system follows this flow:

```text
MCP Client or test runner
        ↓
Tool Registry
        ↓
Tool Function
        ↓
Service Layer
        ↓
Repository Interface
        ↓
Repository Implementation
        ↓
Mock Data / Future Enterprise Backend
```

For example, when `get_access_request_status` is called:

```text
ToolRegistry.execute_tool("get_access_request_status", request_id="REQ-1001")
        ↓
get_access_request_status()
        ↓
RequestService.get_request_by_id()
        ↓
MockRequestRepository.get_request_by_id()
        ↓
MOCK_ACCESS_REQUESTS
        ↓
AccessRequest.to_dict()
        ↓
Structured response returned
```

For a write action such as provisioning retry:

```text
prepare_provisioning_retry("REQ-1003")
        ↓
RetryService validates request status
        ↓
Retry draft is created
        ↓
Human confirmation required
        ↓
submit_provisioning_retry_after_confirmation(retry_id, approved_by)
        ↓
Retry is submitted
        ↓
Audit event is emitted
```

---

## Architecture

```text
MCP Host / AI Assistant
        ↓
MCP Client
        ↓
Streamable HTTP Transport
        ↓
AccessOps MCP Server
        ↓
MCP Tool / Resource / Prompt Wrappers
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

### Layer Responsibilities

| Layer | Responsibility |
|---|---|
| `app/` | Application entry points, MCP server, client tests |
| `tools/` | MCP-facing tool functions and metadata |
| `services/` | Business logic and workflow rules |
| `repositories/` | Data access abstraction |
| `models/` | Domain objects and response models |
| `data/` | Mock enterprise data and static resources |
| `utils/` | Shared utilities such as audit logging and error handling |
| `config/` | Configuration and versioning |

---

## Project Structure

```text
accessops_mcp/
├── CHANGELOG.md
├── README.md
├── requirements.txt
├── app/
│   ├── main.py
│   ├── mcp_server.py
│   └── mcp_client_test.py
├── config/
│   ├── app_config.py
│   └── version.py
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
└── utils/
    ├── audit_logger.py
    └── error_utils.py
```

---

## Core Design Principles

### 1. Business Capability-Based Tools

The project does not expose generic unsafe tools such as:

```text
call_api(method, url, payload)
query_database(sql)
```

Instead, the project exposes meaningful business capabilities:

```text
get_access_request_status
get_pending_approvers
diagnose_access_request
prepare_provisioning_retry
submit_provisioning_retry_after_confirmation
```

This makes the MCP server safer, easier to audit, and easier for an AI assistant to use correctly.

### 2. Separation of Concerns

Each layer has a clear responsibility:

```text
Tool       → MCP-facing input/output
Service    → Business logic
Repository → Data access
Model      → Domain structure
Utility    → Shared support logic
```

### 3. Repository Abstraction

The service layer does not directly depend on mock data. Instead, the project uses repository abstractions so mock repositories can later be replaced with real backend repositories.

Example:

```text
RequestService
        ↓
RequestRepository interface
        ↓
MockRequestRepository today
        ↓
Enterprise API or database repository in future
```

### 4. Human-in-the-Loop for Sensitive Actions

Sensitive actions are not executed directly.

Bad design:

```text
retry_provisioning(request_id)
```

Better design used in this project:

```text
prepare_provisioning_retry(request_id)
submit_provisioning_retry_after_confirmation(retry_id, approved_by)
```

This pattern ensures that AI does not autonomously execute sensitive enterprise operations.

### 5. Structured Errors

Errors are returned in a predictable format:

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

### 6. Auditability

Every important tool call emits an audit event with:

```text
timestamp
event_type
tool_name
request_id
status
correlation_id
```

---

## MCP Tools

### 1. `get_access_request_status`

Retrieves the current status and details of an access request.

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
    "current_stage": "Manager Approval",
    "requested_at": "2026-05-20T10:30:00",
    "last_updated": "2026-05-20T10:45:00"
  }
}
```

---

### 2. `get_pending_approvers`

Returns users or teams that need to approve the access request.

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
    "pending_approvers": [
      "manager_raj",
      "security_team"
    ]
  }
}
```

---

### 3. `diagnose_access_request`

Combines request status and approval information to generate a business-level diagnosis.

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
    "status": "Pending",
    "current_stage": "Manager Approval",
    "diagnosis": "Request is pending at stage 'Manager Approval'. Awaiting approval from: manager_raj, security_team."
  }
}
```

---

### 4. `prepare_provisioning_retry`

Prepares a retry draft for a failed provisioning request.

This tool does not execute the retry.

Input:

```json
{
  "request_id": "REQ-1003"
}
```

Example response:

```json
{
  "success": true,
  "data": {
    "retry_id": "RETRY-REQ-1003-3a154cdd",
    "request_id": "REQ-1003",
    "action": "Retry provisioning",
    "risk_level": "Medium",
    "requires_confirmation": true,
    "status": "Prepared",
    "summary": "Provisioning retry prepared for access request REQ-1003. The request failed during 'Provisioning'. User confirmation is required before execution.",
    "approved_by": null,
    "submitted_at": null
  }
}
```

---

### 5. `submit_provisioning_retry_after_confirmation`

Submits a prepared retry after explicit human approval.

Input:

```json
{
  "retry_id": "RETRY-REQ-1003-3a154cdd",
  "approved_by": "varun.kumar"
}
```

Example response:

```json
{
  "success": true,
  "data": {
    "retry_id": "RETRY-REQ-1003-3a154cdd",
    "request_id": "REQ-1003",
    "action": "Retry provisioning",
    "risk_level": "Medium",
    "status": "Submitted",
    "requires_confirmation": false,
    "approved_by": "varun.kumar",
    "message": "Provisioning retry for request REQ-1003 has been submitted after approval by varun.kumar."
  }
}
```

---

## MCP Resources

Resources provide read-only context to the AI assistant.

### `policy://access/approval-rules`

Contains access approval rules, such as manager approval, security approval for high-risk roles, and escalation guidance.

### `runbook://identity/provisioning-failure`

Contains troubleshooting steps for failed provisioning, such as checking target-system accounts, role mappings, connector errors, and retry safety.

### `schema://access-request/status-codes`

Explains status values such as:

```text
Pending
In Progress
Failed
Completed
Rejected
```

---

## MCP Prompts

Prompts provide reusable workflow templates that guide the AI assistant.

### `troubleshoot_access_request`

Guides the assistant through a standard access request troubleshooting workflow.

### `generate_requester_response`

Helps draft a requester-facing explanation.

### `prepare_support_summary`

Helps create an operations summary for support engineers.

---

## Human-in-the-Loop Write Workflow

This project uses a two-step pattern for sensitive write actions.

### Step 1: Prepare Action

```text
prepare_provisioning_retry
```

The server validates the request and creates a draft.

The action is not executed yet.

### Step 2: Submit After Confirmation

```text
submit_provisioning_retry_after_confirmation
```

The server submits the action only after a human/operator provides approval.

### Why This Matters

This pattern prevents accidental or autonomous execution of sensitive operations by an AI assistant.

It also enables:

```text
approval tracking
audit logging
duplicate execution prevention
clear operational accountability
```

---

## Structured Error Handling

The project uses `ErrorResponse` and `ErrorUtils` to return predictable error objects.

Common error codes:

```text
ACCESS_REQUEST_NOT_FOUND
APPROVERS_NOT_FOUND
RETRY_NOT_ALLOWED
RETRY_DRAFT_NOT_FOUND
RETRY_ALREADY_PROCESSED
APPROVAL_REQUIRED
INTERNAL_ERROR
```

Example:

```json
{
  "success": false,
  "error": {
    "code": "RETRY_ALREADY_PROCESSED",
    "message": "Retry draft 'RETRY-REQ-1003-3a154cdd' has already been processed.",
    "retryable": false,
    "suggested_action": "Prepare a new provisioning retry draft if another retry is required."
  }
}
```

---

## Audit Logging

The project emits audit logs for tool execution.

Example audit event:

```json
{
  "timestamp": "2026-05-24T16:01:42.890918+00:00",
  "event_type": "MCP_TOOL_CALL",
  "tool_name": "submit_provisioning_retry_after_confirmation",
  "request_id": "REQ-1003",
  "status": "success",
  "correlation_id": "e704c346-85cb-4698-9399-782cb648dc66"
}
```

Currently, audit logs are printed to the console. In a production system, the same audit events can be written to:

```text
PostgreSQL audit table
Splunk
ELK / OpenSearch
Azure Application Insights
SAP BTP logging
Cloud-native observability stack
```

---

## Mock Data and Enterprise Replacement Strategy

The current project uses mock data for learning and demonstration.

Current mock data represents enterprise systems:

| Mock Data | Represents |
|---|---|
| `MOCK_ACCESS_REQUESTS` | Access request system |
| `MOCK_APPROVERS` | Approval workflow system |
| `MOCK_RETRY_DRAFTS` | Retry draft/action workflow state |
| `resource_data.py` | Policy and runbook repository |
| Console audit logs | Enterprise audit logging |

In a real enterprise implementation, these should be replaced through repository and client implementations.

Recommended replacement strategy:

```text
MockRequestRepository
        ↓
ApiRequestRepository or DbRequestRepository
```

```text
MOCK_RETRY_DRAFTS
        ↓
Database-backed RetryRepository
```

```text
resource_data.py
        ↓
Document repository, knowledge base, Git repository, or database table
```

```text
Console audit logs
        ↓
Centralized audit/event logging system
```

The tools and services should not be rewritten when replacing mock data. Only repository implementations and backend clients should change.

---

## Setup Instructions

### Prerequisites

Recommended:

```text
Python 3.10 or higher
pip
virtual environment
terminal access
```

### Create Virtual Environment

```bash
python -m venv .venv
```

Activate it:

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not yet complete, install MCP manually:

```bash
pip install mcp
```

---

## Running the Project

### Run Local Tool Registry Test

```bash
python -m app.main
```

This validates the internal tool registry and business logic without needing an MCP client.

### Run MCP Server

```bash
python -m app.mcp_server
```

The server runs using Streamable HTTP transport.

Default endpoint:

```text
http://127.0.0.1:8000/mcp
```

### Run MCP Client Test

Open another terminal and run:

```bash
python -m app.mcp_client_test
```

The client test validates actual MCP-style client-server behavior.

---

## Testing the MCP-Style Tool Registry

`app/main.py` tests:

```text
TEST 1  Valid access request
TEST 2  Invalid access request
TEST 3  Unknown tool
TEST 4  Pending approvers
TEST 5  Diagnose request
TEST 6  Prepare retry for failed request
TEST 7  Submit retry after confirmation
TEST 7A Submit same retry again
TEST 8  Retry not allowed for non-failed request
TEST 9  Submit non-existing retry draft
```

Expected important results:

```text
TEST 6  → success true, retry status Prepared
TEST 7  → success true, retry status Submitted
TEST 7A → RETRY_ALREADY_PROCESSED
TEST 8  → RETRY_NOT_ALLOWED
TEST 9  → RETRY_DRAFT_NOT_FOUND
```

---

## Running the Real MCP Server

The MCP server wrapper is located at:

```text
app/mcp_server.py
```

It exposes project tools, resources, and prompts through MCP.

Typical flow:

```text
MCP client connects
        ↓
Client discovers tools/resources/prompts
        ↓
Client invokes a tool or reads a resource
        ↓
MCP server routes to internal logic
        ↓
Structured response is returned
```

---

## Running the MCP Client Test

The MCP client test is located at:

```text
app/mcp_client_test.py
```

It validates:

```text
tool discovery
tool invocation
resource discovery
resource reading
prompt discovery
prompt retrieval
structured error handling
human-approved retry workflow
```

---

## Example Outputs

### Successful Request Status

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

### Failed Request Lookup

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

### Duplicate Retry Submission

```json
{
  "success": false,
  "error": {
    "code": "RETRY_ALREADY_PROCESSED",
    "message": "Retry draft 'RETRY-REQ-1003-3a154cdd' has already been processed.",
    "retryable": false,
    "suggested_action": "Prepare a new provisioning retry draft if another retry is required."
  }
}
```

---

## How This Project Was Developed

This project was built step by step to make MCP understandable for beginners.

### Step 1: Understand MCP Basics

The first step was understanding:

```text
MCP Host
MCP Client
MCP Server
Tools
Resources
Prompts
```

### Step 2: Build a Simple Tool

The first tool was:

```text
get_access_request_status
```

It retrieved request details from mock data.

### Step 3: Add Clean Architecture

The project was split into:

```text
models
services
repositories
tools
data
utils
```

### Step 4: Add Repository Pattern

A repository interface was introduced so mock data can later be replaced with real enterprise systems.

### Step 5: Add More Tools

Additional tools were added:

```text
get_pending_approvers
diagnose_access_request
```

### Step 6: Add Tool Registry

The tool registry enabled:

```text
tool discovery
tool execution
centralized registration
```

### Step 7: Add MCP Server Wrapper

A real MCP server wrapper was added to expose the internal capabilities through MCP.

### Step 8: Add Resources and Prompts

Resources and prompts were added to provide:

```text
policy context
runbook context
standard troubleshooting workflows
```

### Step 9: Add Structured Errors and Audit Logging

The project added:

```text
ErrorResponse
ErrorUtils
AuditLogger
correlation IDs
```

### Step 10: Add Human-Approved Write Workflow

The provisioning retry workflow was added using:

```text
prepare_provisioning_retry
submit_provisioning_retry_after_confirmation
```

This introduced safe enterprise-style write actions.

---

## How to Extend This Project

Future tools can follow the same pattern.

### Example: Create Ticket

Recommended files:

```text
models/ticket_model.py
services/ticket_service.py
tools/ticket_tool.py
repositories/ticket_repository.py
repositories/mock_ticket_repository.py
```

Recommended tools:

```text
prepare_ticket_creation
submit_ticket_creation_after_confirmation
```

### Example: Send Notification

Recommended tools:

```text
prepare_notification
send_notification_after_confirmation
```

### Example: Revoke Access

Recommended tools:

```text
prepare_access_revocation
submit_access_revocation_after_confirmation
```

High-risk tools such as access revocation, approval, rejection, and ticket closure should always use human confirmation.

---

## Production Readiness Roadmap

Planned enhancements:

```text
Authentication and authorization
Role-based access control
Persistent retry draft storage
Database-backed audit logs
Real enterprise API connectors
Input validation using schemas
Rate limiting
Timeout handling
Retry policies for backend failures
Centralized observability
Deployment to cloud platform
CI/CD pipeline
Automated tests
Docker support
Configuration-based backend selection
```

Recommended future backend strategy:

```text
Use APIs for enterprise source-of-truth systems
Use PostgreSQL for MCP-owned workflow state and audit data
Use repository implementations to switch from mock to real backend
```

## Current Status

```text
MCP tools: complete
MCP resources: complete
MCP prompts: complete
Tool registry: complete
Real MCP server wrapper: complete
Real MCP client-server test: complete
Repository abstraction: complete
Structured error model: complete
Audit logging: complete
Human-in-the-loop retry workflow: complete
Production hardening: in progress
```

---

## Summary

AccessOps MCP Server is more than a basic MCP demo. It is a production-oriented learning project that shows how an AI assistant can safely interact with enterprise access-management workflows.

The project demonstrates:

```text
MCP fundamentals
Clean architecture
Tool/resource/prompt design
Repository abstraction
Structured errors
Audit logging
Human-approved write actions
Enterprise extensibility
```

This makes the project useful for MCP learning, resume building, interview discussions, and future enterprise integration.
