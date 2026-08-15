# Appendix H: Ten Days of Learning by Building

This is a practical sequence for turning the book into a working learning
project. Each day has a narrow technical focus, a visible repository output,
and a gate. The gate is not a grade or a deadline: it says what evidence should
exist before the next abstraction is allowed to hide the previous one.

## Day 0 — Make the baseline visible

Confirm Python, `uv`, Node, Pandoc, and Word. Run the existing Python tests and
site build before changing source. Read the active project journal, record the
source revision, and check disk space before any optional download. The output
is a short baseline record that says what is installed and what remains
available when an optional group is absent. A small deterministic core is more
useful than a collection of untested packages.

## Day 1 — Tensors, derivatives, and one controlled model

Run the broadcasting and autograd examples, then the tiny PyTorch training
program. Predict tensor shapes and scalar gradients before looking at output.
Record seed, package version, selected device, input, expected result, actual
result, and limitation. The gate is correct numerical behavior and an explicit
CPU fallback. A loss curve or an MPS label does not yet establish speed or
generalization.

## Day 2 — Learn to inspect a vision error

Run the small CNN fixture and preserve data split, preprocessing, label map,
metric, and confusion matrix. Inspect one wrong prediction. The output is a
reproducible error-analysis record and a chapter explanation of what that error
does and does not show. The gate is an interpretable pipeline contract, not a
claim that a tiny fixture makes the architecture competitive.

## Day 3 — Compare framework contracts

Install the optional TensorFlow group only after checking space. Match data,
split, seed policy, labels, model intent, and metric definition with the
PyTorch fixture. Investigate differences from preprocessing through loss
semantics before attributing them to a framework. The gate is a limited shared
fixture observation. If a runtime is unavailable, record that fact and retain
the control rather than inventing an incomparable table.

## Day 4 — Trace a transformer input to its label

Run tokenizer inspection and a declared inference route. Inspect text, token
IDs, special tokens, mask, logits, label map, and ranked output. Compare a
manual path with a convenience pipeline only as an interface check. The gate is
an inspectable token-to-label trace. One output does not establish calibration,
safety, or broad language understanding.

## Day 5 — Treat Apple Silicon as an experiment envelope

If a local model runtime and public model are available, record artifact,
quantization, prompt, output limit, cache condition, warm-up, and timing
boundary. Keep download and construction separate from steady-state timing
unless cold start is the question. The gate is an honest local observation,
including an unavailable-model or out-of-space result. It is not a hardware
ranking or a claim about longer contexts.

## Day 6 — Retrieve evidence before generating prose

Begin with the frozen deterministic fixture. Verify expected paths, citation
keys, blank-query refusal, empty-corpus refusal, deterministic ranking, and
unsafe-link reporting. Only then index the live corpus locally. The gate is
provenance: every result resolves inside the declared corpus and every answer
shows evidence or refuses. Learned embeddings inherit this contract and need a
separate relevance set before any quality claim.

## Day 7 — Validate plans as data, not authority

Exercise direct-shaped and LangChain structured paths over the same retrieved
evidence. Inspect rejected paths, restored caller objective,
missing-evidence behavior, and the forced human-approval flag. The gate is that
a valid JSON object cannot widen authority. Keep provider configuration out of
the exercise until a model, endpoint, redaction policy, and evaluation protocol
are deliberately selected.

## Day 8 — Resume without writing

Pause the persisted workflow, reopen its checkpoint, and resume one thread
with rejection and another with approval. Inspect the payload and terminal
states. Verify that the fixture source is unchanged in both cases. The gate is
durable, reviewable no-write state. A future writer would require fresh
evidence, a constrained diff, and another scoped approval.

## Day 9 — Ask whether extra roles earn their cost

Run deterministic, single-planner, and researcher/critic/writer shapes against
the same fixture. Compare evidence paths, editorial finding, approval, and
no-write status. The gate is a visible contract across all shapes. Retain the
smallest workflow unless a versioned evaluation demonstrates that a distinct
handoff catches a useful failure often enough to justify its coordination cost.

## Day 10 — Produce a reviewable beta candidate

Run Ruff, the full tests, deterministic reliability suite, book audit, and site
build. Build the DOCX from canonical Markdown and the committed Lulu template;
render it for editorial inspection. Update the journal with commands, results,
limitations, and next action. The output is a beta candidate, not automatic
publication.

GitHub publishing requires a chosen remote and intentional deployment. Print
release requires a Word-exported PDF, full preflight and page inspection,
frozen page count, final cover template, metadata/ISBN decisions, and a Lulu
proof. These remain human-owned decisions.

## Daily habit

Start with the journal, run the narrowest reproducible control, and change one
declared condition at a time. Before committing, capture changed files,
commands, observations, failures, and the next step. Link detailed benchmark
and research records instead of copying raw terminal output into prose. The
transferable skill is not memorizing a framework: it is leaving an evidence
trail that another reader can inspect and improve.
