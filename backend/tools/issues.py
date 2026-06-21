from sqlalchemy import text
from db.db import engine

def get_open_issues(customer_id: int):
    if not customer_id or not isinstance(customer_id, int):
        return {
            "success": False,
            "error": "invalid_customer_id",
            "message": "customer_id must be an integer"
        }

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT * FROM issues
                WHERE customer_id = :id AND status = 'OPEN'
            """),
            {"id": customer_id}
        )
        return {
            "success": True,
            "issues": [dict(row._mapping) for row in result]
        }


VALID_STATUSES = {"OPEN", "IN_PROGRESS", "CLOSED"}

def update_issue_status(issue_id: int, status: str):
     # 1. Validate issue_id
    if not isinstance(issue_id, int):
        return {
            "success": False,
            "error": "invalid_issue_id",
            "message": "issue_id must be an integer"
        }

    # 2. Validate status exists
    if not status or not isinstance(status, str):
        return {
            "success": False,
            "error": "invalid_status",
            "message": "status must be a non-empty string"
        }

    status = status.strip().upper()

    # 3. Validate allowed values
    if status not in VALID_STATUSES:
        return {
            "success": False,
            "error": "invalid_status_value",
            "allowed": list(VALID_STATUSES),
            "received": status
        }
    
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                UPDATE issues
                SET status = :status
                WHERE id = :issue_id
                RETURNING id, title, status
            """),
            {
                "issue_id": issue_id,
                "status": status,
            }
        )

        row = result.fetchone()

        if row is None:
            return {
                "success": False,
                "message": f"Issue {issue_id} not found"
            }

        return {
            "success": True,
            "issue": dict(row._mapping)
        }