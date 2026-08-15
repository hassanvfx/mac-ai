"""Normalize a generated DOCX to Lulu's 6×9 non-bleed interior trim size.

The downloaded template carries 6.25×9.25-in dimensions because it also
supports full-bleed pages. This manuscript has no full-bleed interior pages;
the generated DOCX therefore needs an explicit non-bleed trim normalization.
"""

from __future__ import annotations

import argparse
import shutil
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}
ET.register_namespace("w", W)
WIDTH_TWIPS = "8640"  # 6 in × 1440
HEIGHT_TWIPS = "12960"  # 9 in × 1440
CONTENT_WIDTH_EMU = 4.55 * 914400


def set_style(
    styles: ET.Element,
    style_id: str,
    *,
    font: str,
    size: int,
    color: str,
    before: int = 0,
    after: int = 0,
    line: int | None = None,
    first_line: int | None = None,
    bold: bool = False,
    italic: bool = False,
) -> None:
    style = styles.find(f"w:style[@w:styleId='{style_id}']", NS)
    if style is None:
        return
    properties = style.find("w:pPr", NS)
    if properties is None:
        properties = ET.SubElement(style, f"{{{W}}}pPr")
    spacing = properties.find("w:spacing", NS)
    if spacing is None:
        spacing = ET.SubElement(properties, f"{{{W}}}spacing")
    spacing.set(f"{{{W}}}before", str(before))
    spacing.set(f"{{{W}}}after", str(after))
    if line is not None:
        spacing.set(f"{{{W}}}line", str(line))
        spacing.set(f"{{{W}}}lineRule", "auto")
    if first_line is not None:
        indent = properties.find("w:ind", NS)
        if indent is None:
            indent = ET.SubElement(properties, f"{{{W}}}ind")
        indent.set(f"{{{W}}}firstLine", str(first_line))
    runs = style.find("w:rPr", NS)
    if runs is None:
        runs = ET.SubElement(style, f"{{{W}}}rPr")
    fonts = runs.find("w:rFonts", NS)
    if fonts is None:
        fonts = ET.SubElement(runs, f"{{{W}}}rFonts")
    for key in ("ascii", "hAnsi", "eastAsia", "cs"):
        fonts.set(f"{{{W}}}{key}", font)
    for tag, enabled in (("b", bold), ("i", italic)):
        node = runs.find(f"w:{tag}", NS)
        if enabled and node is None:
            ET.SubElement(runs, f"{{{W}}}{tag}")
        elif not enabled and node is not None:
            runs.remove(node)
    color_node = runs.find("w:color", NS)
    if color_node is None:
        color_node = ET.SubElement(runs, f"{{{W}}}color")
    color_node.set(f"{{{W}}}val", color)
    size_node = runs.find("w:sz", NS)
    if size_node is None:
        size_node = ET.SubElement(runs, f"{{{W}}}sz")
    size_node.set(f"{{{W}}}val", str(size))


