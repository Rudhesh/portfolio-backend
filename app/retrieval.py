
from app.embeddings import create_embedding
from app.vector_store import search_chunks


def retrieve_knowledge(question):

    print("Creating question embedding...")

    question_vector = create_embedding(question)

    print("Searching Qdrant...")

    results = search_chunks(question_vector, limit=3)

    retrieved_chunks = []

    for result in results:
        retrieved_chunks.append({
            "text": result.payload["text"],
            "score": result.score
        })

    return retrieved_chunks


if __name__ == "__main__":

    question = "What technologies does Rudhesh use?"

    results = retrieve_knowledge(question)

    print("\nRetrieved knowledge:")

    for index, result in enumerate(results):
        print(f"\n--- Result {index + 1} ---")
        print("Score:", result["score"])
        print("Text:", result["text"])
