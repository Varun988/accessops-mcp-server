from datetime import datetime
from models.request_model import AccessRequest


# Simulated database of access requests
MOCK_ACCESS_REQUESTS = {
    "REQ-1001": AccessRequest(
        request_id="REQ-1001",
        requester="varun.kumar",
        target_system="SAP_FINANCE",
        role="FIN_DISPLAY",
        status="Pending",
        current_stage="Manager Approval",
        requested_at=datetime(2026, 5, 20, 10, 30),
        last_updated=datetime(2026, 5, 20, 10, 45),
    ),
    "REQ-1002": AccessRequest(
        request_id="REQ-1002",
        requester="anita.sharma",
        target_system="SAP_HR",
        role="HR_ADMIN",
        status="In Progress",
        current_stage="Provisioning",
        requested_at=datetime(2026, 5, 19, 9, 0),
        last_updated=datetime(2026, 5, 20, 14, 10),
    ),
    "REQ-1003": AccessRequest(
        request_id="REQ-1003",
        requester="rahul.verma",
        target_system="SALESFORCE",
        role="SALES_READ",
        status="Failed",
        current_stage="Provisioning",
        requested_at=datetime(2026, 5, 18, 16, 45),
        last_updated=datetime(2026, 5, 20, 11, 20),
    ),
}

# Simulated approval workflow data
MOCK_APPROVERS = {
    "REQ-1001": ["manager_raj", "security_team"],
    "REQ-1002": ["manager_anu"],
    "REQ-1003": ["manager_vikram", "compliance_team"]
}