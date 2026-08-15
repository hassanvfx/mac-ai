import subprocess
import sys
from pathlib import Path


def test_lulu_metadata_and_isbn_assets_are_consistent() -> None:
    root = Path(__file__).resolve().parents[1]
    completed = subprocess.run(
        [sys.executable, "scripts/validate_lulu_distribution.py"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout
