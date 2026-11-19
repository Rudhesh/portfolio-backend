
from app.ingestion import load_knowledge
from app.chunking import split_into_chunks
from app.embeddings import create_embedding
from app.vector_store import create_collection, save_chunks
from app.vector_store import search_chunks

def ingest_knowledge():

    print("Loading knowledge...")

    document = load_knowledge()

    print("Splitting document into chunks...")

    chunks = split_into_chunks(document)

    print(f"Total chunks: {len(chunks)}")

    print("Generating embeddings...")

    embeddings = []

    for index, chunk in enumerate(chunks):
        print(f"Embedding chunk {index + 1}/{len(chunks)}")

        vector = create_embedding(chunk)

        embeddings.append(vector)

    print("Creating Qdrant collection...")

    create_collection()

    print("Uploading chunks to Qdrant...")

    save_chunks(chunks, embeddings)

    print("Ingestion completed successfully!")


def search_chunks(query_vector, limit=3):

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
        with_payload=True
    )

    return results.points



if __name__ == "__main__":
    ingest_knowledge()
