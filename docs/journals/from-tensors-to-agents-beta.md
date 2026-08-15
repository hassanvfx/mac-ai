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

- [x] Add direct-SDK and LangChain structured-output implementations over identical evidence.
- [x] Implement LangGraph state, checkpoint/resume, interrupt, approval, and rejection paths.
- [x] Compare deterministic retrieval, a single planner, and a researcher/critic/writer graph on book-maintenance tasks.
- [x] Write Chapters 10–13 from observed trade-offs.

**Gate:** No workflow can modify book/code/Git state before explicit human approval; state transitions and fallback paths are tested.

**Status:** Complete. The comparison is a no-network contract baseline, not a
model-quality or performance claim.

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

---

### 2026-08-14 — Milestone 5A structured planning comparison

**What changed:**

- Checked 46 GiB free before installing the optional `agents` dependency group:
  OpenAI Python SDK 2.54.0, LangChain 1.3.15, and LangChain OpenAI 1.5.1.
- Added direct OpenAI-compatible and LangChain structured-plan/review adapters
  in `src/from_tensors_to_agents/structured_planning.py`. Both take the same
  retrieved `Evidence` results and apply the same allowed-path and approval
  policy after parsing.
- Added Pydantic schemas, source-path filtering, empty-evidence warnings,
  malformed-LangChain handling, and configuration validation that occurs before
  any remote request. No adapter can write sources, Git state, or services.
- Added the no-network comparison experiment, research note, benchmark record,
  optional installation instructions, and substantive Chapter 10.

**Recorded observation and limits:**

- The default comparison uses fixture responses, not a provider. Both paths
  received the same retrieval result and returned the same allowed source path
  with approval required.
- API mode is intentionally unrun because no endpoint configuration was
  supplied. It requires `BOOK_INTELLIGENCE_API_KEY`,
  `BOOK_INTELLIGENCE_API_BASE`, and `BOOK_INTELLIGENCE_MODEL` in the process
  environment; no credentials were requested, displayed, or stored.
- This is a contract comparison, not a model-quality, price, latency, token,
  or provider-reliability benchmark.

**Verification:**

- `uv run --group tensorflow --group transformers --group mlx --group embeddings --group agents ruff check .` — passed.
- `uv run --group tensorflow --group transformers --group mlx --group embeddings --group agents pytest` — 36 passed.
- `uv run --group agents python experiments/10-systems/compare_structured_planning.py` — both fixture adapters returned the same allowed path and required approval.
- `cd site && npm run build` — passed.
- `./scripts/build-book.sh` — produced the draft DOCX. Rendered 32 pages and
  inspected the Chapter 10 opening; no visible clipping or overlap was found.

**Next task:**

- [ ] Continue Milestone 5 with LangGraph state, checkpoint/resume, interrupt,
  approval/rejection, and deterministic unavailable-model fallback.
- [ ] Write Chapters 11–12 only after those state transitions have tests and a
  recorded no-network experiment.

---

### 2026-08-14 — Milestone 5B LangGraph persistence and approval workflow

**What changed:**

- Added the optional SQLite LangGraph checkpointer and a deterministic,
  no-write proposal graph: plan → critique → approval interrupt → approved or
  rejected terminal state.
- Added durable `thread_id` checkpoints, `Command(resume=...)` approval and
  rejection, reopened-database resume tests, empty-evidence fallback, and a
  source-unchanged rejection test.
- Fixed the observed SQLite worker-thread error by opening the local demo
  connection with `check_same_thread=False`; the finding is recorded with its
  limitation rather than hidden.
- Added the runnable workflow, research/benchmark records, setup instructions,
  and substantive Chapters 11–12.

**Verification:**

- Full optional-group lint passed; `pytest` passed 39 tests.
- Both local workflow commands reached an interrupt, then ended respectively at
  `rejected_no_write` and `approved_no_write`.
- Docusaurus build passed. The Lulu-template DOCX built and rendered to 35
  pages; this remains a beta draft, not a release PDF.

**Next task:**

- [ ] Complete Milestone 5 with the deterministic/single-planner/
  researcher-critic-writer comparison and expand Chapter 13 from its evidence.

---

### 2026-08-15 — Milestone 5C workflow-shape comparison and closure

**What changed:**

- Added a frozen-fixture comparison of deterministic, single-planner, and
  researcher/critic/writer book-maintenance workflows.
- All workflows are intentionally deterministic control implementations: they
  share the same evidence contract, preserve source attribution, review the
  same editorial finding, require approval, and perform no writes.
