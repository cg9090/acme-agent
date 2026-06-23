from fastapi import FastAPI, Depends
from agent.agent import run_agent
from sqlalchemy import text
from db.db import engine
from pydantic import BaseModel
from auth.keycloak import get_current_user

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
def agent_endpoint(req: QueryRequest, user=Depends(get_current_user)):
    result = run_agent(req.query, user)

    return {
        "query": req.query,
        "result": result
    }

@app.get("/me")
def me(user=Depends(get_current_user)):
    return user