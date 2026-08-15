from __future__ import annotations

import pytest
import torch

from from_tensors_to_agents.transformers import (
    compare_predictions,
    ranked_labels,
    tokenization_summary,
    transformer_device,
)


class FakeTokenizer:
    def __call__(self, text: str, *, truncation: bool, max_length: int) -> dict[str, list[int]]:
        del text, truncation
        return {"input_ids": [101, 2023, 102][:max_length], "attention_mask": [1, 1, 1][:max_length]}

    def convert_ids_to_tokens(self, ids: list[int]) -> list[str]:
        return [f"token-{token_id}" for token_id in ids]


def test_tokenization_summary_is_json_safe() -> None:
    summary = tokenization_summary(FakeTokenizer(), "A test", max_length=3)
    assert summary["tokens"] == ["token-101", "token-2023", "token-102"]
    assert summary["attention_mask"] == [1, 1, 1]
    assert summary["truncated"] is True


def test_ranked_labels_and_pipeline_comparison() -> None:
    ranking = ranked_labels(torch.tensor([1.0, 3.0]), {"0": "NEGATIVE", "1": "POSITIVE"})
    assert ranking[0]["label"] == "POSITIVE"
    comparison = compare_predictions(ranking, {"label": "POSITIVE", "score": ranking[0]["score"]})
    assert comparison["same_top_label"] is True
    assert comparison["score_absolute_difference"] == 0.0


def test_device_selection_rejects_invalid_name() -> None:
    with pytest.raises(ValueError, match="device must be one of"):
        transformer_device("cuda")


def test_cpu_selection_is_always_available() -> None:
    assert transformer_device("cpu") == torch.device("cpu")
