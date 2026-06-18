import os
from dotenv import load_dotenv
from anthropic import Anthropic
from llm.base import LLMClient

load_dotenv()


class ClaudeClient(LLMClient):
    def __init__(self):
        self.client = Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

    def generate(self, prompt: str) -> str:
        response = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )

        return response.content[0].text