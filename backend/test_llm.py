from app.llm import generate_answer


context = """
A LEFT JOIN returns all rows from the left table
and matching rows from the right table.
Non-matching rows contain NULL values.
"""


answer = generate_answer(
    "What is a LEFT JOIN?",
    context
)

print("\n--- LearnLens Answer ---")
print(answer)