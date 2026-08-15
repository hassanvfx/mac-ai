"""Basic Lulu-oriented PDF checks; this is not a substitute for proof review."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pypdf import PdfReader

POINTS_PER_INCH = 72
SIZE_TOLERANCE_POINTS = 2.0  # LibreOffice review export may round Word twips.
INTERIOR = (6 * POINTS_PER_INCH, 9 * POINTS_PER_INCH)
FRONT_COVER = (6.25 * POINTS_PER_INCH, 9.25 * POINTS_PER_INCH)


def page_size(page: object) -> tuple[float, float]:
    box = page.mediabox  # type: ignore[attr-defined]
    return float(box.width), float(box.height)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--kind", choices=("interior", "front-cover", "wrap-cover"), default="interior")
    args = parser.parse_args()
    reader = PdfReader(str(args.pdf))
    if not reader.pages:
        print("ERROR: PDF contains no pages")
        return 1
    expected = INTERIOR if args.kind == "interior" else FRONT_COVER
    expected_label = "6 x 9" if args.kind == "interior" else "6.25 x 9.25"
    failures = 0
    for number, page in enumerate(reader.pages, start=1):
        width, height = page_size(page)
        if abs(width - expected[0]) > SIZE_TOLERANCE_POINTS or abs(height - expected[1]) > SIZE_TOLERANCE_POINTS:
            print(f"ERROR: page {number} is {width / 72:.2f} x {height / 72:.2f} in, expected {expected_label} in")
            failures += 1
    if args.kind == "interior" and len(reader.pages) < 2:
        print("ERROR: interior has fewer than two pages")
        failures += 1
    if args.kind != "interior" and len(reader.pages) != 1:
        print("ERROR: cover PDFs must be one single-page spread or front-cover page")
        failures += 1
    if reader.is_encrypted:
        print("ERROR: PDF is encrypted or password protected")
        failures += 1
    if failures:
        return 1
    print(f"PASS: {len(reader.pages)} single page(s) at {expected_label} in.")
    print("Manual gate: inspect embedded fonts, raster source resolution, safety margins, and every rendered page.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
