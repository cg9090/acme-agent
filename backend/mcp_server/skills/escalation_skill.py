from agent.mcp_client import MCPClient
from llm.claude import ClaudeClient
from db.redis_client import redis_client

import json

mcp = MCPClient(base_url="http://localhost:8001")
llm = ClaudeClient()


def cache(tool_name: str, args: dict) -> dict:

    cache_key = f"{tool_name}:{json.dumps(args, sort_keys=True)}"
    cached_result = redis_client.get(cache_key)

    if cached_result:
        return json.loads(cached_result)

    return None


def escalation_summary_skill(customer_name: str):
    tool_results = []
    # Step 1: customer profile
    customer = cache("get_customer_profile", {"customer_name": customer_name})
    cached = True
    if not customer:
        cached = False
        print(f"Executing tool: get_customer_profile with args: {customer_name}")
        customer = mcp.execute_tool(
            "get_customer_profile",
            {"customer_name": customer_name}
        )
    tool_results.append({
                "tool": "get_customer_profile",
                "args": customer_name,
                "cache_hit": cached,
                "result": customer
            })
    if not customer["success"]:
        return {
            "tool_results": tool_results,
        }
    print(f"Customer profile: {customer}")
    if not customer["success"]:
        return {
            "success": False,
            "error": "customer_lookup_failed",
            "tool_results": tool_results
        }
    # Step 2: open issues
    issues = cache("get_open_issues", {"customer_id": customer["customer"]["id"]})
    cached = True
    if not issues:
        cached = False
        print(f"Executing tool: get_open_issues with args: {customer['customer']['id']}")
        issues = mcp.execute_tool(
            "get_open_issues",
            {"customer_id": customer["customer"]["id"]}
        )
    tool_results.append({
                "tool": "get_open_issues",
                "args": {"customer_id": customer["customer"]["id"]},
                "cache_hit": cached,
                "result": issues
            })

    print(f"Open issues: {issues}")
    if not issues["success"]:
        return {
            "success": False,
            "error": "issues_lookup_failed",
            "tool_results": tool_results
        }
    enriched_issues = []

    # Step 3: issue history (bounded)
    for issue in issues["issues"][:5]:
        history = cache("get_issue_history", {"issue_id": issue["id"]})
        cached = True
        if not history:
            cached = False
            print(f"Executing tool: get_issue_history with args: {issue['id']}")
            history = mcp.execute_tool(
                "get_issue_history",
                {"issue_id": issue["id"]}
            )
        tool_results.append({
                    "tool": "get_issue_history",
                    "args": {"issue_id": issue["id"]},
                    "cache_hit": cached,
                    "result": history
                })
        if not history["success"]:
            return {
                "success": False,
                "error": "issue_history_lookup_failed",
                "tool_results": tool_results
            }
        enriched_issues.append({
            "issue": issue,
            "history": history
        })

    # Step 4: LLM reasoning layer (skill-specific)
    prompt = f"""
You are a customer escalation analyst.

Customer:
{customer_name}

Issues:
{enriched_issues}

Return:

1. Executive summary
2. Risk level (Low / Medium / High / Critical)
3. Recommended next action
4. Missing information (if any)
"""

    analysis = llm.generate(prompt)

    return {
        "result":{
            "customer": customer_name,
            "analysis": analysis,
            "issue_count": len(issues)
        },
        "success": True,
        "tool_results": tool_results
    }