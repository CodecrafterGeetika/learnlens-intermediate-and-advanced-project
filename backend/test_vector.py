from app.vector_store import create_index, search_index


chunks = [
    "SQL is a language used to manage and query relational databases.",
    "A primary key uniquely identifies each row in a table.",
    "A JOIN combines rows from two or more tables using a related column.",
    "GROUP BY groups rows that have the same values in specified columns."
]


index = create_index(chunks)

query = "How can I combine two tables?"

results = search_index(index, query, chunks, top_k=2)

for result in results:
    print("\n--- Result ---")
    print(result["chunk"])
    print("Distance:", result["distance"])