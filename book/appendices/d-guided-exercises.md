# Appendix D: Guided Exercises and Evidence Prompts

These exercises are deliberately small. Their purpose is to make a reader
observe a contract, record the conditions, and explain a failure before moving
to the next abstraction. Each exercise has a runnable companion file, but the
terminal output alone is not the answer. Record the command, source revision,
device, expected result, actual result, and one limitation in your lab notebook.

## 1. Broadcasting is an alignment rule

Run `experiments/01-tensors/broadcasting.py`. Before running it, write down
the shapes you expect for every operand and the resulting tensor. Then change
one axis in a copy of the exercise so that two non-singleton dimensions no
longer agree. Predict whether the failure is caused by values, dtype, device,
or shape; run it; and retain the error message.

The evidence to collect is a shape table, not a vague statement that
“broadcasting happened.” Explain which axis was implicitly repeated and why
the invalid case could not be repeated. Do not turn this into a performance
test; it is a data-contract exercise. Restore the original source after the
experiment or work in a disposable copy.

## 2. Derivatives are local evidence

Run `experiments/02-gradients/autograd.py`. Identify the scalar objective,
input value, and expected derivative before inspecting the output. Change the
input in a copy and calculate the new derivative by hand. If the automatic and
manual values disagree, inspect the definition of the objective and the point
at which the derivative is evaluated before adding an optimizer or a neural
network.

Write one sentence separating the claim the run supports from the claim it does
not. A correct scalar gradient supports that this small autograd path behaves
as expected. It does not establish that a larger network will train, that an
optimizer is configured correctly, or that a chosen loss is appropriate for a
dataset.

## 3. A training curve needs a control

Run `experiments/03-pytorch/train_tiny_network.py`. Record the printed seed,
selected device, initial/final loss, and any declared accuracy or prediction
check. Run it a second time without changing conditions. If the output differs,
identify whether the script controls random seeds, device selection, or data
ordering before interpreting the difference.

Next, make one controlled change: reduce epochs, alter learning rate, or change
the synthetic data size. Do not change more than one. Record the new envelope
in a separate observation rather than overwriting the first. Explain whether
the new result answers the same question. A shorter run may be useful for a
smoke test yet incomparable to the original training observation.

## 4. Device selection is not a speed claim

Run the Day 1 tests and the training example on the available machine. Note
whether MPS or CPU is selected and whether the requested-device fallback is
explicit. On a machine without MPS, the useful result is a clearly labelled CPU
route, not a failure to be hidden. On a machine with MPS, a successful run is
still not a PyTorch-versus-CPU benchmark.

If you measure timing, define the workload first: model, data shape, batch
size, precision, warm-up policy, repeat count, synchronization rule, and clock
boundary. Keep construction and download out of a steady-state measurement
unless cold-start experience is the declared question. Store individual timing
values and name the summary. If you cannot state these conditions, record no
performance conclusion.

## 5. Compare frameworks by invariant

Run the PyTorch and TensorFlow vision fixture commands documented in Chapters
4 and 5. Confirm that data split, seed, labels, metric definition, and expected
fixture output are matched before comparing any result. The first useful check
is whether both implementations satisfy the small shared task. A difference
means inspect preprocessing, label mapping, output activation/loss convention,
and update loop before attributing it to the framework.

Write a two-column note: “observed under this fixture” and “not established.”
For example, agreement on a synthetic classification contract may be observed;
general vision quality, model ecosystem, memory use, and throughput are not.
This habit protects a comparison chapter from becoming an API preference essay.

## 6. Trace a tokenizer to a label

Run `experiments/06-transformers/inspect_sentiment.py` only after checking
available disk space and recording the model revision/configuration. Inspect
the input text, token IDs, special tokens, attention mask, raw logits, label
map, and ranked output. Compare the manual route with any high-level pipeline
only as an interface check: both paths should use the same model and label map.

When the labels disagree, work backwards from the label map to the logits and
then to tokenization. Do not begin by declaring a model hallucination. Record
the exact input and model identity, and state whether model weights were newly
downloaded. A single classification is an inference trace; it is not a
calibration or safety evaluation.

## 7. Treat retrieval results as candidates

Run the deterministic route:

```bash
uv run python experiments/08-embeddings/book_search.py --deterministic \
  --query 'Where are benchmark limitations recorded?'
```

Inspect every returned path. Does it exist inside the configured corpus? Does
the excerpt answer the question, or merely share a word? Identify one relevant
candidate and one possibly misleading neighbor. Then issue a blank query or
use the frozen evaluation suite to observe the refusal path. Record why
missing evidence is safer than a guessed answer.

If you install the optional learned embedding group, pin the package/model,
check storage first, and keep the deterministic result as a control. Compare
paths and relevance judgments, not raw scores across unlike encoders. A score
is a ranking signal within an encoder/corpus combination; it is not a percent
probability of truth.

## 8. Audit a grounded evidence packet

Run `experiments/09-rag/grounded_answer.py --deterministic` with a question
that has a known source. For each displayed excerpt, check path resolution,
citation-key proximity, and whether the excerpt supports the sentence you want
to write. Then ask an unsupported question. Preserve the missing-evidence
message; do not add a web answer or a fluent summary to make the demo look more
useful.

Write a proposed one-sentence answer only after attaching its source path. If
the excerpt does not entail the sentence, rewrite it as a narrower statement or
leave it unanswered. This is the human judgment that structural tests cannot
perform for you.

## 9. Reject a well-formed unsafe plan

Run `experiments/10-systems/compare_structured_planning.py` with its fixture.
Inspect the evidence allow-list, rejected path warning, caller-controlled
objective, and approval flag. Explain why a JSON object containing an
unretrieved path is unsafe even if it parses successfully. Then inspect the
empty-evidence case in the tests: steps should be cleared instead of converted
into generic write-like recommendations.

Your exercise output is a short contract table: input evidence, accepted paths,
rejected paths, warnings, and approval requirement. Do not configure an API key
for this exercise. The deterministic route is sufficient to learn the safety
boundary, and it keeps the result reproducible without a provider decision.

## 10. Resume without executing

Run the no-write LangGraph example and its tests. Pause the graph, inspect the
approval payload, then resume once with rejection and once with approval. In
both cases, confirm the terminal status explicitly says no write and that the
source fixture has not changed. Explain why approval of a proposal is not
permission to apply a diff.

Finally, choose one exercise whose result surprised you. Turn it into a small
record with command, revision, expected result, actual result, limitation, and
next action. That record—not the fact that the command eventually passed—is the
completion artifact for this appendix.
