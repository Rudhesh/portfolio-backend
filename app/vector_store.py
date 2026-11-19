
import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient, models


# Load environment variables
load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

COLLECTION_NAME = "personal_portfolio_knowledge"
VECTOR_SIZE = 768


# Validate credentials
if not QDRANT_URL or not QDRANT_API_KEY:
    raise ValueError("Qdrant credentials are missing from .env")


# Connect to Qdrant Cloud
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)


def create_collection():
    """
    Create the collection if it does not exist,
    and ensure the source payload index exists.
    """

    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE
            )
        )

        print("Qdrant collection created successfully!")
    else:
        print("Collection already exists.")

    # Create an index so Qdrant can filter by source.
    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="source",
        field_schema=models.PayloadSchemaType.KEYWORD,
        wait=True
    )

    print("Source payload index is ready!")


def save_chunks(chunks, embeddings):
    """
    Replace the existing about_me.md chunks
    with the latest document chunks.
    """

    if len(chunks) != len(embeddings):
        raise ValueError(
            "Chunks and embeddings count do not match."
        )

    # Prepare Qdrant points
    points = []

    for index, (chunk, embedding) in enumerate(
        zip(chunks, embeddings)
    ):
        if len(embedding) != VECTOR_SIZE:
            raise ValueError(
                f"Chunk {index} has an invalid vector dimension."
            )

        point = models.PointStruct(
            id=index,
            vector=embedding,
            payload={
                "text": chunk,
                "source": "about_me.md"
            }
        )

        points.append(point)

    # Delete old chunks belonging to this source
    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="source",
                        match=models.MatchValue(
                            value="about_me.md"
                        )
                    )
                ]
            )
        ),
        wait=True
    )

    # Upload the latest chunks
    if points:
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
            wait=True
        )

    print(
        f"Successfully uploaded {len(points)} chunks!"
    )


def search_chunks(query_vector, limit=3):
    """
    Search Qdrant for the most relevant chunks.
    """

    if len(query_vector) != VECTOR_SIZE:
        raise ValueError(
            f"Query vector must have {VECTOR_SIZE} dimensions."
        )

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
        with_payload=True
    )

    return results.points


if __name__ == "__main__":
    create_collection()
    print("Qdrant connection successful!")
