"""Search the book corpus with learned embeddings or deterministic fallback."""

import argparse
from pathlib import Path

from from_tensors_to_agents.book_intelligence import build_index, retrieve, save_index
from from_tensors_to_agents.learned_retrieval import (
    DEFAULT_EMBEDDING_MODEL,
    build_learned_index,
    load_encoder,
    retrieve_learned,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", default="How do embeddings support RAG?")
    parser.add_argument("--deterministic", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    output = root / ".book-intelligence" / "index.json"
    index = build_index(root)
    save_index(index, output)
    print(f"Indexed {len(index)} chunks in {output}")
    if args.deterministic:
        results = retrieve(index, args.query)
        print("Backend: deterministic hashed vectors")
    else:
        encoder = load_encoder(DEFAULT_EMBEDDING_MODEL)
        learned = build_learned_index(index, encoder, DEFAULT_EMBEDDING_MODEL)
        results = retrieve_learned(learned, args.query, encoder)
        print(f"Backend: {DEFAULT_EMBEDDING_MODEL}")
    for result in results:
        print(f"{result.score:.3f} {result.evidence.source}")


if __name__ == "__main__":
    main()
