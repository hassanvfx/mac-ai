from __future__ import annotations

import sqlite3
from pathlib import Path

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command

from from_tensors_to_agents.approval_workflow import build_approval_graph


def invoke_until_interrupt(graph: object, config: dict[str, object]) -> dict[str, object]:
    return graph.invoke(
        {"objective": "Review Chapter 8", "evidence_paths": ["book/chapters/08.md"]},
        config,
    )


def test_rejected_approval_persists_and_never_writes_sources(tmp_path: Path) -> None:
    source = tmp_path / "book" / "chapters" / "08.md"
    source.parent.mkdir(parents=True)
    source.write_text("original", encoding="utf-8")
    database = tmp_path / "local" / "workflow.sqlite"
    database.parent.mkdir()
    with sqlite3.connect(database, check_same_thread=False) as connection:
        checkpointer = SqliteSaver(connection)
        checkpointer.setup()
        graph = build_approval_graph(checkpointer)
        config = {"configurable": {"thread_id": "rejected"}}
        paused = invoke_until_interrupt(graph, config)
        assert paused["__interrupt__"][0].value["action"].startswith("No source")
        final = graph.invoke(Command(resume={"approved": False}), config)
    assert final["status"] == "rejected_no_write"
    assert source.read_text(encoding="utf-8") == "original"
    assert database.exists()


def test_checkpoint_can_resume_after_reopening_sqlite(tmp_path: Path) -> None:
    database = tmp_path / "workflow.sqlite"
    config = {"configurable": {"thread_id": "approved"}}
    with sqlite3.connect(database, check_same_thread=False) as connection:
        checkpointer = SqliteSaver(connection)
        checkpointer.setup()
        paused = invoke_until_interrupt(build_approval_graph(checkpointer), config)
        assert "__interrupt__" in paused
    with sqlite3.connect(database, check_same_thread=False) as connection:
        checkpointer = SqliteSaver(connection)
        graph = build_approval_graph(checkpointer)
        final = graph.invoke(Command(resume={"approved": True}), config)
    assert final["status"] == "approved_no_write"


def test_empty_evidence_uses_deterministic_no_model_fallback(tmp_path: Path) -> None:
    with sqlite3.connect(tmp_path / "workflow.sqlite", check_same_thread=False) as connection:
        checkpointer = SqliteSaver(connection)
        checkpointer.setup()
        graph = build_approval_graph(checkpointer)
        config = {"configurable": {"thread_id": "empty"}}
        paused = graph.invoke({"objective": "Review", "evidence_paths": []}, config)
        state = graph.get_state(config)
    assert "__interrupt__" in paused
    assert state.values["model_status"] == "deterministic_fallback_no_evidence"
    assert state.values["plan"] == []