- Added a runnable comparison, regression test, observation record, and
  substantive Chapter 13. The role pipeline emits a writer brief only; it does
  not gain file, Git, or service tools.

**Verification:**

- Full optional-group lint passed; `pytest` passed 40 tests.
- The comparison reported `True` for path attribution, review coverage,
  approval boundary, and no-write behavior for all three shapes.
- Docusaurus build passed; the Lulu-template DOCX built successfully. It is
  still a beta draft, pending the later Chapter 14/reliability and full-print
  production gates.

**Decision:**

Milestone 5 is complete. This does not establish that multiple agents improve
quality or latency: no remote model was run. It establishes the safe,
versioned control that any future model-backed comparison must match.

**Next task:**

- [ ] Start Milestone 6: evaluation traces, reliability policy, failure
  fixtures, Chapter 14, and beta release-gate audit.

---

### 2026-08-15 — Milestone 6 reliability baseline

- Added a no-secret reliability trace runner and regression test over the
  versioned fixture evaluation. Generated traces stay in ignored local state.
- Expanded Chapter 14 with the demonstrated reliability policy, known failures,
  and strict production boundaries.
- Full optional-group lint passed; 41 tests passed; reliability evaluation
  passed all four fixture cases.

**Next:** complete the broader beta audit: site/DOCX gates, chapter/citation
audit, and document remaining non-code release blockers (remote, Word PDF,
and Lulu proof).

### Beta audit — external release blockers

- No Git remote is configured; GitHub Pages placeholders cannot be finalized or
  published until the project owner chooses the destination.
- The generated DOCX exists, but Word export to the final PDF, PDF preflight,
  and a page-by-page release inspection remain macOS production tasks.
- Lulu cover-template download and proof ordering require finalized page count,
  cover/metadata choices, and explicit publication approval.

### 2026-08-15 — Editorial audit and Chapter 1 expansion

**What changed:**

- Added `scripts/audit_book.py` and `make audit-book`. The audit checks each
  canonical chapter for the required editorial sections, resolves citation
  keys against the shared BibTeX file, verifies relative Markdown links, and
  reports the manuscript word count against the 45,000–55,000 beta target.
- Added a regression test for the audit and documented its use in the README.
- Expanded Chapter 1 from a short outline into a 1,614-word teaching draft:
  shape tables, reshape-versus-permute reasoning, layer-boundary contracts,
  runnable-code linkage, reproducible observation practice, debugging
  invariants, and practical broadcasting alternatives.

**Verification:**

- `make audit-book` passed with no structural, citation, or link findings.
- `UV_CACHE_DIR=/private/tmp/ai-on-mac-uv-cache uv run pytest
  tests/test_book_audit.py` passed.
- The audit reports 10,620 manuscript words. This confirms the beta remains
  materially incomplete: the remaining chapters need the same substantive
  treatment before the 45,000–55,000-word target and new DOCX proof are
  meaningful.

**Next task:**

- [ ] Expand Chapter 2 with a worked loss/gradient-descent narrative, then
  continue the editorial pass chapter by chapter.
- [ ] Add a chapter-by-chapter diagram/evidence checklist to turn the
  word-count target into reviewable editorial work.

### 2026-08-15 — Chapter 2 editorial expansion

**What changed:**

- Expanded Chapter 2 from a short autograd example into a 1,465-word lesson on
  loss as a training measurement, local gradients, gradient-descent updates,
  learning-rate trade-offs, minibatch reduction, computation-graph lifetime,
  finite-difference checking, numerical failures, and optimizer alternatives.
- Linked the explanation to the committed Day 1 regression benchmark without
  converting its machine-specific result into a general performance claim.

**Verification:**

- `make audit-book` passed with no missing required sections, invalid citations,
  or unresolved relative links.
- Manuscript count is now 11,572 words against the 45,000–55,000 beta target.
- `git diff --check` passed.

**Next task:**

- [ ] Expand Chapter 3 around the existing tiny-network/MPS experiment, then
  add the first chapter-by-chapter diagram and evidence checklist.

### 2026-08-15 — Chapter 3 editorial expansion

**What changed:**

- Expanded Chapter 3 to 1,602 words. It now explains module/parameter roles,
  shape preservation through the tiny network, explicit device placement,
  training-loop details, reproducibility layers, safe MPS fallback, benchmark
  interpretation, timing synchronization, common device-split failures, and
  framework/trainer alternatives.
- Kept the recorded M4 Pro observation explicitly scoped to the versioned
  synthetic workload and benchmark record.

**Verification:**

