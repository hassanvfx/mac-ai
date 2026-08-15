# From Tensors to Agents

> Learning modern AI by building it on Apple Silicon.

This is the companion repository for an English-language book and course that
moves from tensors and gradients to RAG and agentic systems. It targets Python
3.11 and Apple Silicon, including an M4 with 24 GB unified memory.

## One source, two publications

`book/chapters/` is the canonical prose. Docusaurus renders those exact files
as the navigable course; Pandoc renders them as a Lulu-ready manuscript. Do not
copy chapter prose into `site/`.

```text
research/ -> book/chapters/ -> GitHub Pages course
                         -> DOCX -> print PDF
experiments/ -> chapter links and reproducible observations
```

## Quick start

Install [uv](https://docs.astral.sh/uv/), then run:

```bash
uv sync --group dev
uv run pytest
uv run python experiments/01-tensors/broadcasting.py
uv run python experiments/02-gradients/autograd.py
uv run python experiments/03-pytorch/train_tiny_network.py
```

The TensorFlow/Keras comparison is optional so a base install stays small. It
uses the supported Python 3.11 dependency group:

```bash
uv sync --group tensorflow
uv run --group tensorflow python experiments/04-tensorflow/train_keras_cnn.py
```

If a later optional dependency is missing, first check available disk space;
install it when there is adequate headroom, and report the space constraint
rather than silently abandoning that part of the curriculum.

Semantic search and evidence-only RAG are another optional group. The first
learned run downloads the public encoder weights into the local Hugging Face
cache, outside Git:

```bash
df -h .
uv sync --group embeddings
uv run --group embeddings python experiments/08-embeddings/book_search.py
uv run --group embeddings python experiments/09-rag/grounded_answer.py
uv run --group embeddings python evals/run_book_intelligence.py
```

Append `--deterministic` to either command to use the small fixture-friendly
hashed-vector baseline instead of loading the learned encoder. See
`benchmarks/05-book-intelligence/README.md` for the recorded observation and
its limits.

For the course site, use Node 20:

```bash
cd site && npm ci && npm start
```

## Ten-day learning roadmap

1. Tensors, gradients, and a first neural network
2. PyTorch and CNNs
3. TensorFlow/Keras comparison
4. Transformers and Hugging Face
5. MLX and local LLMs on Apple Silicon
6. Embeddings and manual RAG
7. LangChain
8. LangGraph, persistence, and HITL
9. Multi-agent systems, MCP, and evaluation
10. Capstone, production concerns, and editing

## Repository map

- `research/` — learning notes and BibTeX sources.
- `book/` — canonical manuscript, assets, and print configuration.
- `site/` — Docusaurus shell only; it reads `../book/chapters`.
- `experiments/` — small runnable programs, grouped by chapter.
- `benchmarks/` — observed measurements and the scripts that produced them.
- `src/` — reusable Python support code.

Book prose, diagrams, and illustrations are all-rights-reserved. The code is
available under the MIT License.
