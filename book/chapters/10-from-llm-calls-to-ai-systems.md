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

Structure is a data contract, not a truth contract. A schema can confirm that
an output has fields called `evidence_paths` and `steps`; it cannot establish
that a cited path exists, that an excerpt supports a claim, or that a suggested
step is appropriate. The adapter must validate model-shaped data against the
evidence the retrieval layer actually supplied. Untrusted input crosses a
boundary, is checked, and is rejected or normalized before downstream code
relies on it.

## Problem

The Book Intelligence Assistant needs to turn retrieved source material into a
chapter-improvement plan and a critique. We want to compare a direct API path
and LangChain without changing the evidence, hiding parsing errors, or giving
either path write access.

Both adapters receive the same objective, allowed source paths, excerpts,
schema, and no-write instruction. If one route retrieves different context or
accepts different paths, a difference in its final plan cannot be attributed to
the SDK/framework choice. Keep provider/model comparisons separate until a
provider is selected and a controlled benchmark records its conditions.

## Minimal implementation

[structured_planning.py](../../src/from_tensors_to_agents/structured_planning.py)
defines Pydantic schemas for a proposal and review. Both receive only retrieved
paths and excerpts. Validation drops paths that were not retrieved, records a
warning, clears action-like steps when no evidence exists, and forces
`approval_required` to `true`.

The direct route is deliberately thin: an OpenAI-compatible client reads three
environment variables only when requested, sends the schema, and returns the
parsed object. Missing configuration fails before a network call.

The plan schema includes an objective, evidence paths, steps,
unsupported-claim warnings, and `approval_required`. The review schema includes
the same objective and paths plus findings. After parsing, validation discards
every path outside the retrieved allow-list, appends a warning, and replaces the
model's objective with the caller's objective. With no retrieved evidence, it
clears plan steps and adds a warning instead of accepting a well-formed but
unsupported proposal. It forces approval to `true` even if a model emits
`false`.

This normalization makes authority explicit. A model can propose text; it
cannot widen the files it may cite, redefine the request it received, or waive
human review through a field in its own output.

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

The environment boundary is intentional. The project does not choose a public
endpoint or a model for the reader, and it does not need an API key for the
deterministic test suite. A configured adapter must still declare endpoint type,
model identifier, retry policy, redaction policy, and timing boundary in a
benchmark record before its output can support a comparison claim. Loading a
key is not authorization to make an uncontrolled experiment or a repository
change.

## Experiment

The recorded fixture run proves a narrow invariant: both adapters receive the
same retrieval result and return the same allowed source path. The regression
tests then send an invented path, an empty evidence set, malformed structured
output, and absent configuration. These are system-contract tests, not a
comparison of model intelligence or provider quality. See
`benchmarks/06-structured-systems/README.md` for the package versions and
limits.

Read the comparison output as a contract trace. It prints the paths preserved
by the direct and composed adapters and whether both demand approval. It does
not say their natural-language plans are equivalent, because the default run
uses fixtures rather than a remote model. The tests exercise an invented
`outside.md` path, an empty evidence list, malformed structured output, and
absent API variables. A future model experiment must hold task set, model,
settings, and retrieved context fixed before interpreting a difference between
adapters as overhead or reliability.

## What broke

A valid schema can still contain an unsupported citation, a plan can sound
reasonable with no evidence, and a compatible-looking endpoint can lack the
structured-output behavior assumed by an adapter. The safe response is to
filter against the retrieved paths, preserve the parse error, and stop. Do not
recover by inventing a fallback answer or silently changing the requested
schema mode.

Parser recovery is not correctness. A framework may retry, coerce a field, or
return a partially parsed value; those behaviors can be useful, but they must
be visible and followed by the same evidence validation. This project chooses
failure over a guessed plan whenever structured output is absent or malformed.
A reader can then fix configuration, adjust a declared schema, or use the
deterministic path without pretending the model supplied grounded output.

## Alternatives

A direct SDK has the smallest abstraction surface and makes HTTP/API behavior
easy to inspect. LangChain is useful when several providers, prompt components,
or structured runnables truly need common composition. A local model adapter or
handwritten JSON validation may fit an offline tool better. The best choice is
the one whose failures the team can understand and test.

A simple typed function around a provider SDK is often enough for one model and
one task. Use an orchestration framework when common adapters, message handling,
retrievers, or tracing reduce repeated, tested code. Avoid an abstraction merely
to make a prototype look agentic: every layer adds defaults, version constraints,
and a new failure vocabulary that tests and benchmarks must cover.

## When to use it—and when not to

Use structured planning when downstream code needs named fields, auditable
evidence paths, and predictable failure handling. Do not use it to disguise an
unsupported conclusion as a typed object, or to bypass a human approval step.
For a one-off inspected model call, a direct prompt may be clearer than adding
an orchestration dependency.

Use schemas at a boundary where another program will inspect fields, route a
workflow, or present a reviewable plan. Do not confuse a schema with a
capability grant: a structured plan remains read-only until a separate,
least-privilege action is explicitly approved.

## Takeaway

The relevant comparison is not “SDK versus framework.” It is whether both paths
preserve the same evidence, expose failure, and stop before any consequential
action. That contract is what lets the next chapter add state without adding
unsafe autonomy.
