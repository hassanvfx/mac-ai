# Milestone 5 LangGraph workflow observation

## Contract

This is a local control-flow and persistence observation, not an AI-model,
throughput, or database-performance benchmark.

| Field | Value |
| --- | --- |
| Script | `experiments/11-langgraph/approval_workflow.py` |
| Dependency group | `agents` |
| Packages | `langgraph` 1.2.11; `langgraph-checkpoint-sqlite` 3.1.1 |
| Checkpoint store | local SQLite below ignored `.book-intelligence/` |
| Thread identity | explicit `thread_id` passed through LangGraph configuration |
| Model | none; deterministic proposal/critique fallback |
| Action capability | read-only proposal/critique; no source, Git, or external write node |

## Recorded runs — 2026-08-14

The default command paused at an approval interrupt and, when resumed with the
default rejection, ended at `rejected_no_write`:

```bash
uv run --group agents python experiments/11-langgraph/approval_workflow.py
```

With `--approve` and a separate thread ID, the same graph resumed from its
interrupt and ended at `approved_no_write`. Approval changes only the terminal
state; it does not apply a revision.

The automated tests verify rejection with an unchanged source file, checkpoint
resume after reopening the SQLite file, and an empty-evidence deterministic
fallback. Initial testing failed with Python SQLite's thread restriction because
the saver writes from LangGraph worker threads. The local connection now uses
`check_same_thread=False`; this is required for this synchronous demo.

## Limits

SQLite is appropriate for a local learning workflow. It is not a blanket
production persistence recommendation. Any production choice needs its own
concurrency, backup, retention, encryption, access-control, and migration
design. No timing or capacity claim is made here.
