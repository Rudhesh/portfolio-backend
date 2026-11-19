
def split_into_chunks(text, chunk_size=500, overlap=50):
    if not isinstance(text, str):
        raise TypeError("Input text must be a string.")

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size.")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


if __name__ == "__main__":
    from app.ingestion import load_knowledge

    document = load_knowledge()
    chunks = split_into_chunks(document)

    print(f"Total chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks):
        print(f"\n--- Chunk {index + 1} ---")
        print(chunk)
