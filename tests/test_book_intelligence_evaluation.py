from pathlib import Path

from from_tensors_to_agents.evaluation import evaluate, load_cases


def test_versioned_book_intelligence_evaluation_passes_without_a_model(tmp_path: Path) -> None:
    repository = Path(__file__).resolve().parents[1]
    cases = load_cases(repository / "evals" / "book_intelligence.jsonl")
    results = evaluate(
        repository / "evals" / "fixture_corpus",
        cases,
        tmp_path / "evaluation.json",
    )
    assert all(result["passed"] for result in results)
    assert (tmp_path / "evaluation.json").exists()
