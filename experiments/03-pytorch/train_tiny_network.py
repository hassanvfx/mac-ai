"""Train a tiny regressor with MPS when it is available.

Run ``uv run python experiments/03-pytorch/train_tiny_network.py`` for the
reading example. The benchmark runner imports ``train`` and supplies an
explicit device so CPU and MPS measurements use the identical workload.
"""

from __future__ import annotations

import torch

from from_tensors_to_agents.device import preferred_device
from from_tensors_to_agents.training import train_tiny_regressor


def train(
    epochs: int = 250, seed: int = 7, device: torch.device | None = None
) -> list[float]:
    """Train the fixed regression workload and return one loss per epoch."""
    active_device = device or preferred_device()
    losses = train_tiny_regressor(epochs=epochs, seed=seed, device=active_device)
    print(
        f"device={active_device.type} initial_loss={losses[0]:.6f} "
        f"final_loss={losses[-1]:.6f}"
    )
    return losses


if __name__ == "__main__":
    train()
