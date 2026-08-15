"""Return evidence excerpts only; this example deliberately does not invent an answer."""

import argparse
from pathlib import Path

from from_tensors_to_agents.book_intelligence import build_index, grounded_answer
from from_tensors_to_agents.learned_retrieval import (
    DEFAULT_EMBEDDING_MODEL,
    build_learned_index,
    learned_grounded_answer,
    load_encoder,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", default="What should an experiment record?")
    parser.add_argument("--deterministic", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    index = build_index(root)
    if args.deterministic:
        print("Backend: deterministic hashed vectors")
        print(grounded_answer(index, args.query))
        return
    encoder = load_encoder(DEFAULT_EMBEDDING_MODEL)
    learned = build_learned_index(index, encoder, DEFAULT_EMBEDDING_MODEL)
    print(f"Backend: {DEFAULT_EMBEDDING_MODEL}")
    print(learned_grounded_answer(learned, args.query, encoder))


if __name__ == "__main__":
    main()
