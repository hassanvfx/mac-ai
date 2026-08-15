"""A framework-neutral checkpoint used before demonstrating the same flow in LangGraph."""

from pathlib import Path

from from_tensors_to_agents.book_intelligence import (
    ApprovalCheckpoint,
    build_index,
    propose_improvement,
)


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    proposal = propose_improvement(build_index(root), "add a benchmark to the embeddings chapter")
    checkpoint = ApprovalCheckpoint(root / ".book-intelligence" / "approval.json")
    checkpoint.create(proposal)
    print("Proposal saved. Approved:", checkpoint.is_approved())
    print("No manuscript or source file has been changed.")


if __name__ == "__main__":
    main()
