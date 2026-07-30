"""
rag_pipeline.py
Single entry point: ask(query) -> retrieves context, generates answer.
This is the function you'll call from main.py or your Telegram bot handler.
"""

from retriever import retrieve
from generator import generate


def ask(query: str, k: int = None) -> dict:
    context_chunks = retrieve(query, k=k)
    answer = generate(query, context_chunks)

    return {
        "query": query,
        "answer": answer,
        "sources": [c["source"] for c in context_chunks],
    }
