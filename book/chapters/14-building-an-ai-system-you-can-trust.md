---
sidebar_position: 14
title: Building an AI System You Can Actually Trust
---

# Building an AI System You Can Actually Trust

## Intuition

Reliability comes from evaluation, observability, constraints, and recovery—not
from a single impressive demo. A fluent plan is not reliable unless its evidence,
failure mode, permission boundary, and trace can be inspected.

## Problem

The Book Intelligence Assistant combines retrieval, planning, critique, and
approval. The beta needs a repeatable way to prove its narrow guarantees and
state plainly what it cannot yet guarantee.

## Minimal implementation

The frozen fixture corpus and [reliability runner](../../evals/run_reliability.py)
exercise evidence location, missing-evidence refusal, no-write planning, and
editorial review. It writes a JSON trace only under ignored
`.book-intelligence/`, with a case count, result details, and explicit no-write
policy.

```bash
uv run --group agents python evals/run_reliability.py
```

## Real implementation

The system’s reliability policy is layered. Retrieval must retain repository
paths and citation keys. Grounded answers return evidence or refuse. Structured
plans discard invented paths. LangGraph pauses before approval and its approved
terminal state still performs no write. These controls are regression-tested
without a credential or remote model.

## Experiment

Run the reliability suite from a clean environment and inspect the generated
trace. A passing trace shows that the frozen cases met their declared contract;
it does not prove correctness on every future manuscript or API response.
Record latency, tokens, provider/model identity, and failures only when a
controlled API experiment actually runs.

## What broke

The project has already observed weak retrieval neighbors, absent API
configuration, malformed structured output, empty evidence, rejected approval,
and a SQLite thread constraint. Each became a test or documented limitation.
The dangerous failure is silent degradation: turning a missing model, source,
or approval into a plausible write.

## Alternatives

Manual editorial review, pull requests, and conventional search remain strong
alternatives. Hosted tracing can help a team, but creates privacy, retention,
and vendor concerns. A small local trace is preferable while this beta has no
remote model run.

## When to use it—and when not to

Use the assistant to locate evidence and prepare proposals. Do not use it as an
authority for unsupported claims, autonomous edits, legal/safety decisions, or
external actions. Any future writer must be a separate, explicitly approved,
least-privilege capability.

## Takeaway

Trust is a continuing engineering practice. This beta is trustworthy only in
the narrow ways its tests and traces demonstrate—and it remains honest about the
work required before production or print release.
