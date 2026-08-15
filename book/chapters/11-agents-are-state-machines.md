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

Write an invariant beside each transition. In this graph, evidence paths are
read-only inputs from retrieval; a planning node may add a proposal but cannot
add authority; the approval node is the only source of a decision; and both
terminal nodes are explicitly no-write. An invariant narrows review: instead
of asking whether an agent “seems safe,” ask whether any edge can reach a
state-changing node without an approval event scoped to the proposed action.

State is not the same thing as a transcript. Save the smallest information
needed to resume and audit the workflow: objective, evidence paths, proposal,
critique, model/fallback status, decision, and terminal status. Avoid placing
credentials, whole repositories, or unnecessary private prompts in a
checkpoint. A useful checkpoint should help recover a pending decision without
creating a new unreviewed data store.

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

The transition table is also a testing plan. For every conditional route, make
one deterministic fixture that reaches it. For every persisted state, close and
reopen the storage used by the demonstration. For every purportedly harmless
node, assert that a tracked source remains unchanged. This is why a state graph
is useful even before a model is selected: its reliability properties can be
verified with ordinary data and control flow rather than sampled language.

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

Thread IDs are part of the integrity boundary. Generate a new, descriptive ID
for each independent revision request, and display the resumed objective and
evidence paths before accepting a decision. If a user cannot recognize the
pending work, reject it and start a fresh graph. A checkpoint proves that some
state was saved; it does not prove that it still matches the current checkout.
For a long-lived workflow, compare an evidence revision or content hash at
resume time and route stale evidence back to retrieval rather than approving an
obsolete plan.

The SQLite example is intentionally local and single-user. Its role is to
demonstrate checkpoint/resume semantics, not to prescribe a shared production
database. Concurrent users, hosted workers, retention requirements, backup,
and access control need a separately designed store. Carry the same state
contract forward, but do not assume that a file created for a tutorial is a
complete operational design.

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

Test the state trace, not just the final label. A rejected workflow should
include the retrieved paths, an empty-or-supported plan according to its input,
the critique, the interruption payload, and the `rejected_no_write` terminal
status. An approved workflow in this beta must end at `approved_no_write` too:
approval confirms review of a proposal, not permission for hidden execution.
This distinction prevents a misleading future change where the approved branch
quietly gains a file-writing tool because it already has a boolean named
`approved`.

For an unavailable planning model, preserve the fallback status in state and
continue only with the deterministic proposal policy. Do not disguise fallback
text as a model result, and do not make a later resume choose a provider that
was not part of the original request. A human can decide to rerun the workflow
under a declared model configuration; that is a new experiment, not automatic
recovery.

### Worked trace: reject, reopen, and approve

Begin with a fresh thread ID such as `chapter-11-reject`. The graph receives an
objective and the evidence path for Chapter 8. Its deterministic plan node
creates three review steps; its critique node adds two checks; then the approval
node emits an interrupt payload. At this point the persisted state has an
objective, one evidence path, plan, critique, deterministic model status, and
an explicit action message: no source, Git, or external action will follow.
It has no file diff and no writer capability.

Resume that same thread with `{"approved": false}`. The conditional edge
selects the rejected node, which records `rejected_no_write`. The test places a
small source fixture beside its SQLite database and compares its text after the
terminal state; it remains `original`. The lesson is not that rejection is
hard to implement. It is that the rejected route is a named, durable outcome
with a direct assertion against the side effect we refuse to permit.

For persistence, start a separate `chapter-11-approve` thread and stop at the
same interrupt. Close the SQLite connection completely. Reopen the database in
a new connection, rebuild the graph with its checkpointer, and resume with
`{"approved": true}`. The terminal status becomes `approved_no_write`. The
reopened process did not reconstruct a proposal from a chat transcript: it read
the checkpoint associated with that thread ID. Yet approval still did not grant
write authority, so the positive path is as safe to exercise in a test as the
negative path.

Finally, invoke the graph with an empty evidence list. The plan is empty and
the saved `model_status` becomes `deterministic_fallback_no_evidence`, while
the graph still pauses for inspection. This trace prevents an important
shortcut: a workflow cannot replace absent evidence with a confident default
plan simply because it has a route to an approval screen. In a real review, the
human should reject or restart with retrieval; the test asserts only the
deterministic, no-model contract.

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

Stale approval is a third hazard. A person may approve a plan, the underlying
chapter may change, and a delayed process may later resume with evidence that no
longer supports the proposed edit. The beta prevents writes entirely, which
keeps this case safe. A future writer must revalidate evidence and display the
exact intended diff immediately before a scoped approval; a broad “continue”
button is not enough.

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

Event logs or a conventional job queue can also model parts of this workflow.
They are useful when many independent tasks need scheduling, but they do not
replace an explicit approval state and evidence contract. A graph library earns
its complexity when its persisted routing, interrupt semantics, and testable
state are requirements; otherwise a typed function plus a reviewable pull
request remains a strong, lower-risk alternative.

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