- `make audit-book` passed with no structural, citation, or local-link findings.
- `git diff --check` passed.
- The audit reports 12,602 words. The chapter expansion is meaningful progress,
  but the manuscript still needs extensive drafts across Chapters 4–14.

**Next task:**

- [ ] Add the chapter-by-chapter evidence and diagram checklist, then expand
  Chapter 4 around the matched PyTorch/TensorFlow comparison.

### 2026-08-15 — Editorial completion matrix

**What changed:**

- Added `docs/editorial-completion-matrix.md`, the manuscript-wide acceptance
  record for all canonical chapters. It distinguishes the automated audit from
  the human checks still needed for explanatory depth, source/evidence scope,
  runnable companions, and print-quality diagrams.
- Verified every path named in the matrix against the tracked experiments,
  benchmarks, research notes, evaluation runner, and tests before recording it.

**Decision:**

The matrix labels Chapters 1–3 as **Draft expanded** only. No chapter is
described as final until its complete prose, evidence, visual, technical edit,
and generated-DOCX inspection have all happened.

**Next task:**

- [ ] Expand Chapter 4 around the matched PyTorch/TensorFlow comparison and
  turn its measured limitations into reader-facing guidance.

### 2026-08-15 — Chapter 4 editorial expansion (first pass)

**What changed:**

- Began the substantive Chapter 4 pass with framework-comparison methodology,
  PyTorch/Keras loop-boundary trade-offs, and the explicit channels-first to
  channels-last data-layout contract.

**Verification:**

- `make audit-book` passed with no structural, citation, or local-link findings.
- `git diff --check` passed; manuscript count is 12,839 words.

**Next task:**

- [ ] Continue Chapter 4 with evidence-table interpretation, timing limits,
  leakage failure analysis, and framework-selection guidance before starting
  Chapter 5.

### 2026-08-15 — Chapter 4 editorial expansion (complete first draft)

**What changed:**

- Completed the Chapter 4 first-draft pass: evaluation-contract reading,
  explicitly documented non-identical implementation choices, microbenchmark
  limits, CPU/MPS interpretation, data-leakage prevention, and framework
  selection guidance are now tied to the committed vision record.

**Verification:**

- `make audit-book` and `git diff --check` passed.
- Manuscript count is 13,199 words. Chapter 4 remains an expanded beta draft,
  pending later technical editing and DOCX inspection.

**Next task:**

- [ ] Expand Chapter 5 with the CNN's spatial-shape flow, split/metric
  discipline, and error-analysis method; add its print-quality architecture
  diagram after the prose identifies the exact concept the image must clarify.

### 2026-08-15 — Chapter 5 CNN visual and editorial expansion (first pass)

**What changed:**

- Added `book/assets/vision/cnn-feature-flow.svg`, an editable vector diagram
  for the exact `TinyConvNet` shape path: `(N, 1, 16, 16)` through feature maps,
  pooling, global average pooling, and three logits.
- Expanded Chapter 5's convolutional inductive-bias explanation, documented
  its real tensor transformations, and scoped pooling as a task-dependent
  architectural trade-off.

**Verification:**

- `make audit-book` passed, including the new local SVG link; `git diff --check`
  passed.
- Manuscript count is 13,445 words.

**Next task:**

- [ ] Complete Chapter 5's evaluation/error-analysis and augmentation sections,
  then render the next DOCX proof after several additional chapter expansions.

### 2026-08-15 — Chapter 5 evaluation pass and site-link correction

**What changed:**

- Completed the first Chapter 5 editorial pass with train/evaluation mode,
  confusion-matrix interpretation, controlled-difficulty experiments,
  incomplete error-analysis failure mode, and augmentation boundaries.
- Docusaurus identified that a Markdown link from Chapter 2 to a repository
  benchmark was interpreted as a missing site route. Replaced only that link
  with its exact code-form path, preserving the manuscript reference without
  asserting a non-existent page in the course site.

**Verification:**

- `make audit-book` passed at 13,815 words.
- `cd site && npm run build` passed after the link correction.
- The Docusaurus update-check permission warning is external configuration
  noise; it did not affect compilation or static-file generation.

**Next task:**

- [ ] Expand Chapter 6 around the tokenizer and fixed transformer-inference
  experiment, then add an editable tokenization/attention data-flow visual.

### 2026-08-15 — Chapter 6 transformer editorial expansion (first pass)

**What changed:**

- Expanded Chapter 6 with tokenizer-vocabulary contracts, the computational
  role and explanatory limits of self-attention, and a careful account of
  logits, softmax, label mappings, and the direct inspection baseline.
- The prose remains scoped to the fixed model revision and two-input experiment;
  it does not convert model score or one-off timing into a quality claim.

