"""Add a verified contents page and restrained running folios to a review PDF."""

from __future__ import annotations

import io
import hashlib
import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas

ROOT = Path(__file__).resolve().parents[1]
BLUE = HexColor("#173F73")
INK = HexColor("#44515E")


def titles() -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for pattern in ("book/chapters/*.md", "book/appendices/*.md"):
        for path in sorted(ROOT.glob(pattern)):
            text = path.read_text(encoding="utf-8")
            if path.name == "00-introduction.md":
                result.append(("Introduction and Setup", "What you are building"))
                continue
            match = re.search(r"^title:\s*[\"']?(.+?)[\"']?\s*$", text, re.MULTILINE)
            display = match.group(1).strip('"') if match else None
            heading = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
            if heading:
                result.append((display or heading.group(1), heading.group(1)))
    return result


def locate(reader: PdfReader, title: str) -> int | None:
    needle = re.sub(r"\s+", " ", title).lower()
    for number, page in enumerate(reader.pages, start=1):
        text = re.sub(r"\s+", " ", page.extract_text()).lower()
        if needle in text:
            return number
    return None


def contents_page(width: float, height: float, entries: list[tuple[str, int | None]]) -> PdfReader:
    stream = io.BytesIO()
    canvas = Canvas(stream, pagesize=(width, height))
    canvas.setFillColor(BLUE)
    canvas.rect(54, height - 72, width - 108, 3, stroke=0, fill=1)
    canvas.setFont("Times-Bold", 22)
    canvas.drawString(54, height - 112, "Contents")
    y = height - 146
    canvas.setStrokeColor(HexColor("#CFD7DF"))
    for index, (title, page) in enumerate(entries):
        if index == 15:
            y -= 8
            canvas.setFont("Times-Bold", 10)
            canvas.setFillColor(BLUE)
            canvas.drawString(54, y, "APPENDICES")
            y -= 18
        canvas.setFont("Times-Roman", 9.5)
        canvas.setFillColor(HexColor("#202020"))
        prefix = f"{index:02d}" if index < 15 else chr(64 + index - 14)
        label = f"{prefix}  {title}"
        canvas.drawString(54, y, label[:76])
        if page is not None:
            number = str(page + 1)  # this contents page is inserted after title page
            canvas.setFont("Times-Bold", 9.5)
            canvas.drawRightString(width - 54, y, number)
            start = 54 + stringWidth(label, "Times-Roman", 9.5) + 8
            canvas.line(start, y - 2, width - 54 - stringWidth(number, "Times-Bold", 9.5) - 8, y - 2)
        y -= 17
    canvas.setFillColor(INK)
    canvas.setFont("Times-Italic", 8)
    canvas.drawString(54, 42, "Online and review edition · generated from the rendered manuscript")
    canvas.save()
    return PdfReader(io.BytesIO(stream.getvalue()))


def footer(width: float, height: float, page_number: int) -> PdfReader:
    stream = io.BytesIO()
    canvas = Canvas(stream, pagesize=(width, height))
    canvas.setStrokeColor(HexColor("#CCD4DC"))
    canvas.line(54, 35, width - 54, 35)
    canvas.setFillColor(INK)
    canvas.setFont("Times-Roman", 7.5)
    canvas.drawString(54, 21, "AI From Tensors to Agents on Mac Silicon")
    canvas.drawRightString(width - 54, 21, str(page_number))
    canvas.save()
    return PdfReader(io.BytesIO(stream.getvalue()))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: polish_pdf.py input.pdf output.pdf")
    source, output = map(Path, sys.argv[1:])
    reader = PdfReader(str(source))
    entries = [(display, search, locate(reader, search)) for display, search in titles()]
    writer = PdfWriter()
    writer.add_page(reader.pages[0])
    width = float(reader.pages[0].mediabox.width)
    height = float(reader.pages[0].mediabox.height)
    writer.add_page(contents_page(width, height, [(title, page) for title, _, page in entries]).pages[0])
    for index, page in enumerate(reader.pages[1:], start=1):
        overlay = footer(float(page.mediabox.width), float(page.mediabox.height), index)
        page.merge_page(overlay.pages[0])
        writer.add_page(page)
    writer.add_metadata(reader.metadata or {})
    writer.add_metadata({"/Subject": "Beta reading PDF with generated contents and page folios"})
    with output.open("wb") as handle:
        writer.write(handle)
    toc_entries = [
        {"title": title, "search_title": search, "page": page + 1 if page is not None else None}
        for title, search, page in entries
    ]
    manifest = {
        "edition": "provisional review interior",
        "source_pdf": str(source.relative_to(ROOT)),
        "source_sha256": digest(source),
        "interior_pdf": str(output.relative_to(ROOT)),
        "interior_sha256": digest(output),
        "page_count": len(writer.pages),
        "toc_entries": toc_entries,
    }
    (output.parent / "publication-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote {output} with {len(writer.pages)} pages and generated contents.")


if __name__ == "__main__":
    main()
