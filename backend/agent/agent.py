import json

from agent.tool_registry import TOOLS, TOOL_DESCRIPTIONS, TOOL_PERMISSIONS
from llm.claude import ClaudeClient

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

    return tool_function(**args)

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


def run_agent(user_query: str, user: dict):
    plan = plan_tools(user_query)

    tool_results = []
    for step in plan.get("steps", []):
        tool_name = step["tool"]

        if not has_permission(tool_name, user["roles"]):
            return {
                "error": f"Access denied for tool: {tool_name}",
                "user_roles": user["roles"]
            }

        tool_resposnse = execute_tool(step)
        tool_results.append({
            "tool": tool_name,
            "args": step.get("args", {}),
            "result": tool_resposnse
        })

    response = respond(user_query, tool_results)

    return {
        "answer": response,
        "tool_calls": tool_results
    }