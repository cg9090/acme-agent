from sqlalchemy import text
from db.db import engine

def get_issue_history(issue_id: int):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT * FROM issue_updates
                WHERE issue_id = :id
                ORDER BY created_at DESC
            """),
            {"id": issue_id}
        )
        return [dict(row._mapping) for row in result]