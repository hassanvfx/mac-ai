# From Tensors to Agents — Beta Implementation Journal

**Last updated:** 2026-08-14  
**Project:** *From Tensors to Agents: Learning Modern AI by Building It on Apple Silicon*  
**Scope:** Book, Docusaurus course, reproducible experiments, Book Intelligence Assistant, and print-ready beta preparation.

---

## Charter and Beta Definition

This repository is the companion learning laboratory for an English 6×9 US Trade paperback and reading-first GitHub Pages course. The beta is complete when it has a coherent 180–220 page draft, one canonical Markdown manuscript shared by the site and book pipeline, runnable evidence for all technical claims, a safe Book Intelligence Assistant, and reproducible validation from a clean checkout.

The beta is **not** a final commercial print release. Copyediting, a full visual proof pass, final cover creation, ISBN/metadata decisions, Lulu upload, and physical proof approval are a post-beta production phase.

### Source-of-truth map

```text
research notes + references.bib ─┐
                                ├──> book/chapters/ canonical published prose
experiments + benchmarks ───────┘             ├──> site/ navigation shell → GitHub Pages
                                              └──> Pandoc + Lulu .dotx → DOCX → Word PDF

book/chapters + research + experiments + benchmarks → Book Intelligence Assistant corpus
```

- `research/` holds source notes, citations, and observations.
- `book/chapters/` is the only published-prose source; the course must not copy chapter text.
- `experiments/`, `benchmarks/`, and `src/` contain executable evidence and reusable implementation.
- `site/` presents canonical chapters and links to code.
- `book/templates/lulu-us-trade-interior-template.dotx` is the versioned interior layout authority.
- `book/build/`, exported PDFs, indexes, caches, and per-developer configuration are generated and remain untracked.
- ClineFlow is an optional, unchanged journaling/context workflow. It is not a runtime dependency of the Book Intelligence Assistant.

## Status Overview

### ✅ Setup — Git baseline and ClineFlow journaling

- [x] Initialize local Git repository on `main`.
- [x] Commit existing project foundation as a baseline.
- [x] Install ClineFlow with its official installer.
- [x] Confirm installation is additive and ignores `.clineflow.local`.
- [x] Create this long-lived project journal from the ClineFlow template.
- [x] Commit the workflow setup and journal.

**Status:** Complete after the setup commit.

### 🔧 Milestone 1 — Foundations and Chapters 1–3

- [ ] Expand tensors, gradients, and PyTorch chapters into evidence-backed drafts.
- [ ] Capture actual M4 Pro MPS measurements for the Day 1 workload.
- [ ] Add print-quality tensor-shape, gradient-flow, and training-loop diagrams.
- [ ] Produce and visually inspect the first 6×9 DOCX proof.

**Gate:** Day 1 code/tests pass, the benchmark record is complete, and Chapters 1–3 contain real prose, experiments, and takeaways.

### Milestone 2 — Vision and Framework Comparison

- [ ] Build a reproducible CNN with train/validation/test metrics and error analysis.
- [ ] Implement the equivalent TensorFlow/Keras model with matched data, split, seed, and metrics.
- [ ] Write Chapters 4–5 around recorded results rather than API walkthroughs.

**Gate:** The PyTorch/TensorFlow comparison table is supported by runnable code and recorded results.

### Milestone 3 — Transformers and Apple Silicon

- [ ] Add tokenizer inspection, pretrained transformer inference, and manual output analysis.
- [ ] Add MLX/MLX-LM local-inference experiments with model, quantization, prompts, timing, and memory methodology declared.
- [ ] Write Chapters 6–7 using PyTorch MPS and MLX/MLX-LM evidence.

**Gate:** Every performance or memory claim has a benchmark record; unsupported hardware claims are removed.

### Milestone 4 — Embeddings, RAG, and Book Intelligence

- [ ] Replace the deterministic retrieval baseline with local learned embeddings while retaining deterministic fixture tests.
- [ ] Add chunking, retrieval quality checks, citation-key propagation, and grounded-answer evaluation.
- [ ] Expand Chapters 8–9 using this repository as the canonical corpus.

**Gate:** The assistant cites real repository paths, refuses unsupported answers, and passes the versioned evaluation dataset.

### Milestone 5 — LangChain, LangGraph, and Agent Comparisons

- [ ] Add direct-SDK and LangChain structured-output implementations over identical evidence.
- [ ] Implement LangGraph state, checkpoint/resume, interrupt, approval, and rejection paths.
- [ ] Compare deterministic retrieval, a single planner, and a researcher/critic/writer graph on book-maintenance tasks.
- [ ] Write Chapters 10–13 from observed trade-offs.

