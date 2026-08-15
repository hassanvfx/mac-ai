# Appendix F: Book Intelligence Capstone Walkthrough

The Book Intelligence Assistant is the book’s canonical capstone because its
corpus, failure cases, and limits are all visible in the same repository that
teaches the techniques. This walkthrough traces one maintenance task through
retrieval, evidence-only answering, planning, critique, approval, and
evaluation. At no point does the workflow modify prose, code, Git state, or an
external service.

## The task

Suppose an editor asks: “Review the embeddings chapter and propose the smallest
evidence-backed improvement.” This is not an instruction to rewrite a chapter.
It is a request for a reviewable proposal. The task enters the system with a
clear objective and a declared corpus boundary: research notes, canonical
chapters, experiments, and benchmark records. Private files, arbitrary
filesystem paths, and the Internet are outside that boundary.

The first question is whether the corpus contains useful evidence. The
retriever chunks allowed files, attaches repository path, corpus kind, chapter
identifier, citation keys, and lightweight metadata, then returns a small
ranked candidate set. A similarity score only routes attention. The editor
opens the returned paths and excerpts before deciding whether they support the
maintenance task.

## Evidence before prose

The grounded-answer layer renders an evidence packet: each excerpt appears
under its repository path, with citation keys where the same chunk contains
them. If retrieval is empty, blank, or too weak for the declared policy, it
returns the fixed missing-evidence response. It does not turn an absent source
into a generic answer, a guessed citation, or a provider call.

This gives the editor a useful checkpoint. A path that merely shares words with
the question is not automatically relevant. A real citation key is not
automatically support for every conclusion near it. The editor can narrow the
question, add missing research, inspect an exact identifier, or stop. The
system has not yet earned a recommendation.

## Plan and critique

When evidence exists, the planning layer receives only the objective and the
retrieved allow-list. Its structured proposal names evidence paths, steps, and
unsupported-claim warnings. Validation removes any path not retrieved,
restores the caller’s objective, and forces `approval_required` to true. With
no evidence it clears action-like steps. A well-formed object is therefore not
enough to become an authorized plan.

The critic then examines the same scope plus deterministic editorial findings.
It can flag missing alternatives, unresolved or unsafe links, missing
experiments, and unsupported claims when those findings are present in the
evidence. It cannot silently widen the corpus or write a fix. A direct SDK
adapter, a LangChain adapter, or a local model may produce wording differently,
but each must pass through this same evidence and approval contract.

## Persisted review, not execution

The LangGraph example persists a proposal under a new thread ID and interrupts
with an approval payload. The payload names objective, evidence paths, plan,
critique, and the explicit statement that no source, Git, or external action
will occur. A rejection ends `rejected_no_write`; an approval ends
`approved_no_write`. Both outcomes are durable and neither edits a file.

This deliberately modest endpoint teaches the critical separation: a reviewer
can accept the *idea* of an evidence-backed revision without granting a broad
writer capability. A future writer would need fresh evidence checks, a
diff-scoped second approval, and access limited to one approved target. The
beta implements none of those write operations.

## Evaluation as a capstone check

The frozen fixture corpus supplies deterministic cases for source attribution,
citation-key preservation, grounded paths, unsupported questions, blank input,
empty corpora, deterministic rank order, unsafe links, planning no-write
behavior, and critic findings. The workflow-comparison fixture runs a
deterministic control, a single planner, and a researcher/critic/writer shape
against the same task. Every route must preserve the expected evidence path,
flag the known omission, require approval, and report no write.

Run the capstone’s baseline evidence gate with:

```bash
uv run pytest tests/test_book_intelligence.py \
  tests/test_book_intelligence_evaluation.py \
  tests/test_approval_workflow.py tests/test_workflow_comparison.py
uv run python evals/run_reliability.py
```

Passing this gate does not claim a general agent-quality result. It establishes
that the repository’s canonical example behaves safely under its versioned
fixture contract. A model-backed comparison remains an optional future
experiment with a selected provider, declared settings, redacted traces, and
separate latency/cost/quality evaluation.

## What the reader should retain

The capstone is not a chatbot that knows the book. It is a chain of explicit
boundaries: corpus membership, provenance-preserving retrieval, evidence-only
grounding, structured validation, critique, persisted human decision, and
no-write termination. Its usefulness comes from making each boundary testable.
That same shape transfers to a real engineering project only after its corpus,
permissions, retention policy, and evaluation dataset have been chosen with
the care they deserve.
