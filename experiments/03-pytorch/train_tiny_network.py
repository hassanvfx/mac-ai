"""Train a tiny regressor with MPS when it is available."""

from __future__ import annotations

import torch
from torch import nn

from from_tensors_to_agents.day1 import make_regression_data, make_tiny_regressor
from from_tensors_to_agents.device import preferred_device


def train(epochs: int = 250, seed: int = 7) -> list[float]:
    torch.manual_seed(seed)
    device = preferred_device()
    inputs, targets = (item.to(device) for item in make_regression_data())
    model = make_tiny_regressor().to(device)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.08)
    loss_fn = nn.MSELoss()
    losses: list[float] = []
    for _ in range(epochs):
        optimizer.zero_grad()
        loss = loss_fn(model(inputs), targets)
        loss.backward()
        optimizer.step()
        losses.append(loss.detach().cpu().item())
    print(f"device={device.type} initial_loss={losses[0]:.6f} final_loss={losses[-1]:.6f}")
    return losses


if __name__ == "__main__":
    train()
