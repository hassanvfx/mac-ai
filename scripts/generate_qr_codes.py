"""Generate versioned SVG QR assets for deployed GitHub Pages chapter labs."""

from __future__ import annotations

import json
from pathlib import Path

from reportlab.graphics import renderSVG
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "book/qrcode-manifest.json"
OUTPUT = ROOT / "book/assets/qrcodes"


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    OUTPUT.mkdir(parents=True, exist_ok=True)
    generated: list[dict[str, str]] = []
    targets = [("start-here", data["start_here"]["url"])]
    targets.append(("clineflow-install", data["tooling"]["clineflow"]["url"]))
    targets.extend((f"chapter-{chapter['id']}-lab", f"{data['base_url']}/{chapter['id']}") for chapter in data["chapters"])
    for name, url in targets:
        widget = qr.QrCodeWidget(url)
        bounds = widget.getBounds()
        drawing = Drawing(bounds[2] - bounds[0], bounds[3] - bounds[1])
        drawing.add(widget)
        target = OUTPUT / f"{name}.svg"
        renderSVG.drawToFile(drawing, str(target))
        generated.append({"target": name, "url": url, "svg": str(target.relative_to(ROOT))})
    (OUTPUT / "manifest.json").write_text(json.dumps(generated, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(generated)} QR assets to {OUTPUT}")


if __name__ == "__main__":
    main()
