import numpy as np
import torch

from from_tensors_to_agents.vision import (
    CLASS_NAMES,
    TinyConvNet,
    confusion_matrix,
    make_vision_fixture,
)


def test_vision_fixture_is_deterministic_and_balanced() -> None:
    first = make_vision_fixture(samples_per_class=6, seed=41)
    second = make_vision_fixture(samples_per_class=6, seed=41)
    assert np.array_equal(first.train.images, second.train.images)
    assert np.array_equal(first.train.labels, second.train.labels)
    assert first.train.images.shape == (18, 1, 16, 16)
    assert np.bincount(first.train.labels).tolist() == [6, 6, 6]


def test_tiny_cnn_preserves_batch_and_class_dimensions() -> None:
    model = TinyConvNet()
    logits = model(torch.zeros((4, 1, 16, 16)))
    assert logits.shape == (4, len(CLASS_NAMES))


def test_confusion_matrix_uses_true_rows_and_predicted_columns() -> None:
    matrix = confusion_matrix(np.array([0, 2, 1]), np.array([0, 1, 1]))
    assert matrix.tolist() == [[1, 0, 0], [0, 1, 1], [0, 0, 0]]
