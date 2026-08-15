"""A persisted, no-write LangGraph workflow for book-maintenance proposals."""

from __future__ import annotations

from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt


class RevisionState(TypedDict, total=False):
    objective: str
    evidence_paths: list[str]
    plan: list[str]
    critique: list[str]
    model_status: str
    approved: bool
    status: str


def draft_plan(state: RevisionState) -> RevisionState:
    """Create a deterministic proposal; no model or repository write occurs here."""
    evidence_paths = state.get("evidence_paths", [])
    if not evidence_paths:
        return {
            "plan": [],
            "model_status": "deterministic_fallback_no_evidence",
            "status": "missing_evidence",
        }
    return {
        "plan": [
            "Inspect the retrieved source paths and verify their current contents.",
            "Draft the smallest evidence-backed chapter or experiment revision.",
            "Run the critic and targeted tests before requesting human approval.",
        ],
        "model_status": "deterministic_fallback",
        "status": "proposed",
    }


def critique_plan(state: RevisionState) -> RevisionState:
    if not state.get("evidence_paths"):
        return {"critique": ["No retrieved evidence: do not propose a source change."]}
    return {
        "critique": [
            "Verify that every claim in the plan has a retrieved source path.",
            "Verify that the target chapter includes experiments and alternatives where applicable.",
        ]
    }


def request_approval(state: RevisionState) -> RevisionState:
    """Pause rather than write; Command(resume=...) supplies the human decision."""
    decision = interrupt(
        {
            "objective": state.get("objective", ""),
            "evidence_paths": state.get("evidence_paths", []),
            "plan": state.get("plan", []),
            "critique": state.get("critique", []),
            "action": "No source, Git, or external action will occur after this decision.",
        }
    )
    approved = bool(decision.get("approved")) if isinstance(decision, dict) else bool(decision)
    return {"approved": approved, "status": "approved" if approved else "rejected"}


def after_approval(state: RevisionState) -> Literal["approved", "rejected"]:
    return "approved" if state.get("approved") else "rejected"


def finish_approved(_: RevisionState) -> RevisionState:
    return {"status": "approved_no_write"}


def finish_rejected(_: RevisionState) -> RevisionState:
    return {"status": "rejected_no_write"}


def build_approval_graph(checkpointer: object):
    workflow = StateGraph(RevisionState)
    workflow.add_node("plan", draft_plan)
    workflow.add_node("critique", critique_plan)
    workflow.add_node("approval", request_approval)
    workflow.add_node("approved", finish_approved)
    workflow.add_node("rejected", finish_rejected)
    workflow.add_edge(START, "plan")
    workflow.add_edge("plan", "critique")
    workflow.add_edge("critique", "approval")
    workflow.add_conditional_edges("approval", after_approval, {"approved": "approved", "rejected": "rejected"})
    workflow.add_edge("approved", END)
    workflow.add_edge("rejected", END)
    return workflow.compile(checkpointer=checkpointer)
