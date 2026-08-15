"""Build a deterministic local semantic index for the book corpus."""

from pathlib import Path

from from_tensors_to_agents.book_intelligence import build_index, retrieve, save_index


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    output = root / ".book-intelligence" / "index.json"
    index = build_index(root)
    save_index(index, output)
    print(f"Indexed {len(index)} chunks in {output}")
    for result in retrieve(index, "How do embeddings support RAG?"):
        print(f"{result.score:.3f} {result.evidence.source}")


if __name__ == "__main__":
    main()
