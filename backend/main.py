from fastapi import FastAPI
from agent.agent import run_agent
from sqlalchemy import text
from db.db import engine
from pydantic import BaseModel

app = FastAPI()
@app.get("/customers")
def get_customers():
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM customers")
        )

        return [dict(row._mapping) for row in result]

class QueryRequest(BaseModel):
    query: str


@app.post("/agent")
def agent_endpoint(req: QueryRequest):
    result = run_agent(req.query)

    return {
        "query": req.query,
        "result": result
    }