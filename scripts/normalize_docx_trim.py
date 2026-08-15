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
        # title, legal, author, acknowledgement, chapter, and appendix pages
        # have intentional starts in both Word and LibreOffice review renders.
        for paragraph in root.findall(".//w:body/w:p", NS):
            text = "".join(run.text or "" for run in paragraph.findall(".//w:t", NS))
            style = paragraph.find("w:pPr/w:pStyle", NS)
            style_name = style.get(f"{{{W}}}val") if style is not None else ""
            begins_section = text in {
                "Copyright © 2026 Hassan Uriostegui. All rights reserved.",
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
