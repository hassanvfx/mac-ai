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

Start a reliability policy with an inventory of promises. For each promise,
name the input boundary, the code path that enforces it, a deterministic test
case, the trace field that makes the result inspectable, and the condition that
would make a release fail. “The assistant is safe” is not an inventory entry.
“A plan cannot retain an evidence path outside its retrieved allow-list” is.
The narrower wording tells a contributor where to look when a regression
appears and tells a reader exactly what has—not—been demonstrated.

Reliability also requires separation of concerns. Correct mathematical
experiments, accurate editorial prose, grounded retrieval, valid navigation,
and print-ready layout are related release properties but have different
authoritative checks. A green Python test suite cannot prove a diagram prints
legibly; a successful DOCX conversion cannot prove a generated plan cites the
right source. The beta release gate must assemble evidence from each layer
without letting one convenient green command stand in for all of them.

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

The fixture cases are specification examples, not merely regression data. A
new capability should arrive with at least one positive case, one missing or
malformed-input case, one provenance or authority-boundary case, and a clear
expected outcome. Keep cases small enough that a failing result points to a
specific contract. If a case needs a real provider, split its deterministic
structural checks from its explicitly configured, non-secret benchmark instead
of making ordinary contributors depend on a credential.

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

Define graceful degradation before an outage occurs. If learned embeddings are
unavailable, label and use the deterministic retrieval baseline for contract
tests; do not claim semantic search occurred. If a model adapter is unavailable,
return its configuration error or continue only through an explicitly
deterministic no-model route. If no evidence is retrieved, refuse rather than
write a generic plan. A reliable fallback preserves the important boundary; it
does not merely keep a user interface talking.

Traces should be actionable but proportionate. Include the case ID, corpus or
fixture revision, declared policy, pass/fail result, and details needed to
reproduce a failure. Redact secrets and avoid storing unnecessary private text.
For a controlled model experiment, add provider/model identity and timing
fields only after choosing a configuration. Trace retention then becomes an
operational decision with ownership and deletion rules, not an accidental pile
of prompts and outputs.

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

Turn these observations into release gates. For a local beta candidate: install
from the locked environment; run format/lint and deterministic tests; execute
the fixture reliability suite; audit manuscript links, citations, and required
sections; build the site; and build the DOCX. Each failure blocks the candidate
until its cause and retest are recorded. The final Word-exported PDF, full
page-by-page visual inspection, and Lulu-specific preflight remain separate
print gates because they depend on an externally produced artifact and current
publication settings.

An explicit unknown is a valid release result. This project has no selected
API provider/model benchmark, no measured API latency or quality comparison,
and no final Word PDF in this repository. Those absences must appear in the
beta record rather than becoming blank cells in a performance table. The
deterministic suite shows its limited contracts; it does not fill the missing
external evidence.

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

Beware of metric theater as well as silent failures. Counting many test cases
does not help if they all exercise the same happy path. A high retrieval score
does not demonstrate citation entailment. A low average latency does not show
that refusals are safe, that every trace was retained, or that a tail latency
is acceptable. Pair quantitative observations with the contract they are meant
to support, preserve failure samples, and revise the evaluation set when a
real incident reveals a missing category.

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

Release checklists and human review are another alternative to automated
evaluation, not an afterthought. They are especially important for claims that
need subject-matter judgment, for print layout, and for changes to the safety
policy itself. Automation makes repeatable facts cheap to recheck; it does not
transfer editorial, legal, or publication responsibility to a script.

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

Before increasing authority, use a capability review: What new action becomes
possible? What exact evidence and approval scope are required? Which test
proves rejection, unavailability, and retry behavior? What state is retained,
where, and for how long? How does the feature roll back without removing source
work? If these questions cannot be answered, keep the capability read-only.
This provides a concrete stopping rule for beta enthusiasm.

### Worked release gate: what a local beta can honestly claim

Start at a clean checkout and install the locked Python environment. Run the
numerical and assistant tests, then run `make audit-book`. A successful result
establishes only the contracts those commands cover: deterministic experiment
expectations, retrieved-path and citation-key preservation, missing-evidence
refusal, no-write planning, workflow state transitions, required chapter
headings, valid citation keys, and resolvable local manuscript paths. Preserve
the command output or CI result with the commit identifier; do not summarize it
as “the book is correct.”

Next build the Docusaurus site from the canonical chapters. That result checks
the presentation shell and navigation build, not whether a reader understands
the material. Build the DOCX from the committed Lulu reference template. That
checks the manuscript conversion and print-asset pipeline, not final print
approval. Render the DOCX to page images and inspect the pages at the intended
6×9 scale; a table break, clipped code listing, or unreadable diagram can pass
every preceding text and Python check.

At this point the project can call itself a *local beta candidate* only if the
word target, editorial matrix, automated gates, and interim visual proof all
meet their stated criteria. It cannot yet claim a release-ready Lulu interior:
the final export must come from Microsoft Word on macOS, its PDF needs
preflight and page-by-page review, and current Lulu requirements must be
checked against the actual upload artifact. It also cannot claim a deployed
course without a chosen GitHub remote and Pages configuration.

Finally, keep the release record honest about exclusions. This repository has
not run a configured API comparison, so it has no comparative API latency,
token-cost, or quality result. It has no final cover because page count is not
frozen. It has no ISBN or proof-order decision. These are not failed tests;
they are deliberate user-gated production decisions. Naming them prevents a
green local suite from being mistaken for authorization to publish or spend
money.

## Evidence trail

Read `research/07-workflow-graphs/notes.md`, run
`evals/run_reliability.py`, and inspect the versioned cases in
`evals/book_intelligence.jsonl`; generated traces remain local under
`.book-intelligence/`.

## Takeaway

Trust is a continuing engineering practice. This beta is trustworthy only in
the narrow ways its tests and traces demonstrate—and it remains honest about the
work required before production or print release.
