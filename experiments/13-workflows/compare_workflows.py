"""Compare safe workflow shapes on the frozen book-maintenance fixture."""

from pathlib import Path

from from_tensors_to_agents.book_intelligence import build_index
from from_tensors_to_agents.workflow_comparison import (
    deterministic_workflow,
    researcher_critic_writer_workflow,
    score_report,
    single_planner_workflow,
)


def main() -> None:
    root = Path(__file__).resolve().parents[2] / "evals" / "fixture_corpus"
    objective = "Explain cosine similarity and review the draft chapter"
    required_path = "research/embeddings.md"
    required_finding = "book/chapters/08-draft.md: missing Alternatives section"
    index = build_index(root)
    reports = [
        deterministic_workflow(index, objective, root),
        single_planner_workflow(index, objective, root),
        researcher_critic_writer_workflow(index, objective, root),
    ]
    print("workflow | path | review | approval | no-write | steps")
    for report in reports:
        score = score_report(report, required_path, required_finding)
        print(
            f"{report.name} | {score['path_attribution']} | {score['review_coverage']} | "
            f"{score['approval_boundary']} | {score['no_write']} | {len(report.plan_steps)}"
        )


if __name__ == "__main__":
    main()
