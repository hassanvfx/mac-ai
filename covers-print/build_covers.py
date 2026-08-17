"""Compose the two standalone print PNGs from approved source-art plates.

Usage:
  python covers-print/build_covers.py <existing-front-cover.png> <back-art.png>

The script intentionally only writes within its own directory.  It does not
touch the GitHub Pages cover or the provisional book-cover assets.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
WIDTH, HEIGHT, DPI = 7500, 11100, 1200
IVORY = "#F8F2E8"
INK = "#11100E"
BLUE = "#173B78"
SERIF = "/System/Library/Fonts/Supplemental/Georgia.ttf"
BOLD = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
ITALIC = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def cover_background(source_path: Path) -> Image.Image:
    """Fit a source plate to the final bleed size without adding borders."""
    with Image.open(source_path) as source:
        return ImageOps.fit(
            source.convert("RGB"), (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS
        )


def centered(draw: ImageDraw.ImageDraw, y: int, text: str, typeface, fill: str) -> None:
    box = draw.textbbox((0, 0), text, font=typeface)
    draw.text(((WIDTH - (box[2] - box[0])) / 2, y), text, font=typeface, fill=fill)


def wrapped(draw: ImageDraw.ImageDraw, text: str, typeface, max_width: int) -> list[str]:
    words, lines, line = text.split(), [], ""
    for word in words:
        candidate = word if not line else f"{line} {word}"
        if draw.textlength(candidate, font=typeface) <= max_width:
            line = candidate
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_paragraph(draw: ImageDraw.ImageDraw, text: str, x: int, y: int, typeface, width: int, leading: int) -> int:
    for line in wrapped(draw, text, typeface, width):
        draw.text((x, y), line, font=typeface, fill=INK)
        y += leading
    return y


def front(source: Path) -> Image.Image:
    """Upscale the published cover unchanged; no typography or art is recreated."""
    with Image.open(source) as original:
        original = original.convert("RGB")
        # Preserve the published cover's aspect ratio and every visual element.
        enlarged = ImageOps.contain(original, (WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    image = Image.new("RGB", (WIDTH, HEIGHT), IVORY)
    x = (WIDTH - enlarged.width) // 2
    y = (HEIGHT - enlarged.height) // 2
    image.paste(enlarged, (x, y))
    return image


def back(source: Path) -> Image.Image:
    image = cover_background(source)
    draw = ImageDraw.Draw(image)
    draw.rectangle((420, 150, WIDTH - 420, 285), fill=BLUE)
    centered(draw, 470, "AI FROM TENSORS TO AGENTS ON MAC SILICON", font(BOLD, 142), BLUE)

    x, width = 750, 6000
    y = 1070
    body = font(SERIF, 168)
    summary = (
        "Modern AI becomes more understandable when you build it. This practical "
        "guide takes you from tensors, gradients, and neural networks to embeddings, "
        "retrieval-augmented generation, and agentic systems—on the Mac you already use."
    )
    second = (
        "Each chapter pairs clear explanations with small, runnable experiments. "
        "Read the idea, run the code, inspect the result, change one variable, and "
        "verify what happened. The companion repository turns the book into a "
        "learning laboratory for Apple Silicon."
    )
    y = draw_paragraph(draw, summary, x, y, body, width, 245)
    y += 310
    y = draw_paragraph(draw, second, x, y, body, width, 245)
    y += 510
    draw.line((x, y, x + width, y), fill=BLUE, width=24)
    y += 260
    draw.text((x, y), "ABOUT THE AUTHOR", font=font(BOLD, 190), fill=BLUE)
    y += 330
    bio = (
        "Hassan Uriostegui is the author of AI From Tensors to Agents on Mac Silicon "
        "and founder of Waken AI Labs."
    )
    draw_paragraph(draw, bio, x, y, body, width, 245)
    return image


def save(image: Image.Image, filename: str) -> None:
    image.save(ROOT / filename, "PNG", dpi=(DPI, DPI), optimize=True)


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: build_covers.py <existing-front-cover.png> <back-art.png>")
    save(front(Path(sys.argv[1])), "ai-from-tensors-to-agents-front-print.png")
    save(back(Path(sys.argv[2])), "ai-from-tensors-to-agents-back-print.png")


if __name__ == "__main__":
    main()
