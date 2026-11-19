
from app.retrieval import retrieve_knowledge
from app.generation import generate_answer


def ask_question(question):

    print("Retrieving relevant knowledge...")

    results = retrieve_knowledge(question)

    if not results:
        return "I don't have enough information to answer that question."

    # Combine retrieved chunks into one context
    context = "\n\n".join(
        result["text"] for result in results
    )

    print("Generating answer with Gemini...")

    answer = generate_answer(question, context)

    return answer


if __name__ == "__main__":

    question = "What technologies does Rudhesh work with?"

    answer = ask_question(question)

    print("\nAI Assistant:")
    print(answer)
