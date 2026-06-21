from sqlalchemy import text
from db.db import engine

def get_customer_profile(customer_name: str):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM customers WHERE name ILIKE :name"),
            {"name": customer_name}
        )
        return [dict(row._mapping) for row in result]