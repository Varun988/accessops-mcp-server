class PromptService:
    """Service layer for managing reusable MCP prompt templates."""

    @staticmethod
    def troubleshoot_access_request(request_id: str) -> str:
        """
        Generate a structured troubleshooting prompt for an access request.

        Args:
            request_id (str): Access request ID

        Returns:
            str: Prompt text
        """
        return f"""
You are an enterprise access operations assistant.

Troubleshoot access request: {request_id}

Follow this workflow:
1. Check the current access request status.
2. Identify the current stage of the request.
3. Check pending approvers if the request is pending.
4. If the request is in provisioning or failed, review provisioning failure guidance.
5. Identify the most likely blocker.
6. Recommend clear next steps.
7. Keep the explanation concise, factual, and audit-friendly.

Expected response format:
- Request ID
- Current status
- Current stage
- Likely blocker
- Evidence
- Recommended next steps
"""

    @staticmethod
    def generate_requester_response(request_id: str) -> str:
        """
        Generate a prompt for drafting a requester-facing response.

        Args:
            request_id (str): Access request ID

        Returns:
            str: Prompt text
        """
        return f"""
You are drafting a professional response to the requester of access request {request_id}.

Write the response in a clear and respectful tone.

Include:
1. Current request status
2. Reason for delay or failure, if known
3. What action is currently pending
4. What the requester can expect next
5. Avoid exposing internal technical details unless necessary

Expected response format:
Subject:
Message:
Next Steps:
"""

    @staticmethod
    def prepare_support_summary(request_id: str) -> str:
        """
        Generate a prompt for support engineer summary.

        Args:
            request_id (str): Access request ID

        Returns:
            str: Prompt text
        """
        return f"""
Prepare a support engineer summary for access request {request_id}.

The summary should help an operations engineer quickly understand the issue.

Include:
1. Request details
2. Approval status
3. Provisioning status
4. Known blocker
5. Suggested troubleshooting path
6. Escalation recommendation if required

Expected response format:
- Summary
- Technical Details
- Recommended Action
- Escalation Required: Yes/No
"""
