from __future__ import annotations

import pytest

from from_tensors_to_agents.local_models import generation_record, validate_generation_settings


class FakeResponse:
    prompt_tokens = 11
    prompt_tps = 100.5
    generation_tokens = 7
    generation_tps = 25.25
    peak_memory = 256.0
    finish_reason = "length"


def test_generation_record_is_json_safe() -> None:
    assert generation_record(FakeResponse()) == {
        "prompt_tokens": 11,
        "prompt_tokens_per_second": 100.5,
        "generated_tokens": 7,
        "generated_tokens_per_second": 25.25,
        "mlx_reported_peak_memory_gib": 256.0,
        "finish_reason": "length",
    }


@pytest.mark.parametrize("max_tokens, temperature", [(0, 0.0), (8, -0.1)])
def test_invalid_generation_settings_are_rejected(max_tokens: int, temperature: float) -> None:
    with pytest.raises(ValueError):
        validate_generation_settings(max_tokens=max_tokens, temperature=temperature)