**Verification:**

- `make audit-book` and `git diff --check` passed.
- Manuscript count is 14,116 words.

**Next task:**

- [ ] Complete Chapter 6 with padding/truncation experiments, offline/cache
  failures, and alternatives; then add the tokenization/attention data-flow
  vector visual.

### 2026-08-15 — Chapter 6 transformer visual and padding boundary

**What changed:**

- Added `book/assets/transformers/tokenization-to-logits.svg`, an editable
  vector diagram of the inspected text → tokenizer → IDs/mask → contextual
  vectors → logits/label path.
- Expanded Chapter 6 with padding-mask behavior and linked the visual directly
  beside the input-contract explanation.

**Verification:**

- `make audit-book` passed at 14,205 words.
- `cd site && npm run build` passed; the new SVG resolves in the course site.

**Next task:**

- [ ] Finish Chapter 6's controlled truncation/cache-failure/alternative
  guidance, then begin Chapter 7's measured MLX and local-model discussion.

### 2026-08-15 — Chapter 7 MLX editorial expansion (first pass)

**What changed:**

- Began Chapter 7's substantive local-inference discussion: unified memory is
  distinguished from a capacity guarantee; the full model identifier and
  quantization are treated as experiment configuration; and model load,
  warm-up, and generation timing are separated into declared measurement
  boundaries.

**Verification:**

- `make audit-book` and `git diff --check` passed.
- Manuscript count is 14,431 words. No new performance or memory claim was
  introduced beyond the existing, scoped MLX benchmark record.

**Next task:**

- [ ] Complete Chapter 7 with controlled workload variations, output-quality
  boundaries, and local-versus-hosted alternatives; then expand Chapter 8's
  learned embedding and retrieval material.

### 2026-08-15 — Reliability fixture expansion

**What changed:**

- Added two deterministic Book Intelligence evaluation cases: grounded answers
  must include the real retrieved source path, and embedding retrieval must
  preserve the expected `reimers2019sentencebert` citation key.
- Extended the evaluator to execute those cases and strengthened the evaluation
  test to assert the new coverage is present.
- The first run exposed a real variable-shadowing error in the evaluator's
  citation branch; it was fixed before recording the result. This is useful
  evidence that the trace itself is exercised, not merely declared.

**Verification:**

- Targeted evaluation and reliability tests passed.
- `evals/run_reliability.py` passed all 6 cases with no model or credentials.
- No source, Git, or external write is authorized by the suite.

**Next task:**

- [ ] Add further failure fixtures for empty corpus and invalid/missing source
  configuration, then continue the Chapter 7 and Chapter 8 editorial passes.

### 2026-08-15 — Empty-corpus and path-boundary failure fixtures

**What changed:**

- Added a deterministic empty-corpus regression: indexing yields no evidence and
  grounded answering refuses the request.
- Hardened corpus review so a Markdown link resolving outside the configured
  corpus is reported as an escaping link, even if that external file exists.
- Added a regression fixture for that path-boundary failure.

**Verification:**

- Book Intelligence, evaluation, and reliability targeted tests passed: 11
  tests total.
- `git diff --check` passed.

**Next task:**

- [ ] Continue Chapter 7's remaining workload/quality boundaries and expand
  Chapter 8's embedding/retrieval teaching prose and visual.

### 2026-08-15 — Chapter 8 retrieval boundary (start)

- Began Chapter 8's editorial pass by making its central safety distinction
  explicit: similarity ranks candidate evidence; it does not prove an answer.
  Provenance must remain available for reader inspection.
- Next: expand chunking, learned-index provenance, retrieval failures, and the
  embedding/retrieval visual.

### 2026-08-15 — DOCX SVG conversion finding

- Rebuilt the manuscript DOCX. Pandoc completed, but warned that it cannot
  convert the new editable SVG diagrams because `rsvg-convert` is unavailable.
- Added the requirement to the living installation chapter: SVG is canonical;
  a rasterizer or source-derived print PNG is required before a visually
  complete DOCX proof can be accepted.
- No PDF or print-ready visual claim is made from this build.

### 2026-08-15 — DOCX SVG conversion resolved and proof rendered

- Checked free space (44 GiB) and installed Homebrew `librsvg`; `rsvg-convert`
  2.62.3 is now available for Pandoc.
- Rebuilt the DOCX with no SVG conversion warnings. Rendered the proof to PNG
  pages and visually inspected normal prose and the CNN diagram page: both are
  clean, readable, and free of clipping in the rendered proof.
- The current proof is 53 pages. This resolves the diagram-conversion blocker,
  not the manuscript-length target or final Word-PDF production gate.