**Gate:** No workflow can modify book/code/Git state before explicit human approval; state transitions and fallback paths are tested.

### Milestone 6 — Reliability and Public Beta

- [ ] Add evaluation runner, traces, latency/error records, failure fixtures, and reliability policy.
- [ ] Complete Chapter 14 and audit all chapters for citations, experiment links, alternatives, and takeaways.
- [ ] Configure real GitHub organization/project values, publish the Docusaurus site, and tag the beta release.

**Gate:** Python tests, site build, link checks, manuscript build, and evaluation suite pass from a clean environment.

### Milestone 7 — Print Production

- [ ] Freeze beta text and complete technical editing/copyediting.
- [ ] Build DOCX using the Lulu reference template; export with Word; render and inspect every page.
- [ ] Run 6×9 preflight, determine final page count, download the exact cover template, create the cover, and order a Lulu proof.
- [ ] Correct proof findings before final publication.

**Gate:** Approved print proof, final interior and cover PDFs, correct metadata, and release archive.

## Current Implemented State

### Repository foundation

- Python project is managed by `uv`, targets Python 3.11, and has `uv.lock` committed.
- Quality commands are exposed through `Makefile`; the initial Python suite contains deterministic Day 1 and Book Intelligence tests.
- Code is MIT licensed in `LICENSE`; book text and visual assets are reserved as described in project documentation.
- A Lulu US Trade interior template is committed at `book/templates/lulu-us-trade-interior-template.dotx` with provenance in `book/templates/README.md`.

### Editorial, site, and publishing baseline

- `book/chapters/00-introduction.md` through `14-building-an-ai-system-you-can-trust.md` exist as initial chapter drafts/skeletons.
- `site/` is a Docusaurus shell over the book chapters, with CI and GitHub Pages workflow definitions in `.github/workflows/`.
- `scripts/build-book.sh`, `scripts/export-pdf.applescript`, and `scripts/preflight_pdf.py` define the DOCX/PDF route. A release PDF still requires Word on macOS and visual inspection.

### Executable learning baseline

- Day 1 examples cover broadcasting, autograd, and a small PyTorch network with MPS selection and CPU fallback.
- The initial Book Intelligence baseline supports deterministic fixture retrieval, grounded-answer behavior, and an approval checkpoint example.
- Versioned evaluation fixtures are in `evals/book_intelligence.jsonl`.

### Validated before this journal

- `uv run ruff check .` — passed.
- `uv run pytest` — 10 tests passed.
- `npm ci` followed by `npm run build` in `site/` — passed under Node 20.

Re-run these commands after dependency or content changes; the above is a recorded baseline, not a perpetual guarantee.

## Decisions and Assumptions

| Decision | Rationale | Consequence |
| --- | --- | --- |
| Markdown chapters are canonical | One prose source prevents site/book drift | Site consumes book Markdown; no duplicate prose |
| Local Apple Silicon first | The learning goal is practical Mac-native AI | Optional OpenAI-compatible comparison is environment-configured; no secrets committed |
| Repository is the assistant corpus | The capstone teaches maintenance of a real artifact | Indexes are local/generated; fixture corpus powers repeatable tests |
| Human approval before writes | Agent lessons must model safe production boundaries | Planning/review flows are read-only until explicit approval |
| ClineFlow stays external to runtime | Journaling should not burden readers or assistant installs | Use its files/workflow only; no ClineFlow application changes |
| No remote yet | Remote ownership/destination remains a user choice | Do not add, push, or publish until supplied |

## Risks and Open Questions

- The current chapters are foundational drafts, not yet the target 180–220 manuscript pages.
- Day 1 MPS measurements have not been captured as a benchmark record on the target Mac.
- TensorFlow, transformer, MLX/MLX-LM, LangChain, and full LangGraph implementations are planned but incomplete.
- DOCX can be generated when Pandoc/template requirements are met; Word export and page-by-page print inspection remain macOS release tasks.
- The GitHub Pages workflow contains placeholder repository/organization values until the publishing destination is chosen.
- Performance and memory statements must remain absent or explicitly provisional until a versioned measurement record exists.

## Evidence and Benchmark Rules

Every experiment and benchmark record must state:

- seed, package/model versions, source data, device, and expected output;
- workload, warmup/measurement method, timing units, and memory-observation method when applicable;
- the related chapter, source/citation key, and limitations;
- whether the result was run on MPS or CPU fallback.

