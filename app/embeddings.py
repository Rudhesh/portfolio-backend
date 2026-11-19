
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


# Load environment variables
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")


# Initialize Gemini client
client = genai.Client(api_key=api_key)


# Embedding configuration
MODEL_NAME = "gemini-embedding-001"
EMBEDDING_DIMENSION = 768


def create_embedding(
    text,
    task_type="RETRIEVAL_DOCUMENT"
):
    """
    Convert text into a vector using Gemini.

    RETRIEVAL_DOCUMENT: Used when storing knowledge.
    RETRIEVAL_QUERY: Used when searching knowledge.
    """

    if not text or not text.strip():
        raise ValueError("Cannot generate an embedding for empty text.")

    response = client.models.embed_content(
        model=MODEL_NAME,
        contents=text,
        config=types.EmbedContentConfig(
            task_type=task_type,
            output_dimensionality=EMBEDDING_DIMENSION
        )
    )

    if not response.embeddings:
        raise ValueError("Gemini returned no embeddings.")

    vector = response.embeddings[0].values

    if len(vector) != EMBEDDING_DIMENSION:
        raise ValueError(
            f"Expected {EMBEDDING_DIMENSION} dimensions, "
            f"but received {len(vector)}."
        )

    return vector


if __name__ == "__main__":
    sample_text = (
        "I am a software developer working with React and Python."
    )

    vector = create_embedding(sample_text)

    print("Embedding generated successfully!")
    print("Vector dimensions:", len(vector))
    print("First five numbers:", vector[:5])
