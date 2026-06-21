from agent.agent import run_agent


TEST_QUERIES = [
    "Show me the profile for Globex Manufacturing",
    "Show me the profile for globex manufacturing",
    # "What open issues does customer 1 have?",
    # "Show me the history for issue 1",
    # "What is the next action for issue 1?"
    # "Get the history for issue 1 and then suggest the next action"
]


def run_agent_evaluation(user: dict):
    for query in TEST_QUERIES:
        print("\n" + "=" * 50)
        print("QUERY:")
        print(query)

        try:
            result = run_agent(query, user)

            print("\nANSWER:")
            print(result["answer"])

            print("\nTOOLS USED:")
            for t in result["tool_calls"]:
                print(t)

        except Exception as e:
            print("\nERROR:")
            print(str(e))

USER = {
    "username": "admin",
    "roles": ["admin"]
}


if __name__ == "__main__":
    run_agent_evaluation(USER)