"""Versioned, no-secret reliability traces for Book Intelligence controls."""

from __future__ import annotations

import json
from pathlib import Path

from from_tensors_to_agents.evaluation import evaluate, load_cases


def run_reliability_suite(repository: Path, output: Path) -> dict[str, object]:
    cases = load_cases(repository / "evals" / "book_intelligence.jsonl")
    results = evaluate(repository / "evals" / "fixture_corpus", cases, output.parent / "evaluation.json")
    trace = {"suite": "book-intelligence-fixture", "case_count": len(results), "passed": all(item["passed"] for item in results), "results": results, "policy": "No source, Git, or external write is authorized by this suite."}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(trace, indent=2) + "\n", encoding="utf-8")
    return trace
