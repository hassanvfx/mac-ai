import subprocess
import sys
from pathlib import Path


def test_book_audit_has_no_structural_or_link_errors() -> None:
    root = Path(__file__).resolve().parents[1]
    completed = subprocess.run(
        [sys.executable, "scripts/audit_book.py"], cwd=root, text=True, capture_output=True, check=False
    )
    assert completed.returncode == 0, completed.stdout
