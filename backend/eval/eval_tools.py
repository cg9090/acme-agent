from tools.customers import get_customer_profile
from tools.issues import get_open_issues, update_issue_status
from tools.history import get_issue_history
from tools.next_action import get_next_action, create_next_action

def run_tests():
    print("\n--- CUSTOMER ---")
    print(get_customer_profile("Globex Manufacturing"))

    print("\n--- OPEN ISSUES ---")
    print(get_open_issues(1))

    print("\n--- ISSUE HISTORY ---")
    print(get_issue_history(1))

    print("\n--- NEXT ACTION ---")
    print(get_next_action(1))

    print("\n--- UPDATE ISSUE STATUS ---")
    print(update_issue_status(1, "Resolved"))

    print("\n--- CREATE NEXT ACTION ---")
    print(
        create_next_action(
            issue_id=1,
            action_text="Contact customer to confirm resolution"
        )
    )

if __name__ == "__main__":
    run_tests()