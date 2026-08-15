"""Deterministic, no-secret regression evaluation for Book Intelligence."""

from __future__ import annotations

import json
from pathlib import Path

from from_tensors_to_agents.book_intelligence import (
    ApprovalCheckpoint,
    build_index,
    grounded_answer,
    grounded_evidence,
    propose_improvement,
    retrieve,
    review_corpus,
)


def load_cases(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def evaluate(root: Path, cases: list[dict[str, object]], output: Path) -> list[dict[str, object]]:
    index = build_index(root)
    results: list[dict[str, object]] = []
    for case in cases:
        task = case["task"]
        passed = False
        detail = ""
        if task == "retrieve":
            paths = [item.evidence.source for item in retrieve(index, str(case["question"]))]
            expected = str(case["must_cite"])
            passed = expected in paths
            detail = f"retrieved={paths}"
        elif task == "grounding":
            answer = grounded_evidence([])
            passed = bool(case["must_refuse"]) and answer.startswith("No grounded answer")
            detail = answer
        elif task == "grounded-answer":
            answer = grounded_answer(index, str(case["question"]))
            expected = str(case["must_cite"])
            passed = answer.startswith("Grounded evidence only:") and f"[{expected}" in answer
            detail = answer
        elif task == "citation":
            retrieved = retrieve(index, str(case["question"]))
            expected_source = str(case["must_cite"])
            expected_key = str(case["must_preserve_key"])
            matching = [item for item in retrieved if item.evidence.source == expected_source]
            passed = bool(matching) and expected_key in matching[0].evidence.citations
            detail = f"retrieved={[item.evidence.source for item in retrieved]}; citations={[item.evidence.citations for item in matching]}"
        elif task == "plan":
            before = {path: path.read_text(encoding="utf-8") for path in root.rglob("*") if path.is_file()}
            proposal = propose_improvement(index, str(case["question"]))
            checkpoint = ApprovalCheckpoint(output.parent / "checkpoint.json")
            checkpoint.create(proposal)
            after = {path: path.read_text(encoding="utf-8") for path in root.rglob("*") if path.is_file()}
            expected = str(case["must_include"])
            passed = proposal.approval_required and expected in " ".join(proposal.steps) and before == after
            detail = f"approval_required={proposal.approval_required}; source_files_unchanged={before == after}"
        elif task == "review":
            findings = review_corpus(root)
            expected = str(case["must_flag"])
            passed = expected in findings
            detail = f"findings={findings}"
        else:
            detail = f"unsupported task: {task}"
        results.append({"id": case["id"], "passed": passed, "detail": detail})
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return results
