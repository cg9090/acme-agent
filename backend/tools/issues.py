from sqlalchemy import text
from db.db import engine

def get_open_issues(customer_id: int):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT * FROM issues
                WHERE customer_id = :id AND status = 'OPEN'
            """),
            {"id": customer_id}
        )
        return [dict(row._mapping) for row in result]


def update_issue_status(issue_id: int, status: str):
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