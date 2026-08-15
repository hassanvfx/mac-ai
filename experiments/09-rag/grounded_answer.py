"""Return evidence excerpts only; this example deliberately does not invent an answer."""

from pathlib import Path

from from_tensors_to_agents.book_intelligence import build_index, grounded_answer


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    print(grounded_answer(build_index(root), "What should an experiment record?"))


if __name__ == "__main__":
    main()
