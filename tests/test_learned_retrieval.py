from __future__ import annotations

from pathlib import Path

import numpy as np

from from_tensors_to_agents.book_intelligence import Evidence
from from_tensors_to_agents.learned_retrieval import (
    build_learned_index,
    learned_grounded_answer,
    retrieve_learned,
)


class FakeEncoder:
    def encode(self, texts: list[str], **_: object) -> np.ndarray:
        return np.asarray([[1.0, 0.0] if "tensor" in text.lower() else [0.0, 1.0] for text in texts])


def test_learned_index_preserves_evidence_metadata() -> None:
    evidence = [
        Evidence("research/tensors.md", "research", None, ("goodfellow2016deep",), "tensor shapes", ()),
        Evidence("benchmarks/rag.md", "benchmarks", None, (), "retrieval score", ()),
    ]
    index = build_learned_index(evidence, FakeEncoder(), "fake")
    result = retrieve_learned(index, "tensor question", FakeEncoder(), limit=1)[0]
    assert result.evidence.source == "research/tensors.md"
    assert result.evidence.citations == ("goodfellow2016deep",)


def test_learned_grounded_answer_refuses_empty_or_weak_evidence() -> None:
    empty = build_learned_index([], FakeEncoder(), "fake")
    assert learned_grounded_answer(empty, "tensor question", FakeEncoder()).startswith("No grounded answer")

    evidence = [Evidence("research/rag.md", "research", None, (), "retrieval score", ())]
    index = build_learned_index(evidence, FakeEncoder(), "fake")
    assert learned_grounded_answer(index, "tensor question", FakeEncoder()).startswith("No grounded answer")


def test_learned_grounded_answer_cites_retrieved_repository_path() -> None:
    evidence = [
        Evidence(
            "research/tensors.md",
            "research",
            None,
            ("goodfellow2016deep",),
            "tensor shapes",
            (),
            (("corpus_kind", "research"),),
        )
    ]
    index = build_learned_index(evidence, FakeEncoder(), "fake")
    answer = learned_grounded_answer(index, "tensor question", FakeEncoder())
    assert "[research/tensors.md citations: goodfellow2016deep]" in answer


def test_learned_answer_path_resolves_inside_fixture_corpus(tmp_path: Path) -> None:
    source = tmp_path / "research" / "tensors.md"
    source.parent.mkdir()
    source.write_text("tensor shapes [@goodfellow2016deep]", encoding="utf-8")
    evidence = [
        Evidence(
            "research/tensors.md",
            "research",
            None,
            ("goodfellow2016deep",),
            "tensor shapes",
            (),
        )
    ]
    index = build_learned_index(evidence, FakeEncoder(), "fake")
    answer = learned_grounded_answer(index, "tensor question", FakeEncoder())
    assert "[research/tensors.md" in answer
    assert (tmp_path / evidence[0].source).is_file()
