import os

from groq import Groq
from dotenv import load_dotenv


load_dotenv()


class LLMService:

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        self.client = Groq(
            api_key=api_key
        )

        self.model = "openai/gpt-oss-20b"


    def generate(
        self,
        question: str,
        context: str,
        mode: str = "simple"
    ):

        mode_instructions = {

            "simple": """
Explain the answer in a simple, beginner-friendly way.
Use clear language and short paragraphs.
Use examples only when they are supported by the document.
""",

            "exam": """
Give an exam-ready answer.

Start with a clear definition.
Then provide important points in an organized manner.
Use headings or bullet points when useful.
Keep the answer suitable for writing in an exam.
Do not add information that is not supported by the document.
""",

            "revision": """
Give a quick revision answer.

Use short bullet points.
Focus only on the most important concepts,
keywords, and facts.
Keep the answer concise and easy to revise.
""",

            "viva": """
Act like a viva preparation assistant.

First, give a clear and concise answer to the question.

Then provide:

### Possible Viva Questions

Give 2 or 3 likely follow-up questions
based ONLY on the document context.

### Quick Check

Give 1 short question that the student
can answer themselves.

Do not provide answers to the follow-up
or quick-check questions.

Do not add information that is not supported
by the document.
"""
        }


        instruction = mode_instructions.get(
            mode,
            mode_instructions["simple"]
        )


        prompt = f"""
You are LearnLens AI,
a document question-answering assistant.

Answer the user's question using ONLY
the provided document context.

{instruction}

If the answer cannot be found in the context,
say:

"I could not find the answer in the provided documents."

Do not use outside knowledge.
Do not invent facts.

Document Context:
{context}

Question:
{question}

Answer:
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


        return response.choices[0].message.content