### 2026-08-15 — Chapter 9 grounding boundary (start)

- Began the RAG chapter expansion by separating retrieval, grounding, and
  generation. The evidence-only control remains the basis for later fluent
  answers, rather than treating fluent prose as proof.
- Added stale-index guidance: indexes are caches rebuilt from tracked files;
  rendered evidence paths must remain inside the corpus and weak retrieval must
  fail closed.

### 2026-08-15 — Chapter 10 adapter contract (start)

- Began the structured-systems editorial pass: direct and framework adapters
  must share retrieved evidence and either return validated, source-scoped
  output or expose their failure; typed output is never permission to act.

### 2026-08-15 — Chapter 11 persisted-state audit boundary

- Clarified that persisted workflow state records considered evidence, proposed
  plan, pause reason, and human decision—not merely enough data to resume code.

### 2026-08-15 — Chapter 12 approval-scope expansion

**What changed:**

- Expanded the human-control chapter from a short outline to a 1,164-word
  first editorial pass. It now distinguishes a durable checkpoint from
  canonical repository evidence and makes approval specific to one reviewable
  proposal rather than standing permission.
- Documented rejection, stale evidence, checkpoint retention, idempotent
  pre-interrupt work, and the division between workflow history and Git
  history. The chapter points readers to the executable approval workflow and
  its reopen/resume/no-write tests.
- Made the DOCX SVG dependency directly reproducible in the living setup
  chapter with the macOS Homebrew `librsvg` install and verification commands.

**Verification:**

- `make audit-book` passed; the manuscript is now 15,420 words, still below
  the 45,000–55,000 beta target.
- `uv run pytest tests/test_approval_workflow.py` passed (3 tests), including
  reject/no-write, persisted resume, and empty-evidence fallback.
- `git diff --check` passed.

**Next task:**

- [ ] Expand Chapter 13 with a controlled comparison design for deterministic,
  single-planner, and researcher/critic/writer workflows; link its claims to
  the versioned evaluation fixtures before making capability claims.

### 2026-08-15 — Chapter 13 workflow-comparison expansion

**What changed:**

- Expanded Chapter 13 to a 1,100-word first editorial pass and added an
  editable vector diagram, `book/assets/agents/workflow-shapes.svg`. It shows
  deterministic, single-planner, and researcher/critic/writer routes converging
  on one evidence, no-write, and human-approval contract.
- Defined the frozen cosine-similarity maintenance fixture as a contract
  comparison rather than a model-quality claim. The prose documents what a
  future API-backed evaluation must hold constant and score before claiming an
  extra role is worthwhile.
- Added explicit guidance on role theatre, handoff inputs/outputs, rules-based
  editorial checks, and why a writer remains a read-only proposal producer.

**Verification:**

- `make audit-book` passed; the manuscript is now 16,131 words, still below
  the 45,000–55,000 beta target.
- `uv run pytest tests/test_workflow_comparison.py` passed.
- The runnable comparison reported `True` for path attribution, review
  coverage, approval boundary, and no-write for all three workflow shapes.
- Docusaurus production build and the Pandoc DOCX build both passed; the latter
  embedded the new SVG without an SVG conversion warning. `git diff --check`
  passed.

**Next task:**

- [ ] Expand Chapter 14 with the reliability policy, evaluation taxonomy,
  trace boundaries, and release-gate interpretation; then revisit Chapters
  8–11, whose prose remains materially shorter than the intended manuscript
  budget.

### 2026-08-15 — Chapter 14 reliability-policy expansion

**What changed:**

- Expanded Chapter 14 to a 1,176-word first editorial pass. It now defines
  trust as six narrow, testable repository contracts rather than an unprovable
  claim about general model correctness.
- Documented the fixture corpus, generated local trace, provenance chain,
  deterministic-versus-model-dependent boundary, evaluation-record protocol,
  observed failure modes, and the distinct roles of audit, tests, site build,
  and DOCX build.
- Added operational guidance for interpreting a trace, investigating a failed
  case, and designing a controlled API-backed evaluation without inventing
  latency, cost, or quality results.

**Verification:**

- `make audit-book` passed; manuscript count is 16,902 words, still below the
  45,000–55,000 beta target.
- `uv run --group agents python evals/run_reliability.py` passed all 6 cases
  and wrote only ignored local trace files.
- Targeted Book Intelligence evaluation/reliability tests passed: 11 tests.
- `git diff --check` passed.

**Next task:**

