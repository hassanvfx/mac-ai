# Milestone 4 learned-retrieval observation

## Contract

This is an execution record for local semantic retrieval over the current
repository corpus. It demonstrates provenance-preserving learned embeddings;
it does **not** measure answer quality, retrieval recall, throughput, or
Apple-Silicon performance.

| Field | Value |
| --- | --- |
| Script | `experiments/08-embeddings/book_search.py` |
| Related RAG script | `experiments/09-rag/grounded_answer.py` |
| Dependency group | `embeddings` (`sentence-transformers` 5.7.0) |
| Encoder | `sentence-transformers/all-MiniLM-L6-v2` |
| Corpus | versioned `research/`, `book/chapters/`, `experiments/`, and `benchmarks/` files; generated indexes excluded |
| Vector treatment | L2 normalization followed by dot-product ranking |
| Model storage | Hugging Face cache outside Git; unauthenticated Hub access may be rate limited |
| Seed | not applicable: encoder inference uses no sampling in this script |
| Timing/memory method | not measured in this initial correctness observation |

## Recorded run — 2026-08-14

After the optional embedding group and model cache were installed on the
project Mac, this command completed:

```bash
uv run --group embeddings python experiments/08-embeddings/book_search.py \
  --query 'Where do we record benchmark timing limitations?'
```

The script indexed 95 chunks and returned these top paths, with cosine scores
rounded by the script: `benchmarks/03-transformers/README.md` (0.556),
`book/chapters/03-building-a-neural-network-with-pytorch.md` (0.549),
`benchmarks/01-day1/README.md` (0.469), and `benchmarks/01-day1/run.py`
(0.446). Corpus count and rankings may change as tracked source material is
added; rerun instead of treating this as a fixed quality score.

The grounded-answer program was also run with the question, “What should an
experiment record?” It returned retrieved excerpts with repository paths and
did not synthesize prose beyond the evidence wrapper. Its neighbors are useful
to inspect, not evidence that the result is complete or ideally ranked.

## Limitations and next measurement

The observed model load printed an unauthenticated-Hub warning; caching made
subsequent runs possible locally. Before making latency or memory claims, add a
declared warm-up, repeated queries, timing boundary, device reporting, and an
evaluation dataset with known relevant paths.
