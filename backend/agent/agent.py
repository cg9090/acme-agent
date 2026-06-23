import json

# from agent.tool_registry import TOOLS, TOOL_DESCRIPTIONS, TOOL_PERMISSIONS
from llm.claude import ClaudeClient
from db.redis_client import redis_client
from agent.mcp_client import MCPClient
from logging_config import logger
from langsmith.run_helpers import traceable


llm = ClaudeClient()
mcp = MCPClient(base_url="http://localhost:8001")

def build_tool_descriptions(tools):
    return "\n".join(
        f"{name}: {meta['description']} | schema: {meta['schema']}"
        for name, meta in tools.items()
    )

def has_permission(tool_roles: list[str], user_roles: list[str]) -> bool:
    return any(role in user_roles for role in tool_roles)

@traceable(name="plan_tools")
def plan_tools(user_query: str, tools: dict) -> dict:
    prompt = f"""
You are a tool planning agent.

Available tools:
{build_tool_descriptions(tools)}

User query:
{user_query}

Return JSON only in this format:

{{
   "steps": [
     {{
       "tool": "<tool_name>",
       "args": {{
         ...
       }}
     }}
   ]
}}

Rules:
- Output ONLY JSON
- No explanations
- No markdown
- No backticks
- No additional text before or after JSON
- If information is missing, use null (do NOT explain missing fields)
"""



    response = llm.generate(prompt)
    response = response.replace("```json", "").replace("```", "").strip()
    return json.loads(response)

@traceable(name="respond")
def respond(user_query: str, tool_output: dict) -> str:
    prompt = f"""


User query:
{user_query}

Tool output:
{json.dumps(tool_output, indent=2, default=str)}
Respond to the users query with the information provided.
"""

    response = llm.generate(prompt)

    return response.strip()

def cached(cache_key: str):

    cached_result = redis_client.get(cache_key)

    if cached_result:
        return json.loads(cached_result)

    return None

@traceable(name="mcp_tool")
def execute_tool(tool_name: str, args: dict) -> dict:
    return mcp.execute_tool(tool_name, args)

@traceable(name="run_agent", project="acme-agent")
def run_agent(user_query: str, user: dict):

    logger.info(f"User query: {user_query}")
    logger.info(f"User roles: {user['roles']}")

    tools = mcp.list_tools()
    plan = plan_tools(user_query, tools)

    logger.info(f"Plan generated: {plan}")

    tool_results = []
    for step in plan.get("steps", []):
        args = step.get("args", {})
        tool_name = step["tool"]

        if not has_permission(tools[tool_name]["roles"], user["roles"]):
            logger.warning(
                f"RBAC denied. Tool={tool_name}, Roles={user['roles']}"
            )
            return {
                "error": f"Access denied for tool: {tool_name}",
                "user_roles": user["roles"]
            }
        
        cache_key = f"{tool_name}:{json.dumps(args, sort_keys=True)}"
        tool_response = cached(cache_key)

        cache_hit = tool_response is not None
        if not cache_hit:
            tool_response = execute_tool(tool_name, args)

            redis_client.setex(
                cache_key,
                300,  # Cache for 5 minutes
                json.dumps(tool_response, default=str)
                )
            
        logger.info(
            f"Tool={tool_name}, CacheHit={cache_hit}"
        )

        tool_results.append({
                "tool": tool_name,
                "args": args,
                "cache_hit": cache_hit,
                "result": tool_response
            })
        
    response = respond(user_query, tool_results)

    return {
        "answer": response,
        "tool_calls": tool_results
    }