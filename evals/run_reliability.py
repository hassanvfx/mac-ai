from pathlib import Path

from from_tensors_to_agents.reliability import run_reliability_suite


def main() -> None:
    repository = Path(__file__).resolve().parents[1]
    trace = run_reliability_suite(repository, repository / ".book-intelligence" / "reliability.json")
    print(f"passed: {trace['passed']}; cases: {trace['case_count']}")
    if not trace["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
