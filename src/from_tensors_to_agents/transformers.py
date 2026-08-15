"""Small, inspectable helpers for the Chapter 6 Transformer experiment."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import torch

DEFAULT_MODEL_ID = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
DEFAULT_TEXTS = (
    "This small experiment is clear and useful.",
    "The installation failed and the result is frustrating.",
)


def transformer_device(requested: str = "auto") -> torch.device:
    """Select MPS when available, otherwise CPU; reject unavailable MPS requests."""
    if requested not in {"auto", "cpu", "mps"}:
        raise ValueError("device must be one of: auto, cpu, mps")
    mps_available = torch.backends.mps.is_available()
    if requested == "mps":
        if not mps_available:
            raise RuntimeError("MPS was requested but is not available in this PyTorch build.")
        return torch.device("mps")
    if requested == "auto" and mps_available:
        return torch.device("mps")
    return torch.device("cpu")


def tokenization_summary(tokenizer: Any, text: str, max_length: int) -> dict[str, Any]:
    """Return a JSON-safe view of a tokenizer's sequence representation."""
    encoded = tokenizer(text, truncation=True, max_length=max_length)
    ids = [int(token_id) for token_id in encoded["input_ids"]]
    mask = [int(mask_value) for mask_value in encoded["attention_mask"]]
    return {
        "text": text,
        "tokens": tokenizer.convert_ids_to_tokens(ids),
        "input_ids": ids,
        "attention_mask": mask,
        "sequence_length": len(ids),
        "truncated": len(ids) == max_length,
    }


def ranked_labels(
    logits: torch.Tensor, id2label: Mapping[int | str, str]
) -> list[dict[str, float | str]]:
    """Apply softmax and make a stable, descending label ranking."""
    probabilities = torch.softmax(logits.detach().to("cpu"), dim=-1).tolist()
    labels = {
        int(label_id): label for label_id, label in id2label.items()
    }
    return sorted(
        [
            {"label": labels[index], "score": float(score)}
            for index, score in enumerate(probabilities)
        ],
        key=lambda item: float(item["score"]),
        reverse=True,
    )


def compare_predictions(
    manual: Sequence[Mapping[str, float | str]],
    pipeline_result: Mapping[str, float | str],
) -> dict[str, float | str | bool]:
    """Compare top-1 results without assuming the pipeline's score formatting."""
    manual_top = manual[0]
    pipeline_label = str(pipeline_result["label"])
    pipeline_score = float(pipeline_result["score"])
    manual_score = float(manual_top["score"])
    return {
        "same_top_label": str(manual_top["label"]) == pipeline_label,
        "manual_label": str(manual_top["label"]),
        "pipeline_label": pipeline_label,
        "score_absolute_difference": abs(manual_score - pipeline_score),
    }
