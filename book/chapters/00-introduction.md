---
sidebar_position: 0
title: Introduction and Setup
slug: /
---

# From Tensors to Agents

This book is a build log for a software engineer learning modern AI on Apple
Silicon. Each chapter connects an idea to runnable code, an experiment, a
failure mode, and a decision about when the technique is worth using.

This is also a living setup chapter. It records the exact way to prepare the
project, run what is currently implemented, and distinguish a working lesson
from a planned one. We will extend it as later milestones add transformers,
local models, retrieval, and agent workflows; do not assume a command exists
until it appears here or in the chapter that introduces it.

## What you are building

The end product has one canonical editorial source and two reading formats:

```text
research notes + citations ─┐
                           ├──> book/chapters/ ──> Docusaurus course site
experiments + benchmarks ──┘                   └──> DOCX ─> Word PDF ─> Lulu proof
```

- `book/chapters/` is the only source of published prose. The course does not
  copy it.
- `research/` holds working notes and the shared `references.bib` bibliography.
- `experiments/` holds small runnable lessons; `src/` contains reusable code.
- `benchmarks/` holds reproducible observations and their limitations.
- `site/` is the Docusaurus navigation shell over the canonical chapters.
- `book/build/` and PDF exports are generated artifacts and must stay out of
  Git.

The book's later capstone is a Book Intelligence Assistant. It will index this
repository's chapters, research notes, experiments, and benchmarks; retrieve
evidence with source paths; propose and critique improvements; and stop for
human approval before any write. It does not modify the project autonomously.

## What is implemented today

Chapters 1–3 have executable tensor, autograd, and PyTorch/MPS lessons with a
recorded Day 1 benchmark. Chapters 4–5 now have a deterministic synthetic
vision fixture plus matched PyTorch and TensorFlow/Keras CNN implementations.
The remaining chapters are deliberately marked as drafts until their evidence
exists. The current project status and next task are maintained in
`docs/journals/from-tensors-to-agents-beta.md`.

## Prerequisites

Use a Mac with Apple Silicon when you want to reproduce MPS observations, but
the early Python tests and examples are designed to fall back to CPU. Install:

- Python 3.11;
- [uv](https://docs.astral.sh/uv/) for Python environments and lockfile-based
  dependency installs;
- Node.js 20 and npm for the Docusaurus course;
- Pandoc for DOCX generation;
- Microsoft Word on macOS for the **release** PDF export. LibreOffice is only a
  non-release fallback.

Before installing a large optional framework or model package, check available
space with:

```bash
df -h .
```

Install it when there is sufficient headroom. If there is not, record the space
constraint and pause that optional milestone rather than pretending it was
completed.

## Base installation

Clone the repository, enter it, and create the locked development environment:

```bash
git clone <your-repository-url> ai-on-mac
cd ai-on-mac
uv sync --group dev
```

The first command intentionally leaves the remote URL to the reader or project
owner. The repository can be used locally without a GitHub remote.

Validate the base environment:

```bash
uv run ruff check .
uv run pytest
uv run python experiments/01-tensors/broadcasting.py
uv run python experiments/02-gradients/autograd.py
uv run python experiments/03-pytorch/train_tiny_network.py
```

The last command chooses MPS when the installed PyTorch build reports it as
available and otherwise uses CPU. An explicit device can be selected in the
benchmark command:

```bash
uv run python benchmarks/01-day1/run.py --device auto --epochs 250 --runs 5 --seed 7
```

Recorded results are machine-specific evidence, not promises of performance on
another Mac. Read `benchmarks/01-day1/README.md` before drawing conclusions.

## Optional TensorFlow/Keras installation

TensorFlow is isolated in an optional `uv` group so the foundation remains
lightweight. Install and run the framework-comparison exercise only when you
reach Chapters 4–5:

```bash
df -h .
uv sync --group tensorflow
uv run --group tensorflow python experiments/04-tensorflow/train_keras_cnn.py --epochs 30
```

Run the matching PyTorch program with the same declared fixture and training
budget:

```bash
uv run python experiments/05-vision/train_pytorch_cnn.py --device auto --epochs 30
```

Compare correctness using the held-out accuracy, confusion matrix, and mistake
list in `benchmarks/02-vision/README.md`. Do not compare the two elapsed values
as framework speed: their current device and timing conditions are not a fair
benchmark.

## Site and manuscript builds

Build the course site with its own Node lockfile:

```bash
cd site
npm ci
npm run build
cd ..
```

Build the draft manuscript DOCX from the committed Lulu 6×9 Word template:

```bash
./scripts/build-book.sh
```

This writes `book/build/from-tensors-to-agents.docx`. It is a review artifact,
not an upload-ready PDF. At print-production time, export it through Word on
macOS, run the preflight script, and inspect every rendered page before calling
the result release-ready.

## Optional ClineFlow journaling

Use [ClineFlow](https://github.com/hassanvfx/clineflow) when persistent journals
and project context would make AI-assisted development easier to resume. It is
an optional workflow aid: this companion repository neither installs nor
depends on it at runtime.

To adopt the same journal workflow, follow ClineFlow's current README in the
repository root and then create a project journal under `docs/journals/`. For
this project the long-lived journal is
`docs/journals/from-tensors-to-agents-beta.md`. Begin each work session by
reading its current status; before each commit, record the decision, changed
paths, commands and results, failures, and next smallest action.

## How to learn with the repository

For every implemented chapter:

1. Read the intuition and predict the result.
2. Run the listed program unchanged.
3. Change one declared condition—shape, seed, device, or data difficulty.
4. Keep the original observation; record the new condition and result
   separately.
5. Read the associated benchmark or research note before making a general
   claim.

The course site and print book share this Markdown source. Complete code and
measured observations stay in the companion repository so the prose can remain
readable without hiding the evidence.
