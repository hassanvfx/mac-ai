"""Flatten risky pages and audit the master submitted to Lulu.

This deterministic final stage belongs to make master-pdf. It replaces only
the visual title page and pages containing transparency with 300 ppi opaque RGB
pages, then rejects residual transparency or used fonts lacking a FontFile.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image
from pypdf import PdfReader, PdfWriter

RENDER_DPI = 300


def resolved(value: object) -> object:
    return value.get_object() if hasattr(value, "get_object") else value


def page_resources(page: object) -> dict:
    return resolved(page.get("/Resources", {}))  # type: ignore[union-attr, return-value]


def transparent(page: object) -> bool:
    resources = page_resources(page)
    group = resolved(page.get("/Group"))  # type: ignore[union-attr]
    if isinstance(group, dict) and group.get("/S") == "/Transparency":
        return True
    states = resolved(resources.get("/ExtGState", {}))
    for state in (states or {}).values():
        state = resolved(state)
        if isinstance(state, dict) and (
            state.get("/ca", 1) != 1
            or state.get("/CA", 1) != 1
            or state.get("/SMask") not in (None, "/None")
        ):
            return True
    objects = resolved(resources.get("/XObject", {}))
    used_objects = used_xobjects(page)
    for name, item in (objects or {}).items():
        if str(name).lstrip("/") not in used_objects:
            continue
        item = resolved(item)
        if isinstance(item, dict) and (item.get("/SMask") is not None or item.get("/Mask") is not None):
            return True
    return False


def used_xobjects(page: object) -> set[str]:
    content = page.get_contents()  # type: ignore[union-attr]
    if content is None:
        return set()
    data = content.get_data().decode("latin-1", errors="ignore")
    return set(re.findall(r"/([^\s/]+)\s+Do", data))


def raster_page(source: Path, number: int, folder: Path) -> object:
    prefix = folder / "page"
    subprocess.run(
        [
            shutil.which("pdftoppm") or "pdftoppm",
            "-f",
            str(number),
            "-l",
            str(number),
            "-r",
            str(RENDER_DPI),
            "-png",
            str(source),
            str(prefix),
        ],
        check=True,
    )
    rendered = next(folder.glob("page-*.png"))
    with Image.open(rendered) as image:
        image.convert("RGB").save(folder / "opaque.pdf", "PDF", resolution=RENDER_DPI)
    return PdfReader(str(folder / "opaque.pdf")).pages[0]


def used_fonts(page: object) -> set[str]:
    content = page.get_contents()  # type: ignore[union-attr]
    if content is None:
        return set()
    data = content.get_data().decode("latin-1", errors="ignore")
    return set(re.findall(r"/([^\s/]+)\s+[-+]?\d+(?:\.\d+)?\s+Tf", data))


def font_is_embedded(font: object) -> bool:
    font = resolved(font)
    descriptor = resolved(font.get("/FontDescriptor")) if isinstance(font, dict) else None
    if not isinstance(descriptor, dict) and isinstance(font, dict):
        descendants = resolved(font.get("/DescendantFonts", []))
        if descendants:
            descendant = resolved(descendants[0])
            descriptor = resolved(descendant.get("/FontDescriptor")) if isinstance(descendant, dict) else None
    return isinstance(descriptor, dict) and any(
        descriptor.get(key) is not None for key in ("/FontFile", "/FontFile2", "/FontFile3")
    )


def audit(pdf: Path) -> None:
    reader = PdfReader(str(pdf))
    errors: list[str] = []
    for number, page in enumerate(reader.pages, 1):
        if transparent(page):
            errors.append(f"page {number}: transparency resource remains")
        fonts = resolved(page_resources(page).get("/Font", {}))
        for name in used_fonts(page):
            if name in fonts and not font_is_embedded(fonts[name]):
                errors.append(f"page {number}: /{name} is used but not embedded")
    if errors:
        raise SystemExit("Lulu PDF audit failed:\n- " + "\n- ".join(errors))
    print(f"PASS: {pdf.name} has no used unembedded fonts or transparency resources.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()
    source = args.pdf.resolve()
    if args.audit_only:
        audit(source)
        return
    reader = PdfReader(str(source))
    targets = {1} | {number for number, page in enumerate(reader.pages, 1) if transparent(page)}
    with tempfile.TemporaryDirectory(prefix="mac-ai-lulu-") as temporary:
        temporary_path = Path(temporary)
        writer = PdfWriter()
        for number, page in enumerate(reader.pages, 1):
            if number in targets:
                page_folder = temporary_path / f"page-{number}"
                page_folder.mkdir()
                page = raster_page(source, number, page_folder)
            writer.add_page(page)
        writer.add_metadata(reader.metadata or {})
        staged = temporary_path / "flattened.pdf"
        with staged.open("wb") as handle:
            writer.write(handle)
        shutil.copy2(staged, source)
    print("Flattened 300 ppi opaque pages: " + ", ".join(map(str, sorted(targets))))
    audit(source)


if __name__ == "__main__":
    main()
