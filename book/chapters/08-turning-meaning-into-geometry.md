---
sidebar_position: 8
title: Turning Meaning Into Geometry
---

# Turning Meaning Into Geometry

## Intuition

An embedding is a numerical coordinate for an item such as a sentence. If an
encoder has learned useful regularities, nearby coordinates can represent texts
that are related even when they do not share the same words. That is not magic:
it is a retrieval heuristic whose output still needs inspection. Sentence-BERT
made this practical by training a BERT-derived model to produce sentence-level
vectors suited to similarity comparison [@reimers2019sentencebert].

Similarity changes the first question from “which exact words occur?” to
“which stored passages might help?” It does not change the second question:
whether a returned passage supports the answer. The assistant therefore treats
a vector score as a routing signal and retains the evidence a reader needs to
inspect.

## Problem

Before adding a vector database, framework, or language model, we need to
answer a smaller question: can this book find its own evidence? The corpus is
versioned Markdown, code, and benchmark records. A useful result must retain
the source path, corpus kind, chapter identifier, citation keys, and relevant
experiment or benchmark grouping—not merely a float score.

## Minimal implementation

The baseline in [book_intelligence.py](../../src/from_tensors_to_agents/book_intelligence.py)
splits allowed repository files into bounded paragraph chunks. It hashes tokens
into a fixed-size vector, normalizes it, and ranks query/chunk dot products.
This deterministic method is intentionally crude, but it is small enough for
fixtures and proves the data contract without a model download.

```bash
uv run python experiments/08-embeddings/book_search.py --deterministic \
  --query 'Where are benchmark limitations recorded?'
```

The index written under `.book-intelligence/` is a generated local artifact.
It is useful for inspection and deliberately ignored by Git.

## Real implementation

The optional learned path uses
`sentence-transformers/all-MiniLM-L6-v2` through
[learned_retrieval.py](../../src/from_tensors_to_agents/learned_retrieval.py).
It encodes each existing `Evidence` chunk locally, L2-normalizes the rows, and
uses a dot product as cosine similarity. Crucially, it does not replace the
evidence record; every ranked result carries the original provenance through
the learned index.

```bash
df -h .
uv sync --group embeddings
uv run --group embeddings python experiments/08-embeddings/book_search.py \
  --query 'Where do we record benchmark timing limitations?'
```

The first learned run may download public weights into a local Hugging Face
cache. The cache is not the corpus and must never be committed. The recorded
project-machine observation, including package/model identity and an explicit
statement of what was not measured, is in
`benchmarks/05-book-intelligence/README.md` in the companion repository.

## Experiment

Ask both backends the same question and compare the *paths*, not just the top
score. For this repository, a useful neighbor should lead a reader to a
benchmark, research note, chapter, or runnable script that can be checked.
Record the exact query, corpus revision, model identifier, returned paths, and
any misleading neighbor. The first learned run is a correctness observation;
it is not a retrieval-quality, latency, memory, or accelerator benchmark.

## What broke

Three failure modes matter immediately. Empty input has no evidence and must
not turn into a confident answer. A mathematically high score can still be a
bad neighbor because the chunk is broad or the query is vague. Finally, a
citation key found in a chunk says that the chunk contains a citation; it does
not automatically support every sentence in the chunk. The tests cover empty
indexes, deterministic rankings, metadata preservation, and weak-result
refusal. The research note records the remaining limits
[@reimers2019sentencebert].

## Alternatives

Keyword search is cheap, predictable, and sometimes best for exact filenames
or citation keys. Sparse BM25-style retrieval, hybrid lexical-plus-vector
retrieval, rerankers, and a dedicated vector store are reasonable later
alternatives. They add operational cost and do not remove the need for source
attribution. For a small changing book corpus, a transparent in-process index
is the right first control.

## When to use it—and when not to

Use semantic retrieval to discover candidate evidence when wording differs
between the question and the source. Do not use similarity as proof, a
substitute for reading the returned source, or a performance claim about a
model. When an answer needs exact legal, safety, or publication requirements,
retrieve the primary source and inspect it directly.

## Takeaway

Embeddings make meaning searchable, not self-verifying. The important product
of this chapter is a provenance-preserving retrieval contract that later RAG
and agent workflows cannot quietly discard.
