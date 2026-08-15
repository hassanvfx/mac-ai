"""Inspect a pretrained Transformer manually and through a pipeline.

Install once (the pretrained model is cached outside this repository):

    uv sync --group transformers

Run with MPS when available, otherwise CPU:

    uv run --group transformers python experiments/06-transformers/inspect_sentiment.py

The model is a compact binary sentiment classifier. Its predictions illustrate
the inference path; they are not a benchmark of sentiment accuracy or safety.
"""

from __future__ import annotations

import argparse
import json
from importlib.metadata import version
from time import perf_counter

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

from from_tensors_to_agents.transformers import (
    DEFAULT_MODEL_ID,
    DEFAULT_TEXTS,
    compare_predictions,
    ranked_labels,
    tokenization_summary,
    transformer_device,
)


def run(
    *, model_id: str = DEFAULT_MODEL_ID, device_name: str = "auto", max_length: int = 64
) -> dict[str, object]:
    """Load a fixed model and compare direct PyTorch with a pipeline call."""
    device = transformer_device(device_name)
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSequenceClassification.from_pretrained(model_id).to(device)
    model.eval()

    tokenizations = [tokenization_summary(tokenizer, text, max_length) for text in DEFAULT_TEXTS]
    manual_results: list[dict[str, object]] = []
    start = perf_counter()
    with torch.inference_mode():
        for text in DEFAULT_TEXTS:
            encoded = tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=max_length,
            ).to(device)
            logits = model(**encoded).logits[0]
            manual_results.append(
                {
                    "text": text,
                    "ranked_labels": ranked_labels(logits, model.config.id2label),
                }
            )
    if device.type == "mps":
        torch.mps.synchronize()
    manual_elapsed_ms = (perf_counter() - start) * 1_000

    classifier = pipeline(
        "text-classification",
        model=model,
        tokenizer=tokenizer,
        device=device,
    )
    pipeline_results = classifier(list(DEFAULT_TEXTS), truncation=True, max_length=max_length)
    comparisons = [
        compare_predictions(
            manual_result["ranked_labels"], pipeline_result
        )
        for manual_result, pipeline_result in zip(manual_results, pipeline_results, strict=True)
    ]
    return {
        "model_id": model_id,
        "model_revision": getattr(model.config, "_commit_hash", None),
        "torch_version": torch.__version__,
        "transformers_version": version("transformers"),
        "device": str(device),
        "mps_available": torch.backends.mps.is_available(),
        "max_length": max_length,
        "tokenizations": tokenizations,
        "manual_results": manual_results,
        "pipeline_results": pipeline_results,
        "comparisons": comparisons,
        "manual_elapsed_ms": manual_elapsed_ms,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=DEFAULT_MODEL_ID)
    parser.add_argument("--device", choices=("auto", "cpu", "mps"), default="auto")
    parser.add_argument("--max-length", type=int, default=64)
    args = parser.parse_args()
    if args.max_length < 2:
        parser.error("--max-length must be at least 2")
    print(json.dumps(run(model_id=args.model, device_name=args.device, max_length=args.max_length), indent=2))


if __name__ == "__main__":
    main()
