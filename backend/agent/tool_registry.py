from tools.customers import get_customer_profile
from tools.issues import get_open_issues, update_issue_status
from tools.history import get_issue_history
from tools.next_action import get_next_action, create_next_action

TOOLS = {
    "get_customer_profile": get_customer_profile,
    "get_open_issues": get_open_issues,
    "get_issue_history": get_issue_history,
    "get_next_action": get_next_action,
    "update_issue_status": update_issue_status,
    "create_next_action": create_next_action
}

TOOL_PERMISSIONS = {
    "get_customer_profile": [
        "sales_user",
        "admin"
    ],
    "get_open_issues": [
        "sales_user",
        "support_user",
        "admin"
    ],
    "get_issue_history": [
        "support_user",
        "sales_user",
        "admin"
    ],
    "get_next_action": [
        "admin"
    ],

    "update_issue_status": [
        "support_user",
        "admin",
    ],

    "create_next_action": [
        "admin",
    ],
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

5. update_issue_status(issue_id: int, status: str)
   Updates the status of an issue.

6. create_next_action(issue_id: int, action_text: str)
   Creates a new next action for an issue.

Return JSON only in this format:

{
  "tool": "<tool_name>",
  "args": {
    ...
  }
}
"""