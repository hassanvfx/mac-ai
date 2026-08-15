---
sidebar_position: 14
title: Building an AI System You Can Actually Trust
---

# Building an AI System You Can Actually Trust

## Intuition

Reliability comes from evaluation, observability, constraints, and recovery—not
from a single impressive demo. A fluent plan is not reliable unless its evidence,
failure mode, permission boundary, and trace can be inspected.

For this book, “trust” is deliberately narrow. It does not mean that the
assistant knows whether a technical claim is true, that a retrieved paragraph
is complete, or that a proposed revision is good prose. It means the program
can demonstrate a few concrete behaviors: preserve an evidence path, preserve
a citation key when one is present, refuse when evidence is missing, keep a
proposal separate from a write, and leave an inspectable record of those
checks. Narrow promises are more useful than a broad promise that no test can
prove.

## Problem

The Book Intelligence Assistant combines retrieval, planning, critique, and
approval. The beta needs a repeatable way to prove its narrow guarantees and
state plainly what it cannot yet guarantee.

Reliability has to survive ordinary changes. A new chapter can alter retrieval
ranking; a refactor can drop a citation key; an optional model installation can
be unavailable on a reader's machine; a graph resume can be mistaken for an
authorization to act. A one-off demo will usually miss these regressions. The
project therefore treats a versioned fixture corpus and deterministic evaluator
as a safety net, while keeping the much larger live book corpus local for
interactive work.

## Minimal implementation

The frozen fixture corpus and [reliability runner](../../evals/run_reliability.py)
exercise evidence location, missing-evidence refusal, no-write planning, and
editorial review. It writes a JSON trace only under ignored
`.book-intelligence/`, with a case count, result details, and explicit no-write
policy.

The frozen cases are small on purpose. They test six distinct contracts:

1. locating a known evidence path;
2. returning a grounded answer with that path visible;
3. carrying a BibTeX citation key from indexed research;
4. refusing an unsupported ISBN question;
5. proposing an experiment without modifying a source; and
6. flagging a deliberately missing editorial `Alternatives` section.

The trace is generated local state, not book evidence and not a substitute for
test output. Its safe location makes it useful for inspecting a run without
asking contributors to commit potentially noisy details. A release record can
summarize its result, but should link to the versioned fixture and evaluator
that made the trace meaningful.

```bash
uv run --group agents python evals/run_reliability.py
```

## Real implementation

The system’s reliability policy is layered. Retrieval must retain repository
paths and citation keys. Grounded answers return evidence or refuse. Structured
plans discard invented paths. LangGraph pauses before approval and its approved
terminal state still performs no write. These controls are regression-tested
without a credential or remote model.

Think of the controls as a chain, not a single guardrail. Ingestion attaches
provenance to each chunk. Retrieval passes that provenance to the answer or
plan layer. The answer layer refuses to manufacture support when the retrieved
set is empty. Planning filters paths against the repository evidence it was
given. Review checks deterministic editorial requirements. Finally, the graph
records an approval decision but reaches an explicit no-write terminal state.
If one link is removed, a later layer must not guess that the earlier guarantee
still holds.

The policy also separates deterministic and model-dependent behavior. Fixture
retrieval, path validation, source-boundary checks, required-section review,
and approval-state transitions should pass without network access. A language
model may help phrase a plan or critique, but it inherits the same evidence and
approval requirements. Missing API configuration, unavailable local weights,
or malformed structured output are failures to surface, not invitations to
fall back to an uncited free-form answer.

## Experiment

Run the reliability suite from a clean environment and inspect the generated
trace. A passing trace shows that the frozen cases met their declared contract;
it does not prove correctness on every future manuscript or API response.
Record latency, tokens, provider/model identity, and failures only when a
controlled API experiment actually runs.

Start with `uv sync --group dev`, then run the suite. A clean result reports the
number of cases and writes `evaluation.json` plus `reliability.json` below the
ignored local directory. Read a failed case before rerunning it: its detail
contains the retrieved paths, refusal text, or review findings needed to decide
whether the regression is in fixture data, the evaluator, or the assistant.

For a model-backed experiment, declare the corpus revision, task set, provider,
model revision, prompt/schema, retries, temperature, timing boundaries, and
redaction rules in a committed benchmark record. Include failed or refused
requests. A median latency without request count, warm-up policy, or model
identity is not a useful reliability result; it is merely a number.

## What broke

The project has already observed weak retrieval neighbors, absent API
configuration, malformed structured output, empty evidence, rejected approval,
and a SQLite thread constraint. Each became a test or documented limitation.
The dangerous failure is silent degradation: turning a missing model, source,
or approval into a plausible write.

There are several subtle ways to make this worse. A trace can claim success
while hiding a failed sub-step; the runner therefore retains per-case details.
An evaluator can test only a mocked answer and miss broken indexing; the frozen
cases build the index before checking results. A safety test can pass while a
different code path writes a file; the planning case snapshots fixture files
before and after the proposal. These are not proofs of universal safety, but
they turn known failure modes into regressions that a contributor can reproduce.

## Alternatives

Manual editorial review, pull requests, and conventional search remain strong
alternatives. Hosted tracing can help a team, but creates privacy, retention,
and vendor concerns. A small local trace is preferable while this beta has no
remote model run.

Static tools also belong in the reliability stack. The book audit validates
chapter sections, citation keys, and local links. The Python tests validate
numerical lessons, retrieval contracts, structured-output failures, and graph
states. The Docusaurus build catches broken course navigation, while the DOCX
build exposes print-asset conversion problems. These tools do different jobs;
none makes the others redundant.

## When to use it—and when not to

Use the assistant to locate evidence and prepare proposals. Do not use it as an
authority for unsupported claims, autonomous edits, legal/safety decisions, or
external actions. Any future writer must be a separate, explicitly approved,
least-privilege capability.

Use the trace to answer a modest operational question: did this revision still
meet the contracts we have chosen to enforce? Do not use it to answer a much
larger epistemic question: is the whole manuscript correct? A human editor,
subject-matter review, and reproducible experiments remain necessary. When a
new capability is proposed, define its failure cases and the evidence required
for release before wiring it into a workflow with more authority.

## Evidence trail

Read `research/07-workflow-graphs/notes.md`, run
`evals/run_reliability.py`, and inspect the versioned cases in
`evals/book_intelligence.jsonl`; generated traces remain local under
`.book-intelligence/`.

## Takeaway

Trust is a continuing engineering practice. This beta is trustworthy only in
the narrow ways its tests and traces demonstrate—and it remains honest about the
work required before production or print release.
