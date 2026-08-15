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

In geometric terms, an encoder maps text to a point in a high-dimensional
space. L2 normalization makes each nonempty vector have length one, so the dot
product measures the angle between two directions: identical directions score
one, orthogonal directions score zero, and opposite directions score below
zero. The implementation uses that relationship because it is easy to inspect,
not because a cosine score has an intrinsic meaning such as “80% correct.” A
score only ranks candidates produced by this encoder over this corpus.

## Problem

Before adding a vector database, framework, or language model, we need to
answer a smaller question: can this book find its own evidence? The corpus is
versioned Markdown, code, and benchmark records. A useful result must retain
the source path, corpus kind, chapter identifier, citation keys, and relevant
experiment or benchmark grouping—not merely a float score.

Chunking is the first practical design decision. A whole chapter is usually too
broad: it can match a query while leaving a reader with thousands of words to
inspect. A sentence can be too narrow: it loses the condition or citation that
makes the statement meaningful. The baseline therefore joins paragraphs up to
a bounded character budget. The boundary is deliberately plain and versioned;
it can be tested, changed, and recorded in a later benchmark rather than being
hidden inside a hosted retrieval service.

Metadata belongs to the chunk that was ranked, not to a guessed answer. If the
chunk came from a benchmark, its record group stays attached. If it came from a
numbered chapter, the chapter identifier stays attached. If it contains a
citation key, that key travels with the result as a clue for the reader to
check in the shared bibliography.

Chunk boundaries are an information-retrieval policy, not cleanup trivia. A
boundary that separates a benchmark number from its workload can produce an
apparently relevant but unusable result. One that merges several unrelated
sections can hide which statement the score actually matched. The baseline
uses blank paragraphs because Markdown authors already use them to group an
idea, and its `limit=1200` character rule is visible in
`src/from_tensors_to_agents/book_intelligence.py`. This is a practical default,
not an ideal universal size. Change it only alongside a fixture evaluation and
record the corpus revision that produced the result.

There are two useful kinds of determinism here. The hash-vector baseline is
deterministic across runs of the same code and text, so a failing attribution
test has a narrow debugging surface. A learned encoder can also be made
repeatable enough for an experiment by pinning its model identifier, package
versions, corpus snapshot, and ranking procedure. Neither form proves that the
ranking is good. Repeatability tells us that we can investigate a result; it
does not turn a similarity score into relevance.

## Minimal implementation

The baseline in [book_intelligence.py](../../src/from_tensors_to_agents/book_intelligence.py)
splits allowed repository files into bounded paragraph chunks. It hashes tokens
into a fixed-size vector, normalizes it, and ranks query/chunk dot products.
This deterministic method is intentionally crude, but it is small enough for
fixtures and proves the data contract without a model download.

The hash is not a learned representation of language. It maps token counts into
a fixed vector using a stable digest and then normalizes the result. Collisions,
synonyms, and word order make it unsuitable for claims about semantic quality.
Its value is different: the same fixture and query produce the same ordering,
so tests can verify chunking, path attribution, citation propagation, empty
input, and refusal behavior on a CPU-only machine.

The fixture is deliberately smaller than the live book corpus. It is a frozen,
non-sensitive set of source-shaped files whose expected paths and citation keys
belong in tests. That gives automated checks a stable oracle even while this
manuscript changes daily. The live corpus is the useful authoring workspace;
its generated index remains local because it reflects the current checkout and
may be stale the moment another chapter is edited. Never treat a passing
fixture ranking as proof that the live corpus has complete coverage.

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

The learned and deterministic indexes share the `Evidence` contract. Both
return a source path, kind, chapter, citations, text, and metadata alongside a
score. This lets later RAG and planning layers work against an explicit
interface rather than assume a particular vector database. If the learned
encoder cannot be installed or loaded, the fallback must label itself instead
of implying that learned search took place.

The implementation normalizes the complete matrix of document vectors and the
query vector before their dot product. This gives cosine similarity for
nonempty vectors, but the score remains relative to this corpus and encoder.
Do not compare a score from one embedding model or chunk policy with a score
from another as though they were calibrated probabilities. Compare outcomes:
did an acceptable evidence path appear in the returned set, did the result
retain its source metadata, and could a reader inspect the supporting passage?

The encoder is optional for two operational reasons. Downloaded weights and
their cache consume local storage, and the model may be unavailable on an
offline or CPU-only machine. The command begins with `df -h .` so an author can
check storage before triggering that download. If the optional path fails, use
the deterministic baseline to keep contract tests and the rest of the book
workflow working; report the learned run as unavailable rather than silently
substituting a different model.

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

Build a small evaluation set before tuning retrieval. For each question, record
one or more acceptable source paths, the reason each is relevant, and any path
that would be dangerously misleading. Run the same set after changing a chunk
limit, embedding model, normalization rule, or corpus snapshot. Separate
retrieval recall from answer grounding: retrieval asks whether useful evidence
appeared; grounding asks whether the response cites only evidence it received.

Use simple measurements before elaborate dashboards. For a question with an
acceptable path set, recall at *k* asks whether at least one acceptable path is
in the first *k* returned results. A path-attribution check asks whether every
displayed result actually resolves inside the corpus. A failure review asks why
the miss occurred: query vocabulary, an over-broad chunk, a missing document,
or a misleading but lexically similar neighbor. These measures expose different
problems and should be stored with the question rather than reconstructed from
a favorable terminal screenshot.

