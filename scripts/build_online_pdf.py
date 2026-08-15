"""Create the screen-first PDF edition with its supplied standalone cover.

This deliberately does not create a Lulu upload file. Its first page preserves
the cover image's native portrait aspect ratio; the following pages are the
review manuscript PDF.
"""

from __future__ import annotations

import io
import hashlib
import json
from pathlib import Path

from PIL import Image
from pypdf import PdfReader, PdfWriter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

ROOT = Path(__file__).resolve().parents[1]
COVER = ROOT / "book/assets/cover/pdf-online-cover.png"
INTERIOR = ROOT / "book/build/ai-from-tensors-to-agents-on-mac-silicon-provisional.pdf"
OUTPUT = ROOT / "book/build/pdf-online.pdf"
POINTS_PER_INCH = 72
COVER_HEIGHT_IN = 9.5


def cover_pdf() -> bytes:
    with Image.open(COVER) as image:
        width_in = COVER_HEIGHT_IN * image.width / image.height
    stream = io.BytesIO()
    canvas = Canvas(stream, pagesize=(width_in * POINTS_PER_INCH, COVER_HEIGHT_IN * POINTS_PER_INCH))
    canvas.drawImage(
        ImageReader(str(COVER)),
        0,
        0,
        width=width_in * POINTS_PER_INCH,
        height=COVER_HEIGHT_IN * POINTS_PER_INCH,
        mask="auto",
    )
    canvas.save()
    return stream.getvalue()


def main() -> None:
    if not COVER.exists():
        raise SystemExit(f"Missing online cover: {COVER}")
    if not INTERIOR.exists():
        raise SystemExit(f"Missing provisional interior: {INTERIOR}; run make provisional-pdf first.")
    writer = PdfWriter()
    writer.append(PdfReader(io.BytesIO(cover_pdf())))
    writer.append(PdfReader(str(INTERIOR)))
    writer.add_metadata(
        {
            "/Title": "AI From Tensors to Agents on Mac Silicon",
            "/Author": "Hassan Uriostegui",
            "/Subject": "Online beta reading edition — not a Lulu print-upload file",
            "/Creator": "ai-on-mac deterministic online PDF build",
        }
    )
    with OUTPUT.open("wb") as destination:
        writer.write(destination)
    manifest_path = INTERIOR.parent / "publication-manifest.json"
    if not manifest_path.exists():
        raise SystemExit("Missing publication manifest; rebuild the provisional interior first.")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    interior_hash = hashlib.sha256(INTERIOR.read_bytes()).hexdigest()
    if manifest.get("interior_sha256") != interior_hash:
        raise SystemExit("Provisional interior differs from the TOC-verified publication manifest.")
    manifest["online_pdf"] = str(OUTPUT.relative_to(ROOT))
    manifest["online_sha256"] = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    manifest["online_page_count"] = len(writer.pages)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT} ({len(writer.pages)} pages; online edition, not Lulu-compliant).")


if __name__ == "__main__":
    main()
