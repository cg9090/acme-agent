from sqlalchemy import text
from db.db import engine

def get_next_action(issue_id: int):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT * FROM next_actions
                WHERE issue_id = :id
                ORDER BY created_at DESC
                LIMIT 1
            """),
            {"id": issue_id}
        )
        return [dict(row._mapping) for row in result]