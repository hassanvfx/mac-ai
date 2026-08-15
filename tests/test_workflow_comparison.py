from pathlib import Path

from from_tensors_to_agents.book_intelligence import build_index
from from_tensors_to_agents.workflow_comparison import (
    deterministic_workflow,
    researcher_critic_writer_workflow,
    score_report,
    single_planner_workflow,
)


def test_workflow_shapes_cover_the_same_safe_book_maintenance_contract() -> None:
    repository = Path(__file__).resolve().parents[1]
    root = repository / "evals" / "fixture_corpus"
    index = build_index(root)
    objective = "Explain cosine similarity and review the draft chapter"
    required_path = "research/embeddings.md"
    required_finding = "book/chapters/08-draft.md: missing Alternatives section"
    reports = [
        deterministic_workflow(index, objective, root),
        single_planner_workflow(index, objective, root),
        researcher_critic_writer_workflow(index, objective, root),
    ]
    for report in reports:
        scores = score_report(report, required_path, required_finding)
        assert all(scores.values())
    assert "Writer:" in reports[-1].plan_steps[2]
    assert reports[-1].writes_performed is False
