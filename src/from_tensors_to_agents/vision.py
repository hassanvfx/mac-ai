"""Small deterministic image-classification fixture shared by framework experiments."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import torch
from torch import nn

CLASS_NAMES = ("vertical", "horizontal", "diagonal")
IMAGE_SIZE = 16


@dataclass(frozen=True)
class VisionSplit:
    """A fixed-size grayscale image split in NCHW layout."""

    images: np.ndarray
    labels: np.ndarray


@dataclass(frozen=True)
class VisionDataset:
    """Versioned fixture generated only from its seed and declared sizes."""

    train: VisionSplit
    validation: VisionSplit
    test: VisionSplit


def _pattern(label: int, rng: np.random.Generator) -> np.ndarray:
    image = np.zeros((IMAGE_SIZE, IMAGE_SIZE), dtype=np.float32)
    offset = int(rng.integers(-2, 3))
    thickness = int(rng.integers(1, 3))
    if label == 0:
        center = IMAGE_SIZE // 2 + offset
        image[:, max(0, center - thickness // 2) : min(IMAGE_SIZE, center + thickness // 2 + 1)] = 1
    elif label == 1:
        center = IMAGE_SIZE // 2 + offset
        image[max(0, center - thickness // 2) : min(IMAGE_SIZE, center + thickness // 2 + 1), :] = 1
    elif label == 2:
        for row in range(IMAGE_SIZE):
            column = row + offset
            for delta in range(-(thickness // 2), thickness // 2 + 1):
                if 0 <= column + delta < IMAGE_SIZE:
                    image[row, column + delta] = 1
    else:
        raise ValueError(f"Unknown class label: {label}")
    noise = rng.normal(loc=0.0, scale=0.12, size=image.shape).astype(np.float32)
    return np.clip(image + noise, 0.0, 1.0)


def _split(samples_per_class: int, seed: int) -> VisionSplit:
    rng = np.random.default_rng(seed)
    labels = np.repeat(np.arange(len(CLASS_NAMES), dtype=np.int64), samples_per_class)
    images = np.stack([_pattern(int(label), rng) for label in labels])[:, None, :, :]
    order = rng.permutation(len(labels))
    return VisionSplit(images=images[order], labels=labels[order])


def make_vision_fixture(samples_per_class: int = 32, seed: int = 41) -> VisionDataset:
    """Create balanced train, validation, and test splits without downloads."""
    if samples_per_class < 2:
        raise ValueError("samples_per_class must be at least 2")
    return VisionDataset(
        train=_split(samples_per_class, seed),
        validation=_split(samples_per_class // 2, seed + 1),
        test=_split(samples_per_class // 2, seed + 2),
    )


class TinyConvNet(nn.Module):
    """A deliberately small CNN for 16×16 single-channel images."""

    def __init__(self, classes: int = len(CLASS_NAMES)) -> None:
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            nn.Conv2d(8, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1)),
        )
        self.classifier = nn.Linear(16, classes)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.features(inputs).flatten(1))


def confusion_matrix(predictions: np.ndarray, labels: np.ndarray) -> np.ndarray:
    """Return rows=true classes and columns=predicted classes."""
    matrix = np.zeros((len(CLASS_NAMES), len(CLASS_NAMES)), dtype=np.int64)
    for actual, predicted in zip(labels, predictions, strict=True):
        matrix[int(actual), int(predicted)] += 1
    return matrix
