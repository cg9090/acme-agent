from sqlalchemy import text
from db.db import engine

def get_issue_history(issue_id: int):
    if not issue_id or not isinstance(issue_id, int):
        return {
            "success": False,
            "error": "invalid_issue_id",
            "message": "issue_id must be an integer"
        }
    
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT * FROM issue_updates
                WHERE issue_id = :id
                ORDER BY created_at DESC
            """),
            {"id": issue_id}
        )
        return {
            "success": True,
            "history": [dict(row._mapping) for row in result]
        }