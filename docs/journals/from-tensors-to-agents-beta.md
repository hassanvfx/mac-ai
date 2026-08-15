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

- [x] Expand tensors, gradients, and PyTorch chapters into evidence-backed drafts.
- [x] Capture actual M4 Pro MPS measurements for the Day 1 workload.
- [x] Add print-quality tensor-shape, gradient-flow, and training-loop diagrams.
- [x] Produce and visually inspect the first 6×9 DOCX proof.

**Gate:** Day 1 code/tests pass, the benchmark record is complete, and Chapters 1–3 contain real prose, experiments, and takeaways.

**Status:** Complete. Historical foundation; current active work is Milestone 5.

### Milestone 2 — Vision and Framework Comparison

- [x] Build a reproducible CNN with train/validation/test metrics and error analysis.
- [x] Implement the equivalent TensorFlow/Keras model with matched data, split, seed, and metrics.
- [x] Write Chapters 4–5 around recorded results rather than API walkthroughs.

**Gate:** The PyTorch/TensorFlow comparison table is supported by runnable code and recorded results.

**Status:** Complete. The fixture demonstrates task-level equivalence only; it
does not make a framework-speed or real-image-performance claim.

### Milestone 3 — Transformers and Apple Silicon

- [x] Add tokenizer inspection, pretrained transformer inference, and manual output analysis.
- [x] Add MLX/MLX-LM local-inference experiments with model, quantization, prompts, timing, and memory methodology declared.
- [x] Write Chapters 6–7 using PyTorch MPS and MLX/MLX-LM evidence.

**Gate:** Every performance or memory claim has a benchmark record; unsupported hardware claims are removed.

**Status:** Complete. The new timings and memory fields are narrow recorded
observations, not cross-runtime performance or total-memory claims.

### Milestone 4 — Embeddings, RAG, and Book Intelligence

- [x] Replace the deterministic retrieval baseline with local learned embeddings while retaining deterministic fixture tests.
- [x] Add chunking, retrieval quality checks, citation-key propagation, and grounded-answer evaluation.
- [x] Expand Chapters 8–9 using this repository as the canonical corpus.

**Gate:** The assistant cites real repository paths, refuses unsupported answers, and passes the versioned evaluation dataset.

**Status:** Complete. The learned path is local and provenance-preserving; its
initial run is a correctness observation, not a retrieval-quality or
performance benchmark.

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
- TensorFlow/Keras is an opt-in `uv` group. Its current recorded run uses
  TensorFlow 2.21.0 on CPU; it is not required by the core development group.
- Transformers 5.15.0 and MLX/MLX-LM 0.31 are opt-in `uv` groups. Public model
  weights are cached locally outside Git; they are not base dependencies.
- Quality commands are exposed through `Makefile`; the initial Python suite contains deterministic Day 1 and Book Intelligence tests.
- Code is MIT licensed in `LICENSE`; book text and visual assets are reserved as described in project documentation.
- A Lulu US Trade interior template is committed at `book/templates/lulu-us-trade-interior-template.dotx` with provenance in `book/templates/README.md`.

### Editorial, site, and publishing baseline

- The introduction is the living onboarding chapter: prerequisites, base and
  optional installation, validation, build paths, and ClineFlow journaling are
  documented there and will grow with the project.
- `book/chapters/00-introduction.md` through `14-building-an-ai-system-you-can-trust.md` exist; Chapters 1–7 now contain substantive draft material.
- `site/` is a Docusaurus shell over the book chapters, with CI and GitHub Pages workflow definitions in `.github/workflows/`.
- `scripts/build-book.sh`, `scripts/export-pdf.applescript`, and `scripts/preflight_pdf.py` define the DOCX/PDF route. A release PDF still requires Word on macOS and visual inspection.

### Executable learning baseline

