from sqlalchemy import text
from db.db import engine

def get_customer_profile(customer_name: str):
    if not customer_name or not isinstance(customer_name, str):
        return {
            "success": False,
            "error": "invalid_customer_name",
            "message": "customer_name must be a non-empty string"
        }

    customer_name = customer_name.strip()

    if not customer_name:
        return {
            "success": False,
            "error": "invalid_customer_name",
            "message": "customer_name cannot be empty"
        }

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM customers WHERE name ILIKE :name"),
            {"name": customer_name}
        )
        return {
            "success": True,
            "customer": [dict(row._mapping) for row in result]
        }