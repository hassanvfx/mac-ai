# Appendix B: Debugging AI Experiments Without Losing the Evidence

AI experiments fail in layers. A package can be absent, a device can be
unavailable, a tensor can have the wrong shape, a training run can be unstable,
an index can be stale, or a generated answer can cite no evidence. The fastest
way to make such failures mysterious is to change several layers at once. This
appendix provides a practical order of operations for the runnable exercises in
this book.

## First, classify the failure

Start by writing one sentence that says what failed and at which boundary. “The
experiment did not work” is not a classification. “The optional TensorFlow
group is not installed,” “the requested MPS device is unavailable,” “the model
output shape differs from the target,” and “the query returned no grounded
evidence” are classifications. Each points to a different next check.

Use five broad categories:

- **Environment:** an executable, dependency group, model artifact, storage
  allocation, device, or API configuration is unavailable.
- **Data contract:** inputs, labels, shapes, dtypes, normalization, split, or
  corpus paths are not what the code expects.
- **Numerical behavior:** a gradient is wrong, loss diverges, a result is
  nondeterministic, or a timing boundary is not valid.
- **Provenance:** an evidence path is missing, a citation key is lost, an index
  is stale, or a Markdown link leaves the configured corpus.
- **Policy:** a model output lacks evidence, attempts to widen its authority,
  or a proposed action reaches an approval boundary.

Classification is not bureaucracy. It limits the next action. An environment
failure calls for an installation or fallback check; it does not call for a
new architecture. A provenance failure calls for rebuilding or reviewing the
index; it does not call for a more fluent model response. A policy failure is a
successful stop condition, not something to optimize away.

## Reproduce the smallest case

Run the narrowest test or command that exercises the failed contract. For a
tensor broadcasting issue, begin with `experiments/01-tensors/broadcasting.py`
or its matching test, not a full neural-network training loop. For gradient
confusion, use the scalar autograd example before inspecting an optimizer. For
retrieval, use the frozen fixture tests before indexing the live manuscript.
For approval, use the no-write checkpoint test before considering a writer.

Reduce inputs while retaining the error. A single batch, one known text query,
or one fixture document is easier to inspect than an entire dataset. Preserve
the exact seed, command, error text, and environment facts. If reducing the
case changes the behavior, record that fact too; it tells you that scale,
ordering, or initialization may matter.

Do not make an optional dependency a prerequisite for basic diagnosis. The
repository deliberately retains deterministic CPU-capable controls. If an
embedding model cannot download or a local runtime is absent, the fixture
retrieval path can still test chunking, path attribution, citation propagation,
and refusal. If MPS is unavailable, device-selection tests can still confirm
that the program labels the fallback rather than silently changing the request.

## Inspect contracts in order

For a learning pipeline, inspect inputs before outputs. Print or assert shape,
dtype, device, and a small value sample. Then inspect the model output shape,
loss input order, gradient presence, and parameter update. Only after those
contracts are true should you reason about a training curve. A falling loss on
misaligned labels is not evidence that a model learned the intended task.

For a benchmark, inspect the workload before the number. Identify model,
input dimensions, batch size, precision, selected device, warm-up policy,
repetitions, and synchronization. A number that cannot be tied to these facts
is an observation to repeat, not a number to put in a comparison table. Keep
cold start, model download, and steady-state work separate whenever the
question distinguishes them.

For Book Intelligence, inspect corpus membership before relevance. A returned
source must be inside the declared repository subtrees and resolve to a current
file. Then inspect the excerpt and its citation keys. A high-ranked chunk is a
candidate, not support. If there is no positive evidence, the correct answer is
the missing-evidence message. Never repair a retrieval miss by letting a model
invent a path or an answer.

For a structured plan, inspect the trusted allow-list before its prose. The
validator may accept only retrieved paths, overwrites caller-controlled fields,
and always restores the human-approval requirement. A syntactically valid JSON
object that names `outside.md` is an unsafe output that has been correctly
rejected, not a mostly successful plan.

## Make installation failures explicit

Before installing an optional group, check both free disk space and the scope
of the dependency. The environment setup chapter documents the commands; the
important debugging principle is to state what is missing and what remains
available. For example: “The TensorFlow group is not installed; the PyTorch
and deterministic tests remain runnable.” This keeps a learning session moving
without pretending that a comparison was executed.

If installation is appropriate, use the project-managed command and rerun the
narrow test first. Do not mix an installation, a package upgrade, a source
change, and a new model download in one unrecorded step. If storage is
insufficient, stop before the download and record the estimate or available
space. Freeing storage is a user decision when it could affect unrelated data.

Credentials deserve a stricter rule. A missing API key or endpoint should fail
before a network call and should never appear in an error report. Record only
non-secret facts needed for reproduction: adapter type, model identifier,
endpoint class, package version, and the fact that credentials were absent or
invalid. The deterministic test suite is the correct fallback until a controlled
provider experiment is deliberately configured.

## Turn the repair into evidence

When you identify a fix, preserve the before-and-after conditions. Add a unit
test when the failure expresses a stable correctness or safety property. Add a
fixture case when it needs frozen source-shaped input. Add a benchmark record
when the observation depends on a machine, workload, or timing method. Add a
chapter warning when the reader is likely to encounter the same confusion.

Keep the repair scoped. A test that proves blank queries refuse an answer should
not also assert model quality. A test that proves MPS falls back to CPU should
not claim a performance advantage. A review test that catches an escaped link
should not read the target outside the corpus. Small tests make a later failure
diagnosable and prevent an attractive demo from becoming a broad, untested
guarantee.

Finally, update the active project journal before committing. Record what
changed, commands run, result, limitations, and the next action. The journal
should link to detailed benchmark or research records instead of pasting raw
terminal output. That leaves the next work session with a decision trail and
keeps the canonical manuscript focused on what readers need to learn.

## A compact triage loop

1. State the failed contract in one sentence.
2. Reproduce it with the smallest fixture or test.
3. Inspect environment, inputs, and provenance before changing a model.
4. Change one declared condition.
5. Re-run the narrow check, then the relevant suite.
6. Record the result, limitation, and whether it became a test, fixture, or
   benchmark.

The point is not to eliminate failure. It is to make failure teach us something
that a later reader can reproduce and a later agent cannot quietly obscure.
