from fastapi import FastAPI, logger
from mcp_server.tool_registry import TOOLS
from logging_config import logger

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

    logger.info(
        f"Executing tool={tool_name}, args={args}"
    )

    if tool_name not in TOOLS:
        return {"error": f"Unknown tool: {tool_name}"}

    tool = TOOLS[tool_name]

    try:
        result = tool["function"](**args)
        return result

    except Exception as e:
        logger.exception(
            f"Tool execution failed: {tool_name}"
        )
        return {
            "error": str(e),
            "tool": tool_name
        }