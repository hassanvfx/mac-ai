"""Compare direct-SDK and LangChain structured planning over identical evidence."""

from __future__ import annotations

import argparse
from collections.abc import Mapping
from pathlib import Path

from pydantic import BaseModel

from from_tensors_to_agents.book_intelligence import build_index, retrieve
from from_tensors_to_agents.structured_planning import (
    StructuredPlan,
    direct_plan,
    langchain_model_from_environment,
    langchain_plan,
    openai_responder_from_environment,
)


class FixtureRunnable:
    def __init__(self, path: str):
        self.path = path

    def invoke(self, _: object) -> Mapping[str, object]:
        return {
            "parsed": StructuredPlan(
                objective="fixture",
                evidence_paths=[self.path],
                steps=["Inspect the retrieved evidence."],
            ),
            "parsing_error": None,
        }


class FixtureLangChainModel:
    def __init__(self, path: str):
        self.path = path

    def with_structured_output(self, _: type[BaseModel], **__: object) -> FixtureRunnable:
        return FixtureRunnable(self.path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--objective", default="Improve the embeddings research note")
    parser.add_argument("--api", action="store_true", help="Use configured OpenAI-compatible API instead of fixtures.")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    results = retrieve(build_index(root), args.objective)
    if args.api:
        direct = direct_plan(openai_responder_from_environment(), args.objective, results)
        composed = langchain_plan(langchain_model_from_environment(), args.objective, results)
    else:
        path = results[0].evidence.source if results else ""

        def fixture_responder(_: str, __: str, ___: type[BaseModel]) -> Mapping[str, object]:
            return {
                "objective": "fixture",
                "evidence_paths": [path],
                "steps": ["Inspect the retrieved evidence."],
                "approval_required": True,
            }

        direct = direct_plan(fixture_responder, args.objective, results)
        composed = langchain_plan(FixtureLangChainModel(path), args.objective, results)
    print(f"direct paths: {direct.evidence_paths}")
    print(f"langchain paths: {composed.evidence_paths}")
    print(f"approval required: {direct.approval_required and composed.approval_required}")
    if direct.evidence_paths != composed.evidence_paths:
        raise SystemExit("The adapters did not preserve the same evidence paths.")


if __name__ == "__main__":
    main()
