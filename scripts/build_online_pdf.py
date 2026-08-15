"""Compatibility check for the single online/interior beta master.

The PDF is now composed by ``make master-pdf``. This command intentionally
does not prepend a second cover or write another edition.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "book/build/pdf-online.pdf"


def main() -> None:
    if not MASTER.is_file():
        raise SystemExit("Missing beta master; run make master-pdf first.")
    print(f"Single beta master is ready: {MASTER}")


if __name__ == "__main__":
    main()
