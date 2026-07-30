"""
retriever.py
Given a user query, embed it and search ChromaDB for the top-k most similar chunks.
"""

import chromadb
import config
from ingest import get_embedding_function


def retrieve(query: str, k: int = None):
    """Returns a list of dicts: [{"text": ..., "source": ..., "score": ...}, ...]"""
    k = k or config.TOP_K

    client = chromadb.PersistentClient(path=config.CHROMA_DB_DIR)
    collection = client.get_or_create_collection(config.COLLECTION_NAME)

    embed = get_embedding_function()
    query_embedding = embed([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
    )

    output = []
    docs = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for doc, meta, dist in zip(docs, metadatas, distances):
        output.append({"text": doc, "source": meta.get("source"), "score": dist})

    return output


if __name__ == "__main__":
    # quick manual test: python retriever.py
    q = input("Test query: ")
    for r in retrieve(q):
        print(f"\n[{r['source']}] (score={r['score']:.4f})\n{r['text'][:200]}...")
