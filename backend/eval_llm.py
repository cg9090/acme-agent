from llm.gemini import generate


def run_llm_evaluation():
    print("Testing Gemini connection...")

    response = generate(
        "Reply with exactly the word: SUCCESS"
    )

    print(response)


if __name__ == "__main__":
    run_llm_evaluation()