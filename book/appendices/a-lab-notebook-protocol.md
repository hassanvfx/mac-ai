# Appendix A: A Lab Notebook Protocol for Reproducible AI Work

The runnable files in this repository are not illustrations to be executed
once and forgotten. They are small experiments: each one asks a bounded
question, controls enough conditions to make the result interpretable, and
leaves an evidence trail that another reader can inspect. This appendix is the
protocol used throughout the book. Use it when adapting a chapter experiment,
when adding a new comparison, or when a result seems surprising enough to
deserve more than a terminal screenshot.

## Start with a question that can fail

Avoid questions such as “Is MPS fast?” or “Does RAG work?” They combine too
many conditions and invite a persuasive answer. A useful first question names a
workload, a condition, and an observable outcome. For example: “Does the tiny
network reduce its loss on the fixed synthetic dataset when the selected device
is available?” Or: “Does the fixture retrieval query return the expected
source path in the first four candidates?” These questions can return a useful
*no*.

Write the expected result before you run the program. For a numerical exercise,
that might be a tensor shape, a known gradient, or a loss that falls below a
declared threshold. For a retrieval exercise, it might be a source path,
citation key, or missing-evidence refusal. For a framework comparison, it
might be agreement on a tiny controlled fixture rather than agreement on a
headline performance number. An expected result is a debugging aid, not a
license to discard failures.

State what the run cannot answer. A tiny synthetic training run can test the
data/device/gradient contract; it cannot estimate production throughput or
generalization. A versioned fixture can test provenance and refusal; it cannot
prove semantic retrieval quality on the changing manuscript. This sentence
often prevents the most common error in AI experimentation: a narrow
observation quietly becoming a broad claim.

## Record the experimental envelope

Every record should make it possible to reconstruct the envelope around a
result. At minimum, record:

- the exact command and its working directory;
- the Git commit or another immutable source revision;
- the seed and every deterministic setting that the program controls;
- Python and relevant package versions;
- operating system, hardware, and selected device;
- input data identity, split, preprocessing, and model identifier where used;
- the measurement boundary, warm-up policy, repeat count, and summary rule;
- the expected outcome, actual result, and conditions that were not measured.

This is intentionally more than a benchmark table. A median timing without a
workload is not a meaningful comparison. A model name without a revision can
resolve to changed weights later. A device name without a fallback rule can hide
that a CPU-only machine ran different code. The repository's benchmark records
are Markdown so that the explanatory conditions live beside the values instead
of being buried in a dashboard.

Use a fresh record when a material condition changes. Changing model weights,
batch size, sequence length, precision, device, warm-up policy, or timing
boundary creates a new experiment. Do not overwrite an earlier number so that
two incompatible runs look comparable. Link both records and explain the
change. Version history is useful here: it preserves the fact that an earlier
observation was true under its own stated conditions even when a later run uses
a better protocol.

## Run in a deliberate order

Begin with the smallest deterministic route. The tensor, gradient, and
Book-Intelligence fixture tests run without a downloaded model or API key, so
they are useful controls on a new machine. Run the relevant test first; then
run the companion program with its documented default. If the control fails,
do not start installing larger optional stacks in the hope that a different
backend will hide the problem.

Before an optional download, check disk space with `df -h .`. Before a GPU or
MPS observation, print the selected device and retain the CPU fallback test.
Before a provider-backed comparison, verify that the endpoint, model, and key
are supplied through the documented environment variables. Never put a key in
the notebook, source file, benchmark record, or shell transcript. If an
optional dependency is absent, record that it was unavailable and continue
with the baseline route where possible. Unavailability is a result about the
environment, not a reason to invent a substitute measurement.

Make one change at a time. If a local-model run fails after increasing context,
do not simultaneously change quantization, prompt, and runtime. Revert to the
last known-good envelope, verify it, then vary one input. This rule is slower
than speculative tweaking in the first minute and much faster once someone has
to explain why two terminal outputs disagree.

## Read results as evidence, not verdicts

For learning code, inspect the thing the program claims to compute. Check
tensor shapes before interpreting loss. Check a gradient on a small analytic
case before trusting a training curve. Check individual errors and the
confusion matrix before claiming that a vision model learned a class. Check
paths and excerpts before treating a RAG packet as support. The final scalar is
usually the last piece of evidence, not the first.

For timing, separate setup from steady-state work. Model construction,
download, compilation-like initialization, allocator behavior, and the first
device call can dominate short runs. Record whether the clock includes them.
Use a declared warm-up, repeat the measured portion, retain the individual
values when practical, and state the summary statistic. Synchronize around an
asynchronous device measurement when the runtime requires it. None of these
rules creates a universal “real” number; they make the number answer a visible
question.

For qualitative outputs, retain the prompt or query, the retrieved paths or
model artifact, the exact response, and a reviewer judgment. Do not substitute
an attractive screenshot for the whole output. Keep counterexamples and
refusals in the same dataset as successes. A system that is safe only in the
examples selected for a chapter has not yet earned a reliability claim.

## Turn a surprise into a durable test

When a run breaks, first classify the failure. Is it an environment issue, an
input/shape issue, a numerical issue, a provenance issue, an unavailable
optional backend, or an unsupported claim? Preserve the smallest reproduction:
command, inputs, error, environment facts, and any safe workaround. Then decide
whether the failure should become a unit test, a fixture evaluation, a benchmark
note, or a warning in the chapter.

A good regression test is narrow. The Book Intelligence suite, for example,
asserts path attribution, citation-key preservation, blank-query refusal,
empty-corpus refusal, deterministic ranking, and escaped-link reporting. It
does not pretend to evaluate a language model. Likewise, the device-selection
tests assert explicit MPS selection and CPU fallback without claiming that
either device is faster. The test's name should state the safety or correctness
property it preserves.

When a result changes after a code revision, do not ask only whether the new
number is better. Ask which layer changed: input, seed, dependency, device,
measurement boundary, model, chunking, or interpretation. A written record
makes this comparison possible. If no layer can explain the change, label the
observation unresolved and reproduce it before using it in a chapter.

## A pre-commit checklist

Before committing an experiment or its manuscript claim, verify the following:

- The code runs from the documented command or its limitation is stated.
- The record identifies versions, seed, data/model, device, and measurement
  method appropriate to the claim.
- The prose separates observed facts from interpretation and from open work.
- A citation or committed benchmark record supports every performance, memory,
  framework, or model-behavior statement.
- Generated caches, indexes, checkpoints, downloads, and credentials are not
  staged for Git.
- A failure or fallback path is tested where the experiment depends on one.

The same discipline applies to editorial work. A chapter change should name
the experiment or source it relies on, pass the book audit, and link to a
runnable file when it describes an implementation. When a proposed AI workflow
suggests a change, it stops at the human approval boundary described in Chapters
11 and 12. A plan is evidence for a review conversation; it is not permission
to rewrite the book.

## Closing principle

Reproducibility is not the promise that every reader gets the same number on a
different machine. It is the stronger practical promise that a reader can see
what was run, under which conditions, what it produced, what it did not show,
and how to investigate a difference. That is enough to turn a learning project
into an engineering record—and enough to keep a later agent workflow grounded
in inspectable work rather than confident-looking guesses.