- Day 1 examples cover broadcasting, autograd, and a small PyTorch network with MPS selection and CPU fallback.
- The Day 1 benchmark runner records an explicit device, warmup, MPS synchronization, timing samples, and deterministic final loss.
- The initial Book Intelligence baseline supports deterministic fixture retrieval, grounded-answer behavior, and an approval checkpoint example.
- Versioned evaluation fixtures are in `evals/book_intelligence.jsonl`.

### Validated before this journal

- `uv run --group tensorflow --group transformers --group mlx ruff check .` — passed.
- `uv run --group tensorflow --group transformers --group mlx pytest` — 22 tests passed.
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
- LangChain and full LangGraph implementations are planned but incomplete.
- The Milestone 2 timing observations are deliberately not a framework-speed comparison; a normalized multi-run protocol remains future work.
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
| 1–3 | tensors, gradients, PyTorch | substantive evidence-backed drafts | Day 1 examples, tests, MPS record, and diagrams committed |
| 4–5 | TensorFlow comparison, vision | substantive evidence-backed drafts | matched CNN fixture, tests, results, and limitations committed |
| 6–7 | transformers, Apple Silicon | substantive evidence-backed drafts | tokenizer/pipeline inspection, MPS/CPU result, MLX-LM observation, and records committed |
| 8–9 | embeddings and RAG | substantive evidence-backed drafts | local learned retrieval, evidence-only RAG, fixtures, and evaluation committed |
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

## Execution Plan — Work Remaining

This is the operational order of work. A later milestone may be designed early, but its gate cannot be claimed until the required code, recorded evidence, manuscript prose, and verification are all committed.

### Track A — Shared engineering and editorial infrastructure

- [ ] Add a reusable experiment-record format and apply it to every new experiment.
- [ ] Add a benchmark-record format with machine, dependency, workload, warmup, timing, and limitations fields.
- [ ] Add a citation/link validation command for chapters, code paths, BibTeX keys, and site links.
- [ ] Keep dependency groups intentional: core/test tooling always reproducible; large frameworks and model adapters opt-in where practical.
- [ ] Maintain fixture data that is small, versioned, non-sensitive, and sufficient for CPU-only CI.
- [ ] Update README and course landing page as capabilities become real; keep ClineFlow a recommendation only, never a required dependency.

**Completion definition:** A contributor can clone, install documented prerequisites, run the checks, understand source ownership, and distinguish tracked evidence from generated artifacts.

### Track B — Manuscript and visual system

- [ ] Establish a chapter-level editorial checklist and target word/page budget (approximately 10–14 manuscript pages per chapter).
- [ ] Expand Chapters 1–3 from their current draft state, citing research and linking runnable examples.
- [ ] Write Chapters 4–7 only after the matched framework, tokenizer, transformer, and local-inference evidence exists.
- [ ] Write Chapters 8–14 alongside the Book Intelligence implementation, using its own artifacts as the evidence base.
- [ ] Create diagrams as editable, print-quality originals under `book/`; derive web-friendly copies only when necessary.
- [ ] Maintain front matter, copyright page, chapter ordering, bibliography treatment, listing style, and cross-references.
- [ ] Build a DOCX early and repeatedly to expose print-layout issues before the manuscript is large.

**Completion definition:** Every chapter has intuition, problem, minimal and real implementation, experiment, failures, alternatives, guidance, takeaway, citations, and tested links.

### Track C — Learning experiments and Apple Silicon evidence

- [x] Record the exact Day 1 M4 Pro result: OS/device, Python/Torch versions, seed, workload, MPS/CPU selection, time, output checks, and observed limitations.
- [x] Add a reproducible vision dataset fixture, CNN train/validation/test loop, metrics, and error-analysis output.
- [x] Add a TensorFlow/Keras equivalent that explicitly matches data preprocessing, split, seed, epoch budget, and metrics.
- [x] Add tokenizer vocabulary/segmentation inspection and controlled pretrained-transformer inference.
- [x] Add MLX and MLX-LM local experiments only after selecting versions/models that run on the target Mac; document quantization and prompt workload.
- [ ] Normalize benchmark methods before comparing PyTorch MPS, TensorFlow, MLX, and MLX-LM; do not imply comparisons from incompatible workloads.

