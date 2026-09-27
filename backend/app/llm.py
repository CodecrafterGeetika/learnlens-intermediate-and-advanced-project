import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)



def generate_answer(question: str, context: str, mode: str = "simple"):

    mode_instructions = {

        "simple": """
Explain the concept like you are teaching a complete beginner.
Use simple language and a small example when useful.
Avoid unnecessary technical complexity.
""",

        "exam": """
Give a structured exam-style answer.
Start with a clear definition.
Then explain the concept using important points.
Use headings or bullet points where helpful.
Make the answer suitable for writing in a college exam.
""",

        "revision": """
Give a short revision-friendly answer.
Use concise bullet points.
Highlight important keywords.
Focus only on the most important information needed for quick revision.
""",

        "viva": """
Explain the concept clearly and then provide possible viva questions
with short answers.
Focus on questions a teacher might ask to test understanding.
"""
    }

    instruction = mode_instructions.get(
        mode,
        mode_instructions["simple"]
    )

    prompt = f"""
You are LearnLens AI, an evidence-grounded document learning assistant.

Answer the user's question using ONLY the provided document context.

If the answer cannot be found in the context, say:
"I couldn't find the answer in the uploaded document."

Do not invent facts or use outside knowledge.

Learning mode:
{mode}

Mode instructions:
{instruction}

Document context:
{context}

User question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content