def polish_layout(root: ET.Element, temporary: Path) -> None:
    styles_path = temporary / "word/styles.xml"
    styles_tree = ET.parse(styles_path)
    styles = styles_tree.getroot()
    set_style(styles, "Normal", font="Garamond", size=21, color="262626", after=110, line=276)
    set_style(styles, "FirstParagraph", font="Garamond", size=21, color="262626", after=110, line=276)
    set_style(styles, "BodyText", font="Garamond", size=21, color="262626", after=110, line=276, first_line=240)
    set_style(styles, "Heading1", font="Georgia", size=38, color="173F73", after=300, bold=True)
    set_style(styles, "Heading2", font="Georgia", size=29, color="173F73", before=340, after=120, bold=True)
    set_style(styles, "Heading3", font="Georgia", size=23, color="50657A", before=260, after=90, bold=True)
    set_style(styles, "SourceCode", font="Menlo", size=17, color="243447", before=100, after=150, line=220)
    set_style(styles, "ImageCaption", font="Garamond", size=17, color="50657A", before=50, after=160, italic=True)
    set_style(styles, "Title", font="Georgia", size=44, color="173F73", before=1600, after=260, bold=True)
    set_style(styles, "Subtitle", font="Garamond", size=28, color="50657A", after=180, italic=True)
    set_style(styles, "Author", font="Garamond", size=25, color="262626", after=90)
    source = styles.find("w:style[@w:styleId='SourceCode']", NS)
    if source is not None:
        properties = source.find("w:pPr", NS)
        if properties is None:
            properties = ET.SubElement(source, f"{{{W}}}pPr")
        indent = properties.find("w:ind", NS)
        if indent is None:
            indent = ET.SubElement(properties, f"{{{W}}}ind")
        indent.set(f"{{{W}}}left", "240")
        indent.set(f"{{{W}}}right", "240")
        shading = properties.find("w:shd", NS)
        if shading is None:
            shading = ET.SubElement(properties, f"{{{W}}}shd")
        shading.set(f"{{{W}}}val", "clear")
        shading.set(f"{{{W}}}fill", "F1F5F8")
        borders = properties.find("w:pBdr", NS)
        if borders is None:
            borders = ET.SubElement(properties, f"{{{W}}}pBdr")
        for side in ("top", "left", "bottom", "right"):
            border = borders.find(f"w:{side}", NS)
            if border is None:
                border = ET.SubElement(borders, f"{{{W}}}{side}")
            border.set(f"{{{W}}}val", "single")
            border.set(f"{{{W}}}sz", "4")
            border.set(f"{{{W}}}color", "D6E0E8")
            border.set(f"{{{W}}}space", "6")
    inline = styles.find("w:style[@w:styleId='VerbatimChar']", NS)
    if inline is not None:
        runs = inline.find("w:rPr", NS)
        if runs is None:
            runs = ET.SubElement(inline, f"{{{W}}}rPr")
        fonts = runs.find("w:rFonts", NS)
        if fonts is None:
            fonts = ET.SubElement(runs, f"{{{W}}}rFonts")
        for key in ("ascii", "hAnsi", "eastAsia", "cs"):
            fonts.set(f"{{{W}}}{key}", "Menlo")
        color = runs.find("w:color", NS)
        if color is None:
            color = ET.SubElement(runs, f"{{{W}}}color")
        color.set(f"{{{W}}}val", "173F73")
        shading = runs.find("w:shd", NS)
        if shading is None:
            shading = ET.SubElement(runs, f"{{{W}}}shd")
        shading.set(f"{{{W}}}val", "clear")
        shading.set(f"{{{W}}}fill", "EAF0F5")
    styles_tree.write(styles_path, encoding="utf-8", xml_declaration=True)

    for section in root.findall(".//w:sectPr", NS):
        margins = section.find("w:pgMar", NS)
        if margins is None:
            margins = ET.SubElement(section, f"{{{W}}}pgMar")
        for key, value in {
            "top": "1080", "bottom": "1008", "left": "1008", "right": "1008",
            "header": "432", "footer": "432", "gutter": "0",
        }.items():
            margins.set(f"{{{W}}}{key}", value)

    drawing_ns = {**NS, "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"}
    for extent in root.findall(".//wp:extent", drawing_ns):
        width = int(extent.get("cx", "0"))
        if width > CONTENT_WIDTH_EMU:
            height = int(extent.get("cy", "0"))
            scale = CONTENT_WIDTH_EMU / width
            extent.set("cx", str(round(CONTENT_WIDTH_EMU)))
            extent.set("cy", str(round(height * scale)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("docx", type=Path)
    args = parser.parse_args()
    source = args.docx
    if not source.exists():
        raise SystemExit(f"Missing DOCX: {source}")

    with tempfile.TemporaryDirectory() as temporary:
        temp = Path(temporary)
        with zipfile.ZipFile(source) as archive:
            archive.extractall(temp)
        document = temp / "word/document.xml"
        tree = ET.parse(document)
        root = tree.getroot()
        sizes = root.findall(".//w:pgSz", NS)
        if not sizes:
            raise SystemExit("No Word page-size elements found")
        for size in sizes:
            size.set(f"{{{W}}}w", WIDTH_TWIPS)
            size.set(f"{{{W}}}h", HEIGHT_TWIPS)
        # The reference template applies consistent styles, but not page breaks
        # to Pandoc's front-matter blocks. Add them by structural role so the
        # legal, author, acknowledgement, chapter, and appendix pages
        # have intentional starts in both Word and LibreOffice review renders.
        for paragraph in root.findall(".//w:body/w:p", NS):
            text = "".join(run.text or "" for run in paragraph.findall(".//w:t", NS))
            style = paragraph.find("w:pPr/w:pStyle", NS)
            style_name = style.get(f"{{{W}}}val") if style is not None else ""
            begins_section = text in {
                "About the Author",
                "Acknowledgements",
            }
            begins_section = begins_section or style_name == "Heading1"
            if begins_section:
                properties = paragraph.find("w:pPr", NS)
                if properties is None:
                    properties = ET.Element(f"{{{W}}}pPr")
                    paragraph.insert(0, properties)
                if properties.find("w:pageBreakBefore", NS) is None:
                    properties.append(ET.Element(f"{{{W}}}pageBreakBefore"))
        polish_layout(root, temp)
        tree.write(document, encoding="utf-8", xml_declaration=True)
        rebuilt = temp / "normalized.docx"
        with zipfile.ZipFile(rebuilt, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in temp.rglob("*"):
                if path.is_file() and path != rebuilt:
                    archive.write(path, path.relative_to(temp))
        shutil.copy2(rebuilt, source)
    print(f"Normalized {source} to 6 x 9 in non-bleed trim.")


if __name__ == "__main__":
    main()
