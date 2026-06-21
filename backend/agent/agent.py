import json

from agent.tool_registry import TOOLS, TOOL_DESCRIPTIONS, TOOL_PERMISSIONS
from llm.claude import ClaudeClient
from db.redis_client import redis_client

llm = ClaudeClient()

def has_permission(tool_name: str, roles: list[str]) -> bool:
    allowed = TOOL_PERMISSIONS.get(tool_name)

    if allowed is None:
        return True

    return any(role in roles for role in allowed)

# def choose_tool(user_query: str) -> dict:
#     prompt = f"""
# {TOOL_DESCRIPTIONS}

# User query:
# {user_query}

# Respond with JSON only.
# """

#     response = llm.generate(prompt)
#     response = response.replace("```json", "")
#     response = response.replace("```", "")
#     response = response.strip()
#     return json.loads(response)

def plan_tools(user_query: str) -> dict:
    prompt = f"""
You are a tool planning agent.

Available tools:
{TOOL_DESCRIPTIONS}

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


def execute_tool(tool_call: dict):
    tool_name = tool_call["tool"]
    args = tool_call.get("args", {})

    if tool_name not in TOOLS:
        raise ValueError(f"Unknown tool: {tool_name}")

    tool_function = TOOLS[tool_name]

    try:
        return tool_function(**args)

    except TypeError as e:
        return {
            "error": "invalid_tool_arguments",
            "tool": tool_name,
            "details": str(e),
            "args_received": args
        }

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

    # tool_function = TOOLS[tool_name]
    # result = tool_function(**args)

    # 

    return None


def run_agent(user_query: str, user: dict):
    plan = plan_tools(user_query)

    tool_results = []
    for step in plan.get("steps", []):
        args = step.get("args", {})
        tool_name = step["tool"]

        if not has_permission(tool_name, user["roles"]):
            return {
                "error": f"Access denied for tool: {tool_name}",
                "user_roles": user["roles"]
            }
        
        cache_key = f"{tool_name}:{json.dumps(args, sort_keys=True)}"
        tool_response = cached(cache_key)

        cache_hit = tool_response is not None

        if not cache_hit:
            tool_response = execute_tool(step)
            
            redis_client.setex(
                cache_key,
                300,  # Cache for 5 minutes
                json.dumps(tool_response, default=str)
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