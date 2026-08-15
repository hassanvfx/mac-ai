"""Basic Lulu-oriented PDF checks; this is not a substitute for proof review."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pypdf import PdfReader

POINTS_PER_INCH = 72
EXPECTED = (6 * POINTS_PER_INCH, 9 * POINTS_PER_INCH)


def page_size(page: object) -> tuple[float, float]:
    box = page.mediabox  # type: ignore[attr-defined]
    return float(box.width), float(box.height)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    args = parser.parse_args()
    reader = PdfReader(str(args.pdf))
    if not reader.pages:
        print("ERROR: PDF contains no pages")
        return 1
    failures = 0
    for number, page in enumerate(reader.pages, start=1):
        width, height = page_size(page)
        if (round(width), round(height)) != EXPECTED:
            print(f"ERROR: page {number} is {width / 72:.2f} x {height / 72:.2f} in, expected 6 x 9 in")
            failures += 1
    if failures:
        return 1
    print(f"PASS: {len(reader.pages)} single pages at 6 x 9 in.")
    print("Review fonts, images, margins, and Lulu proof manually.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
