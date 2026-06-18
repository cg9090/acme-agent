from sqlalchemy import text
from db.db import engine

def get_customer_profile(name: str):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM customers WHERE name = :name"),
            {"name": name}
        )
        return [dict(row._mapping) for row in result]