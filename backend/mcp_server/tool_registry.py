from mcp_server.tools.customers import get_customer_profile
from mcp_server.tools.issues import get_open_issues, update_issue_status
from mcp_server.tools.history import get_issue_history
from mcp_server.tools.next_action import get_next_action, create_next_action

TOOLS = {
    "get_customer_profile": {
        "function": get_customer_profile,
        "description": "Returns customer information.",
        "roles": ["sales_user", "admin"],
        "schema": {
            "customer_name": "string"
        }
    },

    "get_open_issues": {
        "function": get_open_issues,
        "description": "Returns open issues for a customer.",
        "roles": ["sales_user", "support_user", "admin"],
        "schema": {
            "customer_id": "integer"
        }
    },

    "get_issue_history": {
        "function": get_issue_history,
        "description": "Returns the history of an issue.",
        "roles": ["sales_user", "support_user", "admin"],
        "schema": {
            "issue_id": "integer"
        }
    },

    "get_next_action": {
        "function": get_next_action,
        "description": "Returns the recommended next action.",
        "roles": ["admin"],
        "schema": {
            "issue_id": "integer"
        }
    },

    "update_issue_status": {
        "function": update_issue_status,
        "description": "Updates issue status.",
        "roles": ["support_user", "admin"],
        "schema": {
            "issue_id": "integer",
            "status": "string"
        }
    },

    "create_next_action": {
        "function": create_next_action,
        "description": "Creates a next action.",
        "roles": ["admin"],
        "schema": {
            "issue_id": "integer",
            "action_text": "string"
        }
    }
}