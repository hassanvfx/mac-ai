# Appendix G: Comparison Methods Without False Rankings

The word *compare* is deceptively simple. Two programs can both produce a
number while answering different questions; two model outputs can look similar
while using different data; two agent workflows can both sound helpful while
one has silently widened its authority. This appendix is a method for making
comparisons useful rather than theatrical.

## Begin with the decision

Write the decision the comparison should inform. “Choose a framework for a
small teaching classifier,” “decide whether learned retrieval improves a
fixture task,” and “decide whether a critic role catches a known omission” are
decisions. “Find the fastest model” is not yet a decision, because speed
depends on model artifact, workload, device, setup policy, precision, batch,
sequence length, and what the user values.

Once the decision is named, list the outcomes that matter. A framework exercise
may care first about matched predictions and failure inspection. A local-model
experiment may care about whether the model fits, follows a fixed prompt
contract, and remains responsive under a declared workload. A retrieval change
may care about acceptable-path recall and citation preservation. An agent
workflow may care about review coverage and unsafe-action refusal. Do not add a
metric because a tool happens to print it.

The comparison should be able to recommend “no difference established” or
“keep the simpler control.” That result is especially valuable in a learning
repository. It prevents an unmeasured preference from entering a chapter as a
technical conclusion.

## Hold the treatment still

For a framework comparison, hold data identity, train/validation/test split,
label mapping, preprocessing, seed policy, model capacity, objective,
optimizer semantics where comparable, metric definition, epoch/batch policy,
and reporting boundary as still as practical. Some APIs will differ. Record
those differences instead of pretending the programs are identical. The first
question is often narrower: do the implementations satisfy the same small
fixture contract?

For a device comparison, hold code path, model, input shapes, batch size,
precision, warm-up policy, repeat count, synchronization, and timing boundary.
Record OS, package versions, hardware, memory conditions if observed, and
whether the model was already cached. Separate model download and construction
from steady-state work unless cold start is the explicit treatment. A result
from a different workload is a new record, not the other row of the same table.

For retrieval, hold corpus snapshot, file allow-list, chunking policy, query
set, acceptable-path judgments, ranking limit, and scoring rule. A learned
encoder and a deterministic baseline may legitimately use different vector
representations; compare their returned paths and human relevance judgments,
not raw score magnitudes. Cosine values from different encoders are not a
common probability scale.

For workflow shapes, hold objective, corpus revision, retrieved evidence,
editorial checklist, output schema, approval rule, and evaluator fixed. If a
researcher/critic/writer graph receives richer context than a single planner,
then a changed outcome is not evidence that role specialization alone caused
the change. Compare a deterministic control first, then introduce one distinct
handoff whose failure-prevention value can be tested.

## Define success and failure before looking

Pre-register the smallest scorecard useful for the decision. For a classifier
fixture, include expected prediction/metric agreement and a selected error
case. For retrieval, include acceptable path at *k*, source resolution,
citation-key preservation, and a known unsupported query. For structured
planning, include allowed-path adherence, parse-failure visibility,
missing-evidence behavior, and approval requirement. For workflows, include
path attribution, review coverage, no-write behavior, and explicit terminal
status.

Define failures too. A timeout, missing model, malformed response, unsupported
path, empty retrieval, device fallback, or out-of-memory result is part of the
comparison data. Do not remove it from a summary because it makes one row less
attractive. If a condition cannot run, report it as unavailable under the
declared envelope. Another system running a different workload does not repair
that missing observation.

Use separate columns for observation and interpretation. “Both fixture
implementations classified the controlled examples correctly” is an
observation. “Framework A is better for vision” is a broad interpretation that
the fixture does not support. “The learned encoder placed an acceptable source
in the top four for this frozen question set” is an observation. “It understands
the book” is not.

## Measure with visible boundaries

Timing begins and ends somewhere. State where. If device work is asynchronous,
synchronize according to the runtime before measuring the wall-clock interval.
State whether warm-up was performed and whether a value is a minimum, median,
mean, percentile, or full list of repeats. State whether retries occurred. A
median over five warmed runs can answer a modest steady-state question; it does
not reveal first-use experience, tails, energy, multi-user contention, or
memory headroom.

Quality also needs a boundary. For a small RAG evaluation, create a versioned
question set before tuning, name acceptable and insufficient source paths, and
retain reviewer judgments. For a plan comparison, define the required sections
and evidence links. For a qualitative inference comparison, retain exact input,
model revision, decoding settings, output, and a rubric. A screenshot or one
attractive completion is evidence for a demonstration, not a quality rate.

Cost must be measured under the same protocol as quality and latency. API
requests may add retries, input tokens, output tokens, and provider-specific
billing; local runs may add model-download, disk-cache, memory, and thermal
conditions. Record what was actually observed. Do not infer cost from a model’s
parameter label or infer memory use from a marketing figure.

## Read a comparison table responsibly

A table should make mismatch visible. Put the workload, source revision,
device/model, measurement boundary, and limitation near the result. Use “not
measured” instead of leaving a reader to infer a zero or a win. Keep different
evidence types separate: a unit-test pass is not a millisecond result; a
reviewer judgment is not a package feature; an unavailable dependency is not a
failure of the underlying technique.

Prefer paired observations. Run two alternatives on the same case, preserve the
same trace fields, and inspect differences one row at a time. If an unexpected
result appears, return to the envelope: input, seed, version, model, device,
warm-up, corpus, prompt, schema, or evaluator. Do not immediately add more
abstractions or rerun until a preferred result appears.

If the comparison cannot support a decision, say so. The correct next step may
be a smaller fixture, a more precise workload, additional evidence cases, or no
comparison at all. This is not a weakness. It is the point at which an honest
engineering record remains more useful than a false ranking.

## A reusable comparison record

For every row, retain:

- Decision and question being answered.
- Alternative, exact version/model, and configuration.
- Input/corpus/data snapshot and expected outcome.
- Device/environment and dependency versions.
- Measurement or evaluation method, including warm-up/retries.
- Raw observations or a link to their committed record.
- Result, limitation, and the next decision it supports.

Commit the record when it supports manuscript prose. Keep generated caches,
local indexes, credentials, and bulky artifacts out of Git. A reader should be
able to reproduce the *question* and investigate a difference, even if their
machine cannot reproduce the same absolute value.

## Closing principle

The best comparison is not the one with the most rows or the strongest
headline. It is the one whose alternatives answer the same declared question,
whose failure cases remain visible, and whose conclusion stops exactly where
the evidence stops. That discipline is what allows this book to compare tensors
to models, models to workflows, and workflows to human control without turning
any of them into mythology.
