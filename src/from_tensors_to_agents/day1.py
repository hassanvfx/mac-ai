"""Small, deterministic building blocks used in Day 1."""

from __future__ import annotations

import torch
from torch import nn


def mean_squared_error(predictions: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
    return ((predictions - targets) ** 2).mean()


def make_tiny_regressor() -> nn.Module:
    return nn.Sequential(nn.Linear(1, 8), nn.Tanh(), nn.Linear(8, 1))


def make_regression_data(samples: int = 64) -> tuple[torch.Tensor, torch.Tensor]:
    inputs = torch.linspace(-1, 1, samples).unsqueeze(1)
    targets = 2 * inputs + 0.5
    return inputs, targets
