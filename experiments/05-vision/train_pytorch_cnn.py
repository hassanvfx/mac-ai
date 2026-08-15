"""Train and evaluate the Milestone 2 PyTorch CNN on the versioned fixture.

Run:
    uv run python experiments/05-vision/train_pytorch_cnn.py --epochs 30
"""

from __future__ import annotations

import argparse
import json
import time

import numpy as np
import torch
from torch import nn

from from_tensors_to_agents.device import preferred_device
from from_tensors_to_agents.vision import (
    CLASS_NAMES,
    TinyConvNet,
    confusion_matrix,
    make_vision_fixture,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--samples-per-class", type=int, default=32)
    parser.add_argument("--device", choices=("auto", "cpu", "mps"), default="auto")
    return parser.parse_args()


def select_device(requested: str) -> torch.device:
    if requested == "cpu":
        return torch.device("cpu")
    if requested == "mps":
        if not torch.backends.mps.is_available():
            raise RuntimeError("MPS was requested but is not available.")
        return torch.device("mps")
    return preferred_device()


def tensors(images: np.ndarray, labels: np.ndarray, device: torch.device) -> tuple[torch.Tensor, torch.Tensor]:
    return torch.from_numpy(images).to(device), torch.from_numpy(labels).to(device)


def accuracy(model: nn.Module, inputs: torch.Tensor, labels: torch.Tensor) -> float:
    with torch.no_grad():
        return (model(inputs).argmax(dim=1) == labels).float().mean().item()


def run(
    epochs: int = 30,
    seed: int = 17,
    samples_per_class: int = 32,
    device: torch.device | None = None,
) -> dict[str, object]:
    """Run one fully deterministic fixture experiment and return JSON-safe evidence."""
    if epochs < 1:
        raise ValueError("epochs must be at least 1")
    torch.manual_seed(seed)
    active_device = device or preferred_device()
    fixture = make_vision_fixture(samples_per_class=samples_per_class)
    train_x, train_y = tensors(fixture.train.images, fixture.train.labels, active_device)
    validation_x, validation_y = tensors(fixture.validation.images, fixture.validation.labels, active_device)
    test_x, _ = tensors(fixture.test.images, fixture.test.labels, active_device)
    model = TinyConvNet().to(active_device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_fn = nn.CrossEntropyLoss()

    if active_device.type == "mps":
        torch.mps.synchronize()
    started = time.perf_counter()
    model.train()
    for _ in range(epochs):
        optimizer.zero_grad()
        loss = loss_fn(model(train_x), train_y)
        loss.backward()
        optimizer.step()
    if active_device.type == "mps":
        torch.mps.synchronize()

    model.eval()
    with torch.no_grad():
        predictions = model(test_x).argmax(dim=1).cpu().numpy()
    test_labels = fixture.test.labels
    mistakes = [
        {"index": int(index), "actual": CLASS_NAMES[int(actual)], "predicted": CLASS_NAMES[int(predicted)]}
        for index, (actual, predicted) in enumerate(zip(test_labels, predictions, strict=True))
        if actual != predicted
    ]
    return {
        "framework": "pytorch",
        "torch_version": torch.__version__,
        "device": active_device.type,
        "mps_available": torch.backends.mps.is_available(),
        "seed": seed,
        "epochs": epochs,
        "samples_per_class": samples_per_class,
        "train_accuracy": accuracy(model, train_x, train_y),
        "validation_accuracy": accuracy(model, validation_x, validation_y),
        "test_accuracy": float((predictions == test_labels).mean()),
        "final_train_loss": float(loss.detach().cpu().item()),
        "elapsed_ms": round((time.perf_counter() - started) * 1_000, 3),
        "confusion_matrix": confusion_matrix(predictions, test_labels).tolist(),
        "class_names": list(CLASS_NAMES),
        "mistakes": mistakes,
    }


def main() -> None:
    args = parse_args()
    result = run(
        epochs=args.epochs,
        seed=args.seed,
        samples_per_class=args.samples_per_class,
        device=select_device(args.device),
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
