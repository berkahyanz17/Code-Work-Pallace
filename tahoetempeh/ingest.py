"""
ingest.py
Run this whenever your dataset changes.

Flow:
  1. Read files from data/raw/
  2. Split into chunks
  3. Embed each chunk
  4. Store (text + embedding + metadata) into ChromaDB

Usage:
  python ingest.py
"""

import os
import glob
import chromadb

import config


def load_raw_files(raw_dir: str):
    """Read all .txt / .md files from raw_dir. Extend this for .pdf, .docx, etc."""
    paths = glob.glob(os.path.join(raw_dir, "**", "*.txt"), recursive=True)
    paths += glob.glob(os.path.join(raw_dir, "**", "*.md"), recursive=True)

    documents = []
    for path in paths:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        documents.append({"source": path, "text": text})
    return documents


def chunk_text(text: str, chunk_size: int, overlap: int):
    """Naive fixed-size chunking with overlap. Swap for a smarter splitter later if needed."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def get_embedding_function():
    """Returns a function: List[str] -> List[List[float]]"""
    if config.EMBEDDING_MODE == "local":
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(config.LOCAL_EMBEDDING_MODEL)

        def embed(texts):
            return model.encode(texts, show_progress_bar=False).tolist()

        return embed

    elif config.EMBEDDING_MODE == "gemini":
        import google.generativeai as genai
        genai.configure(api_key=config.GEMINI_API_KEY)

        def embed(texts):
            vectors = []
            for t in texts:
                result = genai.embed_content(
                    model=config.GEMINI_EMBEDDING_MODEL,
                    content=t,
                )
                vectors.append(result["embedding"])
            return vectors

        return embed

    else:
        raise ValueError(f"Unknown EMBEDDING_MODE: {config.EMBEDDING_MODE}")


def main():
    print("Loading raw files...")
    documents = load_raw_files(config.RAW_DATA_DIR)
    if not documents:
        print(f"No files found in {config.RAW_DATA_DIR}. Add some .txt/.md files first.")
        return

    print(f"Found {len(documents)} document(s). Chunking...")
    all_chunks, all_ids, all_metadatas = [], [], []
    chunk_counter = 0
    for doc in documents:
        chunks = chunk_text(doc["text"], config.CHUNK_SIZE, config.CHUNK_OVERLAP)
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_ids.append(f"chunk_{chunk_counter}")
            all_metadatas.append({"source": doc["source"], "chunk_index": i})
            chunk_counter += 1

    print(f"Created {len(all_chunks)} chunks. Embedding...")
    embed = get_embedding_function()
    embeddings = embed(all_chunks)

    print("Storing in ChromaDB...")
    client = chromadb.PersistentClient(path=config.CHROMA_DB_DIR)
    collection = client.get_or_create_collection(config.COLLECTION_NAME)

    collection.add(
        ids=all_ids,
        documents=all_chunks,
        embeddings=embeddings,
        metadatas=all_metadatas,
    )

    print(f"Done. {len(all_chunks)} chunks stored in collection '{config.COLLECTION_NAME}'.")


if __name__ == "__main__":
    main()
