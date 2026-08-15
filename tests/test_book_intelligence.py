from pathlib import Path

from from_tensors_to_agents.book_intelligence import (
    ApprovalCheckpoint,
    build_index,
    grounded_answer,
    propose_improvement,
    retrieve,
    review_corpus,
    save_index,
)


def make_corpus(root: Path) -> None:
    (root / "research").mkdir(parents=True)
    (root / "book" / "chapters").mkdir(parents=True)
    (root / "experiments").mkdir()
    (root / "benchmarks").mkdir()
    (root / "research" / "notes.md").write_text("Embeddings use cosine similarity. [@vaswani2017attention]")
    (root / "book" / "chapters" / "08-embeddings.md").write_text(
        "# Embeddings\n\n## Alternatives and takeaway\n\nUse semantic retrieval carefully."
    )
    (root / "experiments" / "search.py").write_text("def search_embeddings(): pass")
    (root / "benchmarks" / "results.md").write_text("Device: MPS. Retrieval benchmark.")


def test_retrieval_preserves_source_and_citation(tmp_path: Path) -> None:
    make_corpus(tmp_path)
    results = retrieve(build_index(tmp_path), "cosine similarity embeddings")
    assert results[0].evidence.source == "research/notes.md"
    assert results[0].evidence.citations == ("vaswani2017attention",)


def test_grounded_answer_refuses_missing_evidence(tmp_path: Path) -> None:
    make_corpus(tmp_path)
    assert grounded_answer(build_index(tmp_path), "unrelated legal compliance").startswith("No grounded answer")


def test_plan_requires_approval_and_checkpoint_never_touches_sources(tmp_path: Path) -> None:
    make_corpus(tmp_path)
    proposal = propose_improvement(build_index(tmp_path), "improve embeddings experiment")
    checkpoint = ApprovalCheckpoint(tmp_path / "local-cache" / "checkpoint.json")
    checkpoint.create(proposal)
    assert proposal.approval_required
    assert not checkpoint.is_approved()
    checkpoint.approve(True)
    assert checkpoint.is_approved()
    assert (tmp_path / "book" / "chapters" / "08-embeddings.md").read_text() != ""


def test_review_finds_unresolved_links(tmp_path: Path) -> None:
    make_corpus(tmp_path)
    chapter = tmp_path / "book" / "chapters" / "08-embeddings.md"
    chapter.write_text("# Embeddings\n\n[Missing](missing.md)")
    assert any("unresolved link" in finding for finding in review_corpus(tmp_path))


def test_saved_indexes_are_local_artifacts(tmp_path: Path) -> None:
    make_corpus(tmp_path)
    output = tmp_path / "local-cache" / "index.json"
    save_index(build_index(tmp_path), output)
    assert output.exists()
