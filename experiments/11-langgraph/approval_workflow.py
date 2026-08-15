"""Run a no-write LangGraph proposal and explicitly approve or reject it."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command

from from_tensors_to_agents.approval_workflow import build_approval_graph


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--approve", action="store_true", help="Resume with approval; default is rejection.")
    parser.add_argument("--thread-id", default="chapter-11-demo")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    database = root / ".book-intelligence" / "approval-workflow.sqlite"
    database.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database, check_same_thread=False) as connection:
        checkpointer = SqliteSaver(connection)
        checkpointer.setup()
        graph = build_approval_graph(checkpointer)
        config = {"configurable": {"thread_id": args.thread_id}}
        paused = graph.invoke(
            {
                "objective": "Review the embeddings chapter without changing it.",
                "evidence_paths": ["book/chapters/08-turning-meaning-into-geometry.md"],
            },
            config,
        )
        print(f"interrupt: {paused['__interrupt__'][0].value['action']}")
        final = graph.invoke(Command(resume={"approved": args.approve}), config)
        print(f"final status: {final['status']}")
        print(f"checkpoint database: {database}")


if __name__ == "__main__":
    main()