- [ ] Expand Chapter 8 with chunk boundaries, deterministic-versus-learned
  embedding trade-offs, retrieval-quality checks, and an editable visual; then
  continue Chapters 9–11 to bring the agent half of the manuscript toward its
  page budget.

### 2026-08-15 — Chapter 8 retrieval-contract expansion

**What changed:**

- Expanded Chapter 8 to a 1,265-word first editorial pass, covering cosine
  interpretation, paragraph chunking trade-offs, chunk-scoped metadata, the
  stable hashed-vector control, and the shared `Evidence` contract used by
  learned retrieval.
- Added a concrete evaluation-design boundary: compare acceptable and
  misleading paths across declared corpus/model/chunk revisions, and keep
  retrieval recall distinct from grounded-answer attribution.
- Documented cache staleness and corpus-boundary validation, plus practical
  lexical, hybrid, and persistent-store alternatives.

**Verification:**

- `make audit-book` passed; manuscript count is 17,454 words, still below the
  45,000–55,000 beta target.
- Targeted retrieval and evaluation tests passed: 14 tests total.
- `git diff --check` passed.

**Next task:**

- [ ] Expand Chapter 9's grounded-answer material: chunk-to-answer citation
  mechanics, retrieval failures, context budgeting, and the distinction between
  repository evidence and a generative response.

### 2026-08-15 — Chapter 9 grounded-RAG expansion

**What changed:**

- Expanded Chapter 9 to a 1,379-word first editorial pass. It now separates
  retrieved context from model weights, defines the reader-visible evidence
  packet, and documents threshold and context-budget limits without treating
  either as a truth guarantee.
- Added deterministic failure/evaluation guidance for empty inputs, weak
  neighbors, citations, path resolution, retrieval recall, and grounded-answer
  support. It also calls out citation laundering and repository text that must
  never become workflow instructions.
- Clarified when curated links or manual search are the better option, and the
  required primary-source boundary for high-stakes external questions.

**Verification:**

- `make audit-book` passed; manuscript count is 18,085 words, still below the
  45,000–55,000 beta target.
- Targeted Book Intelligence retrieval/evaluation tests passed: 14 tests.
- The deterministic grounded-answer exercise ran and returned only labeled
  repository excerpts; it did not generate a free-form answer.
- `git diff --check` passed.

**Next task:**

- [ ] Expand Chapter 10's direct-SDK and structured-output comparison: schema
  validation, adapter failures, configuration boundaries, and the no-write plan
  contract.

### 2026-08-15 — Chapter 10 structured-adapter expansion

**What changed:**

- Expanded Chapter 10 to a 1,202-word first editorial pass. It now treats a
  schema as a data contract rather than a truth or permission contract, and
  documents the fair-context requirement for comparing direct and composed
  adapters.
- Described concrete normalization: allow-listed evidence paths, caller-owned
  objectives, cleared steps without evidence, forced approval, visible parse
  failures, and environment-only optional API configuration.
- Added future controlled-comparison conditions, parser-recovery limits, and
  a practical choice rule for direct SDK versus orchestration abstraction.

**Verification:**

- `make audit-book` passed; manuscript count is 18,662 words, still below the
  45,000–55,000 beta target.
- `uv run pytest tests/test_structured_planning.py` passed (7 tests).
- The no-network adapter comparison preserved the same source path for both
  adapters and reported approval required.
- `git diff --check` passed.

**Next task:**

- [ ] Expand Chapter 11's state-machine material: explicit state data,
  transition design, deterministic fallback, trace interpretation, and why
  state graphs do not by themselves create safe agents.

### 2026-08-15 — Chapter 11 state-machine expansion

**What changed:**

- Expanded Chapter 11 to a 1,180-word first editorial pass. It now explains
  the graph's typed state, transition-table design, deterministic fallback,
  checkpoint scope, thread-ID lifecycle, and the distinct approval/rejection
  terminal states.
- Added operational guidance on inspecting an interrupt payload, idempotent
  pre-interrupt work, replay hazards, and why a future write needs its own
  scoped approval and reviewable diff.
- Positioned pull requests as a valid human-operated graph and clarified when
  a persisted graph reduces real work versus merely adding abstraction.

**Verification:**

- `make audit-book` passed; manuscript count is 19,283 words, still below the
  45,000–55,000 beta target.
- `uv run pytest tests/test_approval_workflow.py` passed (3 tests).
- The runnable workflow paused with the explicit no-action message and resumed
  to `rejected_no_write`; its SQLite checkpoint remained under ignored local
  state.
- `git diff --check` passed.

**Next task:**

- [ ] Begin a second editorial pass on the shortest chapters (7, 4, 5, 6),
  adding missing worked examples, evidence interpretation, and diagrams while
  keeping performance claims tied to benchmark records.