**Completion definition:** Claims in Chapters 1–7 link to committed scripts and records that a reader can rerun or accurately interpret as machine-specific.

### Track D — Book Intelligence Assistant

- [x] Define corpus ingestion contracts for Markdown, code, benchmark records, and BibTeX-backed research notes.
- [x] Preserve path, chapter identifier, citation key, source type, and experiment/benchmark metadata in every chunk.
- [x] Retain deterministic retrieval tests; add a local learned-embedding implementation behind a stable interface.
- [x] Add chunking configuration, retrieval-quality evaluation, citation-key propagation, and source-path validation.
- [x] Enforce grounded answers: each answer cites retrieved repository evidence or explicitly reports missing evidence.
- [x] Implement structured chapter/experiment plans and a critic that flags unsupported claims, missing evidence, broken links, and missing alternatives.
- [ ] Implement direct SDK (optional environment configuration) and LangChain structured-output paths over the same retrieved context.
- [ ] Implement LangGraph persistence, checkpoint/resume, interrupts, approval/rejection, unavailable-model/API fallback, and a strict no-write boundary.
- [ ] Compare deterministic retrieval, single planner, and researcher/critic/writer graph using the same versioned book-maintenance evaluation tasks.

**Completion definition:** The assistant is useful against this repository, testable on fixtures without secrets, accurately cites evidence, and cannot write until a human explicitly approves a proposed action.

### Track E — Evaluation, reliability, and beta release

- [ ] Add an evaluation runner for retrieval, grounding, plan completeness, citation accuracy, latency, fallback behavior, and unsafe-action refusal.
- [ ] Store traces/results as concise, versioned records; exclude indexes, secrets, and bulky local model artifacts.
- [ ] Add failure fixtures: empty corpus, missing source, unavailable local model, invalid API configuration, unsupported request, rejected approval, and interrupted/resumed graph.
- [ ] Write a reliability policy in Chapter 14 and project documentation that distinguishes demo behavior from production guarantees.
- [ ] Run clean-environment validation: `uv sync --group dev`, quality checks, tests, site install/build/link check, and DOCX build.
- [ ] Once a GitHub destination is supplied, configure Pages values, push, publish, attach beta artifacts, and create the beta tag.

**Completion definition:** A clean checkout passes release gates and the published beta accurately communicates its capabilities and limits.

### Track F — Post-beta print production

- [ ] Freeze beta text and run technical and copyediting passes.
- [ ] Generate DOCX with the committed Lulu template and export the release PDF through Word on macOS.
- [ ] Render and inspect each page, run preflight, and resolve dimensions, font, page-layout, margin, and image-resolution findings.
- [ ] After the final interior page count, obtain the exact Lulu cover template, build the color cover, and validate metadata.
- [ ] Order and inspect a Lulu proof; fix findings; archive final release inputs and outputs.

**Completion definition:** A physically/digitally approved proof exists before the book is submitted for publication.

## Dependency-Safe Work Sequence

The recommended sequence prevents prose and comparison claims from outrunning evidence:

1. **Milestone 1:** instrument and record existing Day 1 work; improve Chapters 1–3; make the first DOCX proof.
2. **Milestone 2:** build matched PyTorch and TensorFlow vision experiments; then write Chapters 4–5.
3. **Milestone 3:** build transformer/tokenizer and MLX evidence; then write Chapters 6–7.
4. **Milestone 4:** evolve retrieval and grounding against the book corpus; then write Chapters 8–9.
5. **Milestone 5:** add structured planning, graph state, approval, and comparative evaluation; then write Chapters 10–13.
6. **Milestone 6:** harden tests/evaluations, finish Chapter 14, run release gates, and publish only after a remote is chosen.
7. **Milestone 7:** perform the deliberately separate print-production pass and Lulu proof cycle.

## Current Progress Snapshot

