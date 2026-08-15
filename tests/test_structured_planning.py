from __future__ import annotations

from pathlib import Path

import pytest

from from_tensors_to_agents.book_intelligence import Evidence, SearchResult
from from_tensors_to_agents.structured_planning import (
    ConfigurationError,
    StructuredPlan,
    direct_plan,
    direct_review,
    langchain_plan,
    langchain_review,
    openai_responder_from_environment,
)


def results() -> list[SearchResult]:
    evidence = Evidence(
        "book/chapters/08-turning-meaning-into-geometry.md",
        "book",
        "08",
        ("reimers2019sentencebert",),
        "Embeddings make meaning searchable.",
        (),
    )
    return [SearchResult(evidence, 0.9)]


def responder(_: str, __: str, schema: type[StructuredPlan]) -> dict[str, object]:
    return {
        "objective": "ignored",
        "evidence_paths": ["book/chapters/08-turning-meaning-into-geometry.md", "outside.md"],
        "steps": ["Inspect the retrieved evidence."],
        "unsupported_claim_warnings": [],
        "approval_required": False,
    }


class FakeRunnable:
    def __init__(self, response: object):
        self.response = response

    def invoke(self, _: object) -> object:
        return self.response


class FakeModel:
    def __init__(self, response: object):
        self.response = response

    def with_structured_output(self, _: type[StructuredPlan], **__: object) -> FakeRunnable:
        return FakeRunnable(self.response)


def test_direct_plan_rejects_unsupported_paths_and_forces_approval() -> None:
    proposal = direct_plan(responder, "Improve Chapter 8", results())
    assert proposal.objective == "Improve Chapter 8"
    assert proposal.evidence_paths == ["book/chapters/08-turning-meaning-into-geometry.md"]
    assert proposal.approval_required
    assert proposal.unsupported_claim_warnings == ["Rejected unsupported evidence paths: outside.md"]


def test_direct_plan_with_no_evidence_clears_write_like_steps() -> None:
    proposal = direct_plan(responder, "Change a chapter", [])
    assert proposal.steps == []
    assert "No retrieved evidence" in proposal.unsupported_claim_warnings[-1]


def test_direct_review_uses_only_retrieved_paths(tmp_path: Path) -> None:
    chapter = tmp_path / "book" / "chapters" / "08.md"
    chapter.parent.mkdir(parents=True)
    chapter.write_text("# Draft", encoding="utf-8")
    critique = direct_review(responder, "Review", results(), tmp_path)
    assert critique.evidence_paths == ["book/chapters/08-turning-meaning-into-geometry.md"]
    assert critique.approval_required


def test_langchain_plan_uses_the_same_evidence_contract() -> None:
    response = {
        "parsed": StructuredPlan(
            objective="ignored",
            evidence_paths=["book/chapters/08-turning-meaning-into-geometry.md"],
            steps=["Inspect the retrieved evidence."],
            approval_required=False,
        ),
        "parsing_error": None,
    }
    proposal = langchain_plan(FakeModel(response), "Improve Chapter 8", results())
    assert proposal.evidence_paths == ["book/chapters/08-turning-meaning-into-geometry.md"]
    assert proposal.approval_required


def test_langchain_rejects_a_parse_failure(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="valid structured review"):
        langchain_review(FakeModel({"parsed": None, "parsing_error": ValueError("bad json")}), "Review", results(), tmp_path)


def test_missing_api_configuration_fails_before_a_network_call(monkeypatch: pytest.MonkeyPatch) -> None:
    for variable in ("BOOK_INTELLIGENCE_API_KEY", "BOOK_INTELLIGENCE_API_BASE", "BOOK_INTELLIGENCE_MODEL"):
        monkeypatch.delenv(variable, raising=False)
    with pytest.raises(ConfigurationError):
        openai_responder_from_environment()


def test_langchain_openai_adapter_exposes_structured_output_without_network() -> None:
    from langchain_openai import ChatOpenAI

    model = ChatOpenAI(model="test", api_key="not-a-real-key", base_url="http://localhost:9/v1")
    assert model.with_structured_output(StructuredPlan, include_raw=True) is not None
