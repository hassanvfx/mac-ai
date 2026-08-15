# Provisional cover package

`../assets/cover/rottweiler-art-plate.png` is the text-free approved visual
direction. `scripts/build-cover.py` turns it and `metadata-placeholder.yaml`
into a deterministic, full-bleed 6.25×9.25 in **front-cover review PDF**.
Typography is vector text in the PDF, not AI-generated lettering.

This is a style direction, not a Lulu upload cover. The build prints the
approved source art's effective resolution. The current generated art plate is
below 300 ppi at full-bleed size, so it is suitable for design review only and
must be replaced or professionally upscaled before a Lulu upload. Do not create
the final wraparound cover or barcode until the final interior PDF page count
and real ISBN/metadata are available. Lulu's downloaded cover template—not an
inferred spine calculation—controls the final back/spine/front dimensions and
barcode safe zone.

`pdf-online-cover.png` is the shared beta title plate. `make master-pdf` fits
it proportionally onto the first 6×9 interior page, then adds copyright,
one courtesy blank page, generated contents, and the manuscript. The same
`book/build/pdf-online.pdf` is the online reading edition and interior-layout
review master; it is not a Lulu upload file because LibreOffice produced it and
the current title art is below 300 ppi at full interior size.