| Area | Present now | Remaining before beta |
| --- | --- | --- |
| Repository | Git `main`, local setup and Day 1 commits, Python/Node lockfiles, CI workflows | choose remote; configure real Pages destination; publish/tag only with approval |
| Book | 15 Markdown files: a living setup introduction, Chapters 1–7 substantive drafts, Lulu interior template committed | 180–220-page prose, later citations/diagrams, cross-link audit, iterative proofs |
| Site | Docusaurus configuration and lockfile; build previously passed | content/link audit and real deployment configuration |
| Day 1 | tensor, autograd, tiny PyTorch/MPS examples, tests, MPS record, diagrams | retain evidence discipline through later chapters |
| Vision / TensorFlow | matched synthetic CNN scripts, tests, record, and Chapters 4–5 | controlled-difficulty/real-data work only before broader vision claims |
| Transformers / MLX | inspected pretrained classifier, MLX-LM local model, tests, records, and Chapters 6–7 | normalized cross-runtime generative benchmark only before speed claims |
| Later experiments | directory structure and planning only | learned embeddings, RAG evaluation, LangChain, LangGraph, and reliability work |
| Book Intelligence | deterministic search, grounded-answer baseline, approval checkpoint, fixtures/tests | learned embeddings, metadata-rich ingestion, quality evaluation, SDK/LangChain/LangGraph, workflow comparison |
| Publishing | Pandoc/Word/preflight scripts and Lulu template | successful iterative DOCX proof, Word PDF, preflight/render inspection, final print proof |

## Immediate Next Session Plan — Milestone 4

1. Read this journal and the current Book Intelligence baseline.
2. Check space before adding a local embedding dependency; use a small frozen fixture corpus for CPU-only tests.
3. Replace the deterministic-only retrieval path behind a stable interface while preserving its existing fixture behavior.
4. Add corpus metadata, chunking, citation-key propagation, retrieval evaluation, and grounded-answer tests.
5. Only after evidence exists, expand Chapters 8–9 and update Chapter 0 with the new optional installation commands.
6. Run Python, site, DOCX, and visual-layout checks; update this journal before committing.

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

---

### 2026-08-14 — Completion-plan recap

**What changed:**

- Reviewed the active journal and the tracked project inventory.
- Added a complete operational work breakdown: shared infrastructure, manuscript/visual system, experiments, Book Intelligence Assistant, beta reliability/release, and post-beta print production.
- Added the dependency-safe milestone order, a current-progress table, and an immediate Milestone 1 checklist.

**Current reality:**

- The repository and workflow foundation are complete.
- The book/course exists as an initial structured draft, not yet as a substantive beta manuscript.
- Day 1 code and deterministic Book Intelligence fixtures are the only implemented evidence base; later learning, model, and agent milestones remain planned work.

**Decision:**

Use this journal as the single project execution record. Work proceeds evidence first, then chapter prose, then milestone verification. Publishing and Lulu actions remain blocked until the user supplies a destination or explicitly authorizes the applicable step.

**Next steps:**

- [ ] Begin the Day 1 benchmark record on this Mac.
- [ ] Expand Chapters 1–3 from that measured evidence.
- [ ] Produce the first DOCX proof and record blockers/findings.

**Status:** Milestone 1 in progress; no implementation changes made in this planning update.

---

### 2026-08-14 — Day 1 evidence, drafts, and first DOCX proof

**What changed:**

- Added `benchmarks/01-day1/run.py`, a repeatable CPU/MPS benchmark runner with explicit device selection, one unmeasured warmup, MPS synchronization, fixed seed, and configurable timed runs.
- Moved the shared synthetic training workload into `src/from_tensors_to_agents/training.py`; the reading example and the benchmark now use the same implementation.
- Added a CPU deterministic-training regression test.
- Replaced the Day 1 observation placeholder with a complete, limited benchmark record in `benchmarks/01-day1/README.md`.
- Expanded Chapters 1–3 into evidence-backed drafts with minimal/real implementations, experiments, failure modes, alternatives, and takeaways.
- Fixed the DOCX build pipeline: it now strips leading Docusaurus front matter only in temporary print copies, preventing chapter metadata from overriding the book title.

