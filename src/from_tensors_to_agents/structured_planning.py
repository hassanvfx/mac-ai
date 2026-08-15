"""Optional direct-SDK and LangChain planning over constrained book evidence."""

from __future__ import annotations

import os
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Protocol

from pydantic import BaseModel, Field

from from_tensors_to_agents.book_intelligence import SearchResult, review_corpus


class ConfigurationError(RuntimeError):
    """Raised before a network call when optional API configuration is absent."""


class StructuredPlan(BaseModel):
    """A proposal only; it is never authorization to change repository state."""

    objective: str
    evidence_paths: list[str] = Field(default_factory=list)
    steps: list[str] = Field(default_factory=list)
    unsupported_claim_warnings: list[str] = Field(default_factory=list)
    approval_required: bool = True


class StructuredReview(BaseModel):
    objective: str
    evidence_paths: list[str] = Field(default_factory=list)
    findings: list[str] = Field(default_factory=list)
    approval_required: bool = True


class Runnable(Protocol):
    def invoke(self, input: object) -> object: ...


class StructuredModel(Protocol):
    def with_structured_output(self, schema: type[BaseModel], **kwargs: object) -> Runnable: ...


JsonResponder = Callable[[str, str, type[BaseModel]], Mapping[str, object]]

SYSTEM_PROMPT = """You are the Book Intelligence Assistant. Use only the supplied repository evidence.
Do not claim that a change is applied. Do not request or perform writes, Git actions, or external actions.
Every cited path must be one of the supplied evidence paths. Human approval is always required."""


def evidence_paths(results: Sequence[SearchResult]) -> list[str]:
    return sorted({result.evidence.source for result in results})


def evidence_context(results: Sequence[SearchResult]) -> str:
    if not results:
        return "No retrieved evidence is available. Return a warning and no implementation steps."
    entries = []
    for result in results:
        citation_text = ", ".join(result.evidence.citations) or "none"
        entries.append(
            f"PATH: {result.evidence.source}\nCITATIONS: {citation_text}\nEXCERPT:\n{result.evidence.text}"
        )
    return "\n\n---\n\n".join(entries)


def plan_prompt(objective: str, results: Sequence[SearchResult]) -> str:
    return (
        f"Objective: {objective}\n\n"
        f"Allowed evidence:\n{evidence_context(results)}\n\n"
        "Return a structured plan. Include unsupported-claim warnings and set approval_required to true."
    )


def review_prompt(objective: str, results: Sequence[SearchResult], corpus_findings: Sequence[str]) -> str:
    findings = "\n".join(corpus_findings) or "No mechanical corpus findings."
    return (
        f"Review objective: {objective}\n\nAllowed evidence:\n{evidence_context(results)}\n\n"
        f"Mechanical review findings:\n{findings}\n\n"
        "Return a structured critique. Include unsupported claims, missing experiments, broken links, or "
        "missing alternatives when supported by these inputs. Set approval_required to true."
    )


def validate_plan(raw: Mapping[str, object], objective: str, allowed_paths: Sequence[str]) -> StructuredPlan:
    proposal = StructuredPlan.model_validate(raw)
    permitted = set(allowed_paths)
    cited = [path for path in proposal.evidence_paths if path in permitted]
    rejected = sorted(set(proposal.evidence_paths) - permitted)
    warnings = list(proposal.unsupported_claim_warnings)
    if rejected:
        warnings.append(f"Rejected unsupported evidence paths: {', '.join(rejected)}")
    if not permitted:
        warnings.append("No retrieved evidence: do not make an implementation claim.")
    return StructuredPlan(
        objective=objective,
        evidence_paths=cited,
        steps=[] if not permitted else proposal.steps,
        unsupported_claim_warnings=warnings,
        approval_required=True,
    )


def validate_review(raw: Mapping[str, object], objective: str, allowed_paths: Sequence[str]) -> StructuredReview:
    critique = StructuredReview.model_validate(raw)
    permitted = set(allowed_paths)
    cited = [path for path in critique.evidence_paths if path in permitted]
    rejected = sorted(set(critique.evidence_paths) - permitted)
    findings = list(critique.findings)
    if rejected:
        findings.append(f"Rejected unsupported evidence paths: {', '.join(rejected)}")
    if not permitted:
        findings.append("No retrieved evidence: no grounded critique is available.")
    return StructuredReview(
        objective=objective,
        evidence_paths=cited,
        findings=findings,
        approval_required=True,
    )


