"""Build deterministic print-ready art derived from versioned source assets."""

from __future__ import annotations

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
COVER_SOURCE = ROOT / "book/assets/cover/pdf-online-cover.png"
INTERIOR_COVER = ROOT / "book/assets/cover/pdf-online-cover-interior-white.png"
PRODUCTION_INTERIOR_COVER = ROOT / "book/assets/cover/pdf-online-cover-interior-production.png"
CLINEFLOW_SOURCE = ROOT / "book/assets/tooling/clineflow-open-knowledge-format.png"
CLINEFLOW_PRINT = ROOT / "book/assets/tooling/clineflow-open-knowledge-format-print.png"
FLOW_SOURCE = ROOT / "book/assets/generative-ai/generative-ai-lab-flow-imagegen2.png"
INFOGRAPHIC_ONE = ROOT / "book/assets/generative-ai/generative-ai-lab-comparison-1.png"
INFOGRAPHIC_TWO = ROOT / "book/assets/generative-ai/generative-ai-lab-comparison-2.png"
FONT_DIR = Path("/System/Library/Fonts/Supplemental")

NAVY = "#12345C"
BLUE = "#1E5BA8"
GOLD = "#B88A35"
INK = "#1F2933"
MIST = "#EDF3F8"
WARM_WHITE = "#FCFDFE"


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_DIR / name, size)


def normalize_interior_cover() -> None:
    """Whiten neutral paper while preserving the cover illustration and text."""
    source = Image.open(COVER_SOURCE).convert("RGB")
    pixels = source.load()
    for y in range(source.height):
        for x in range(source.width):
            red, green, blue = pixels[x, y]
            value = (red + green + blue) / 3
            saturation = max(red, green, blue) - min(red, green, blue)
            if value >= 230 and saturation <= 26:
                pixels[x, y] = (255, 255, 255)
    INTERIOR_COVER.parent.mkdir(parents=True, exist_ok=True)
    source.save(INTERIOR_COVER, dpi=(300, 300))
    # Mechanical 300 ppi upscale: it preserves the approved composition exactly,
    # but proof review remains required before a final print declaration.
    source.resize((1800, 2700), Image.Resampling.LANCZOS).save(PRODUCTION_INTERIOR_COVER, dpi=(300, 300))


def make_clineflow_print_variant() -> None:
    """Rebuild the web poster's message as a low-ink, print-safe plate."""
    width, height = Image.open(CLINEFLOW_SOURCE).size
    output = Image.new("RGB", (width, height), "#FFFFFF")
    draw = ImageDraw.Draw(output)
    title = font("Arial Bold.ttf", 72)
    subtitle = font("Arial.ttf", 32)
    small = font("Arial.ttf", 22)
    tiny = font("Arial.ttf", 18)
    draw.rectangle((72, 56, width - 72, 69), fill=BLUE)
    draw.text((92, 112), "Persistent context,", fill=NAVY, font=title)
    draw.text((92, 196), "open knowledge", fill=BLUE, font=title)
    draw.text((94, 290), "ClineFlow — AI coding memory with a portable, agent-readable project record.", fill=INK, font=subtitle)
    nodes = [(280, 455), (560, 400), (840, 475), (1120, 405), (1400, 465)]
    for left, right in zip(nodes, nodes[1:]):
        draw.line((*left, *right), fill="#7EA9D6", width=4)
    for x, y in nodes:
        draw.ellipse((x - 21, y - 21, x + 21, y + 21), fill="#FFFFFF", outline=BLUE, width=5)
        draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=BLUE)
    cards = (
        (104, 560, "JOURNAL", "decisions, evidence, next step"),
        (570, 560, "OKF BUNDLE", "Markdown + YAML, Git-native"),
        (1036, 560, "REUSE", "human and agent-readable context"),
    )
    for x, y, heading, detail in cards:
        draw.rounded_rectangle((x, y, x + 360, y + 182), radius=18, fill="#F4F8FC", outline="#A7C3DE", width=3)
        draw.text((x + 28, y + 28), heading, fill=NAVY, font=small)
        text_block(draw, detail, x + 28, y + 72, 305, tiny, INK, leading=25)
    draw.text((94, 828), "Open Knowledge Format: durable context, open formats, and visible decision history.", fill="#526779", font=small)
    CLINEFLOW_PRINT.parent.mkdir(parents=True, exist_ok=True)
    output.save(CLINEFLOW_PRINT, dpi=(300, 300))


def wrap(draw: ImageDraw.ImageDraw, text: str, width: int, face: ImageFont.FreeTypeFont) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if not current or draw.textlength(candidate, font=face) <= width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block(
    draw: ImageDraw.ImageDraw,
    text: str,
    x: int,
    y: int,
    width: int,
    face: ImageFont.FreeTypeFont,
    fill: str,
    *,
    leading: int,
) -> int:
    for line in wrap(draw, text, width, face):
        draw.text((x, y), line, fill=fill, font=face)
        y += leading
    return y