**Recorded benchmark:**

- Target Mac: macOS 26.1 arm64; Python 3.11.9; PyTorch 2.13.0.
- MPS was available. The fixed seed-7, 250-epoch workload reached final loss `0.000994` in every timed run.
- Five MPS timings were 120.537, 122.571, 119.637, 121.099, and 119.836 ms; median 120.537 ms.
- The record explicitly makes no CPU-versus-MPS, general hardware, or memory claim.

**Verification:**

- `uv run ruff check .` — passed.
- `uv run pytest` — 11 passed.
- `cd site && npm run build` — passed after one broken benchmark Markdown link was converted to a print-safe repository path.
- `./scripts/build-book.sh` — produced `book/build/from-tensors-to-agents.docx`.
- Rendered and inspected all 15 DOCX pages. The title now correctly reads *From Tensors to Agents*; no visible clipping or overlap was found.

**Print-proof finding:**

The initial proof is readable but intentionally not release-ready: it is short because Chapters 4–14 remain skeletons, and the single bibliography entry leaves substantial white space on the final page. These are expected beta-draft conditions, not a preflight pass for publication.

**Next steps:**

- [ ] Create the tensor-shape, gradient-flow, and training-loop diagrams as editable print-quality source assets.
- [ ] Rebuild/render after adding diagrams; then close Milestone 1.
- [ ] Start Milestone 2 with a versioned vision-data fixture and a PyTorch CNN before writing the framework-comparison prose.

**Status:** Milestone 1 substantially progressed; diagram assets remain before its gate can close.

---

### 2026-08-14 — Day 1 diagrams and Milestone 1 closure

**What changed:**

- Added editable SVG masters and matching PNG derivatives under `book/assets/day1/` for tensor broadcasting, autograd gradient flow, and the six-step PyTorch training loop.
- Embedded the PNG derivatives in canonical Chapters 1–3 so the same Markdown renders the diagrams on the course site and in the DOCX.
- Updated the DOCX builder’s temporary workspace to retain the canonical `chapters/` → `assets/` relationship and to rewrite print-copy asset paths safely.
- Documented the SVG-master/PNG-derivative policy in `book/README.md`.

**Why:**

SVG is the editable, resolution-independent visual source. The local Pandoc installation lacks an SVG converter, so PNG derivatives provide reliable DOCX embedding without losing the editable original.

**Verification:**

- Docusaurus production build completed with the chapter images.
- The manuscript DOCX built with no missing-image warnings after the asset-path fix.
- Rendered and inspected all 16 pages of the current DOCX proof. All three diagrams are legible in the 6×9 layout; no clipping or overlap was observed.

**Decision:**

Milestone 1 is complete. The proof is still a draft artifact—not a release PDF—because later chapters remain incomplete and must add citations, experiments, and visual content before print production.

**Next steps:**

- [ ] Start Milestone 2: create a small versioned vision fixture and reproducible PyTorch CNN with train/validation/test metrics and error analysis.
- [ ] Only then implement a matched TensorFlow/Keras version with the same split, seed, preprocessing, and metrics.
- [ ] Expand Chapters 4–5 from recorded comparison evidence.

**Status:** Milestone 1 complete; Milestone 2 ready to begin.

---

### 2026-08-14 — Vision comparison, optional TensorFlow, and living setup chapter

**What changed:**

- Added the deterministic 16×16 geometric-image fixture, reusable PyTorch CNN,
  and confusion-matrix utility in `src/from_tensors_to_agents/vision.py`.
- Added matched PyTorch and TensorFlow/Keras training programs under
  `experiments/05-vision/` and `experiments/04-tensorflow/`.
- Added fixture/model regression tests and the complete observation record at
  `benchmarks/02-vision/README.md`.
