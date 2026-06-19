from agent.agent import run_agent


TEST_QUERIES = [
    "Show me the profile for Globex Manufacturing",
    "What open issues does customer 1 have?",
    "Update issue 1 to Resolved",
    "Create a next action for issue 1",
]


USERS = [
    {
        "username": "alice",
        "roles": ["sales_user"]
    },
    {
        "username": "bob",
        "roles": ["support_user"]
    },
    {
        "username": "admin",
        "roles": ["admin"]
    }
]


def run_eval():
    for user in USERS:
        print("\n" + "#" * 60)
        print(f"USER: {user['username']} | ROLES: {user['roles']}")

        for query in TEST_QUERIES:
            print("\n" + "-" * 50)
            print("QUERY:", query)

            result = run_agent(query, user)

            print("RESULT:", result)


if __name__ == "__main__":
    run_eval()