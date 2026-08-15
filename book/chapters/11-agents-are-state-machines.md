---
sidebar_position: 11
title: Agents Are State Machines
---

# Agents Are State Machines

## Intuition

An agent is easier to trust when we can name its states and legal transitions.
“Think, act, observe” is a useful sketch, but a production-minded workflow
needs to answer sharper questions: what state is saved, what causes a pause,
what happens after rejection, and which transition is allowed to mutate the
world?

State is also an audit record. It should say which evidence was considered,
which plan was proposed, why a workflow paused, and whether a human accepted or
rejected it. If those facts exist only in transient prompt text, a restart or a
later review cannot distinguish a deliberate decision from an accidental one.

## Problem

The Book Intelligence Assistant has retrieved evidence, a plan, and a critique.
It needs a durable approval boundary before any future writing capability. A
single function can hide that boundary; a state graph makes it testable.

## Minimal implementation

[approval_workflow.py](../../src/from_tensors_to_agents/approval_workflow.py)
defines a small LangGraph state: objective, evidence paths, plan, critique,
model status, decision, and terminal status. Its edges are explicit:

```text
START → plan → critique → approval interrupt → approved_no_write | rejected_no_write
```

The plan and critique nodes are deterministic in this first version. If no
evidence is available, the plan is empty and the state records a deterministic
fallback. There is no tool that edits a file or runs Git.

## Real implementation

Run the local SQLite-backed graph:

```bash
uv sync --group agents
uv run --group agents python experiments/11-langgraph/approval_workflow.py
uv run --group agents python experiments/11-langgraph/approval_workflow.py \
  --approve --thread-id chapter-11-approved
```

The first invocation pauses at `interrupt()`. The second invocation in this
small demonstration resumes immediately with the declared decision. LangGraph
checkpointing ties state to a `thread_id`, allowing a later process to resume
the same workflow [@langgraph2026persistence; @langgraph2026interrupts].

## Experiment

Run the rejection and approval cases with distinct thread IDs. Confirm their
terminal states are `rejected_no_write` and `approved_no_write`; inspect the
SQLite file only as generated local state. Then run the test that opens a new
SQLite connection after the interrupt and resumes the old thread. That is the
actual persistence property demonstrated here.

## What broke

The first synchronous SQLite run failed because Python normally binds a
connection to the thread that created it, while the saver can checkpoint from a
worker thread. The local fix is `check_same_thread=False`, as recorded in
`benchmarks/07-workflow-graphs/README.md`. The more important lesson is not the
flag: persistence is a real systems dependency with concurrency behavior that
must be tested rather than assumed.

## Alternatives

For a short, stateless task, a plain function and an explicit confirmation can
be clearer than a graph. An in-memory checkpointer is useful in unit tests. A
database-backed checkpointer becomes worthwhile when an interrupt must survive
a process boundary. Other backends may be better for concurrent, hosted, or
regulated deployments, but they need their own operational design.

## When to use it—and when not to

Use a graph when state, recovery, routing, or human control is part of the
product behavior. Do not use a graph merely to make one model call look more
agentic. A graph does not create safety by itself; its nodes must still have
least privilege.

## Takeaway

An agent is a state machine with a language model somewhere inside or beside
it. Defining the state first makes interruption, recovery, and permission
boundaries concrete instead of aspirational.