- Added a TensorFlow 2.21 opt-in `uv` group and its lockfile resolution after
  checking that this Mac had 14 GiB free. TensorFlow imported successfully and
  reported CPU as its only visible device.
- Added the framework/vision research note and TensorFlow installation citation.
- Expanded Chapters 4–5 from the observed contract and results, without a
  speed or real-image-performance claim.
- Rewrote Chapter 0 as a living installation and onboarding chapter. It now
  documents prerequisites, base validation, optional TensorFlow installation,
  site/DOCX builds, disk-space policy, and optional ClineFlow journaling.

**Recorded results:**

- PyTorch 2.13.0 reached 1.000 train/validation/test accuracy on the fixture
  with MPS selected and with CPU explicitly selected.
- TensorFlow/Keras 2.21.0 reached the same metrics on CPU.
- Every held-out confusion matrix was the identity matrix with zero mistakes.
- The TensorFlow run emitted a non-fatal `use_unbounded_threadpool` NodeDef
  compatibility warning. Training and evaluation completed; the warning is
  preserved as an environment observation.
- The elapsed values are intentionally not compared: they are one-run
  observations with different device paths and no shared warmup protocol.

**Verification:**

- `uv run --group tensorflow ruff check .` — passed.
- `uv run --group tensorflow pytest` — 15 passed.
- `cd site && npm run build` — passed.
- `./scripts/build-book.sh` — produced the draft DOCX.
- Rendered the 22-page DOCX proof and inspected representative opening,
  Chapter 4, Chapter 5, and later-draft pages. The new content is readable;
  no clipping or overlap was found. The document remains a draft because most
  later chapters are still short skeletons.

**Decision:**

Milestone 2 is complete. A zero-error toy fixture is evidence that both
declared implementations learned that controlled task, not evidence of general
vision capability or framework speed. The introduction will be maintained as
the single reader-facing installation guide as each optional milestone becomes
real.

**Next task:**

- [ ] Start Milestone 3 with tokenizer inspection and a controlled
  pretrained-transformer inference fixture.
- [ ] Check storage before installing transformer/MLX dependencies and document
  the resulting installation path in Chapter 0.

---

### 2026-08-14 — Transformer inspection and local MLX-LM evidence

**What changed:**

- Added opt-in `transformers` and `mlx` dependency groups. MLX-LM 0.31 required
  Transformers 5, so the existing optional Transformers group was upgraded and
  the Chapter 6 CPU/MPS inference checks were rerun under Transformers 5.15.0.
- Added an inspectable pretrained-classifier experiment at
  `experiments/06-transformers/inspect_sentiment.py`, pure helpers/tests, a
  research note, and `benchmarks/03-transformers/README.md`.
- Added a local MLX-LM experiment at `experiments/07-mlx/run_local_model.py`,
  pure helpers/tests, a research note, and `benchmarks/04-mlx/README.md`.
- Expanded Chapters 6–7 after the evidence existed and updated the living
  setup chapter with the two optional installation paths.

**Recorded results and boundaries:**

- The DistilBERT sentiment experiment used model revision
  `714eb0fa89d2f80546fda750413ed43d93601a13`. Direct logits/softmax and the
  high-level pipeline agreed on both fixed inputs under MPS and CPU.
- Its 380.206 ms MPS and 120.787 ms CPU observations are deliberately **not** a
  speed comparison: they are one tiny, one-off workload without a normalized
  warmup or overhead boundary.
- The MLX-LM run used `mlx-community/Qwen2.5-0.5B-Instruct-4bit`, temperature
  zero, a four-token warm-up, and a 64-token cap. It recorded 342.260 generated
  tokens/s, Metal active/peak memory in bytes, MLX-LM peak memory in GiB, and
  process RSS as separate partial observations.
- The public Transformer and MLX model caches were about 256 MiB and 276 MiB
  respectively. They are local-only and untracked. The model completion was not
  quality-scored.

**Verification:**

