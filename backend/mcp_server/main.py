from fastapi import FastAPI
from mcp_server.tool_registry import TOOLS

app = FastAPI(title= "Acme MCP Server")

@app.get("/tools")
def list_tools():
    return {
        name: {
            "description": tool["description"],
            "roles": tool["roles"],
            "schema": tool["schema"]
        }
        for name, tool in TOOLS.items()
    }

@app.post("/tools/execute")
def execute_tool(request: dict):
    tool_name = request.get("tool")
    args = request.get("args", {})

    if tool_name not in TOOLS:
        return {"error": f"Unknown tool: {tool_name}"}

    tool = TOOLS[tool_name]

    try:
        result = tool["function"](**args)
        return {"result": result}

    except Exception as e:
        return {
            "error": str(e),
            "tool": tool_name
        }