Performance, memory, framework, and model-behavior statements must cite either `research/references.bib` or a committed benchmark record. Keep raw large output out of the journal; link to its durable record instead.

## Chapter Status

| Chapters | Topic | Editorial state | Evidence state |
| --- | --- | --- | --- |
| 1–3 | tensors, gradients, PyTorch | initial drafts | Day 1 examples/tests exist; benchmark/diagrams pending |
| 4–5 | TensorFlow comparison, vision | skeletons | CNN and matched comparison pending |
| 6–7 | transformers, Apple Silicon | skeletons | tokenizer, inference, MLX benchmarks pending |
| 8–9 | embeddings and RAG | initial baseline | deterministic fixture implementation exists; learned embeddings/evaluation pending |
| 10–13 | systems, graphs, agents | skeletons | direct SDK/LangChain/LangGraph comparison pending |
| 14 | reliability | skeleton | full evaluation and policy audit pending |

All chapters must ultimately include intuition, problem, minimal implementation, real implementation, experiment, failures, alternatives, usage guidance, and takeaway.

## Working Rules

1. Begin each work session by reading this journal’s current state and next task.
2. Before every commit, append the decision, changed paths, commands/results, failures, and immediate next action.
3. Keep each milestone incomplete until its code, evidence, prose, and verification are present.
4. Keep `.clineflow.local`, `.book-intelligence/`, virtual environments, caches, indexes, site build output, and generated DOCX/PDF artifacts untracked.
5. ClineFlow reference symlinks are optional. Do not run `setup-refs.sh` or create external references unless the user deliberately chooses their sources.
6. Do not add a GitHub remote, publish a site, create a release, or submit anything to Lulu without explicit destination/approval.

## Completion Checklist

### Code and evidence

- [ ] All experiments have declared inputs, seed, versions, device, expected output, and tests.
- [ ] Benchmark records support every performance/memory claim.
- [ ] Book Intelligence Assistant passes retrieval, grounding, planning/review, approval, fallback, and evaluation tests.
- [ ] All agent workflows stop before modifying prose, code, Git, or external services.

### Manuscript and course

- [ ] Fourteen substantive, cited chapters meet the editorial rhythm.
- [ ] Internal links, code links, bibliography keys, and site navigation are valid.
- [ ] Docusaurus production build succeeds and is configured for the selected GitHub Pages destination.
- [ ] Manuscript DOCX builds against the committed Lulu template.

### Print and release

- [ ] Word exports a 6×9 single-page interior PDF.
- [ ] Preflight and rendered-page inspection pass.
- [ ] Final cover template is downloaded only after final page count is known.
- [ ] Lulu proof is reviewed and approved before publication.
- [ ] Beta tag, artifacts, release notes, and publishing archive are prepared after remote selection.

## Journal Entries

### 2026-08-14 — Baseline and journaling setup

**What changed:**

- Initialized this repository locally on the `main` branch.
- Created baseline commit `aeeb59b` (`chore: establish from tensors to agents foundation`) containing the pre-existing book/course/experiment/publishing foundation and Lulu template.
- Installed ClineFlow with its official installer command.
- Added ClineFlow’s additive agent instructions, templates, workflow documentation, optional reference helper, and ignored per-developer configuration entry.
- Created this project-long journal at `docs/journals/from-tensors-to-agents-beta.md`.

**Collision inspection:**

- `README.md` was not changed.
- Existing `.github/workflows/ci.yml` and `.github/workflows/deploy-pages.yml` were not changed; ClineFlow added only `.github/copilot-instructions.md`.
- The only existing-file modification is an additive `.clineflow.local` rule in `.gitignore`.
- The book layout and chapter directories were not changed by installation.

**Why:**

Git establishes a recoverable, reviewable baseline before workflow changes. ClineFlow provides persistent project context while remaining optional for readers and independent of the Book Intelligence Assistant runtime.

**Verification:**

- Installation completed successfully and created `.clinerules`, `AGENTS.md`, `.windsurf/rules/clineflow.md`, `clineflow/`, `docs/journals/.gitkeep`, `.clineflow.example`, `setup-refs.sh`, and `VERSION`.
- `.gitignore` now excludes `.clineflow.local`.
- Prior baseline validation: Ruff passed, 10 pytest tests passed, and the Docusaurus production build passed under Node 20.

**Next task:**

- [ ] Start Milestone 1 by running and recording Day 1 measurements on this Mac, then turn Chapters 1–3 into evidence-backed drafts.
- [ ] Decide the GitHub remote before configuring live GitHub Pages values.

**Status:** Setup complete; Milestone 1 ready to begin.

