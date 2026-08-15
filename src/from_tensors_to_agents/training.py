"""Deterministic training workload shared by the Day 1 example and benchmark."""

from __future__ import annotations

import torch
from torch import nn

from from_tensors_to_agents.day1 import make_regression_data, make_tiny_regressor


def train_tiny_regressor(
    epochs: int = 250, seed: int = 7, device: torch.device | None = None
) -> list[float]:
    """Fit the fixed synthetic regression task and return the loss at each epoch."""
    if epochs < 1:
        raise ValueError("epochs must be at least 1")

    torch.manual_seed(seed)
    active_device = device or torch.device("cpu")
    inputs, targets = (item.to(active_device) for item in make_regression_data())
    model = make_tiny_regressor().to(active_device)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.08)
    loss_fn = nn.MSELoss()
    losses: list[float] = []
    for _ in range(epochs):
        optimizer.zero_grad()
        loss = loss_fn(model(inputs), targets)
        loss.backward()
        optimizer.step()
        losses.append(loss.detach().cpu().item())
    return losses
