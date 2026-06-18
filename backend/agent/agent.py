import json
from unittest import result
from urllib import response

from agent.tool_registry import TOOLS, TOOL_DESCRIPTIONS
from llm.claude import ClaudeClient

llm = ClaudeClient()

def choose_tool(user_query: str) -> dict:
    prompt = f"""
{TOOL_DESCRIPTIONS}

User query:
{user_query}

Respond with JSON only.
"""

    response = llm.generate(prompt)
    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()
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


def run_agent(user_query: str):
    tool_call = choose_tool(user_query)

    tool_resposnse = execute_tool(tool_call)

    response = respond(user_query, tool_resposnse)

    return response
    