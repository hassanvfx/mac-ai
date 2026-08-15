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

This is an experimental control rather than a contest between two brand names.
Fix the task, retrieved evidence, schema version, decoding settings, retry
policy, and clock boundary before comparing a configured provider run. If the
answers differ, inspect the context and validation traces before calling either
route more reliable. A framework can introduce defaults, while a direct client
can expose details a framework normally manages; neither fact predicts answer
quality on its own.

Separate configuration from content. The objective and evidence arrive from
the caller. Endpoint, model identifier, and credentials arrive from the
environment only when an optional API experiment is explicitly requested.
Package versions, model names, retry behavior, redaction decisions, and timing
method belong in the resulting benchmark record. That separation prevents a
chapter draft or test fixture from becoming an accidental vehicle for a secret
or a provider-specific production decision.

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

The validation order matters. First parse the shape; then compare every path
with the retrieval allow-list; then overwrite caller-controlled fields such as
the objective and approval flag; finally decide whether the object has enough
evidence to be useful. A response that is valid JSON but includes
`outside.md` is an authorization failure, not a successful plan with one small
warning. This project retains the permitted portion for inspection and records
the rejected path, but it never treats the discarded citation as support.

No evidence has a stronger consequence. The plan schema may still parse, but
the implementation clears its steps and appends a missing-evidence warning.
That prevents a fluent model from converting an empty retrieval result into an
apparently actionable edit list. A human may use the objective to search again
or add research, but the system has not earned a grounded recommendation.

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

Use a narrow environment file or shell session for a controlled run and keep
it outside version control. Do not print the key while diagnosing a failure;
log only the non-secret configuration fields needed to reproduce the experiment.
If the base URL, model, or credential is absent, the adapter raises a
configuration error before a network request. That explicit failure is better
than a silent fallback to an unknown default model, whose output could later be
mistaken for a recorded comparison.

The optional local path follows the same discipline. A local endpoint or model
is still a configured provider with a model revision, context policy, and
failure modes. “Local” describes a deployment location, not an exemption from
schemas, provenance, evaluation, or approval. The deterministic fixture run is
the baseline that remains available when neither a local model nor an API is
configured.

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

Treat malformed output as a first-class test case. It can be invalid JSON,
missing fields, a response object with a parsing error, an unexpected scalar,
or a formally valid schema that contains an unapproved evidence path. The
direct and LangChain adapters must expose the failure rather than retry until
they get a convenient result. Retrying may be appropriate in a measured
production policy, but it changes cost, latency, and the probability of a
different answer, so it must be declared and evaluated.

The fixture comparison does not measure network latency or token use. It proves
that a composed adapter does not weaken the evidence allow-list or human
approval requirement. Once a provider is chosen, record separate timing
observations for request construction, remote response, parsing, and validation
where those boundaries matter. Do not use a no-network unit test to support a
claim about an API's speed, reliability, or model quality.

### Worked validation: a well-formed but unsafe plan

The fixture responder receives one allowed result:
`book/chapters/08-turning-meaning-into-geometry.md`. It returns an object that
looks valid: it has an objective, an evidence-path list, one implementation
step, no warnings, and `approval_required: false`. But the path list also adds
`outside.md`, and the model-supplied objective does not match the caller's
request. A parser that only checks JSON shape would accept this object and make
it look authoritative.

`validate_plan` applies the actual contract. It keeps only the retrieved
Chapter 8 path, records `Rejected unsupported evidence paths: outside.md`,
replaces the objective with the caller's objective, and forces
`approval_required` to true. The surviving step remains a proposal, not a
write. This is a useful distinction: the response was syntactically valid but
failed an evidence/authority check. A schema did its job only after the
application compared its fields with trusted context.

Run the same responder with no retrieved evidence. The path allow-list is
empty, so the validator clears every plan step and appends the warning “No
retrieved evidence: do not make an implementation claim.” It does not invent a
generic safe-sounding task list. The caller can retrieve again, narrow the
objective, or stop; it cannot present the model-shaped object as an
evidence-backed recommendation.

The LangChain fixture follows the same exercise through a different adapter.
It returns a parsed structured object through `with_structured_output`, then
passes it to the same validator. A parsing error or missing parsed object raises
instead of becoming a guessed fallback. The two routes therefore share the
important behavior even though their client code differs: only the supplied
evidence may survive, approval cannot be waived by the response, and malformed
output remains visible to the operator.

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

Schema evolution is another quiet failure mode. Adding a required field,
renaming a review finding, or changing the meaning of a status value can make
old fixtures appear to pass while downstream users interpret them differently.
Version the contract in the experiment record, keep compatibility decisions
explicit, and add a regression case for each newly enforced safety rule. A
schema migration is an interface change, not merely a prompt edit.

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

Template engines, tool-call APIs, and model-specific JSON modes are additional
alternatives. Choose them when they solve a demonstrated integration problem,
such as a provider's reliable native structured output, rather than because a
schema looks more official. The invariant survives the implementation choice:
only retrieved evidence may be cited, malformed or unsupported output is
visible, and the resulting object is a proposal awaiting human approval.

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

## Evidence trail

Read `research/06-structured-ai-systems/notes.md`, run
`experiments/10-systems/compare_structured_planning.py`, and use
`benchmarks/06-structured-systems/README.md` for the no-network contract run.

## Takeaway

The relevant comparison is not “SDK versus framework.” It is whether both paths
preserve the same evidence, expose failure, and stop before any consequential
action. That contract is what lets the next chapter add state without adding
unsafe autonomy.