- `uv run --group tensorflow --group transformers --group mlx ruff check .` — passed.
- `uv run --group tensorflow --group transformers --group mlx pytest` — 22 passed.
- `cd site && npm run build` — passed.
- `./scripts/build-book.sh` — produced the draft DOCX.
- Rendered the 27-page DOCX proof and inspected representative Chapter 6–7 and
  later-draft pages. No visible clipping or overlap was found; it remains a
  draft, not a release PDF.

**Decision:**

Milestone 3 is complete. Do not compare Chapter 6 classifier timing with
Chapter 7 generation timing, or either with another framework, until a common
generative workload and benchmark method exists.

**Next task:**

- [ ] Start Milestone 4 by adding local learned embeddings and metadata-rich
  ingestion over a frozen book-corpus fixture.
- [ ] Preserve deterministic retrieval tests while adding learned retrieval and
  grounded-answer evaluation.

---

### 2026-08-14 — Learned retrieval, grounded evidence, and Milestone 4 closure

**What changed:**

- Added the optional `embeddings` dependency group with Sentence Transformers
  5.7.0 and the local `sentence-transformers/all-MiniLM-L6-v2` encoder.
- Added `learned_retrieval.py`, which preserves the existing `Evidence`
  provenance record while locally encoding, normalizing, and ranking chunks.
  The deterministic hashed-vector implementation remains the fixture-friendly
  control; the interactive Chapter 8–9 scripts default to learned retrieval.
- Extended ingestion metadata with corpus kind, chapter identifier, and a
  stable experiment/benchmark record group. Saved indexes remain generated
  `.book-intelligence/` artifacts.
- Made both backends use an evidence-only answer formatter. The learned path
  returns only thresholded retrieved excerpts, repository paths, and any
  citation keys; it explicitly refuses empty or weak evidence.
- Added a frozen non-sensitive corpus and versioned evaluation runner covering
  evidence location, missing-evidence refusal, proposal/no-write behavior, and
  editorial review. It needs no model download or credential.
- Added the embeddings/RAG research note, Sentence-BERT citation, recorded
  local observation, optional installation instructions, and substantive
  Chapters 8–9.

**Recorded observation:**

- After confirming 53 GiB free storage, `uv sync --group embeddings` installed
  the optional dependency group. The public model loaded locally; the Hugging
  Face client emitted an unauthenticated-access warning, which is a rate-limit
  concern rather than a correctness error.
- Before the new Chapter 8–9 corpus material was added, the live search indexed
  95 chunks for the recorded benchmark-limitation query. Its top path was
  `benchmarks/03-transformers/README.md` at the script's rounded 0.556 score.
  Corpus count/ranking will change with tracked prose and records; this is not
  a quality, latency, memory, or accelerator claim.

**Verification:**

- `uv run --group tensorflow --group transformers --group mlx --group embeddings ruff check .` — passed.
- `uv run --group tensorflow --group transformers --group mlx --group embeddings pytest` — 29 passed.
- `uv run --group embeddings python evals/run_book_intelligence.py` — all four
  frozen cases passed.
- `cd site && npm run build` — passed after repository-only references were
  made print-safe paths rather than invalid Docusaurus links.
- `./scripts/build-book.sh` — produced the draft DOCX. Rendered 31 pages with
  the Lulu template and inspected the Chapter 8–9 pages; no clipping or overlap
  was observed. This remains a beta-draft layout, not a release PDF.

**Decision:**

Milestone 4 is complete. Do not describe the learned ranking as semantic truth,
retrieval quality, or hardware performance. Later generative, LangChain, and
LangGraph paths must consume the same evidence contract and retain the explicit
human-approval boundary before any source, Git, or external write.

**Next task:**

- [ ] Start Milestone 5 with an optional direct-SDK adapter and a LangChain
  structured-output path over identical retrieved evidence.
- [ ] Add LangGraph persistence, interrupt/resume, approval/rejection, and
  unavailable-model/API fallback tests before writing Chapters 10–13.
