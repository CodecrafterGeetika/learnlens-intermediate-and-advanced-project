import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class QueryRewriter:

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        self.client = Groq(api_key=api_key)

        self.model = "openai/gpt-oss-20b"

    def rewrite(self, question: str) -> str:

        prompt = f"""
You are a search query rewriting component in a RAG system.

Your job is ONLY to rewrite the user's question
into a clearer and more specific search query.

Rules:
- Preserve the original meaning.
- Do not answer the question.
- Do not add unrelated information.
- Expand vague references when possible.
- Return ONLY the rewritten query.
- Do not add explanations or quotation marks.

User question:
{question}

Rewritten search query:
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        return response.choices[0].message.content.strip()