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
    

def create_next_action(issue_id: int, action_text: str):
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                INSERT INTO next_actions (issue_id, action_text)
                VALUES (:issue_id, :action_text)
                RETURNING id, issue_id, action_text
            """),
            {
                "issue_id": issue_id,
                "action_text": action_text,
            }
        )

        row = result.fetchone()

        if row is None:
            return {
                "success": False,
                "message": f"Failed to create next action for issue {issue_id}"
            }

        return {
            "success": True,
            "next_action": dict(row._mapping)
        }