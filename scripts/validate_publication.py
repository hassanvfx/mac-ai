"""Fail when a packaged review PDF no longer matches its generated contents."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "book/build"
MANIFEST = BUILD / "publication-manifest.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def locate_after_contents(page_texts: list[str], title: str) -> int | None:
    needle = re.sub(r"\s+", " ", title).replace("’", "'").replace("‘", "'").lower()
    for number, text in enumerate(page_texts[4:], start=5):
        if needle in text:
            return number
    return None


def main() -> None:
    if not MANIFEST.exists():
        raise SystemExit("Missing publication manifest; run make provisional-pdf first.")
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    interior = ROOT / data["interior_pdf"]
    if not interior.is_file() or digest(interior) != data["interior_sha256"]:
        raise SystemExit("Master PDF is missing or has changed since contents generation.")
    reader = PdfReader(str(interior))
    if len(reader.pages) != data["page_count"]:
        raise SystemExit("Master PDF page count differs from publication manifest.")
    page_texts = [
        re.sub(r"\s+", " ", page.extract_text() or "").replace("’", "'").replace("‘", "'").lower()
        for page in reader.pages
    ]
    if page_texts[0].strip():
        raise SystemExit("Master page 1 must be the visual title page, without a generated text title.")
    copyright_text = page_texts[1]
    if "copyright © 2026 hassan uriostegui" not in copyright_text or "isbn" not in copyright_text:
        raise SystemExit("Master page 2 must be the copyright page with the assigned ISBN.")
    if "to my friend arturo castelan" not in page_texts[2] or "and to zeus" not in page_texts[2]:
        raise SystemExit("Master page 3 must be the authored dedication page.")
    if "contents" not in page_texts[3]:
        raise SystemExit("Master page 4 must be the generated contents page.")
    for entry in data["toc_entries"]:
        actual = locate_after_contents(page_texts, entry.get("search_title", entry["title"]))
        if actual != entry["page"]:
            raise SystemExit(f"TOC mismatch for {entry['title']!r}: expected {entry['page']}, found {actual}")
    print("Publication validation passed: master page order and generated contents are synchronized.")


if __name__ == "__main__":
    main()
