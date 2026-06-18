from tools.customers import get_customer_profile
from tools.issues import get_open_issues
from tools.history import get_issue_history
from tools.next_action import get_next_action

TOOLS = {
    "get_customer_profile": get_customer_profile,
    "get_open_issues": get_open_issues,
    "get_issue_history": get_issue_history,
    "get_next_action": get_next_action,
}

TOOL_DESCRIPTIONS = """
Available tools:

1. get_customer_profile(customer_name: str)
   Returns customer information.

2. get_open_issues(customer_id: int)
   Returns open issues for a customer.

3. get_issue_history(issue_id: int)
   Returns the history of an issue.

4. get_next_action(issue_id: int)
   Returns the recommended next action for an issue.

Return JSON only in this format:

{
  "tool": "<tool_name>",
  "args": {
    ...
  }
}
"""