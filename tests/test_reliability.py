from pathlib import Path

from from_tensors_to_agents.reliability import run_reliability_suite


def test_reliability_trace_is_versioned_and_no_secret(tmp_path: Path) -> None:
    repository = Path(__file__).resolve().parents[1]
    trace = run_reliability_suite(repository, tmp_path / "trace.json")
    assert trace["passed"]
    assert trace["policy"].startswith("No source")
