from agent.agent import run_agent


TEST_QUERIES = [
    "Show me the profile for Globex Manufacturing",
    "What open issues does customer 1 have?",
    "Show me the history for issue 1",
    "What is the next action for issue 1?"
]


def run_agent_evaluation():
    for query in TEST_QUERIES:
        print("\n" + "=" * 50)
        print("QUERY:")
        print(query)

        try:
            result = run_agent(query)

            print("\nRESULT:")
            print(result)

        except Exception as e:
            print("\nERROR:")
            print(str(e))


if __name__ == "__main__":
    run_agent_evaluation()