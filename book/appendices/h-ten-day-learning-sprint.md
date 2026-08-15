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

## After the first sprint: turn activity into a maintained project

Finishing a sequence of exercises creates many small artifacts: commands that
worked, commands that did not, scratch observations, cached models, questions
that led nowhere, and a few results worth carrying into the manuscript. The
next job is editorial selection. A repository becomes a useful companion when a
reader can tell which artifact is a stable lesson, which is a measured record,
which is a generated cache, and which is merely a future idea.

Start with the canonical chapter, not the terminal history. For each chapter,
ask four questions. What concept does the reader need before running anything?
What smallest program demonstrates the mechanism? What real implementation or
fixture makes the mechanism useful? What failure, alternative, and usage limit
prevent the lesson from becoming a slogan? If a section cannot answer one of
these questions, it may belong in a research note or journal instead of the
published prose.

Then link every substantive claim to an evidence path. A training paragraph
should link to the experiment and the observation record that supports its
scope. A framework comparison should link to matched fixtures and state the
conditions that were held fixed. A retrieval claim should link to a fixture
case, source paths, and the rule that governs missing evidence. An agent claim
should link to its no-write workflow test. Links are not decorative references:
they are invitations for a reader to inspect the exact boundary of the claim.

Keep experimental records factual. A good record says that a named model,
version, device, prompt, workload, and timing method produced an observation on
a certain date. It also says what was not measured. Avoid retrospective prose
that turns an early run into a universal finding because later chapters happen
to need an example. If a result needs a stronger claim, design a stronger
experiment and commit a new record rather than editing the old observation.

Use the journal to protect decisions that do not belong in the book. The
journal can explain why a dependency was deferred, why an optional model was
not downloaded, why a page layout is interim, or which release input is still
user-owned. It should point to benchmark and research files rather than become
a second manuscript. Before each commit, update it with the decision, files,
commands, result, limitation, and next task. This makes a later session
resumable without forcing readers of the book through project-management notes.

Finally, maintain the difference between a learning beta and publication.
Passing tests, a site build, and an interim DOCX render show that a source
revision is healthy enough to review. They do not choose a GitHub destination,
publish a site, export the final Word PDF, choose an ISBN, create a cover, or
approve a Lulu proof. Treat those as visible handoffs. The engineering work is
to prepare reproducible inputs and honest checks; the release decision remains
with the person responsible for the book.

## Choosing the next experiment

After the sprint, let a recorded uncertainty choose the next experiment. If a
training result is confusing, reduce the data and inspect the gradient or label
contract. If a framework result differs, hold the fixture still and compare
preprocessing and objective semantics. If retrieval returns a misleading
neighbor, preserve the query and excerpt, then decide whether chunking,
corpus coverage, or evaluation labels need attention. If a plan is unsupported,
retrieve again or stop; do not ask for more fluent prose. If an approval thread
becomes stale, start a new scoped proposal rather than reusing an old decision.

This rule prevents a project from becoming a tour of tools. The next library,
model, or workflow is justified only when it addresses a named limitation in
the current evidence trail. That keeps the manuscript coherent, keeps optional
dependencies optional, and gives a reader a repeatable way to continue beyond
the first ten days without abandoning the project’s central promise: learn
modern AI by building systems whose claims, failures, and boundaries can be
inspected.

When work pauses, leave a handoff that someone else can use without guessing:
the current objective, completed evidence, exact commands that passed, the
remaining uncertainty, generated artifacts to ignore, and the next smallest
safe action. This is as important for a solo learning project as it is for a
team. It turns a future return to the repository into continuation rather than
rediscovery.

Use the same standard when a result is disappointing. A failed download,
unavailable accelerator, weak retrieval result, malformed structured response,
or rejected plan may be the most educational output of the day. Preserve its
conditions, state what the system refused to do, and decide whether the durable
lesson belongs in a test, fixture, benchmark record, journal, or chapter. A
project that records these paths honestly becomes easier to trust and easier to
extend than one that presents only successful screenshots.

The final habit is to revisit earlier assumptions after each new chapter. A
later retrieval experiment can refine how you describe embeddings; a benchmark
can narrow an earlier device observation; a rejected approval can clarify a
workflow boundary. Revision is not evidence that the first lesson failed. It
is the normal process by which a living technical book stays aligned with the
code and records it asks readers to inspect.