### 2026-08-15 — Chapter 7 local-inference second pass

**What changed:**

- Expanded Chapter 7 to 1,338 words. It now separates disk/download capacity
  from unified-memory capacity, rules out invalid cross-task runtime rankings,
  and explains the declared load, warm-up, generation, RSS, Metal, and MLX-LM
  measurement boundaries.
- Added quality-boundary guidance for the fixed prompt, a reproducible local
  failure taxonomy, and clearer task-specific/local/remote runtime alternatives.
- Retained the existing single-workload MLX-LM observation without adding any
  unmeasured latency, capacity, or quality claims.

**Verification:**

- `make audit-book` passed; manuscript count is 19,720 words, still below the
  45,000–55,000 beta target.
- `uv run pytest tests/test_local_models.py` passed (3 tests).
- `git diff --check` passed.

**Next task:**

- [ ] Expand Chapter 6's transformer inference material with an explicit
  token-to-logit walkthrough, prompt/context failure cases, and model/pipeline
  interpretation boundaries.

### 2026-08-15 — Chapter 6 transformer-inference second pass

**What changed:**

- Expanded Chapter 6 to 1,605 words. It now explains the attention operation
  without treating attention as explanation, defines the shared manual/pipeline
  input contract, and separates softmax label scores from calibration or truth.
- Added a controlled interface-change procedure, context-window/truncation and
  label-map failure modes, and clearer classifier/instruction-model/rules-based
  alternatives.
- Retained the recorded MPS/CPU values as a deliberately non-comparable tiny
  workload observation; no new performance or model-quality claim was added.

**Verification:**

- `make audit-book` passed; manuscript count is 20,198 words, still below the
  45,000–55,000 beta target.
- `uv run pytest tests/test_transformers_helpers.py` passed (4 tests).
- `git diff --check` passed.

**Next task:**

- [ ] Begin the Chapter 4 framework-comparison second pass, making data/split/
  metric equivalence, backend/device limits, and what the measured comparison
  does not establish more concrete.

### 2026-08-15 — Chapter 4 framework-comparison second pass

**What changed:**

- Expanded Chapter 4 to 1,644 words. It now separates shared task invariants
  from framework/runtime choices, makes the confusion matrix and empty error
  list interpretable, and defines task-level topology equivalence without
  requiring identical parameters.
- Added explicit reproducibility limits across kernels/versions/devices and a
  two-report design: establish correctness first, then run an independently
  declared performance protocol if one is needed.
- No measured result was changed or reinterpreted as framework-speed evidence.

**Verification:**

- `make audit-book` passed; manuscript count is 20,562 words, still below the
  45,000–55,000 beta target.
- Vision and TensorFlow fixture tests passed: 4 tests.
- `git diff --check` passed.

**Next task:**

- [ ] Expand Chapter 5's CNN learning material with receptive-field intuition,
  train/validation/test roles, error-analysis procedure, and controlled-
  difficulty fixture design.

### 2026-08-15 — Chapter 5 CNN second pass

**What changed:**

- Expanded Chapter 5 to 1,630 words. It now explains receptive-field growth,
  global pooling as a task hypothesis, cross-entropy versus accuracy, and the
  distinct roles of training, validation, and held-out test data.
- Added a controlled-difficulty experiment protocol and explains why separate
  fixture seeds still do not establish deployment robustness.
- Retained the existing zero-error fixture observation without treating it as
  real-world image-performance evidence.

**Verification:**

- `make audit-book` passed; manuscript count is 20,931 words, still below the
  45,000–55,000 beta target.
- `uv run pytest tests/test_vision.py` passed (3 tests).
- `git diff --check` passed.

**Next task:**

- [ ] Complete a cross-chapter technical-editing pass for Chapters 1–7 and
  Chapters 8–14, then strengthen the audit to enforce runnable code/research
  evidence links before another full site and DOCX proof build.

### 2026-08-15 — Repository-path editorial audit hardening

**What changed:**

- Extended `scripts/audit_book.py` so inline-code references to repository
  files below `experiments/`, `src/`, `benchmarks/`, and `research/` must
  resolve to a tracked file, in addition to existing heading, BibTeX, and
  Markdown-link checks.
- The new check exposed a misleading fixture-only research path in Chapter 13;
  the prose now describes it as a fixture expectation rather than presenting it
  as a root-repository research file.

**Verification:**

- `make audit-book` passed all chapters with the stricter path check; current
  manuscript count is 20,932 words, still below the 45,000–55,000 beta target.
