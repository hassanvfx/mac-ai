"""Prepare a temporary print chapter and append its manifest-backed lab panel."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "book/qrcode-manifest.json").read_text(encoding="utf-8"))


def without_front_matter(text: str) -> str:
    return re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)


def panel_for(chapter_id: str) -> str:
    if chapter_id == "00":
        start = MANIFEST["start_here"]
        return f"""

\\newpage

## Start the course on your Mac

![QR code for the online course start page](assets/qrcodes/start-here.svg){{width=0.82in}}

**Start here:** <{start["url"]}>

Clone the repository, follow the ten-day roadmap, and use the chapter QR codes
to move from each lesson to its runnable lab. Scan with your phone and use
Safari Share → AirDrop to send the course link to your Mac.
"""
    lab = next(item for item in MANIFEST["chapters"] if item["id"] == chapter_id)
    url = f"{MANIFEST['base_url']}/{chapter_id}"
    return f"""

\\newpage

## Run the lab on your Mac

![QR code for Chapter {chapter_id} lab](assets/qrcodes/chapter-{chapter_id}-lab.svg){{width=0.82in}}

**Online lab:** <{url}>

**Repository:** `{lab["experiment"]}`

```bash
{lab["command"]}
```

**Expected:** {lab["expected"]}

**Evidence:** `{lab["benchmark"]}`

Scan the code to open the live lab, then use Safari Share → AirDrop to send it
to your Mac. The lab follows `main`; clone the repository once and run the
command from its root directory.
"""


def clineflow_panel() -> str:
    tool = MANIFEST["tooling"]["clineflow"]
    return f"""

\\newpage

## Optional: install ClineFlow

![QR code for ClineFlow](assets/qrcodes/clineflow-install.svg){{width=0.82in}}

**ClineFlow:** <{tool["url"]}>

```bash
{tool["command"]}
```

ClineFlow is optional. Scan the code to read its current README on your phone,
then use Safari Share → AirDrop to send the link to your Mac before installing.
Keep the journal, agent instructions, and project-specific rules you already
use; review the added files before committing them.
"""


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: prepare_print_chapter.py SOURCE OUTPUT")
    source, output = map(Path, sys.argv[1:])
    chapter_id = source.name[:2]
    text = without_front_matter(source.read_text(encoding="utf-8"))
    text = text.replace("](../assets/", "](assets/")
    if source.name == "00-preamble-the-authors-toolkit.md":
        panel = clineflow_panel()
    else:
        # The preamble deliberately sorts before the introduction but is not a
        # lab. Only the actual introduction receives the course-start panel.
        has_lab_panel = source.parent.name == "chapters"
        panel = panel_for(chapter_id) if has_lab_panel else ""
    output.write_text(text.rstrip() + panel + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
