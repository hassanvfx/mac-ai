---
sidebar_position: 12
title: Memory, State, and Human Control
---

# Memory, State, and Human Control

## Intuition

“Memory” is overloaded. A model’s learned weights, retrieved documents, a chat
history, and a database checkpoint are different things with different failure
modes. For a safe workflow, the relevant memory is saved state that a person
can inspect before deciding whether to continue.

Approval must be scoped to a specific, reviewable proposal. It is not standing
permission for an agent to edit unrelated files, rerun a different plan, or
call an external service later. Binding the decision to recorded evidence and
the proposed change makes the boundary meaningful when state is resumed.

## Problem

A chapter-revision proposal may take longer than one process or one work
session. The assistant must preserve its plan and critique without treating a
paused workflow as implicit approval. It must also distinguish a durable
checkpoint from the repository itself: the checkpoint is local operational
state, not canonical editorial evidence.

There are two tempting but unsafe shortcuts. The first is to keep all context
only in a chat window. That makes a restart indistinguishable from a new
request and gives neither the reviewer nor the program a stable record of what
was considered. The second is to put the proposed edit in the checkpoint and
apply it automatically after a positive response. That turns a review decision
into a write capability. This book uses a narrower contract: a checkpoint can
remember a proposal, but it cannot be a substitute for the repository, a
permission system, or a change log.

Approval is strongest when the reviewer can answer four questions without
reconstructing hidden context: what is proposed, which evidence supports it,
what exact effect would follow, and what happens if the answer is no. The beta
answers the third question with “nothing is executed.” That may feel limited,
but it is a valuable capability boundary: a reviewer can exercise approval and
rejection paths before any code has authority to write prose, change Git state,
or contact an external service.

Human control is also more than a boolean. A useful decision can be approve,
reject, request a revision, or abandon a stale proposal. This small graph uses
approve and reject to keep the state space testable. If a revision option is
added later, it should route back to evidence and planning with an explicit
reason, not mutate the old plan in place and reuse an approval that was scoped
to different text.

## Minimal implementation

The graph from Chapter 11 stores a checkpoint after each super-step under an
explicit `thread_id`. The approval node emits a JSON-serializable payload with
the objective, evidence paths, plan, critique, and a statement that no action
will occur. It waits for a value passed by `Command(resume=...)`
[@langgraph2026interrupts].

The resumed value is only a boolean decision. Even `true` reaches
`approved_no_write`, not a writer node. This deliberately separates *approval
of a proposal* from *execution of a change*.

This also makes a negative outcome useful rather than exceptional. A rejection
is durable information: the proposal was reviewed and is not authorized to
continue. A later attempt needs a new proposal with new evidence, or a clearly
identified resume of the same proposal. It must not silently reinterpret an
old approval after the chapter, corpus, or requested objective has changed.

The pause payload is an interface for a human, so design it for review rather
than for a model. Keep paths readable, state why each item was retrieved, show
the critique and unsupported-claim warnings, and name the no-write boundary in
plain language. Do not make a reviewer infer scope from a long free-form
prompt. A good interface makes it easy to reject an unclear proposal; rejection
is a safe outcome, not an error that must be optimized away.

## Real implementation

The local example uses `SqliteSaver` because a file makes resume testable after
the original connection closes. Its path is `.book-intelligence/approval-workflow.sqlite`,
which is ignored by Git. The test suite proves that a source fixture remains
unchanged after rejection and that a reopened SQLite store can complete a
previously interrupted approved thread.

Use one new `thread_id` for each independent proposal. Reusing a thread ID is a
resume operation, not a clean new request. That is why stable IDs should be
chosen deliberately and never derived from secret or sensitive user content.

The checkpoint has a limited retention purpose. It records workflow state such
as the objective, paths used as evidence, plan, critique, decision, and
terminal status. It should not become a second index of the whole book or a
dumping ground for retrieved documents. Keeping evidence as repository paths
means a reviewer can reopen the canonical file, while keeping the local SQLite
file ignored prevents operational state from polluting a commit or an exported
manuscript.

Retention is a design choice, not a side effect of choosing SQLite. Decide how
long pending proposals are useful, who may read their objectives and evidence
paths, where backups reside, and how generated state is removed when the work
ends. For this repository, local generated state is ignored and can be deleted
without deleting canonical prose or experiment records. A shared deployment
would need access controls and an explicit retention/deletion policy before
storing project context for more than a local learning exercise.

Do not put raw secrets in an approval payload, even if a future action needs an
API credential. The credential should be resolved only by the least-privileged
executor after a scoped approval, and its value should never be checkpointed or
rendered in logs. The current graph has no executor, so it offers a simple
property to test: there is nowhere for a secret-backed external call to occur.

## Experiment

