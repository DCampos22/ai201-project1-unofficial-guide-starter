import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_documents, chunk_text

def build_vector_store():
    # Load and chunk documents
    print("Loading and chunking documents...")
    documents = load_documents()
    all_chunks = []
    for doc in documents:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            if len(chunk.split()) > 30:
                all_chunks.append({
                    "source": doc["source"],
                    "chunk": chunk,
                    "chunk_index": i
                })
    print(f"Total chunks to embed: {len(all_chunks)}")

    # Load embedding model
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Set up ChromaDB
    client = chromadb.Client()
    collection = client.create_collection("qc_cs_guide")

    # Embed and store chunks
    print("Embedding and storing chunks...")
    texts = [c["chunk"] for c in all_chunks]
    embeddings = model.encode(texts, show_progress_bar=True)

    collection.add(
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=[{"source": c["source"], "chunk_index": c["chunk_index"]} for c in all_chunks],
        ids=[f"{c['source']}_{c['chunk_index']}" for c in all_chunks]
    )
    print("Done! Vector store ready.\n")
    return collection, model


def retrieve(query, collection, model, k=5):
    query_embedding = model.encode([query])[0]
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=k
    )
    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    return list(zip(chunks, metadatas, distances))


if __name__ == "__main__":
    collection, model = build_vector_store()

    test_queries = [
        "What courses are required for the CS BA degree?",
        "What do students say about Professor Goswami?",
        "What is the prerequisite for CS 320?",
    ]

    for query in test_queries:
        print(f"QUERY: {query}")
        print("-" * 60)
        results = retrieve(query, collection, model)
        for chunk, metadata, distance in results:
            print(f"[{metadata['source']}] distance: {round(distance, 3)}")
            print(chunk[:300])
            print()
        print("=" * 60 + "\n")