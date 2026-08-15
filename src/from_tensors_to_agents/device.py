"""Device selection that keeps examples runnable off Apple Silicon too."""

from __future__ import annotations

import torch


def preferred_device() -> torch.device:
    """Return Apple MPS when available, otherwise CPU."""
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")
