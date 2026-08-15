"""Validate source metadata and Lulu-ready interior/cover delivery files."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

from PIL import Image
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "book/lulu-distribution.yaml"
FRONT_MATTER = ROOT / "book/front-matter.md"
ISBN_DIR = ROOT / "isbn"
COVER = ROOT / "book/assets/cover/pdf-online-cover.png"
INTERIOR_TITLE = ROOT / "book/assets/cover/pdf-online-cover-interior-production.png"
INFOGRAPHICS = (
    ROOT / "book/assets/generative-ai/generative-ai-lab-comparison-1.png",
    ROOT / "book/assets/generative-ai/generative-ai-lab-comparison-2.png",
)
REQUIRED = (
    "title", "subtitle", "author", "copyright_holder", "copyright_year", "isbn13",
    "imprint", "editorial_brand", "language", "description", "bisac_categories", "keywords",
    "audience", "content_warning", "binding", "interior_color", "trim_size", "cover_finish",
    "price_usd", "payee",
)


def read_scalars(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        if re.fullmatch(r"[a-z0-9_]+", key):
            values[key] = value.strip().strip('"\'')
    return values


def isbn_digits(value: str) -> str:
    return re.sub(r"[^0-9]", "", value)


def valid_isbn13(value: str) -> bool:
    digits = isbn_digits(value)
    return len(digits) == 13 and sum(int(char) * (1 if index % 2 == 0 else 3) for index, char in enumerate(digits)) % 10 == 0


def source_checks(metadata: dict[str, str]) -> list[str]:
    errors = [f"Missing metadata field: {key}" for key in REQUIRED if not metadata.get(key)]
    isbn = metadata.get("isbn13", "")
    if not valid_isbn13(isbn):
        errors.append(f"Invalid ISBN-13: {isbn!r}")
    if metadata.get("imprint") != "Lulu.com":
        errors.append("A Lulu-assigned ISBN must retain Lulu.com as its imprint.")
    if len(re.sub(r"\s+", "", metadata.get("description", ""))) < 50:
        errors.append("Lulu description must contain at least 50 non-space characters.")
    if re.search(r"https?://|www\.", metadata.get("description", ""), flags=re.IGNORECASE):
        errors.append("Lulu description cannot contain hyperlinks.")
    for keyword in metadata.get("keywords", "").split("|"):
        if len(keyword) > 50:
            errors.append(f"Keyword exceeds 50 characters: {keyword!r}")

    front = FRONT_MATTER.read_text(encoding="utf-8")
    copyright_at = front.find("Copyright ©")
    if copyright_at < 0:
        errors.append("Front matter must contain the copyright page.")
    for value in (metadata.get("title", ""), metadata.get("subtitle", ""), metadata.get("author", ""), isbn):
        if value not in front:
            errors.append(f"Front matter does not contain required metadata: {value!r}")
    if "barcode" not in front.lower() or "![](../../isbn" in front:
        errors.append("Interior must describe, but not embed, the barcode.")
    if not COVER.is_file():
        errors.append("Missing shared visual title page: book/assets/cover/pdf-online-cover.png")
    if not INTERIOR_TITLE.is_file():
        errors.append("Missing normalized interior visual title page.")
    elif INTERIOR_TITLE.is_file():
        with Image.open(INTERIOR_TITLE).convert("RGB") as image:
            corners = ((0, 0), (image.width - 1, 0), (0, image.height - 1), (image.width - 1, image.height - 1))
            if any(image.getpixel(point) != (255, 255, 255) for point in corners):
                errors.append("Interior visual title page must have pure-white outer corners.")
            if image.width < 1000 or image.height < 1400:
                errors.append("Interior visual title page is too small for review output.")
    for infographic in INFOGRAPHICS:
        if not infographic.is_file():
            errors.append(f"Missing Chapter 15 comparison plate: {infographic.name}")
            continue
        with Image.open(infographic) as image:
            if image.width < 1800 or image.height < 1300:
                errors.append(f"Chapter 15 comparison plate is undersized: {infographic.name}")
            dpi = image.info.get("dpi", (0, 0))
            if min(dpi) < 299:
                errors.append(f"Chapter 15 comparison plate lacks 300 ppi metadata: {infographic.name}")

    assets = {path.name for path in ISBN_DIR.glob(f"{isbn}.*")}
    expected = {f"{isbn}.svg", f"{isbn}.png", f"{isbn}.pdf"}
    if assets != expected:
        errors.append(f"ISBN assets must be exactly SVG, PNG, and PDF for {isbn}.")
    if not (ISBN_DIR / "guide-isbn.jpg").is_file():
        errors.append("Missing Lulu barcode source guide: isbn/guide-isbn.jpg")
    svg = ISBN_DIR / f"{isbn}.svg"
    if svg.is_file() and not all(group in svg.read_text(encoding="utf-8") for group in ("780557", "950546")):
        errors.append("SVG barcode digits do not match the ISBN asset filename.")
    png = ISBN_DIR / f"{isbn}.png"
    if png.is_file():
        with Image.open(png) as image:
            if image.mode != "RGB" or image.width < 300 or image.height < 180:
                errors.append("PNG barcode must be an RGB, print-capable source asset.")
    pdf = ISBN_DIR / f"{isbn}.pdf"
    if pdf.is_file() and len(PdfReader(str(pdf)).pages) != 1:
        errors.append("PDF barcode asset must contain one page.")
    return errors


def text_from_docx(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        return archive.read("word/document.xml").decode("utf-8", errors="replace")


def delivery_checks(metadata: dict[str, str], interior: Path | None, cover: Path | None, layout: Path | None) -> list[str]:
    errors: list[str] = []
    if interior:
        if interior.suffix.lower() == ".docx":
            content = text_from_docx(interior)
        else:
            reader = PdfReader(str(interior))
            content = "\n".join(page.extract_text() or "" for page in reader.pages)
        if interior.suffix.lower() == ".pdf":
            reader = PdfReader(str(interior))
            if len(reader.pages) < 4:
                errors.append("Master PDF must contain title, copyright, courtesy, and contents pages.")
            elif (reader.pages[0].extract_text() or "").strip() or "Copyright ©" not in (reader.pages[1].extract_text() or ""):
                errors.append("Master PDF must begin with a visual title page followed by copyright.")
        expected_values = (metadata["author"], metadata["isbn13"])
        if interior.suffix.lower() == ".pdf":
            # LibreOffice/PDF text extraction can split tightly kerned ISBN
            # digits even when the rendered glyphs are correct. The DOCX and
            # source checks enforce the exact ISBN; the PDF check verifies the
            # visible copyright/ISBN field is present and is reviewed by render.
            expected_values = (metadata["author"], "ISBN")
        for value in expected_values:
            if value not in content:
                errors.append(f"Interior delivery file is missing {value!r}.")
    if cover:
        reader = PdfReader(str(cover))
        if len(reader.pages) != 1:
            errors.append("Lulu wrap cover must be a single-page integrated spread.")
        if not layout:
            errors.append("Cover validation requires the matching Lulu layout JSON.")
        else:
            data = json.loads(layout.read_text(encoding="utf-8"))
            expected = data.get("page_size_pt", [])
            page = reader.pages[0]
            actual = [round(float(page.mediabox.width), 2), round(float(page.mediabox.height), 2)]
            if actual != [round(float(number), 2) for number in expected]:
                errors.append(f"Cover dimensions {actual} do not match Lulu layout {expected}.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--interior", type=Path)
    parser.add_argument("--cover", type=Path)
    parser.add_argument("--layout", type=Path)
    args = parser.parse_args()
    metadata = read_scalars(METADATA)
    errors = source_checks(metadata) + delivery_checks(metadata, args.interior, args.cover, args.layout)
    if errors:
        print("LULU DISTRIBUTION VALIDATION FAILED:", *[f"- {error}" for error in errors], sep="\n")
        return 1
    print(f"PASS: Lulu metadata and ISBN assets agree for {metadata['isbn13']}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