The retrieval interface is intentionally read-only. It can assemble evidence
for a later plan, but it cannot edit a chapter, rewrite a benchmark, or alter
Git state. This boundary keeps the first capability easy to audit: input files
produce chunks; chunks produce ranked candidates; candidates preserve paths.
Chapters 9 through 12 add answers, structured plans, and approval state on top
of this contract without granting retrieval itself write authority.

## Worked retrieval audit: from a question to inspectable evidence

Take the fixture question, “Where is cosine similarity explained?” The right
way to judge the result is not to celebrate a number in the terminal. First,
the evaluator builds an index only from its frozen `research/`,
`book/chapters/`, `experiments/`, and `benchmarks/` directories. It deliberately
does not crawl the parent checkout, a home directory, or an arbitrary path
named in a Markdown link. That bounded input is what makes a returned relative
path meaningful.

Second, it asks for a small ranked set and checks that
`evals/fixture_corpus/research/embeddings.md` occurs among the candidates. That
fixture source says what
normalization and cosine comparison mean and carries the
`reimers2019sentencebert` citation key. A useful display therefore includes
the path, excerpt, and key—not just “similarity score: 0.42.” The reader can
open the note, locate the cited claim in `research/references.bib`, and decide
whether it answers the question. If the model had instead returned only a
benchmark record mentioning the word *similarity*, that would be a candidate
to inspect, not evidence that the explanation was found.

Third, repeat the same query against the unchanged fixture. The deterministic
baseline must return the same ordered paths. This is a regression property,
not a semantic-quality result: hash collisions can still make the order
unhelpful. Its practical value is that a changed order now has a short list of
possible causes—fixture text, tokenization, chunking, vector dimensions, or
the tie-break rule—rather than an unexplained hosted-service change.

Finally, probe the refusal edges. A blank query produces an all-zero query
vector, so the retriever returns no candidates and the grounded-answer layer
must say that no indexed evidence matched. An absent corpus produces an empty
index and the same refusal. A deliberately unsafe fixture link to a path above
the corpus root is reported by the reviewer as an escaped link; it is never
followed. These cases make the boundary concrete: retrieval can name evidence
inside its declared corpus, but it cannot invent an answer or use a link as
permission to read elsewhere.

Run the frozen audit with:

```bash
uv run pytest tests/test_book_intelligence.py \
  tests/test_book_intelligence_evaluation.py tests/test_reliability.py
uv run python evals/run_reliability.py
```

The expected result is that the versioned cases pass. It is not an expected
retrieval score, a claim that learned embeddings are installed, or a claim
about the quality of a model on a different corpus. When replacing the hash
baseline with the optional encoder, retain this exact audit shape and add a
separate versioned relevance set before asserting that learned retrieval is an
improvement.

## What broke

Three failure modes matter immediately. Empty input has no evidence and must
not turn into a confident answer. A mathematically high score can still be a
bad neighbor because the chunk is broad or the query is vague. Finally, a
citation key found in a chunk says that the chunk contains a citation; it does
not automatically support every sentence in the chunk. The tests cover empty
indexes, deterministic rankings, metadata preservation, and weak-result
refusal. The research note records the remaining limits
[@reimers2019sentencebert].

Stale indexes are another failure mode. A local index is a cache of tracked
files at a particular moment, not an authority over the current working tree.
Rebuild it after editorial changes, and resolve every returned path inside the
configured corpus before displaying it. The corpus reviewer rejects Markdown
links that escape that boundary.

Similarity can also encode an accidental shortcut. A query asking about
“memory” may retrieve a local-inference benchmark when the author meant a
LangGraph checkpoint, because both use the same word. A query with a citation
key may be better served by exact lookup than embedding search. Preserve the
query and the returned excerpt in an evaluation failure fixture; saying only
that “retrieval was bad” leaves no way to tell whether an embedding change,
chunk boundary, or task wording should change next.

## Alternatives

Keyword search is cheap, predictable, and sometimes best for exact filenames
or citation keys. Sparse BM25-style retrieval, hybrid lexical-plus-vector
retrieval, rerankers, and a dedicated vector store are reasonable later
alternatives. They add operational cost and do not remove the need for source
attribution. For a small changing book corpus, a transparent in-process index
is the right first control.

Use exact search first when the reader knows a section name, experiment path,
or BibTeX key. Use a hybrid approach when exact identifiers and paraphrased
questions are both common. Consider a persistent vector store only when corpus
size, update rate, filtering needs, or multi-user access makes an in-process
index impractical. In every case, keep the index revision, chunking policy, and
returned paths inspectable before optimizing ranking sophistication.

Reranking is useful when a cheap first pass returns many candidates but the
top few need finer discrimination. It is not a free accuracy button: it adds a
second model or rule, another versioned dependency, and another place to lose
provenance. Add it only when a recorded evaluation miss justifies it, and make
the reranker return the original `Evidence` records rather than a detached
summary. For this book-sized corpus, transparent candidates are more valuable
than an opaque score improvement.

## When to use it—and when not to

Use semantic retrieval to discover candidate evidence when wording differs
between the question and the source. Do not use similarity as proof, a
substitute for reading the returned source, or a performance claim about a
model. When an answer needs exact legal, safety, or publication requirements,
retrieve the primary source and inspect it directly.

## Evidence trail

Read `research/05-embeddings-and-rag/notes.md`, run
`experiments/08-embeddings/book_search.py`, and inspect the local model
observation and limits in `benchmarks/05-book-intelligence/README.md`.

## Takeaway

Embeddings make meaning searchable, not self-verifying. The important product
of this chapter is a provenance-preserving retrieval contract that later RAG
and agent workflows cannot quietly discard.