def draw_card(draw: ImageDraw.ImageDraw, y: int, heading: str, left: str, right: str, shaded: bool) -> None:
    label = font("Arial Bold.ttf", 32)
    detail = font("Arial.ttf", 40)
    fill = "#FFFFFF" if not shaded else MIST
    draw.rounded_rectangle((92, y, 1708, y + 250), radius=26, fill=fill, outline="#C7D6E5", width=4)
    draw.rounded_rectangle((120, y + 38, 430, y + 212), radius=20, fill=NAVY)
    heading_y = y + 76
    for line in textwrap.wrap(heading, width=12):
        draw.text((150, heading_y), line, fill="#FFFFFF", font=label)
        heading_y += 39
    draw.line((1000, y + 36, 1000, y + 214), fill="#C7D6E5", width=4)
    text_block(draw, left, 468, y + 57, 486, detail, INK, leading=52)
    text_block(draw, right, 1040, y + 57, 610, detail, INK, leading=52)


def build_infographic() -> None:
    """Create two readable 6×9 comparison plates from the Image 2 visual."""
    title = font("Georgia Bold.ttf", 66)
    subtitle = font("Georgia Italic.ttf", 30)
    product = font("Arial Bold.ttf", 34)
    detail = font("Arial.ttf", 28)
    caption = font("Georgia Italic.ttf", 25)

    first = Image.new("RGB", (1800, 2220), WARM_WHITE)
    draw = ImageDraw.Draw(first)
    draw.rectangle((78, 74, 1722, 92), fill=BLUE)
    draw.text((110, 130), "Two creative systems, one control contract", fill=NAVY, font=title)
    text_block(draw, "Generative AI becomes useful when the creator can inspect every transformation and decide what may leave the project.", 112, 218, 1576, subtitle, INK, leading=39)
    flow = Image.open(FLOW_SOURCE).convert("RGB").resize((980, 700), Image.Resampling.LANCZOS)
    first.paste(flow, (410, 335))
    draw.rounded_rectangle((92, 410, 460, 625), radius=24, fill="#FFFFFF", outline=BLUE, width=4)
    draw.text((122, 443), "LYRICS REFINER", fill=NAVY, font=product)
    text_block(draw, "A writer-controlled local studio for Spanish lyrics.", 122, 495, 300, detail, INK, leading=36)
    draw.rounded_rectangle((1340, 410, 1708, 625), radius=24, fill="#FFFFFF", outline=BLUE, width=4)
    draw.text((1370, 443), "NEWSMUSIC", fill=NAVY, font=product)
    text_block(draw, "A review-gated news-to-original-video production line.", 1370, 495, 300, detail, INK, leading=36)
    draw.text((112, 1085), "Part I — work made visible", fill=NAVY, font=font("Georgia Bold.ttf", 46))
    for index, card in enumerate((
        ("CONTEXT", "Original lyric plus optional structural reference.", "Configured sources, transcripts, metadata, and editorial brief."),
        ("PIPELINE", "Analyze → structure → refine → annotate → arrange.", "Ingest → brief → original corpus → music/image → video."),
        ("CHECK", "Preservation reports flag source words dropped by a model pass.", "Dry-run and configuration checks stop spend, rendering, and upload."),
    )):
        draw_card(draw, 1165 + index * 285, *card, index % 2 == 1)
    first.save(INFOGRAPHIC_ONE, dpi=(300, 300))

    second = Image.new("RGB", (1800, 1360), WARM_WHITE)
    draw = ImageDraw.Draw(second)
    draw.rectangle((78, 74, 1722, 92), fill=BLUE)
    draw.text((110, 130), "The creator stays in charge", fill=NAVY, font=title)
    text_block(draw, "The value of the system is not unattended output. It is a controlled path from an idea to a reviewable result.", 112, 218, 1576, subtitle, INK, leading=39)
    for index, card in enumerate((
        ("STATE + CREDENTIALS", "Local browser state and a creator-owned key stay on the machine.", "Local OAuth and API configuration remain ignored runtime state."),
        ("HUMAN CONTROL", "The writer reviews intermediate stages and chooses whether to export.", "The creator reviews the package before any consequential delivery."),
        ("EVALUATION", "A deterministic check detects omissions, not artistic truth.", "Factual, rights, and suitability judgment remain human work."),
    )):
        draw_card(draw, 365 + index * 285, *card, index % 2 == 1)
    draw.line((112, 1290, 1688, 1290), fill="#B9C8D7", width=3)
    draw.text((112, 1314), "Figure 15.1 — Applied systems earn leverage through staged work, explicit checks, and human approval.", fill="#526779", font=caption)
    second.save(INFOGRAPHIC_TWO, dpi=(300, 300))


def main() -> None:
    normalize_interior_cover()
    make_clineflow_print_variant()
    build_infographic()
    for path in (INTERIOR_COVER, PRODUCTION_INTERIOR_COVER, CLINEFLOW_PRINT, INFOGRAPHIC_ONE, INFOGRAPHIC_TWO):
        with Image.open(path) as image:
            print(f"Wrote {path.relative_to(ROOT)} ({image.width}×{image.height}, {image.info.get('dpi')})")


if __name__ == "__main__":
    main()
