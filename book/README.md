# Book source

`chapters/` contains the only publishable chapter prose. The Docusaurus site
reads it directly. Pandoc combines the ordered files in `manuscript.yaml` into
the DOCX. Generated output belongs in `build/` and is never committed.

`assets/` contains versioned visual sources. Day 1 diagrams use editable SVG
masters and matching PNG derivatives: the PNG files are embedded by Pandoc for
reliable Word/DOCX output, while the SVGs remain the print-quality source of
truth for later edits.
