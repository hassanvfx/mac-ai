"""Pure helpers shared by the MLX/MLX-LM local-inference experiment."""

from __future__ import annotations

from typing import Any

DEFAULT_MLX_MODEL_ID = "mlx-community/Qwen2.5-0.5B-Instruct-4bit"
DEFAULT_MLX_PROMPT = "In one short sentence, explain why an experiment record needs a seed."


def validate_generation_settings(*, max_tokens: int, temperature: float) -> None:
    """Reject unsafe or ambiguous benchmark settings before a model is loaded."""
    if max_tokens < 1:
        raise ValueError("max_tokens must be at least 1")
    if temperature < 0:
        raise ValueError("temperature must be non-negative")


def generation_record(response: Any) -> dict[str, float | int | str | None]:
    """Extract stable, JSON-safe metrics from MLX-LM's final stream response."""
    return {
        "prompt_tokens": int(response.prompt_tokens),
        "prompt_tokens_per_second": float(response.prompt_tps),
        "generated_tokens": int(response.generation_tokens),
        "generated_tokens_per_second": float(response.generation_tps),
        "mlx_reported_peak_memory_gib": float(response.peak_memory),
        "finish_reason": response.finish_reason,
    }
