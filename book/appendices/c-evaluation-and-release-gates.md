# Appendix C: Evaluation and Release Gates

A beta is a defined set of artifacts and checks at a named revision. It is not
a promise that every future capability is measured. This appendix separates
four kinds of evidence: unit tests establish small contracts; fixture
evaluations establish reproducible provenance and refusal behavior; benchmark
records establish observations on a declared machine and workload; human review
establishes whether evidence supports a claim or a print page is acceptable.
None can substitute for the others.

## Code and evidence gate

Run the baseline checks from a synchronized environment:

```bash
uv sync --group dev
uv run ruff check .
uv run pytest
uv run python evals/run_reliability.py
make audit-book
```

The test suite covers numerical expectations, CPU fallback, framework and
transformer helpers, retrieval contracts, structured-output validation,
approval state, and workflow comparisons. The no-secret reliability runner
uses frozen fixtures to check source paths, citation keys, missing-evidence
refusal, deterministic ranking, and unsafe-link reporting. The book audit
checks canonical chapter sections, citations, links, runnable paths, research
references, and the declared word budget.

Read each failed gate as a routing signal. A broken code path means prose and
repository drifted. A missing citation means the claim needs evidence or a
narrower wording. A fixture failure means a provenance or policy invariant
changed. A word-budget failure means the manuscript is not at its planned beta
scope, even if every unit test is green. Do not replace a failed gate with a
manual claim that the system “mostly works.”

## Site gate

The Docusaurus site presents canonical Markdown; it is not a second manuscript.
Build it after source or navigation changes:

```bash
cd site
npm ci
npm run build
```

A successful build proves that the current site can be generated. It does not
publish anything. Publishing requires a chosen GitHub destination, deliberate
Pages configuration, a remote, and an intentional push. Those are release
decisions; neither an exercise nor an agent workflow should make them by
default. Inspect generated reading flow, diagrams, and code links before a
human release decision.

## Manuscript gate

Build the canonical Markdown with the versioned Lulu reference template:

```bash
./scripts/build-book.sh
```

This creates an ignored DOCX. It proves that citations, assets, and the
template can produce a Word document from the current source. It does not prove
that the PDF is printable. An interim DOCX render is valuable editorial
evidence, but the release path still requires a Microsoft Word PDF export on
macOS, PDF preflight, and visual inspection of every page at print scale.

Preflight the actual upload PDF for the 6×9 target, single-page layout,
embedded fonts, and detectable image-resolution concerns. Treat every issue as
a source/layout correction followed by another export, not a cosmetic exception
to the evidence trail. Generated DOCX/PDF artifacts remain untracked during
editing.

Final page count is a dependency: download the exact paperback cover template
only after it is frozen, because spine width depends on it. Cover artwork,
metadata, ISBN, upload, and proof ordering remain human choices. A local build
must never be described as a Lulu submission or approved proof.

## Optional provider-comparison gate

API-backed comparisons begin only when a provider, model, endpoint, and
evaluation protocol are chosen. Credentials are environment configuration,
never fixture, source, journal, or benchmark content. Fix the task set, corpus
revision, retrieved evidence, prompt/schema version, model/settings, retries,
and timing boundary. Record successes, refusals, malformed outputs, timeouts,
and configuration failures; score citation accuracy, plan completeness, review
coverage, latency, cost, and unsafe-action refusal under that same protocol.

The no-write rule survives every provider choice. A model may propose only from
supplied evidence. Validation rejects unapproved paths and restores the human
approval requirement. Any source, Git, journal, or external action needs a
separate, scoped approval.

## Release checklist

- The manuscript meets scope and passes its editorial/evidence audit.
- Python tests and deterministic evaluations have passing records.
- The site builds from canonical Markdown.
- DOCX builds through the committed template and receives layout inspection.
- The final Word PDF is preflighted and every page is reviewed.
- Release notes distinguish observations from unmeasured work.

After beta, freeze the text, copyedit, finalize page count, create the cover
from Lulu's exact template using the assigned ISBN metadata, and order a Lulu
proof. Proof findings create new tracked corrections and another preflight. A
successful build is necessary; an approved proof is the evidence needed before
publication.
