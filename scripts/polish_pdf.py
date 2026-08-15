"""Compose the single beta master PDF from the rendered interior and title art."""

from __future__ import annotations

import hashlib
import io
import json
import re
import sys
from pathlib import Path

from PIL import Image
from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas

ROOT = Path(__file__).resolve().parents[1]
COVER = ROOT / "book/assets/cover/pdf-online-cover.png"
BLUE = HexColor("#173F73")
INK = HexColor("#44515E")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def titles() -> list[tuple[str, str, bool]]:
    result: list[tuple[str, str, bool]] = []
    chapters = ROOT / "book" / "chapters"
    ordered = [
        chapters / "00-preamble-the-authors-toolkit.md",
        chapters / "00-introduction.md",
        *sorted(path for path in chapters.glob("[0-9][0-9]-*.md") if not path.name.startswith("00-")),
        *sorted((ROOT / "book" / "appendices").glob("*.md")),
    ]
    for path in ordered:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if path.name == "00-introduction.md":
            result.append(("Introduction and Setup", "What you are building", False))
            continue
        match = re.search(r"^title:\s*[\"']?(.+?)[\"']?\s*$", text, re.MULTILINE)
        display = match.group(1).strip('"') if match else None
        heading = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
        if heading:
            result.append((display or heading.group(1), heading.group(1), path.parent.name == "appendices"))
    return result


def locate(reader: PdfReader, title: str) -> int | None:
    needle = re.sub(r"\s+", " ", title).replace("’", "'").replace("‘", "'").lower()
    for number, page in enumerate(reader.pages, start=1):
        text = re.sub(r"\s+", " ", page.extract_text() or "").replace("’", "'").replace("‘", "'").lower()
        if needle in text:
            return number
    return None


def visual_title_page(width: float, height: float) -> PdfReader:
    """Fit the shared online cover without cropping or redesigning it."""
    with Image.open(COVER) as image:
        image_width, image_height = image.size
    scale = min(width / image_width, height / image_height)
    placed_width, placed_height = image_width * scale, image_height * scale
    stream = io.BytesIO()
    canvas = Canvas(stream, pagesize=(width, height))
    canvas.setFillColor(HexColor("#FFFFFF"))
    canvas.rect(0, 0, width, height, stroke=0, fill=1)
    canvas.drawImage(
        ImageReader(str(COVER)),
        (width - placed_width) / 2,
        (height - placed_height) / 2,
        width=placed_width,
        height=placed_height,
        mask="auto",
    )
    canvas.save()
    return PdfReader(io.BytesIO(stream.getvalue()))


def contents_page(width: float, height: float, entries: list[tuple[str, int | None, bool]]) -> PdfReader:
    stream = io.BytesIO()
    canvas = Canvas(stream, pagesize=(width, height))
    canvas.setFillColor(BLUE)
    canvas.rect(54, height - 72, width - 108, 3, stroke=0, fill=1)
    canvas.setFont("Times-Bold", 22)
    canvas.drawString(54, height - 112, "Contents")
    y = height - 146
    chapter_number = 0
    appendix_number = 0
    in_appendices = False
    for title, page, is_appendix in entries:
        if is_appendix and not in_appendices:
            y -= 8
            canvas.setFont("Times-Bold", 10)
            canvas.setFillColor(BLUE)
            canvas.drawString(54, y, "APPENDICES")
            y -= 18
            in_appendices = True
        canvas.setFont("Times-Roman", 9.5)
        canvas.setFillColor(HexColor("#202020"))
        if is_appendix:
            appendix_number += 1
            prefix = chr(64 + appendix_number)
        elif title == "The Author's Toolkit":
            prefix = "Pre"
        elif title == "Introduction and Setup":
            prefix = "Intro"
        else:
            chapter_number += 1
            prefix = f"{chapter_number:02d}"
        label = f"{prefix}  {title}"
        canvas.drawString(54, y, label[:76])
        if page is not None:
            number = str(page)
            canvas.setFont("Times-Bold", 9.5)
            canvas.drawRightString(width - 54, y, number)
            start = 54 + stringWidth(label, "Times-Roman", 9.5) + 8
            canvas.line(start, y - 2, width - 54 - stringWidth(number, "Times-Bold", 9.5) - 8, y - 2)
        y -= 17
    canvas.setFillColor(INK)
    canvas.setFont("Times-Italic", 8)
    canvas.drawString(54, 42, "Beta master edition · generated from the rendered manuscript")
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


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: polish_pdf.py rendered-interior.pdf beta-master.pdf")
    source, output = map(Path, sys.argv[1:])
    if not COVER.is_file():
        raise SystemExit(f"Missing shared title art: {COVER}")
    reader = PdfReader(str(source))
    if not reader.pages:
        raise SystemExit("Rendered interior contains no pages")
    width = float(reader.pages[0].mediabox.width)
    height = float(reader.pages[0].mediabox.height)
    source_entries = [(display, search, locate(reader, search), is_appendix) for display, search, is_appendix in titles()]
    toc_entries = [
        (title, page + 3 if page is not None else None, is_appendix)
        for title, _, page, is_appendix in source_entries
    ]
    first_content = locate(reader, "The Author's Toolkit") or 2

    writer = PdfWriter()
    writer.add_page(visual_title_page(width, height).pages[0])
    writer.add_page(reader.pages[0])  # copyright page
    writer.add_blank_page(width, height)  # courtesy page
    writer.add_page(contents_page(width, height, toc_entries).pages[0])
    for source_page, page in enumerate(reader.pages[1:], start=2):
        physical_page = source_page + 3
        if source_page >= first_content:
            overlay = footer(float(page.mediabox.width), float(page.mediabox.height), physical_page)
            page.merge_page(overlay.pages[0])
        writer.add_page(page)
    writer.add_metadata(reader.metadata or {})
    writer.add_metadata({"/Subject": "Beta master interior and online reading edition"})
    with output.open("wb") as handle:
        writer.write(handle)

    manifest = {
        "edition": "beta master interior and online reading edition",
        "source_pdf": str(source.relative_to(ROOT)),
        "source_sha256": digest(source),
        "interior_pdf": str(output.relative_to(ROOT)),
        "interior_sha256": digest(output),
        "page_count": len(writer.pages),
        "title_art": {
            "path": str(COVER.relative_to(ROOT)),
            "sha256": digest(COVER),
            "placement": "proportional fit on 6 x 9 in non-bleed page",
        },
        "toc_entries": [
            {"title": title, "search_title": search, "page": page}
            for (title, search, _, _), (_, page, _) in zip(source_entries, toc_entries, strict=True)
        ],
    }
    (output.parent / "publication-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote {output} with {len(writer.pages)} pages and generated contents.")


if __name__ == "__main__":
    main()
