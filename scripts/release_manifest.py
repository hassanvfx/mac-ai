"""Record reproducible publishing inputs without treating review PDFs as releases."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "book/build"
MANIFEST = BUILD / "release-manifest.json"
INPUTS = [
    ROOT / "book/manuscript.yaml",
    ROOT / "book/front-matter.md",
    ROOT / "book/templates/lulu-us-trade-interior-template.dotx",
    ROOT / "book/cover/metadata-placeholder.yaml",
    ROOT / "book/assets/cover/rottweiler-art-plate.png",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    entries = {str(path.relative_to(ROOT)): digest(path) for path in INPUTS if path.exists()}
    MANIFEST.write_text(
        json.dumps(
            {
                "generated_at": datetime.now(UTC).isoformat(),
                "edition": "beta / provisional PDF only",
                "release_pdf_authority": "Microsoft Word on macOS",
                "inputs_sha256": entries,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {MANIFEST}")


if __name__ == "__main__":
    main()
