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


def locate_after_contents(reader: PdfReader, title: str) -> int | None:
    needle = re.sub(r"\s+", " ", title).lower()
    for number, page in enumerate(reader.pages[2:], start=3):
        if needle in re.sub(r"\s+", " ", page.extract_text()).lower():
            return number
    return None


def main() -> None:
    if not MANIFEST.exists():
        raise SystemExit("Missing publication manifest; run make provisional-pdf first.")
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    interior = ROOT / data["interior_pdf"]
    online = ROOT / data.get("online_pdf", "")
    if not interior.is_file() or digest(interior) != data["interior_sha256"]:
        raise SystemExit("TOC-verified interior is missing or has changed since contents generation.")
    reader = PdfReader(str(interior))
    if len(reader.pages) != data["page_count"]:
        raise SystemExit("Interior page count differs from publication manifest.")
    for entry in data["toc_entries"]:
        actual = locate_after_contents(reader, entry.get("search_title", entry["title"]))
        if actual != entry["page"]:
            raise SystemExit(f"TOC mismatch for {entry['title']!r}: expected {entry['page']}, found {actual}")
    if not online.is_file() or digest(online) != data.get("online_sha256"):
        raise SystemExit("Online PDF is missing or differs from the TOC-verified publication manifest.")
    if len(PdfReader(str(online)).pages) != data.get("online_page_count"):
        raise SystemExit("Online PDF page count differs from publication manifest.")
    print("Publication validation passed: TOC, interior, and online PDF are synchronized.")


if __name__ == "__main__":
    main()