Pause the graph, close the process, reopen the SQLite checkpoint, and resume
with rejection. Check that the terminal state is `rejected_no_write` and no
source changed. Repeat with approval and verify that it still ends in
`approved_no_write`. These two outcomes make the human boundary observable.

The runnable implementation is
`experiments/11-langgraph/approval_workflow.py`; its durable behavior is
checked in `tests/test_approval_workflow.py`. The tests create an isolated
SQLite file, invoke until the interrupt, reopen the database in a new
connection, and resume it. They also start a graph with no evidence and verify
the deterministic fallback. That last case matters: an unavailable model or
empty retrieval result must reduce the proposal's authority, not encourage the
system to invent support.

For a manual inspection, copy the experiment's local checkpoint path to a
temporary directory, run it once until it reports an interrupt, then run the
resume command with `{"approved": false}`. Inspect the resulting state and
confirm that no tracked source file has changed. Repeat in a fresh thread with
approval. The expected terminal labels are deliberately explicit so logs and
tests do not mistake a pause for success.

Run a stale-proposal exercise as well. Pause with one objective and evidence
set, change or replace a cited file in a disposable fixture, then inspect the
resume boundary. The safe policy is to invalidate or re-review the proposal,
not to treat the old decision as portable. The current beta expresses this as a
design rule because it has no writer; a writer-capable version must enforce it
with a revision/hash check and a new approval payload containing the intended
diff.

Review ergonomics are measurable. Record whether a reviewer can identify the
objective, paths, limitations, decision, and final no-write status from the
payload and trace. If they cannot, the system has a transparency failure even
when the graph reaches the expected node. A future usability evaluation can
use scripted review cases, but it should preserve the same safety rule: a
positive label is not evidence of an executed or correct change.

## What broke

An interrupt node restarts from the beginning when resumed. Therefore code
before `interrupt()` must be idempotent and must not perform an irreversible
action. This graph constructs only a JSON payload before the pause. If a future
writer is added, it must be a separate post-approval node with its own explicit
confirmation and tests—not an accidental side effect of rebuilding the
approval payload.

Another failure is treating the checkpoint as current evidence. A path can
move, a benchmark can be superseded, and a chapter can change while a thread is
paused. Before any future writer acts, it must re-read every cited path,
validate that the proposal still applies, and show the resulting diff to the
human. A saved `approved` flag alone is never enough to prove that a changed
proposal remains safe.

Rejection needs an equally clear recovery route. Preserve the rejected status
and reviewer reason when there is one, then require a fresh retrieval and plan
for materially changed work. Do not reset a rejected checkpoint to pending in
place, because that erases the audit trail and can confuse a later reviewer
about which proposal was actually declined. Starting a new thread is cheaper
than interpreting a history with ambiguous scope.

## Alternatives

A manual ticket, pull request, or command-line confirmation can be the right
human-control mechanism for a simpler workflow. Stateless requests avoid
checkpoint retention but lose recovery. Hosted database checkpointing may suit
teams, while local SQLite keeps a single-developer learning project easy to
inspect. None of these replaces access control or a clear retention policy.

It is also reasonable to avoid an agent graph altogether. A deterministic
script that gathers links and runs the editorial audit is easier to reproduce
and often sufficient. Use a persisted graph only when resumable, inspectable
workflow state provides a real benefit. The comparison in Chapter 13 treats
that extra machinery as a cost to be justified by the task, rather than a
default sign of sophistication.

## When to use it—and when not to

Use persisted state when interruption and recovery are requirements. Do not
persist more context than the next decision needs, and do not put credentials,
private journals, or unreviewed generated text into a checkpoint by default.
If there is no safe execution path yet, the correct terminal state is still a
proposal, not an automatic change.

For collaborative work, combine the checkpoint with ordinary version control:
the graph identifies a reviewed proposal; a human creates or approves the
actual diff; Git records the final change. This division is intentionally
boring. It gives a reader one place to inspect operational history and another
place to inspect published source history, without asking either system to
pretend it can replace the other.

A future writer should be a narrow, separate capability: receive an approved
proposal and freshly verified evidence; calculate a single inspectable diff;
pause again with that diff; then write only the approved target if the revision
still matches. It should not receive a shell, a broad filesystem path, Git
credentials, or network tools by default. This is more restrictive than many
agent demonstrations, but it turns “human in the loop” into a technical
property instead of an honor system.

## Evidence trail

Read `research/07-workflow-graphs/notes.md`, run the no-write graph at
`experiments/11-langgraph/approval_workflow.py`, and inspect
`tests/test_approval_workflow.py` for persistence, rejection, and fallback
contracts.

## Takeaway

Human-in-the-loop is not a decorative confirmation button. It is a persisted
state transition whose resume behavior, data scope, and failure paths must be
designed before the system earns the right to act.
