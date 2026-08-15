"""Train the Milestone 2 Keras CNN on the shared versioned vision fixture.

Run after the optional dependency install:
    uv sync --group tensorflow
    uv run --group tensorflow python experiments/04-tensorflow/train_keras_cnn.py --epochs 30
"""

from __future__ import annotations

import argparse
import json
import os
import time

import numpy as np

# Suppress informational backend logs before TensorFlow initializes.
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import tensorflow as tf

from from_tensors_to_agents.vision import CLASS_NAMES, confusion_matrix, make_vision_fixture


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--samples-per-class", type=int, default=32)
    return parser.parse_args()


def to_nhwc(images: np.ndarray) -> np.ndarray:
    """Convert the shared NCHW fixture to Keras's channels-last convention."""
    return np.transpose(images, (0, 2, 3, 1))


def make_model() -> tf.keras.Model:
    """Match the PyTorch TinyConvNet topology as closely as Keras permits."""
    return tf.keras.Sequential(
        [
            tf.keras.Input(shape=(16, 16, 1)),
            tf.keras.layers.Conv2D(8, kernel_size=3, padding="same", activation="relu"),
            tf.keras.layers.MaxPool2D(pool_size=2),
            tf.keras.layers.Conv2D(16, kernel_size=3, padding="same", activation="relu"),
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(len(CLASS_NAMES)),
        ]
    )


def run(epochs: int = 30, seed: int = 17, samples_per_class: int = 32) -> dict[str, object]:
    """Run Keras against the exact fixture split used by the PyTorch experiment."""
    if epochs < 1:
        raise ValueError("epochs must be at least 1")
    tf.keras.utils.set_random_seed(seed)
    try:
        tf.config.experimental.enable_op_determinism()
    except AttributeError:
        pass

    fixture = make_vision_fixture(samples_per_class=samples_per_class)
    train_x, validation_x, test_x = (
        to_nhwc(fixture.train.images),
        to_nhwc(fixture.validation.images),
        to_nhwc(fixture.test.images),
    )
    model = make_model()
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy(name="accuracy")],
    )
    started = time.perf_counter()
    history = model.fit(
        train_x,
        fixture.train.labels,
        validation_data=(validation_x, fixture.validation.labels),
        batch_size=32,
        epochs=epochs,
        shuffle=False,
        verbose=0,
    )
    elapsed_ms = (time.perf_counter() - started) * 1_000
    logits = model.predict(test_x, verbose=0)
    predictions = logits.argmax(axis=1)
    mistakes = [
        {"index": int(index), "actual": CLASS_NAMES[int(actual)], "predicted": CLASS_NAMES[int(predicted)]}
        for index, (actual, predicted) in enumerate(zip(fixture.test.labels, predictions, strict=True))
        if actual != predicted
    ]
    return {
        "framework": "tensorflow-keras",
        "tensorflow_version": tf.__version__,
        "visible_devices": [device.device_type for device in tf.config.list_physical_devices()],
        "seed": seed,
        "epochs": epochs,
        "samples_per_class": samples_per_class,
        "train_accuracy": float(history.history["accuracy"][-1]),
        "validation_accuracy": float(history.history["val_accuracy"][-1]),
        "test_accuracy": float((predictions == fixture.test.labels).mean()),
        "final_train_loss": float(history.history["loss"][-1]),
        "elapsed_ms": round(elapsed_ms, 3),
        "confusion_matrix": confusion_matrix(predictions, fixture.test.labels).tolist(),
        "class_names": list(CLASS_NAMES),
        "mistakes": mistakes,
    }


def main() -> None:
    args = parse_args()
    print(json.dumps(run(args.epochs, args.seed, args.samples_per_class), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
