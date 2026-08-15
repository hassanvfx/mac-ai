---
sidebar_position: 10
title: From LLM Calls to AI Systems
---

# From LLM Calls to AI Systems

## Intuition

An LLM call becomes a system when its input, output, failure behavior, and
permissions are explicit. An orchestration library can make integration easier,
but it cannot turn ungrounded context into evidence or a parsed JSON object
into permission to act.

The useful unit of comparison is an adapter contract. Given the same retrieved
evidence and requested schema, each adapter should either return a validated,
source-scoped object or expose why it cannot. Provider choice, prompt wording,
and parsing convenience are secondary to that invariant when the result may
influence a chapter or experiment plan.

## Problem

The Book Intelligence Assistant needs to turn retrieved source material into a
chapter-improvement plan and a critique. We want to compare a direct API path
and LangChain without changing the evidence, hiding parsing errors, or giving
either path write access.

## Minimal implementation

[structured_planning.py](../../src/from_tensors_to_agents/structured_planning.py)
defines Pydantic schemas for a proposal and review. Both receive only retrieved
paths and excerpts. Validation drops paths that were not retrieved, records a
warning, clears action-like steps when no evidence exists, and forces
`approval_required` to `true`.

The direct route is deliberately thin: an OpenAI-compatible client reads three
environment variables only when requested, sends the schema, and returns the
parsed object. Missing configuration fails before a network call.

## Real implementation

LangChain’s `ChatOpenAI` integration exposes a similarly structured runnable
through `with_structured_output`. The implementation uses `include_raw=True`
so parsing failures remain visible instead of being silently converted into a
plausible result. The two routes are compared over the same evidence list, not
over separately retrieved contexts. LangChain documents structured output for
this integration [@langchain2026chatopenai].

Install the optional group and run the no-network fixture comparison:

```bash
df -h .
uv sync --group agents
uv run --group agents python experiments/10-systems/compare_structured_planning.py
```

The `--api` flag is deliberately separate. It requires
`BOOK_INTELLIGENCE_API_KEY`, `BOOK_INTELLIGENCE_API_BASE`, and
`BOOK_INTELLIGENCE_MODEL`; credentials belong in the process environment, never
in a source file, shell history, benchmark record, or commit.

## Experiment

The recorded fixture run proves a narrow invariant: both adapters receive the
same retrieval result and return the same allowed source path. The regression
tests then send an invented path, an empty evidence set, malformed structured
output, and absent configuration. These are system-contract tests, not a
comparison of model intelligence or provider quality. See
`benchmarks/06-structured-systems/README.md` for the package versions and
limits.

## What broke

A valid schema can still contain an unsupported citation, a plan can sound
reasonable with no evidence, and a compatible-looking endpoint can lack the
structured-output behavior assumed by an adapter. The safe response is to
filter against the retrieved paths, preserve the parse error, and stop. Do not
recover by inventing a fallback answer or silently changing the requested
schema mode.

## Alternatives

A direct SDK has the smallest abstraction surface and makes HTTP/API behavior
easy to inspect. LangChain is useful when several providers, prompt components,
or structured runnables truly need common composition. A local model adapter or
handwritten JSON validation may fit an offline tool better. The best choice is
the one whose failures the team can understand and test.

## When to use it—and when not to

Use structured planning when downstream code needs named fields, auditable
evidence paths, and predictable failure handling. Do not use it to disguise an
unsupported conclusion as a typed object, or to bypass a human approval step.
For a one-off inspected model call, a direct prompt may be clearer than adding
an orchestration dependency.

## Takeaway

The relevant comparison is not “SDK versus framework.” It is whether both paths
preserve the same evidence, expose failure, and stop before any consequential
action. That contract is what lets the next chapter add state without adding
unsafe autonomy.
