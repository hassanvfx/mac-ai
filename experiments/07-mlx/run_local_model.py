"""Run one declared local MLX-LM workload on Apple Silicon.

Install the optional group after checking storage:

    df -h .
    uv sync --group mlx

The first run downloads the declared 4-bit model to the local Hugging Face
cache, not this Git repository:

    uv run --group mlx python experiments/07-mlx/run_local_model.py

This prints an observation record. It is not a quality evaluation or a fair
comparison with PyTorch or another local-runtime configuration.
"""

from __future__ import annotations

import argparse
import json
from importlib.metadata import version
from time import perf_counter

import mlx.core as mx
import psutil
from mlx_lm import load, stream_generate
from mlx_lm.sample_utils import make_sampler

from from_tensors_to_agents.local_models import (
    DEFAULT_MLX_MODEL_ID,
    DEFAULT_MLX_PROMPT,
    generation_record,
    validate_generation_settings,
)


def chat_prompt(tokenizer: object, prompt: str) -> str:
    """Apply the declared one-message chat framing used by the model."""
    apply_template = getattr(tokenizer, "apply_chat_template", None)
    if not callable(apply_template):
        raise TypeError("The selected model tokenizer has no chat template.")
    return apply_template(
        [{"role": "user", "content": prompt}],
        tokenize=False,
        add_generation_prompt=True,
    )


def run(
    *,
    model_id: str = DEFAULT_MLX_MODEL_ID,
    prompt: str = DEFAULT_MLX_PROMPT,
    max_tokens: int = 64,
    temperature: float = 0.0,
) -> dict[str, object]:
    """Load, warm up, and stream one deterministic local generation."""
    validate_generation_settings(max_tokens=max_tokens, temperature=temperature)
    process = psutil.Process()
    rss_before_load = process.memory_info().rss
    mx.reset_peak_memory()
    load_start = perf_counter()
    model, tokenizer = load(model_id)
    load_elapsed_ms = (perf_counter() - load_start) * 1_000
    rendered_prompt = chat_prompt(tokenizer, prompt)
    rss_after_load = process.memory_info().rss

    # Warm-up is not included in the measured result. A short deterministic
    # generation makes lazy runtime initialization visible without changing the
    # declared measurement prompt.
    sampler = make_sampler(temp=temperature)
    for _ in stream_generate(model, tokenizer, rendered_prompt, max_tokens=4, sampler=sampler):
        pass
    mx.reset_peak_memory()
    rss_before_generation = process.memory_info().rss
    generation_start = perf_counter()
    pieces: list[str] = []
    final_response = None
    for response in stream_generate(
        model,
        tokenizer,
        rendered_prompt,
        max_tokens=max_tokens,
        sampler=sampler,
    ):
        pieces.append(response.text)
        final_response = response
    generation_elapsed_ms = (perf_counter() - generation_start) * 1_000
    if final_response is None:
        raise RuntimeError("MLX-LM yielded no generation response.")

    return {
        "model_id": model_id,
        "mlx_version": version("mlx"),
        "mlx_lm_version": version("mlx-lm"),
        "quantization": "4-bit (as declared by the selected MLX Community model name)",
        "prompt": prompt,
        "rendered_prompt_token_count": len(tokenizer.encode(rendered_prompt)),
        "max_tokens": max_tokens,
        "temperature": temperature,
        "warmup_tokens": 4,
        "load_elapsed_ms": load_elapsed_ms,
        "generation_elapsed_ms": generation_elapsed_ms,
        "completion": "".join(pieces),
        "generation": generation_record(final_response),
        "memory_observation": {
            "method": "process RSS via psutil plus MLX Metal active/peak memory after warmup",
            "process_rss_before_load_bytes": rss_before_load,
            "process_rss_after_load_bytes": rss_after_load,
            "process_rss_before_generation_bytes": rss_before_generation,
            "metal_active_memory_bytes": int(mx.get_active_memory()),
            "metal_peak_memory_bytes": int(mx.get_peak_memory()),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=DEFAULT_MLX_MODEL_ID)
    parser.add_argument("--prompt", default=DEFAULT_MLX_PROMPT)
    parser.add_argument("--max-tokens", type=int, default=64)
    parser.add_argument("--temperature", type=float, default=0.0)
    args = parser.parse_args()
    try:
        result = run(
            model_id=args.model,
            prompt=args.prompt,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
        )
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