- `uv run pytest tests/test_book_audit.py` passed.
- `git diff --check` passed.

**Next task:**

- [ ] Add explicit per-chapter research/evidence references where a chapter
  currently relies only on a citation, then run a full technical consistency
  audit and build a fresh site/DOCX proof.

### 2026-08-15 — Chapter-level evidence trails

**What changed:**

- Added an `Evidence trail` section to every substantive chapter. Each points
  to its working research note plus the relevant runnable experiment, benchmark,
  or deterministic evaluation artifact.
- Extended the editorial audit with the expected research-note mapping for
  Chapters 1–14, so a later prose edit cannot silently remove the reader's
  route from a lesson to its evidence base.

**Verification:**

- `make audit-book` passed all mandatory sections, citations, Markdown links,
  inline repository paths, and chapter research-evidence references. Manuscript
  count is 21,333 words, still below the 45,000–55,000 beta target.
- `uv run pytest tests/test_book_audit.py` passed.
- `git diff --check` passed.

**Next task:**

- [ ] Run the full Python/site/DOCX gates after this cross-chapter update,
  render a fresh DOCX proof for visual inspection, then prioritize a larger
  third editorial pass to close the remaining manuscript-length gap.

### 2026-08-15 — Full gate run and refreshed DOCX proof

**What changed:**

- Ran the full Python, editorial, site, and DOCX gates after the cross-chapter
  evidence-trail update.
- Rendered the DOCX proof to PNG pages for layout inspection. This exposed a
  Chapter 1 Markdown table that broke across the print layout and detached its
  cell text. Replaced it with an equivalent compact definition-list paragraph;
  the repaired page renders cleanly.

**Verification:**

- Ruff passed; all 44 Python tests passed; `make audit-book` passed; and the
  Docusaurus production build passed. The harmless Docusaurus update-check
  permissions warning did not affect the generated static site.
- Pandoc built `book/build/from-tensors-to-agents.docx` with SVG conversion
  available. The rendered proof is 75 pages. Sampled front matter, prose,
  code, diagrams, workflow pages, and bibliography were legible and unclipped;
  the Chapter 1 table defect was fixed and re-rendered successfully.
- This is an interim DOCX proof, not a Word-exported final PDF or a 180–220
  page manuscript. No final-PDF, Lulu, or release claim is made.

**Next task:**

- [ ] Plan and execute the larger third editorial pass needed to move from the
  current 21k-word/75-page proof toward the 45k–55k-word/180–220-page target;
  retain the full gate suite after each substantial batch.

### 2026-08-15 — Chapter 1 third editorial pass

**What changed:**

- Expanded Chapter 1 from 1,671 to 2,439 words with a worked axis audit:
  permutation versus reshape, image and language-model axis contracts,
  dtype/device boundaries, matrix-multiplication preservation of leading axes,
  and memory implications of materializing broadcasts.
- Added an experiment design that distinguishes an incompatible broadcast from
  a valid but semantically wrong `(2, 1)` broadcast, plus a repeatable method
  for turning a shape error into an axis comparison.

**Verification:**

- `make audit-book` passed; manuscript count is 22,127 words, still below the
  45,000–55,000 beta target.
- `uv run pytest tests/test_day1.py` passed (6 tests).
- The Chapter 1 broadcasting example ran and printed the expected shapes and
  values. `git diff --check` passed.

**Next task:**

- [ ] Give Chapter 2 the same third-pass treatment: derive the scalar gradient,
  connect it to vector/matrix gradients, show finite-difference checks and loss
  reduction behavior, and keep the claims tied to the runnable autograd lesson.

### 2026-08-15 — Chapter 2 third editorial pass

**What changed:**

- Expanded Chapter 2 from 1,503 to 2,078 words with a chain-rule derivation of
  the scalar result, vector-gradient interpretation, batch reduction/gradient
  scaling, and local-gradient limits.
- Added concrete finite-difference epsilon guidance, a sum-versus-mean
  experiment, and a detachment/logging boundary that preserves autograd
  correctness.

**Verification:**

- `make audit-book` passed; manuscript count is 22,702 words, still below the
  45,000–55,000 beta target.
- `uv run pytest tests/test_day1.py` passed (6 tests).
- The autograd experiment printed the expected prediction `6.0`, loss `16.0`,
  and gradient `-16.0`. `git diff --check` passed.

**Next task:**

- [ ] Give Chapter 3 a third-pass expansion: trace the tiny regressor's data,
  parameter, loss, optimizer, and device contracts; then connect observed loss
  curves to held-out evaluation boundaries without making speed claims.
