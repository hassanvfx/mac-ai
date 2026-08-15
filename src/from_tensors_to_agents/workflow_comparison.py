"""Compare safe book-maintenance workflow shapes over identical evidence."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from from_tensors_to_agents.book_intelligence import (
    ImprovementPlan,
    SearchResult,
    propose_improvement,
    retrieve,
    review_corpus,
)


@dataclass(frozen=True)
class WorkflowReport:
    name: str
    evidence_paths: tuple[str, ...]
    plan_steps: tuple[str, ...]
    findings: tuple[str, ...]
    writer_brief: str
    approval_required: bool = True
    writes_performed: bool = False


def deterministic_workflow(index: list, objective: str, root: Path) -> WorkflowReport:
    plan: ImprovementPlan = propose_improvement(index, objective)
    return WorkflowReport(
        name="deterministic",
        evidence_paths=plan.evidence_paths,
        plan_steps=plan.steps,
        findings=tuple(review_corpus(root)),
        writer_brief="No writer role; inspect the proposal manually.",
    )


def single_planner_workflow(index: list, objective: str, root: Path) -> WorkflowReport:
    results: list[SearchResult] = retrieve(index, objective, 4)
    paths = tuple(sorted({result.evidence.source for result in results if result.score > 0}))
    findings = tuple(review_corpus(root))
    return WorkflowReport(
        name="single_planner",
        evidence_paths=paths,
        plan_steps=(
            "Verify the retrieved evidence before drafting a change.",
            "Address the objective with the smallest testable revision.",
            "Request human approval before any source action.",
        )
        if paths
        else (),
        findings=findings,
        writer_brief="One planner combines retrieval, planning, and review context; no source is changed.",
    )


def researcher_critic_writer_workflow(index: list, objective: str, root: Path) -> WorkflowReport:
    """Model specialization as explicit roles, with no tool that can write."""
    research_results: list[SearchResult] = retrieve(index, objective, 4)
    paths = tuple(sorted({result.evidence.source for result in research_results if result.score > 0}))
    critic_findings = list(review_corpus(root))
    if not paths:
        critic_findings.append("No retrieved evidence: writer brief must not propose a change.")
        brief = "No draft brief: the researcher found no evidence."
        steps: tuple[str, ...] = ()
    else:
        brief = (
            "Draft a revision brief that cites only the researcher paths, carries critic findings, "
            "and waits for human approval."
        )
        steps = (
            "Researcher: verify the retrieved paths and citation keys.",
            "Critic: identify unsupported claims, missing experiments, links, or alternatives.",
            "Writer: prepare a proposal only; do not modify a source file.",
            "Human: approve or reject before any future write-capable step.",
        )
    return WorkflowReport(
        name="researcher_critic_writer",
        evidence_paths=paths,
        plan_steps=steps,
        findings=tuple(critic_findings),
        writer_brief=brief,
    )


def score_report(report: WorkflowReport, required_path: str, required_finding: str) -> dict[str, bool]:
    return {
        "path_attribution": required_path in report.evidence_paths,
        "review_coverage": required_finding in report.findings,
        "approval_boundary": report.approval_required,
        "no_write": not report.writes_performed,
    }
