# Changelog

All notable changes to AccessOps MCP Server will be documented in this file.

## [0.1.0] - 2026-05-22

### Added

- Implemented real MCP server using Python and Streamable HTTP transport.
- Added MCP tools for access request status lookup, pending approver lookup, and access request diagnosis.
- Added MCP resources for access approval policy, provisioning failure runbook, and access request status codes.
- Added MCP prompts for access request troubleshooting, requester response drafting, and support engineer summaries.
- Added repository abstraction layer to separate business logic from mock data.
- Added structured error model with error codes, retryability, and suggested actions.
- Added audit logging utility with correlation IDs for MCP tool execution.
- Added human-in-the-loop provisioning retry workflow.
- Added retry draft model and retry service.
- Added safe two-step retry flow:
  - `prepare_provisioning_retry`
  - `submit_provisioning_retry_after_confirmation`
- Added application configuration layer using environment variables.
- Added `.env.example` for supported environment variables.
- Added dependency management through `requirements.txt`.
- Added application version metadata.


### Current Capabilities

- MCP tool discovery and invocation.
- MCP resource discovery and reading.
- MCP prompt discovery and retrieval.
- Real MCP client-server validation.
- Structured error responses.
- Audit event generation.
- Human-approved action execution pattern.

### Notes

This version uses mock enterprise data for demonstration and learning purposes.

The architecture is designed so the mock data layer can be replaced with real enterprise integrations such as SAP IDM or IGA APIs, ServiceNow or Jira workflows, PostgreSQL, Splunk, SharePoint, Confluence, or SAP BTP-based services.
