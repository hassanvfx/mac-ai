"""Build a deterministic provisional Lulu full-bleed front-cover PDF.

The final back/spine/front cover is intentionally out of scope until Lulu
provides a template sized from the frozen interior page count.
"""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "book/cover/metadata-placeholder.yaml"
ART = ROOT / "book/assets/cover/rottweiler-art-plate.png"
BUILD = ROOT / "book/build"
OUTPUT = BUILD / "ai-from-tensors-to-agents-on-mac-silicon-front-cover-provisional.pdf"
RASTER = BUILD / "ai-from-tensors-to-agents-on-mac-silicon-front-cover-300ppi.png"
WIDTH_IN, HEIGHT_IN, DPI = 6.25, 9.25, 300
WIDTH_PT, HEIGHT_PT = WIDTH_IN * 72, HEIGHT_IN * 72


def read_metadata() -> dict[str, str]:
    data: dict[str, str] = {}
    for line in METADATA.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^([a-z_]+):\s*[\"']?(.*?)[\"']?\s*$", line)
        if match:
            data[match.group(1)] = match.group(2)
    return data


def fit_cover_art() -> None:
    """Create the review raster at the exact full-bleed pixel dimensions."""
    target = (round(WIDTH_IN * DPI), round(HEIGHT_IN * DPI))
    with Image.open(ART) as source:
        effective_ppi = min(source.width / WIDTH_IN, source.height / HEIGHT_IN)
        if effective_ppi < DPI:
            print(
                f"WARNING: approved source art is effectively {effective_ppi:.0f} ppi at full bleed; "
                "the rendered review raster is 300 ppi but the source must be replaced or professionally "
                "upscaled before a Lulu upload."
            )
        image = source.convert("RGB")
        scale = max(target[0] / image.width, target[1] / image.height)
        size = (round(image.width * scale), round(image.height * scale))
        image = image.resize(size, Image.Resampling.LANCZOS)
        left = (image.width - target[0]) // 2
        top = (image.height - target[1]) // 2
        image.crop((left, top, left + target[0], top + target[1])).save(
            RASTER, "PNG", dpi=(DPI, DPI), optimize=True
        )


def register_fonts() -> tuple[str, str]:
    regular = "/System/Library/Fonts/Supplemental/Georgia.ttf"
    bold = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
    if Path(regular).exists() and Path(bold).exists():
        pdfmetrics.registerFont(TTFont("CoverSerif", regular))
        pdfmetrics.registerFont(TTFont("CoverSerifBold", bold))
        return "CoverSerif", "CoverSerifBold"
    return "Times-Roman", "Times-Bold"


def main() -> None:
    if not ART.exists():
        raise SystemExit(f"Missing approved art plate: {ART}")
    BUILD.mkdir(parents=True, exist_ok=True)
    metadata = read_metadata()
    fit_cover_art()
    serif, bold = register_fonts()
    canvas = Canvas(str(OUTPUT), pagesize=(WIDTH_PT, HEIGHT_PT), pageCompression=1)
    canvas.drawImage(ImageReader(str(RASTER)), 0, 0, width=WIDTH_PT, height=HEIGHT_PT, mask="auto")

    # Full-bleed blue title panel; text is held 0.25 in inside trim for review.
    panel_h = 2.03 * 72
    canvas.setFillColor(HexColor("#123B73"))
    canvas.rect(0, 0, WIDTH_PT, panel_h, stroke=0, fill=1)
    canvas.setFillColor(HexColor("#F8F2E8"))
    canvas.setFont(bold, 21)
    canvas.drawString(0.38 * 72, panel_h - 0.46 * 72, "AI From Tensors to")
    canvas.drawString(0.38 * 72, panel_h - 0.78 * 72, "Agents on Mac Silicon")
    canvas.setFont(serif, 12.5)
    canvas.drawString(0.38 * 72, panel_h - 1.12 * 72, metadata["subtitle"])
    canvas.setFillColor(HexColor("#F8F2E8"))
    canvas.setFont(bold, 11)
    canvas.drawCentredString(WIDTH_PT / 2, 0.54 * 72, metadata["author"])
    canvas.setFont(serif, 8.5)
    canvas.drawCentredString(WIDTH_PT / 2, 0.29 * 72, metadata["imprint"])
    canvas.save()
    print(f"Wrote {OUTPUT}")
    print(f"Wrote {RASTER}")
    print("PROVISIONAL FRONT ONLY: no barcode, spine, or final Lulu template.")


if __name__ == "__main__":
    main()
