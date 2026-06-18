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