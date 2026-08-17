# AI From Tensors to Agents on Mac Silicon

> Learning modern AI by building it on Apple Silicon.

By Hassan Uriostegui · Waken AI Labs

![Cover of AI From Tensors to Agents on Mac Silicon](https://raw.githubusercontent.com/hassanvfx/mac-ai/main/book/assets/cover/pdf-online-cover.png)

This is the companion repository for an English-language book and course that
moves from tensors and gradients to RAG and agentic systems. It targets Python
3.11 and Apple Silicon, including an M4 with 24 GB unified memory.

[Buy the printed hardcover edition](https://www.lulu.com/shop/hassan-uriostegui/ai-from-tensors-to-agents-on-mac-silicon/hardcover/product-e7qy7gy.html?page=1&pageSize=4)

## One source, two publications

`book/chapters/` is the canonical prose. Docusaurus renders those exact files
as the navigable course; Pandoc renders them as a Lulu-ready manuscript. Do not
copy chapter prose into `site/`.

```text
research/ -> book/chapters/ -> GitHub Pages course
                         -> DOCX -> print PDF
experiments/ -> chapter links and reproducible observations
```

For the reusable production method behind this project, see the Spanish
[book + repository publishing playbook](https://github.com/hassanvfx/mac-ai/blob/main/docs/reusable-book-repo-publishing-playbook.md).

### Agent handoff: reuse this publishing method

Copy this brief into another coding agent when adapting the method to a new
book-plus-repository project:

```text
Use the documented book + repository publishing method from this completed
project as the starting point for the new project. Read the reusable playbook
first, then inspect the canonical examples and preserve the same principles:
one Markdown source of published prose; a manifest-generated bridge between
chapters, exercises, QR codes, and the course site; deterministic TOC and PDF
production; and separate automated preflight from human print-proof decisions.

Workspace root:
/Users/hassan/repos/ai-on-mac

Primary reusable guide:
/Users/hassan/repos/ai-on-mac/docs/reusable-book-repo-publishing-playbook.md

Canonical publishing protocol:
/Users/hassan/repos/ai-on-mac/book/appendices/i-reproducible-publishing-protocol.md

Reader/repository onboarding reference:
/Users/hassan/repos/ai-on-mac/README.md

Historical decisions and validation record:
/Users/hassan/repos/ai-on-mac/docs/journals/from-tensors-to-agents-beta.md

Key implementation references:
/Users/hassan/repos/ai-on-mac/book/qrcode-manifest.json
/Users/hassan/repos/ai-on-mac/scripts/build-book.sh
/Users/hassan/repos/ai-on-mac/scripts/polish_pdf.py
/Users/hassan/repos/ai-on-mac/scripts/prepare_lulu_pdf.py
/Users/hassan/repos/ai-on-mac/scripts/preflight_pdf.py

Before changing anything, read the project journal and identify the new
project's audience, canonical source location, print target, exercise format,
and public repository/site destination. Do not copy title-specific prose,
metadata, ISBN, cover assets, or distribution claims from mac-ai.
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

The base environment includes the lightweight Pydantic and LangGraph
checkpoint packages used by the repository's test suite. It does not install
model downloads, API credentials, or the later course-framework integrations.

> **Reader repair notice.** If you cloned the repository before this
> installation fix, run `git pull --ff-only` and then rerun the same
> `uv sync --group dev` command above. The printed setup commands themselves
> have not changed. If Git reports local changes, preserve them first or clone
> a fresh copy rather than overwriting your work.

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

The direct-SDK/LangChain comparison is another opt-in group. Its default is
fully local and uses fixture model responses; `--api` is an explicitly separate
mode that requires environment-only credentials:

```bash
df -h .
uv sync --group agents
uv run --group agents python experiments/10-systems/compare_structured_planning.py
uv run --group agents python experiments/11-langgraph/approval_workflow.py
```

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

## How to read this book

This is a build-first book. Read one chapter, run its smallest experiment,
inspect the result against its benchmark record, then change one variable and
run it again. The book explains the ideas; the repository is the laboratory.

Start by cloning the public repository on your Mac:

```bash
git clone https://github.com/hassanvfx/mac-ai.git
cd mac-ai
uv sync --group dev
```

Every chapter has a companion lab on the course site. A chapter-end QR code
opens that lab on a phone; use Safari Share → AirDrop to send the page to your
Mac, then open the experiment source and run its displayed command. The lab
also links to the benchmark record, expected behavior, tests, and the next
exercise. QR codes are convenience links, not a replacement for cloning the
repository: experiments run locally on your Mac.

The live learning path deliberately follows the repository's `main` branch.
When a chapter changes, update its prose, manifest entry, command, benchmark,
QR target, Pages lab, and regenerated PDFs together. The build validates this
bridge before publishing; do not hand-edit PDF contents page numbers.

## Learn this with your AI copilot

Use an AI coding assistant as a tutor and reviewer, not as a substitute for
running the work. After cloning the repository, give your assistant a narrow,
evidence-based request such as:

```text
Read README.md and docs/journals/from-tensors-to-agents-beta.md. I am on Day 3
of the ten-day plan. Guide me through Chapter 3 and its lab one step at a time.
Do not edit files or install optional dependencies without asking me first.
After each command, help me compare the output with the linked benchmark and
choose one small experiment to modify.
```

Adapt the pace to your background: repeat a day when an experiment is unclear,
skip only a lesson whose prerequisites you can demonstrate, and record what you
observed. Ask the copilot to explain an error, propose a small hypothesis, or
review a change against the chapter and benchmark—but keep final actions and
claims under your control.

## Repository map

- `research/` — learning notes and BibTeX sources.
- `book/` — canonical manuscript, assets, and print configuration.
- `site/` — Docusaurus shell only; it reads `../book/chapters`.
- `experiments/` — small runnable programs, grouped by chapter.
- `benchmarks/` — observed measurements and the scripts that produced them.
- `src/` — reusable Python support code.

Book prose, diagrams, and illustrations are all-rights-reserved. The code is
available under the MIT License.

## Publishing workflow

The Markdown manuscript builds into a 6×9 Lulu-oriented DOCX using the
versioned Word template. `book/build/pdf-online.pdf` is the single master:
it is both the online reading PDF and the Lulu interior submission candidate. Its
first page reuses the shared visual title plate, followed by copyright with the
assigned ISBN, a dedication page, and a generated contents page. The same
pipeline embeds the fonts it uses and flattens detected transparency; it still
requires page-by-page inspection and a physical proof. Cover production remains
a separate workflow.

```bash
make book
make master-pdf
make preflight
make validate-lulu
```

The current title art is approximately 162 ppi at 6×9, so the master remains a
beta/review artifact. `make preflight` warns about this; a release preflight
will fail until it is replaced with 300 ppi artwork. See `book/cover/README.md`
for the page-count and Lulu-template boundary that prevents a provisional cover
from being mistaken for an upload-ready wrap.

## Editorial audit and beta target

Run the canonical prose audit before each editorial checkpoint:

```bash
make audit-book
```

It checks required lesson sections, local runnable-code links, citation keys,
and the manuscript word budget. The current beta target is 45,000–55,000 words
(roughly 180–220 6×9 pages); the audit reports progress without treating word
count alone as evidence of editorial quality.
