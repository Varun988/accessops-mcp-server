# AccessOps MCP Server

AccessOps MCP Server is a production-style **Model Context Protocol (MCP)** project built in Python. It demonstrates how an AI assistant can safely interact with enterprise access-operation workflows using MCP tools, resources, prompts, structured error handling, audit logging, human-in-the-loop approvals, and role-based authorization.

This project is designed as a beginner-friendly learning project and also as a resume-worthy implementation that shows how MCP can be used in real enterprise scenarios.

---

## Table of Contents

1. [Project Summary](#project-summary)
2. [Problem Statement](#problem-statement)
3. [What This Project Solves](#what-this-project-solves)
4. [Beginner Explanation: What Is MCP?](#beginner-explanation-what-is-mcp)
5. [Core MCP Concepts Used](#core-mcp-concepts-used)
6. [Real-World Scenario](#real-world-scenario)
7. [Current Features](#current-features)
8. [Architecture Overview](#architecture-overview)
9. [Layer-by-Layer Explanation](#layer-by-layer-explanation)
10. [Project Structure](#project-structure)
11. [How the Application Works](#how-the-application-works)
12. [MCP Tools Implemented](#mcp-tools-implemented)
13. [MCP Resources Implemented](#mcp-resources-implemented)
14. [MCP Prompts Implemented](#mcp-prompts-implemented)
15. [Human-in-the-Loop Write Action Design](#human-in-the-loop-write-action-design)
16. [Role-Based Authorization](#role-based-authorization)
17. [Structured Error Handling](#structured-error-handling)
18. [Audit Logging](#audit-logging)
19. [Mock Data Strategy](#mock-data-strategy)
20. [How Mock Data Can Be Replaced in Enterprise](#how-mock-data-can-be-replaced-in-enterprise)
21. [Setup Instructions](#setup-instructions)
22. [Running Local Tool Tests](#running-local-tool-tests)
23. [Running the MCP Server](#running-the-mcp-server)
24. [Running the MCP Client Test](#running-the-mcp-client-test)
25. [Important Test Scenarios](#important-test-scenarios)
26. [Development Journey](#development-journey)
27. [How to Add a New Tool](#how-to-add-a-new-tool)
28. [Production Readiness Roadmap](#production-readiness-roadmap)
29. [Resume and Interview Explanation](#resume-and-interview-explanation)
30. [Current Status](#current-status)

---

## Project Summary

**AccessOps MCP Server** is an MCP-based enterprise access operations assistant backend.

The server exposes controlled capabilities that allow an AI assistant to:

- Retrieve access request status
- Find pending approvers
- Diagnose access request issues
- Read policy and runbook resources
- Use standard troubleshooting prompts
- Prepare and submit provisioning retries after approval
- Prepare and create tickets after approval
- Prepare and send notifications after approval
- Prepare and close tickets after approval
- Enforce role-based permissions for sensitive actions
- Emit audit events for traceability

The current implementation uses mock enterprise data, but the code is structured so that the mock layer can later be replaced with real APIs, databases, workflow engines, ticketing platforms, notification services, or identity governance systems.

---

## Problem Statement

In large organizations, access requests often get delayed or fail because of:

- Pending manager approval
- Security or compliance approval delays
- Provisioning failures
- Missing target-system account mappings
- Role mapping issues
- Workflow errors
- Lack of visibility for support teams

Users and support teams frequently ask:

```text
Why is my access request pending?
Who needs to approve it?
Did provisioning fail?
Can provisioning be retried?
Can a support ticket be created?
Can the requester be notified?
Can the ticket be closed after resolution?
```

Without automation, support engineers may need to manually inspect multiple systems. This project shows how MCP can provide an AI assistant with safe, structured, auditable access to these capabilities.

---

## What This Project Solves

AccessOps MCP Server solves the problem of connecting an AI assistant to enterprise access operations in a controlled way.

Instead of exposing raw APIs directly to an AI model, the project exposes **business-safe MCP tools** such as:

```text
get_access_request_status
diagnose_access_request
prepare_provisioning_retry
submit_provisioning_retry_after_confirmation
prepare_ticket_creation
submit_ticket_creation_after_confirmation
prepare_notification
send_notification_after_confirmation
prepare_ticket_closure
submit_ticket_closure_after_confirmation
```

This gives the AI assistant useful enterprise capabilities while still enforcing:

- Human confirmation
- Role-based authorization
- Structured errors
- Audit logging
- Duplicate execution protection
- Clear business boundaries

---

## Beginner Explanation: What Is MCP?

**MCP** stands for **Model Context Protocol**.

A simple way to understand MCP:

```text
MCP lets AI assistants safely connect to external tools, systems, and data sources.
```

Without MCP, every AI application would need custom integration code for every system.

With MCP, the AI application talks to an MCP server, and the MCP server exposes controlled capabilities.

Basic architecture:

```text
User
  ↓
AI Assistant / MCP Host
  ↓
MCP Client
  ↓
MCP Server
  ↓
External System / API / Database / Workflow
```

In this project:

```text
User
  ↓
AI Assistant
  ↓
AccessOps MCP Server
  ↓
Access request data, approval data, ticket workflow, retry workflow, notification workflow
```

---

## Core MCP Concepts Used

This project uses the three main MCP capability types.

### 1. Tools

Tools are functions that the AI assistant can call.

Examples:

```text
get_access_request_status
prepare_ticket_creation
send_notification_after_confirmation
```

Tools are used when the assistant needs to do something or retrieve computed data.

### 2. Resources

Resources are read-only pieces of context.

Examples:

```text
policy://access/approval-rules
runbook://identity/provisioning-failure
schema://access-request/status-codes
```

Resources are used when the assistant needs reference information.

### 3. Prompts

Prompts are reusable workflow templates.

Examples:

```text
troubleshoot_access_request
generate_requester_response
prepare_support_summary
```

Prompts help the assistant follow a consistent process.

---

## Real-World Scenario

Example user question:

```text
Why is access request REQ-1003 stuck, and can we notify the support team?
```

The AI assistant can use the MCP server as follows:

```text
1. Call get_access_request_status("REQ-1003")
2. Call diagnose_access_request("REQ-1003")
3. Read provisioning failure runbook
4. Prepare notification draft
5. Ask a human operator for confirmation
6. Send notification after confirmation
7. Emit audit logs
```

If provisioning failed, the AI assistant can also prepare a retry action:

```text
1. prepare_provisioning_retry("REQ-1003")
2. Show retry draft to operator
3. submit_provisioning_retry_after_confirmation(retry_id, approved_by)
```

The AI does not directly execute sensitive operations. Every write action is reviewed and confirmed by a human.

---

## Current Features

### Read and Diagnostic Features

- Get access request status
- Get pending approvers
- Diagnose pending, in-progress, or failed requests
- Read access approval policy
- Read provisioning failure runbook
- Read access request status-code reference
- Retrieve workflow prompts

### Write / Action Features

All write actions use a two-step human approval pattern.

- Prepare provisioning retry
- Submit provisioning retry after confirmation
- Prepare ticket creation
- Submit ticket creation after confirmation
- Prepare notification
- Send notification after confirmation
- Prepare ticket closure
- Submit ticket closure after confirmation

### Security and Reliability Features

- Role-based authorization checks
- Structured error responses
- Audit logging with correlation IDs
- Duplicate execution prevention
- Modular service-based design
- Repository abstraction
- Mock-to-real backend replacement path

---

## Architecture Overview

High-level architecture:

```text
MCP Host / AI Assistant
        ↓
MCP Client
        ↓
AccessOps MCP Server
        ↓
Tool / Resource / Prompt Wrappers
        ↓
Tool Layer
        ↓
Service Layer
        ↓
Repository Layer
        ↓
Mock Data / Future Enterprise Backend
```

Detailed internal flow:

```text
User request
  ↓
AI assistant selects tool
  ↓
MCP server receives tool call
  ↓
Tool function validates input/output behavior
  ↓
Service applies business rules
  ↓
Repository retrieves or updates data
  ↓
Model converts response to dictionary
  ↓
Structured response returned
  ↓
Audit event emitted
```

---

## Layer-by-Layer Explanation

### `app/`

Contains application entry points.

Important files:

```text
main.py
mcp_server.py
mcp_client_test.py
```

Purpose:

- Run local tests
- Start MCP server
- Run MCP client integration tests

### `tools/`

Contains MCP-facing tool wrappers.

Important files:

```text
access_request_tool.py
retry_tool.py
ticket_tool.py
notification_tool.py
tool_registry.py
```

Purpose:

- Define tool metadata
- Define tool input schemas
- Convert service results into MCP-friendly responses
- Convert exceptions into structured errors
- Register tools for discovery and execution

### `services/`

Contains business logic.

Important files:

```text
request_service.py
retry_service.py
ticket_service.py
notification_service.py
authorization_service.py
resource_service.py
prompt_service.py
```

Purpose:

- Apply business rules
- Enforce human approval
- Enforce RBAC permissions
- Prevent duplicate execution
- Coordinate repositories and models

### `repositories/`

Contains data-access abstraction.

Important files:

```text
request_repository.py
mock_request_repository.py
```

Purpose:

- Hide whether data comes from mock data, database, or enterprise API
- Make backend replacement easier

### `models/`

Contains domain objects.

Important files:

```text
request_model.py
retry_model.py
ticket_model.py
notification_model.py
error_model.py
```

Purpose:

- Represent access requests, retry drafts, ticket drafts, closure drafts, notification drafts, and errors
- Provide `to_dict()` conversion for structured responses

### `data/`

Contains mock data.

Important files:

```text
mock_data.py
mock_auth_data.py
resource_data.py
```

Purpose:

- Simulate enterprise backend systems
- Store mock requests, approvers, drafts, tickets, notifications, and authorization mappings

### `utils/`

Contains reusable helper logic.

Important files:

```text
audit_logger.py
error_utils.py
```

Purpose:

- Generate structured error responses
- Emit audit events

---

## Project Structure

```text
accessops_mcp/
├── CHANGELOG.md
├── README.md
├── requirements.txt
├── app/
│   ├── main.py
│   ├── mcp_client_test.py
│   └── mcp_server.py
├── config/
│   ├── app_config.py
│   └── version.py
├── data/
│   ├── mock_auth_data.py
│   ├── mock_data.py
│   └── resource_data.py
├── models/
│   ├── error_model.py
│   ├── notification_model.py
│   ├── request_model.py
│   ├── retry_model.py
│   └── ticket_model.py
├── repositories/
│   ├── mock_request_repository.py
│   └── request_repository.py
├── services/
│   ├── authorization_service.py
│   ├── notification_service.py
│   ├── prompt_service.py
│   ├── request_service.py
│   ├── resource_service.py
│   ├── retry_service.py
│   └── ticket_service.py
├── tools/
│   ├── access_request_tool.py
│   ├── notification_tool.py
│   ├── retry_tool.py
│   ├── ticket_tool.py
│   └── tool_registry.py
└── utils/
    ├── audit_logger.py
    └── error_utils.py
```

---

## How the Application Works

### Example: Read Tool Flow

Tool:

```text
get_access_request_status
```

Flow:

```text
ToolRegistry.execute_tool("get_access_request_status")
  ↓
access_request_tool.get_access_request_status()
  ↓
RequestService.get_request_by_id()
  ↓
MockRequestRepository.get_request_by_id()
  ↓
MOCK_ACCESS_REQUESTS
  ↓
AccessRequest.to_dict()
  ↓
Structured response
```

### Example: Write Tool Flow

Tool:

```text
submit_ticket_creation_after_confirmation
```

Flow:

```text
ToolRegistry.execute_tool("submit_ticket_creation_after_confirmation")
  ↓
ticket_tool.submit_ticket_creation_after_confirmation()
  ↓
TicketService.submit_ticket_creation_after_confirmation()
  ↓
Approval check
  ↓
AuthorizationService.require_permission("ticket:create")
  ↓
Duplicate execution check
  ↓
Mock ticket creation
  ↓
Audit event
  ↓
Structured response
```

---

## MCP Tools Implemented

### Access Request Tools

#### `get_access_request_status`

Retrieves details for an access request.

Input:

```json
{
  "request_id": "REQ-1001"
}
```

Output includes:

```text
request_id
requester
target_system
role
status
current_stage
requested_at
last_updated
```

#### `get_pending_approvers`

Returns pending approvers for a request.

Input:

```json
{
  "request_id": "REQ-1001"
}
```

#### `diagnose_access_request`

Combines request status and approval data to provide a business diagnosis.

---

### Provisioning Retry Tools

#### `prepare_provisioning_retry`

Prepares a retry draft for a failed request.

This tool does not execute the retry.

#### `submit_provisioning_retry_after_confirmation`

Submits the retry only after approval.

Required permission:

```text
provisioning:retry
```

---

### Ticket Creation Tools

#### `prepare_ticket_creation`

Prepares a ticket creation draft.

#### `submit_ticket_creation_after_confirmation`

Creates the ticket after approval.

Required permission:

```text
ticket:create
```

---

### Ticket Closure Tools

#### `prepare_ticket_closure`

Prepares a ticket closure draft.

#### `submit_ticket_closure_after_confirmation`

Closes the ticket after approval.

Required permission:

```text
ticket:close
```

---

### Notification Tools

#### `prepare_notification`

Prepares a notification draft.

#### `send_notification_after_confirmation`

Sends the notification after approval.

Required permission:

```text
notification:send
```

---

## MCP Resources Implemented

The project exposes read-only resources that provide policy, runbook, and schema context.

### `policy://access/approval-rules`

Contains access approval rules.

### `runbook://identity/provisioning-failure`

Contains troubleshooting guidance for failed provisioning.

### `schema://access-request/status-codes`

Explains access request statuses such as:

```text
Pending
In Progress
Failed
Completed
Rejected
```

---

## MCP Prompts Implemented

The project exposes prompts that guide standard workflows.

### `troubleshoot_access_request`

Guides the AI assistant through access request troubleshooting.

### `generate_requester_response`

Helps generate a requester-facing response.

### `prepare_support_summary`

Helps generate a support or operations summary.

---

## Human-in-the-Loop Write Action Design

Every sensitive action follows this pattern:

```text
prepare_action
  ↓
review draft
  ↓
submit_action_after_confirmation
```

Example:

```text
prepare_ticket_creation
  ↓
submit_ticket_creation_after_confirmation
```

Why this is important:

- Prevents autonomous AI execution
- Allows human review before action
- Enables audit trails
- Supports compliance
- Makes duplicate prevention possible
- Makes authorization checks explicit

---

## Role-Based Authorization

The project includes mock RBAC using:

```text
data/mock_auth_data.py
services/authorization_service.py
```

### Roles

Example roles:

```text
identity_operator
support_engineer
access_manager
admin
```

### Permissions

Current permissions:

```text
provisioning:retry
ticket:create
ticket:close
notification:send
access:approve
access:revoke
```

### Protected Actions

| Action | Required Permission |
|---|---|
| Submit provisioning retry | `provisioning:retry` |
| Submit ticket creation | `ticket:create` |
| Submit ticket closure | `ticket:close` |
| Send notification | `notification:send` |

### Example Authorization Failure

```json
{
  "success": false,
  "error": {
    "code": "AUTHORIZATION_FAILED",
    "message": "User 'readonly.user' is not authorized to perform this action. Required permission: 'ticket:create'.",
    "retryable": false,
    "suggested_action": "Use an authorized operator or request the required access."
  }
}
```

---

## Structured Error Handling

The project uses a standard error response model.

Error format:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "retryable": false,
    "suggested_action": "Recommended next step"
  }
}
```

Common error codes:

```text
ACCESS_REQUEST_NOT_FOUND
APPROVERS_NOT_FOUND
RETRY_NOT_ALLOWED
RETRY_DRAFT_NOT_FOUND
RETRY_ALREADY_PROCESSED
TICKET_DRAFT_NOT_FOUND
TICKET_ALREADY_PROCESSED
TICKET_NOT_FOUND
TICKET_ALREADY_CLOSED
TICKET_CLOSURE_DRAFT_NOT_FOUND
TICKET_CLOSURE_ALREADY_PROCESSED
NOTIFICATION_DRAFT_NOT_FOUND
NOTIFICATION_ALREADY_PROCESSED
AUTHORIZATION_FAILED
INTERNAL_ERROR
```

---

## Audit Logging

Every important tool execution emits an audit event.

Example:

```json
{
  "timestamp": "2026-05-24T16:17:03.020642+00:00",
  "event_type": "MCP_TOOL_CALL",
  "tool_name": "submit_ticket_creation_after_confirmation",
  "request_id": "REQ-1003",
  "status": "success",
  "correlation_id": "7a016669-ec92-41e1-a2ed-6382fbf968a1"
}
```

Current behavior:

```text
Audit events are printed to the console.
```

Future production behavior:

```text
Write audit events to a database, log platform, SIEM, or observability tool.
```

---

## Mock Data Strategy

The project currently uses mock data for learning and demonstration.

Mock data represents:

```text
Access requests
Approvers
Retry drafts
Ticket drafts
Created tickets
Ticket closure drafts
Notification drafts
Sent notifications
Authorization roles and permissions
Resources such as policies and runbooks
```

This makes the project easy to run locally without depending on external systems.

---

## How Mock Data Can Be Replaced in Enterprise

The correct enterprise replacement strategy is not to call APIs directly from tools.

Bad design:

```text
Tool → external API
```

Good design:

```text
Tool → Service → Repository → Client → external API/database
```

Recommended real replacements:

| Current Mock Component | Enterprise Replacement |
|---|---|
| `MOCK_ACCESS_REQUESTS` | Access request API or database |
| `MOCK_APPROVERS` | Workflow or approval engine |
| `MOCK_RETRY_DRAFTS` | Database table for retry drafts |
| `MOCK_TICKET_DRAFTS` | Database table for ticket drafts |
| `MOCK_CREATED_TICKETS` | Ticketing system or ticket database |
| `MOCK_NOTIFICATION_DRAFTS` | Notification draft table |
| `MOCK_SENT_NOTIFICATIONS` | Email, Teams, Slack, or enterprise notification API |
| `mock_auth_data.py` | Identity provider, JWT claims, IAM/IGA system, or RBAC database |
| `resource_data.py` | Knowledge base, SharePoint, Confluence, Git, or document repository |

Recommended future architecture:

```text
MCP Tool
  ↓
Service Layer
  ↓
Repository Interface
  ↓
Real Repository Implementation
  ↓
Enterprise API / Database / Workflow System
```

---

## Setup Instructions

### Prerequisites

```text
Python 3.10 or higher
pip
virtual environment recommended
```

### Create Virtual Environment

```bash
python -m venv .venv
```

Activate environment:

```bash
source .venv/bin/activate
```

For Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

If the MCP package is not already listed in requirements:

```bash
pip install mcp
```

---

## Running Local Tool Tests

Run:

```bash
python -m app.main
```

This runs the local test runner and validates:

- Tool discovery
- Read tools
- Retry workflow
- Ticket creation workflow
- Notification workflow
- Ticket closure workflow
- RBAC authorization checks
- Structured errors
- Audit logging

---

## Running the MCP Server

Run:

```bash
python -m app.mcp_server
```

Default endpoint:

```text
http://127.0.0.1:8000/mcp
```

The MCP server exposes tools, resources, and prompts.

---

## Running the MCP Client Test

Open another terminal and run:

```bash
python -m app.mcp_client_test
```

This validates real MCP client-server behavior.

---

## Important Test Scenarios

The local test runner validates scenarios such as:

```text
Valid request lookup
Invalid request lookup
Unknown tool handling
Pending approver lookup
Access request diagnosis
Prepare retry
Submit retry
Duplicate retry submission
Unauthorized retry submission
Prepare ticket creation
Submit ticket creation
Duplicate ticket creation
Unauthorized ticket creation
Prepare notification
Send notification
Duplicate notification send
Unauthorized notification send
Prepare ticket closure
Submit ticket closure
Duplicate ticket closure
Unauthorized ticket closure
```

---

## Development Journey

This project was developed step by step.

### Phase 1: MCP Basics

The project started by understanding:

```text
MCP Host
MCP Client
MCP Server
Tools
Resources
Prompts
```

### Phase 2: First Read Tool

The first tool was:

```text
get_access_request_status
```

### Phase 3: Clean Architecture

The project was split into:

```text
models
services
repositories
tools
data
utils
```

### Phase 4: Tool Registry

A tool registry was added to simulate MCP-style discovery and invocation.

### Phase 5: Real MCP Server

An MCP server wrapper was added.

### Phase 6: Resources and Prompts

Resources and prompts were added for policy, runbook, and workflow guidance.

### Phase 7: Safe Write Workflows

Human-approved workflows were added:

```text
provisioning retry
ticket creation
notification sending
ticket closure
```

### Phase 8: Authorization

RBAC authorization was added for sensitive submit actions.

---

## How to Add a New Tool

To add a new write tool, follow this pattern.

### Step 1: Add Model

Example:

```text
models/access_revocation_model.py
```

### Step 2: Add Mock Store

Example:

```text
MOCK_ACCESS_REVOCATION_DRAFTS = {}
```

### Step 3: Add Service

Example:

```text
services/access_revocation_service.py
```

### Step 4: Add Tool

Example:

```text
tools/access_revocation_tool.py
```

### Step 5: Add Error Methods

Add structured errors in:

```text
utils/error_utils.py
```

### Step 6: Register Tool

Update:

```text
tools/tool_registry.py
```

### Step 7: Add Tests

Update:

```text
app/main.py
```

### Step 8: Add Authorization

Add permission check using:

```text
AuthorizationService.require_permission(...)
```

---

## Production Readiness Roadmap

Planned enhancements:

```text
Persistent database storage
Database-backed audit logging
Real enterprise API integrations
Authentication for MCP clients
JWT/OAuth-based user context
Fine-grained RBAC
Input validation with schema models
Unit tests and integration tests
Dockerfile
CI/CD pipeline
Deployment to SAP BTP or cloud platform
Observability metrics
Rate limiting
Timeout and retry handling
Secrets management
Environment-based configuration
```

Recommended production backend pattern:

```text
Use APIs for enterprise source-of-truth systems.
Use a database for MCP-owned workflow state.
Use centralized logging for audit and observability.
Use repository implementations to switch between mock and real backend.
```

---

Strong interview points:

```text
MCP tool/resource/prompt implementation
Human-in-the-loop write actions
RBAC for sensitive operations
Repository abstraction
Structured error design
Audit logging with correlation IDs
Mock-to-enterprise backend replacement strategy
Production-readiness roadmap
```

---

## Current Status

```text
MCP tools: implemented
MCP resources: implemented
MCP prompts: implemented
Tool registry: implemented
Real MCP server wrapper: implemented
MCP client test: implemented
Repository abstraction: implemented
Structured errors: implemented
Audit logging: implemented
Provisioning retry workflow: implemented
Ticket creation workflow: implemented
Notification workflow: implemented
Ticket closure workflow: implemented
RBAC authorization: implemented for existing write submit actions
Production hardening: in progress
```

---

## Summary

AccessOps MCP Server is a practical, production-oriented MCP learning project.

It demonstrates how an AI assistant can safely interact with enterprise systems using:

```text
MCP tools
MCP resources
MCP prompts
Clean architecture
Human approvals
RBAC authorization
Structured errors
Audit logs
Mock-to-real backend extensibility
```

The project is suitable for:

```text
Learning MCP
Understanding AI-to-enterprise-system integration
Future enterprise deployment
```
