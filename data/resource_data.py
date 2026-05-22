ACCESS_APPROVAL_RULES = """
Access Approval Rules

1. All access requests must be approved by the requester's manager.
2. High-risk roles require additional security team approval.
3. Finance-related roles may require compliance approval.
4. Requests pending for more than 3 business days should be escalated.
5. Access must follow least-privilege principles.
"""


PROVISIONING_FAILURE_RUNBOOK = """
Identity Provisioning Failure Runbook

Use this runbook when an access request is approved but provisioning fails.

Troubleshooting steps:
1. Verify that the requester has a valid target-system account.
2. Check whether the requested role exists in the target system.
3. Confirm that the role mapping is active.
4. Review provisioning logs for connector or dispatcher errors.
5. Retry provisioning only after validating that the failure is safe to retry.
6. Escalate to the identity operations team if the failure repeats.
"""


ACCESS_STATUS_CODES = """
Access Request Status Codes

Pending:
The request is waiting for one or more approvals.

In Progress:
The request has completed approval and is being provisioned.

Failed:
The request could not be completed due to provisioning or workflow failure.

Completed:
The access request has been successfully fulfilled.

Rejected:
The request was denied by an approver.
"""