def direct_plan(responder: JsonResponder, objective: str, results: Sequence[SearchResult]) -> StructuredPlan:
    allowed = evidence_paths(results)
    raw = responder(SYSTEM_PROMPT, plan_prompt(objective, results), StructuredPlan)
    return validate_plan(raw, objective, allowed)


def direct_review(
    responder: JsonResponder,
    objective: str,
    results: Sequence[SearchResult],
    corpus_root: Path,
) -> StructuredReview:
    allowed = evidence_paths(results)
    raw = responder(
        SYSTEM_PROMPT,
        review_prompt(objective, results, review_corpus(corpus_root)),
        StructuredReview,
    )
    return validate_review(raw, objective, allowed)


def openai_responder_from_environment() -> JsonResponder:
    """Build the opt-in OpenAI-compatible responder without exposing credentials."""
    api_key = os.environ.get("BOOK_INTELLIGENCE_API_KEY")
    base_url = os.environ.get("BOOK_INTELLIGENCE_API_BASE")
    model = os.environ.get("BOOK_INTELLIGENCE_MODEL")
    if not api_key or not base_url or not model:
        raise ConfigurationError(
            "Set BOOK_INTELLIGENCE_API_KEY, BOOK_INTELLIGENCE_API_BASE, and BOOK_INTELLIGENCE_MODEL."
        )
    from openai import OpenAI

    client = OpenAI(api_key=api_key, base_url=base_url)

    def respond(system: str, prompt: str, schema: type[BaseModel]) -> Mapping[str, object]:
        completion = client.chat.completions.parse(
            model=model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            response_format=schema,
        )
        parsed = completion.choices[0].message.parsed
        if parsed is None:
            raise RuntimeError("The direct SDK returned no parsed structured response.")
        return parsed.model_dump()

    return respond


def langchain_model_from_environment() -> StructuredModel:
    """Build an opt-in LangChain OpenAI-compatible model without a network call."""
    api_key = os.environ.get("BOOK_INTELLIGENCE_API_KEY")
    base_url = os.environ.get("BOOK_INTELLIGENCE_API_BASE")
    model = os.environ.get("BOOK_INTELLIGENCE_MODEL")
    if not api_key or not base_url or not model:
        raise ConfigurationError(
            "Set BOOK_INTELLIGENCE_API_KEY, BOOK_INTELLIGENCE_API_BASE, and BOOK_INTELLIGENCE_MODEL."
        )
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(model=model, api_key=api_key, base_url=base_url, temperature=0)


def langchain_plan(model: StructuredModel, objective: str, results: Sequence[SearchResult]) -> StructuredPlan:
    allowed = evidence_paths(results)
    response = model.with_structured_output(StructuredPlan, include_raw=True).invoke(
        [("system", SYSTEM_PROMPT), ("human", plan_prompt(objective, results))]
    )
    if not isinstance(response, Mapping) or response.get("parsing_error") or response.get("parsed") is None:
        raise RuntimeError("LangChain did not return a valid structured plan.")
    parsed = response["parsed"]
    raw = parsed.model_dump() if isinstance(parsed, BaseModel) else parsed
    if not isinstance(raw, Mapping):
        raise TypeError("LangChain returned a non-mapping structured plan.")
    return validate_plan(raw, objective, allowed)


def langchain_review(
    model: StructuredModel,
    objective: str,
    results: Sequence[SearchResult],
    corpus_root: Path,
) -> StructuredReview:
    allowed = evidence_paths(results)
    response = model.with_structured_output(StructuredReview, include_raw=True).invoke(
        [("system", SYSTEM_PROMPT), ("human", review_prompt(objective, results, review_corpus(corpus_root)))]
    )
    if not isinstance(response, Mapping) or response.get("parsing_error") or response.get("parsed") is None:
        raise RuntimeError("LangChain did not return a valid structured review.")
    parsed = response["parsed"]
    raw = parsed.model_dump() if isinstance(parsed, BaseModel) else parsed
    if not isinstance(raw, Mapping):
        raise TypeError("LangChain returned a non-mapping structured review.")
    return validate_review(raw, objective, allowed)
