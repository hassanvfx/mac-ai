"""Validate the one manifest that connects chapters, labs, code, and QR assets."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "book/qrcode-manifest.json"


def fail(message: str) -> None:
    raise SystemExit(f"Reader bridge validation failed: {message}")


def main() -> None:
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    expected_ids = [f"{number:02d}" for number in range(1, 16)]
    ids = [chapter["id"] for chapter in data["chapters"]]
    if ids != expected_ids:
        fail(f"expected chapter IDs {expected_ids}, found {ids}")
    if data["branch"] != "main":
        fail("reader destinations must track main")
    if data["base_url"] != "https://hassanvfx.github.io/mac-ai/labs":
        fail("unexpected deployed lab base URL")
    if data["start_here"]["url"] != "https://hassanvfx.github.io/mac-ai/":
        fail("unexpected course start URL")
    clineflow = data.get("tooling", {}).get("clineflow", {})
    if clineflow.get("url") != "https://github.com/hassanvfx/clineflow":
        fail("unexpected ClineFlow reader-tool URL")
    if clineflow.get("command") != "curl -fsSL https://raw.githubusercontent.com/hassanvfx/clineflow/main/install.sh | bash":
        fail("unexpected ClineFlow install command")
    preamble = (ROOT / "book/chapters/00-preamble-the-authors-toolkit.md").read_text(encoding="utf-8")
    if clineflow["url"] not in preamble or clineflow["command"] not in preamble:
        fail("The Author's Toolkit must expose the ClineFlow link and install command")
    for lab in data["chapters"]:
        for key in ("chapter", "experiment", "benchmark"):
            path = ROOT / lab[key]
            if not path.is_file():
                fail(f"chapter {lab['id']} references missing {key}: {lab[key]}")
        heading = re.search(r"^#\s+(.+)$", (ROOT / lab["chapter"]).read_text(encoding="utf-8"), re.MULTILINE)
        if not heading or heading.group(1).strip() != lab["title"]:
            fail(f"chapter {lab['id']} title does not match its canonical Markdown")
        if not lab["command"].startswith("uv run "):
            fail(f"chapter {lab['id']} does not have a reproducible uv command")
    print(f"Reader bridge validation passed for {len(expected_ids)} labs and the introduction start page.")


if __name__ == "__main__":
    main()
