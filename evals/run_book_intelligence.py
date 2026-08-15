"""Run deterministic, no-secret Book Intelligence regression cases."""

from __future__ import annotations

import argparse
from pathlib import Path

from from_tensors_to_agents.evaluation import evaluate, load_cases


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture-root", type=Path, default=Path(__file__).with_name("fixture_corpus"))
    parser.add_argument("--cases", type=Path, default=Path(__file__).with_name("book_intelligence.jsonl"))
    parser.add_argument("--output", type=Path, default=Path(".book-intelligence/evaluation.json"))
    args = parser.parse_args()
    results = evaluate(args.fixture_root, load_cases(args.cases), args.output)
    for result in results:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"{status} {result['id']}: {result['detail']}")
    if not all(result["passed"] for result in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
