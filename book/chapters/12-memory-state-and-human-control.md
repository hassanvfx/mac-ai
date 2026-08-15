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

## Problem

A chapter-revision proposal may take longer than one process or one work
session. The assistant must preserve its plan and critique without treating a
paused workflow as implicit approval. It must also distinguish a durable
checkpoint from the repository itself: the checkpoint is local operational
state, not canonical editorial evidence.

## Minimal implementation

The graph from Chapter 11 stores a checkpoint after each super-step under an
explicit `thread_id`. The approval node emits a JSON-serializable payload with
the objective, evidence paths, plan, critique, and a statement that no action
will occur. It waits for a value passed by `Command(resume=...)`
[@langgraph2026interrupts].

The resumed value is only a boolean decision. Even `true` reaches
`approved_no_write`, not a writer node. This deliberately separates *approval
of a proposal* from *execution of a change*.

## Real implementation

The local example uses `SqliteSaver` because a file makes resume testable after
the original connection closes. Its path is `.book-intelligence/approval-workflow.sqlite`,
which is ignored by Git. The test suite proves that a source fixture remains
unchanged after rejection and that a reopened SQLite store can complete a
previously interrupted approved thread.

Use one new `thread_id` for each independent proposal. Reusing a thread ID is a
resume operation, not a clean new request. That is why stable IDs should be
chosen deliberately and never derived from secret or sensitive user content.

## Experiment

Pause the graph, close the process, reopen the SQLite checkpoint, and resume
with rejection. Check that the terminal state is `rejected_no_write` and no
source changed. Repeat with approval and verify that it still ends in
`approved_no_write`. These two outcomes make the human boundary observable.

## What broke

An interrupt node restarts from the beginning when resumed. Therefore code
before `interrupt()` must be idempotent and must not perform an irreversible
action. This graph constructs only a JSON payload before the pause. If a future
writer is added, it must be a separate post-approval node with its own explicit
confirmation and tests—not an accidental side effect of rebuilding the
approval payload.

## Alternatives

A manual ticket, pull request, or command-line confirmation can be the right
human-control mechanism for a simpler workflow. Stateless requests avoid
checkpoint retention but lose recovery. Hosted database checkpointing may suit
teams, while local SQLite keeps a single-developer learning project easy to
inspect. None of these replaces access control or a clear retention policy.

## When to use it—and when not to

Use persisted state when interruption and recovery are requirements. Do not
persist more context than the next decision needs, and do not put credentials,
private journals, or unreviewed generated text into a checkpoint by default.
If there is no safe execution path yet, the correct terminal state is still a
proposal, not an automatic change.

## Takeaway

Human-in-the-loop is not a decorative confirmation button. It is a persisted
state transition whose resume behavior, data scope, and failure paths must be
designed before the system earns the right to act.
