"""
main.py
Simple CLI for testing the RAG pipeline before wiring it into Telegram.

Usage:
  python main.py
"""

from rag_pipeline import ask


def main():
    print("RAG CLI. Type 'exit' to quit.\n")
    while True:
        query = input("You: ").strip()
        if query.lower() in ("exit", "quit"):
            break
        if not query:
            continue

        result = ask(query)
        print(f"\nAnswer: {result['answer']}")
        print(f"Sources: {result['sources']}\n")


if __name__ == "__main__":
    main()
