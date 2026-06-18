import requests

TEST_CASES = [
    "Show me the profile for Globex Manufacturing",
    "What open issues does Globex have?",
    "What is the history of issue 1?",
    "What is the next action for issue 1?"
]


def run_api_eval():
    for query in TEST_CASES:
        print("\n" + "=" * 50)
        print("QUERY:", query)

        response = requests.post(
            "http://127.0.0.1:8000/agent",
            json={"query": query}
        )

        try:
            data = response.json()
        except Exception:
            print("FAILED TO PARSE RESPONSE")
            print(response.text)
            continue

        print("\nRESPONSE:")
        print(data)


if __name__ == "__main__":
    run_api_eval()