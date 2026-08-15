---
sidebar_position: 9
title: "RAG: Giving Models a Memory They Never Learned"
---

# RAG: Giving Models a Memory They Never Learned

## Intuition

Retrieval-augmented generation (RAG) changes what a model can see at answer
time. It does not retrain the model or make it truthful. A good RAG system
therefore begins with a more modest promise: retrieve evidence, show where it
came from, and say when there is no evidence.

That promise separates three stages that are often collapsed: retrieval finds
candidate chunks, grounding constrains output to those chunks, and generation
turns grounded material into prose. A fluent response can fail at any stage.
This chapter keeps generation out of the control path so a reader can inspect
the evidence before trusting a summary.

## Problem

The Book Intelligence Assistant must answer questions about this changing
repository without inventing facts about experiments, benchmarks, or chapters.
Its first RAG stage should be inspectable without an API key or a generative
model. That gives us a control before we add prompt templates and agent graphs.

## Minimal implementation

[grounded_answer.py](../../experiments/09-rag/grounded_answer.py) builds the
same corpus index from Chapter 8 and formats only the retrieved excerpts. It
places the repository path and any citation keys next to each excerpt. If no
deterministic result has positive similarity, it returns an explicit
missing-evidence message.

```bash
uv run python experiments/09-rag/grounded_answer.py --deterministic \
  --query 'What should an experiment record?'
```

This is intentionally not a conversational answer. It is a reader-visible
evidence packet: the safe object that a later model may summarize only under a
grounding policy.

## Real implementation

With the optional local encoder installed, the same program uses the learned
index from [learned_retrieval.py](../../src/from_tensors_to_agents/learned_retrieval.py).
It applies a conservative score threshold before formatting evidence. A weak
or empty result fails closed rather than producing a plausible paragraph.

```bash
uv run --group embeddings python experiments/09-rag/grounded_answer.py \
  --query 'What should an experiment record?'
```

The current output remains excerpt-only. That boundary is deliberate: it lets
us test retrieval, citation propagation, and source paths independently from a
language model’s writing quality. The current implementation and limitations
are recorded in `benchmarks/05-book-intelligence/README.md` and
`research/05-embeddings-and-rag/notes.md` in the companion repository.

## Experiment

Use a question whose answer has a known source path. Confirm that each rendered
path exists in the checkout, inspect each excerpt, and mark whether it actually
answers the question. Then ask an unsupported question and verify the refusal.
The versioned evaluation set will grow from these cases: locating evidence,
spotting an unsupported statement, proposing an experiment, and reviewing a
chapter change. A retrieved path is auditable evidence; an uncited answer is
not.

## What broke

RAG breaks in mundane ways: chunk boundaries omit a qualifier, a ranking favors
a nearby but irrelevant benchmark, a moved file leaves a stale index, or a
model paraphrases beyond the excerpts. The first two are retrieval failures;
the latter two are provenance and generation failures. Generated indexes are
therefore local, live indexes are rebuilt from tracked files, and tests assert
missing-evidence behavior and citation/path propagation.

Treat an index as a cache, not as the corpus. When a chapter moves or a
benchmark is revised, an old index can still return text that looks relevant
but no longer represents the checked-out project. Rebuild from tracked files,
verify that every rendered path resolves inside the corpus, and refuse to turn
an empty or weak retrieval result into a confident conclusion.

## Alternatives

A traditional search UI can be preferable when the reader wants to browse, and
manually curated links are best for stable navigation. A full RAG stack may use
hybrid retrieval, reranking, context compression, and a hosted or local model.
Those components can improve usability but also make it easier to hide an
unsupported leap. We add them only after this evidence-only control is solid.

## When to use it—and when not to

Use this workflow to find and inspect project evidence, to prepare a revision
plan, or to check whether a technical claim has a record behind it. Do not use
it as authority when no result is retrieved, when the cited source is stale, or
when a decision needs a primary external source. In later chapters, any
proposed modification still stops for explicit human approval.

## Takeaway

RAG is not a memory implant. It is a disciplined context pipeline. The first
safe version does less—returning evidence rather than fluent prose—so that the
rest of the system has something trustworthy to build on.
