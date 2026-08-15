---
sidebar_position: 13
title: When One Agent Is Not Enough
---

# When One Agent Is Not Enough

## Intuition

Multiple agents add specialization and review, but also coordination cost and
new failure modes. The useful question is not how many role labels a workflow
has; it is whether the added handoff catches a real risk.

## Problem

Compare three safe shapes on the same frozen book-maintenance task: deterministic
retrieval and review, one planner, and researcher/critic/writer roles. Every
shape must cite the same evidence, flag the same missing editorial section,
require human approval, and make no write.

## Minimal implementation

[workflow_comparison.py](../../src/from_tensors_to_agents/workflow_comparison.py)
keeps the roles deterministic so the comparison is repeatable without an API
key. The writer produces only a brief; it has no file or Git capability.

```bash
uv run --group agents python experiments/13-workflows/compare_workflows.py
```

## Real implementation

The deterministic workflow is the control. The single planner combines
retrieval, planning, and review context. The role pipeline separates researcher,
critic, and writer responsibilities, then stops for approval. All three passed
the same path-attribution, review-coverage, approval-boundary, and no-write
checks in the frozen fixture. See `benchmarks/08-workflow-comparison/README.md`.

## Experiment

The recorded output shows all four contract checks as true. This does not show
that a multi-agent system is more accurate or useful: no remote model was run.
It establishes a baseline that an API-backed comparison must beat under a
declared quality, cost, and latency protocol.

## What broke

Role separation can duplicate retrieval, lose context at a handoff, or make
responsibility less clear. A writer role is especially dangerous when it can
quietly turn a proposal into a mutation. This implementation avoids that risk
by making its output a read-only brief.

## Alternatives

Use one deterministic workflow for routine, inspectable checks. Use a single
planner when one coherent proposal is enough. Add specialist roles only when
their independently testable review adds value. A pull request or human editor
can be a better critic than another model.

## When to use it—and when not to

Use multi-role workflow when research, criticism, and drafting have different
evidence needs and their handoffs are observable. Do not use it to manufacture
confidence, parallelize an already simple task, or evade approval.

## Takeaway

More agents are justified only by measured, auditable improvement. Until then,
the smallest workflow that preserves evidence and human control is the best one.
