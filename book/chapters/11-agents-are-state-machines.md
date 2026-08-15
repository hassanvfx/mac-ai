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

This perspective removes unnecessary mystery. A language model may help choose
words in a plan, but the workflow still has inputs, state updates, branches,
terminal conditions, and side effects. Naming them lets a reviewer ask ordinary
questions: which field came from retrieval, which node can change it, what
happens if a node is replayed, and which final states are acceptable?

## Problem

The Book Intelligence Assistant has retrieved evidence, a plan, and a critique.
It needs a durable approval boundary before any future writing capability. A
single function can hide that boundary; a state graph makes it testable.

The graph must represent more than a happy path. It needs a no-evidence path,
an interrupted path, an approval path, a rejection path, and a safe response to
an unavailable model. If these outcomes live only in prose around a prompt,
they are easy to forget during a refactor. If they are states and edges, a test
can enter each branch and assert its terminal status without relying on a model
to behave consistently.

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

Treat the state type as an interface. `objective` identifies the proposed work;
`evidence_paths` identifies what the proposal may rely on; `plan` and `critique`
are reviewable intermediate products; `model_status` makes deterministic
fallback visible; and `approved` plus `status` record the decision and outcome.
The graph does not store an implicit “go ahead” between fields. Its conditional
edge reads an explicit decision and routes only to named no-write terminal
nodes. This is easier to audit than a long loop that decides for itself when to
call a tool.

Before adding nodes, write the transition table in words: what causes entry,
what data it reads, what it writes, whether it can be retried, and whether it
has an external effect. A node with an external effect deserves a separate
approval boundary, not merely an earlier confirmation in an unrelated branch.

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

The checkpoint is operational state, not published evidence. It lives under
the ignored `.book-intelligence/` directory so an interrupted run can resume
locally without putting transient plans or decisions into Git. A `thread_id`
names one sequence of work. Starting an unrelated proposal with an old ID risks
mixing its history with a new objective, so use a new ID for a new proposal and
resume only when the pending decision is genuinely the same one.

## Experiment

Run the rejection and approval cases with distinct thread IDs. Confirm their
terminal states are `rejected_no_write` and `approved_no_write`; inspect the
SQLite file only as generated local state. Then run the test that opens a new
SQLite connection after the interrupt and resumes the old thread. That is the
actual persistence property demonstrated here.

Inspect the pause payload before supplying a decision. It contains the
objective, evidence paths, plan, critique, and an explicit statement that no
source, Git, or external action will follow. Resume once with rejection and
once with approval under separate IDs. The important observation is not that a
graph resumes—it is that both paths are visible, deterministic, and end without
modifying a tracked source. The automated reopen test is stronger evidence than
leaving one SQLite file on a laptop after a manual run.

## What broke

The first synchronous SQLite run failed because Python normally binds a
connection to the thread that created it, while the saver can checkpoint from a
worker thread. The local fix is `check_same_thread=False`, as recorded in
`benchmarks/07-workflow-graphs/README.md`. The more important lesson is not the
flag: persistence is a real systems dependency with concurrency behavior that
must be tested rather than assumed.

Retries expose a second hazard. In an interrupt-capable graph, code before an
interrupt can run again on resume. It must therefore be idempotent: constructing
a plan payload is safe to repeat, while sending a message, editing a file, or
charging an account is not. If a future system adds a writer, put it after a
fresh, scoped approval and make its intended diff inspectable. Never hide an
irreversible effect in a node that may be replayed.

## Alternatives

For a short, stateless task, a plain function and an explicit confirmation can
be clearer than a graph. An in-memory checkpointer is useful in unit tests. A
database-backed checkpointer becomes worthwhile when an interrupt must survive
a process boundary. Other backends may be better for concurrent, hosted, or
regulated deployments, but they need their own operational design.

A conventional pull-request workflow is also a graph, implemented by people
and version control: gather evidence, prepare a diff, review, approve, merge
or reject. For many editorial tasks it is clearer than an agent runtime. Use a
programmatic graph when durable routing and interruption reduce real work, not
because state diagrams make a simple question more impressive.

## When to use it—and when not to

Use a graph when state, recovery, routing, or human control is part of the
product behavior. Do not use a graph merely to make one model call look more
agentic. A graph does not create safety by itself; its nodes must still have
least privilege.

Use state graphs when a user needs to inspect progress across a process restart,
when approval and rejection must route differently, or when checks must run in
a declared order. Do not use them to conceal broad tool access behind a chat
interface. A state machine can make unsafe authority easier to automate as well
as safe authority easier to test.

## Evidence trail

The workflow source note is `research/07-workflow-graphs/notes.md`. Run
`experiments/11-langgraph/approval_workflow.py` and review the local-persistence
observation in `benchmarks/07-workflow-graphs/README.md`.

## Takeaway

An agent is a state machine with a language model somewhere inside or beside
it. Defining the state first makes interruption, recovery, and permission
boundaries concrete instead of aspirational.
