---
title: Reproducible Publishing Protocol
---

# Reproducible Publishing Protocol

A print file is not a snapshot of whatever happened to be open on one laptop.
It is a build result with inputs, tools, decisions, and review evidence. This
appendix defines the small publishing protocol used for this book. It is useful
for a first proof, but it becomes essential after an editor, a proofreader, or
a printer finding changes the manuscript.

## What must be repeatable

There are four things to reproduce: the prose, the layout, the visual assets,
and the decision record. Markdown is the prose source. The committed Word
reference template is the layout authority. The cover artwork and its editable
metadata are visual inputs. The journal records why a particular release was
built and what review results mean.

Those layers answer different questions. A Git commit can prove which words
were used, but it cannot prove that a font embedded correctly. A PDF preflight
can prove page boxes and detect encryption, but it cannot decide whether a
diagram is understandable at print scale. A rendered-page review can expose a
widow or a clipped caption, but it cannot establish whether an ISBN belongs to
the work. Treating one check as a substitute for the others creates quiet,
expensive errors.

The release manifest closes part of that gap. It records hashes of the
manuscript metadata, front matter, Word template, cover metadata, and approved
art plate. If a later PDF differs, compare those hashes before guessing at what
changed. A different hash is not an error; it is a prompt to record an edition
decision.

## The build sequence

Start from a clean working tree. Run the editorial audit before creating a
document because a visually attractive PDF with a broken code link is still a
broken book. Then build the DOCX, normalize the non-bleed interior to the 6×9
trim, and render it to pages. Use the same order every time:

```bash
uv run ruff check .
uv run pytest
make audit-book
make validate-reader-bridge
make qrcodes
make book
make master-pdf
make preflight
make validate-publication
make release-manifest
```

The LibreOffice route produces one beta master at `book/build/pdf-online.pdf`.
It is both the online reading edition and the interior-layout review artifact:
visual title page, copyright/ISBN page, courtesy blank, generated contents, and
manuscript. The release candidate is produced by opening the same DOCX in
Microsoft Word on macOS and exporting to PDF with the final printer settings.
Never label the beta master as a release artifact.

The reader bridge is one synchronized publishing unit. Its manifest maps every
numbered chapter to the live `main`-branch lab URL, code command, expected
result, benchmark, and QR image. The print build derives each chapter-end lab
panel from that manifest; the course build derives its lab pages from the same
source. Update prose, command, benchmark, manifest, QR, Pages output, and PDF
in the same publication change.

After LibreOffice renders the body, the publishing step creates the one master
sequence: shared visual title page, copyright/ISBN page, one blank courtesy
page, contents, then the remaining manuscript. It locates chapter starts in
that same result, generates the contents from measured pagination, applies
folios only after the front matter, and records hashes and page counts in the
publication manifest. The future Microsoft Word/Lulu export must repeat this
render → derive contents → validate sequence; page numbers are never maintained
by hand.

The build script handles a subtle but important source-sharing detail. Chapter
files carry Docusaurus front matter for course navigation. Pandoc would treat
that same front matter as document metadata, allowing a chapter title to
silently replace the book title. The print build therefore makes temporary
copies with that front matter removed; it never edits the canonical chapters.
The web and print readers still receive the same prose.

## Inspecting the interior

Review pages in a sequence rather than scrolling randomly. Begin with the
shared visual title page, copyright, courtesy blank page, and contents page.
Confirm that the assigned ISBN matches the centralized Lulu distribution
metadata and that there is no accidental barcode in the interior. The barcode
belongs only in Lulu's final cover-template area. Then inspect every chapter
opener: it should have a clear title, breathing room, and a stable relationship
to the preceding chapter. Inspect every chapter ending for an isolated takeaway
heading, a lone line, or a next-step reference that points nowhere.

Next inspect the technical pages. Code should remain readable without forcing
the reader to rotate the book. Figure captions must stay with their figures.
Tables should not extend past the safe area. Citations should retain their
brackets and bibliography references. A high-resolution source image can still
look bad if Word scaled it badly, so judge the placed result rather than only
the file’s pixel dimensions.

Finally inspect the first and last printed pages. The first interior page is on
the right-hand side of a bound book, so front matter and chapter breaks should
respect odd/even sequencing. The final page should end deliberately, without a
half-empty bibliography fragment or a dangling heading. A small correction is
often enough: move a figure, revise a paragraph, or add a meaningful
cross-reference. Do not add filler just to solve a page-turn problem.

## Cover boundaries

The provisional cover is a front-cover review asset. It uses a 6.25×9.25 inch
full-bleed canvas, an original Rottweiler art plate, and vector title text. The
art direction can be approved before the manuscript is frozen, but the final
cover cannot. Lulu calculates the wrap width from the actual interior page
count and provides a template with the spine and barcode safe zones. A guessed
spine is a promise to trim incorrectly.

Keep two cover decisions separate. The first is editorial: is the title,
subtitle, illustration, author credit, and imprint communicating the book?
The second is production: does the final one-piece back/spine/front PDF match
the exact Lulu template, include safe margins and bleed, and contain the
assigned ISBN barcode in Lulu's designated safe area? The first can be repeated
locally. The second begins after the page count is frozen.

Do not reuse the provisional cover's placeholder metadata or make a barcode
outside Lulu's final template. The assigned ISBN is recorded in
`book/lulu-distribution.yaml` and printed as text in the interior; once Lulu
provides the final wrap template, regenerate the cover from that same metadata,
regenerate the manifest, and visually compare the results before upload.

## Handling a proof finding

Every proof finding gets one of four labels: content correction, layout
correction, production correction, or deferred decision. A content correction
changes canonical Markdown and may require source or experiment review. A
layout correction changes styles, the reference template, or build rules. A
production correction changes only release inputs such as an image profile or
cover template. A deferred decision is an intentional pause, such as choosing
an ISBN or approving a cover after a physical proof.

Record the label, affected pages, source files, and verification command in the
journal before committing. This makes a second proof explainable. If a page
number moved, the journal should show whether it moved because prose changed,
a figure changed, or a style changed. The goal is not bureaucratic paperwork;
it is to avoid “fixing” a symptom while reintroducing the original problem.

## Human approvals are not optional

Automation can build and inspect artifacts, but it cannot make publication
decisions. A human must approve the final text, any substantive visual change,
the real ISBN and metadata, the Lulu-selected product options, the upload, and
the proof order. The same principle appears in the Book Intelligence Assistant:
retrieval and critique can prepare evidence, while write and external actions
remain behind an approval boundary.

This division keeps the workflow fast without pretending that it is
autonomous. Build tools should make the next decision easier to inspect. They
should never obscure who made it.

## Release checklist

Before calling a PDF release-ready, answer yes to each question:

- Is the working tree clean apart from intentionally untracked build outputs?
- Do tests, audit, site build, and DOCX build pass from the documented setup?
- Does the final PDF use Word rather than the provisional LibreOffice route?
- Does preflight confirm the intended page size, single-page layout, and no
  security protection?
- Were fonts, image placement, safety margins, first/last pages, and every
  chapter opener inspected at print scale?
- Is the interior page count frozen before requesting the Lulu cover template?
- Do title, author, imprint, ISBN, and barcode agree across the interior,
  cover, Lulu form, and release manifest?
- Has a human approved the physical or digital proof?

If any answer is no, the project is still a beta or a review artifact. That is
not a failure. It is an accurate description of the state of the work.
