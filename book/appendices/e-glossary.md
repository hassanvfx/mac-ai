# Appendix E: Working Glossary

**Approval boundary.** A point at which a workflow stops and requires a human
decision before any consequential action. In this project, approval can resume
a no-write proposal state; it is not standing permission to edit files, commit,
or use an external service.

**Attention.** A mechanism that combines token representations according to
content-dependent weights. In a transformer, queries, keys, and values make the
relationship between tokens explicit for the current input.

**Autograd.** Automatic differentiation: a system records differentiable
operations and computes derivatives of a scalar objective with respect to
selected inputs or parameters.

**Batch.** A group of examples processed together. Batch size changes the
shape, memory demand, gradient estimate, and often the timing question; it is
therefore part of an experiment envelope.

**Benchmark record.** A committed description of an observed run that names
workload, machine/device, versions, timing method, result, and limitations. It
is evidence for its own conditions, not a general product ranking.

**Checkpoint.** Persisted operational workflow state used to resume a paused
process. It is not the canonical manuscript, not a Git history, and not proof
that the evidence referenced by an old proposal remains current.

**Chunk.** A bounded unit of indexed source text. This project uses paragraph
groups with a visible character limit so returned excerpts retain enough local
context to be inspected.

**Citation key.** The identifier inside a citation marker or BibTeX entry. A
retrieval result may preserve a key found in its excerpt; that preservation does
not mean the key supports every sentence someone might write about the excerpt.

**Context window.** The amount of tokenized input and output a model can handle
for one request. It is a model/runtime constraint, not a guarantee that all
provided context is relevant or used correctly.

**Corpus.** The configured set of documents eligible for indexing or retrieval.
The Book Intelligence Assistant uses allowlisted repository subtrees rather
than following arbitrary filesystem paths or Markdown links.

**Cosine similarity.** For normalized vectors, the dot product measuring their
directional alignment. It ranks candidates inside a chosen encoder and corpus;
it is not a calibrated probability that a source is true or answers a question.

**Deterministic fallback.** A documented route whose behavior does not depend
on an optional model or provider. It keeps core tests and safety checks useful
when a dependency, credential, model download, or accelerator is unavailable.

**Device fallback.** Explicitly selecting a safe supported device when a
requested accelerator cannot be used. It must be labelled so a user does not
mistake a CPU run for an MPS observation.

**Embedding.** A numeric vector representing an item such as text. A learned
embedding may capture useful relationships, while the repository’s hash-vector
baseline exists to make contracts repeatable without claiming semantic quality.

**Entailment.** Whether supplied evidence actually supports a proposed claim.
Path resolution, citation-key propagation, and schema validation are useful
structural checks, but a reader still judges entailment.

**Evidence packet.** The retrieved paths, excerpts, metadata, and citation keys
shown before or instead of a generated answer. A packet is inspectable context,
not a conclusion.

**Fixture.** A small, frozen test input with known expected properties. Fixtures
make source attribution, failure behavior, and workflow contracts testable even
while the live manuscript changes.

**Gradient.** The derivative of an objective with respect to parameters or
inputs. Gradient descent uses it to select a local update direction; a correct
gradient alone does not prove a model will generalize.

**Grounding.** Constraining an answer or proposal to retrieved, inspectable
evidence. Grounding is stronger than merely displaying a citation, but it still
requires evaluation of whether a cited excerpt supports the claim.

**Human in the loop.** A system design in which a human makes a named decision
at a persisted, reviewable transition. It is not a decorative confirmation
button placed after an autonomous write already occurred.

**Index.** A data structure derived from a corpus to support search. An index
is a cache of a particular source revision and becomes stale when its inputs
change; it is not the authority over current source files.

**Inference.** Computing model outputs from inputs using fixed parameters. It
differs from training, which also computes gradients and updates parameters.

**LangGraph.** A framework for defining stateful graph workflows. In this book
it illustrates explicit nodes, edges, checkpoints, interrupts, and no-write
approval states; it is not itself a permission system.

**Loss.** A scalar objective that quantifies disagreement between model outputs
and targets under a declared rule. Its absolute scale depends on the chosen
loss and data, so values from unlike runs are not automatically comparable.

**MPS.** Apple’s Metal Performance Shaders backend used by PyTorch on supported
Apple Silicon systems. Its availability and measurement boundaries must be
recorded before interpreting a local observation.

**Normalization.** Transforming values to a declared scale. L2-normalizing a
nonempty vector makes its dot product with another normalized vector equal to
cosine similarity; normalizing input data changes a model’s effective problem.

**Prompt injection.** Untrusted text attempting to change an assistant’s
instructions or authority. Retrieved repository material is evidence to cite,
not authority to override corpus boundaries, no-write rules, or approval.

**Provenance.** Information that lets a reader trace a result to its source,
such as repository path, chapter identifier, citation key, experiment metadata,
corpus revision, or benchmark conditions.

**RAG.** Retrieval-augmented generation: retrieving context at answer time and
using it to constrain a response. It does not retrain the model or make the
response automatically truthful.

**Recall at k.** For a question with acceptable sources, whether at least one
acceptable source appears among the first *k* retrieved candidates. It measures
a retrieval condition, not whether a generated answer is fully supported.

**Reference template.** A Word document that supplies the intended print layout
to a DOCX conversion. The Lulu template governs the generated manuscript’s
layout; final PDF inspection is still required.

**Regression test.** A test retained because a specific failure or invariant
must not silently return. A narrow regression test is more diagnosable than a
broad demonstration that blends many possible causes.

**Retriever.** A component that ranks or selects corpus candidates for a query.
It should preserve the original evidence record rather than returning only
detached text or a score.

**Seed.** A value controlling pseudo-random choices. It improves repeatability
when recorded with versions and inputs, but cannot remove every hardware or
runtime source of nondeterminism.

**Structured output.** Model output parsed into named fields under a schema.
The schema checks shape; application validation must still enforce evidence
allow-lists, caller-controlled objectives, and human approval.

**Token.** A unit produced by a model’s tokenizer. Tokens are not necessarily
words; special tokens, padding, and masks are part of an inference trace.

**Trace.** A record of workflow inputs, state transitions, outputs, timing
boundaries, and errors. A safe trace omits credentials and does not turn raw
private context into a permanent log by default.

**Vector store.** A persistent system for searching vector embeddings. It may
be useful for a larger or multi-user corpus, but it adds operational cost and
does not remove the need for source provenance and evaluation.

**Warm-up.** Unmeasured work performed before a timing sample to separate setup
effects from a declared steady-state measurement. It must be stated, not
silently applied, because it changes the question a benchmark answers.
