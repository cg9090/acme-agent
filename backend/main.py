from fastapi import FastAPI
from sqlalchemy import text
from db.db import engine

app = FastAPI()
@app.get("/customers")
def get_customers():
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM customers")
        )

        return [dict(row._mapping) for row in result]