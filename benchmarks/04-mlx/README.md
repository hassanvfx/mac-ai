# Milestone 3 MLX-LM local-inference record

## Contract

This record captures one local, deterministic sampling run with MLX-LM on the
target Apple Silicon Mac. It is designed to make model identity, quantization,
prompt framing, timing boundaries, and memory observations explicit—not to rank
local runtimes or establish answer quality.

| Field | Value |
| --- | --- |
| Script | `experiments/07-mlx/run_local_model.py` |
| Dependency group | `mlx` (`mlx` 0.31.2; `mlx-lm` 0.31.3) |
| Model | `mlx-community/Qwen2.5-0.5B-Instruct-4bit` |
| Quantization | 4-bit, as declared in the selected MLX Community model identifier |
| Prompt | `In one short sentence, explain why an experiment record needs a seed.` |
| Prompt framing | Model tokenizer's one-user-message chat template with generation prompt |
| Sampling | temperature 0.0; max 64 generated tokens |
| Warmup | one unmeasured 4-token generation after model load |
| Timing boundary | measured streamed generation after warmup; excludes first download and model load |
| Cache | First download produced approximately 276 MiB in the local Hugging Face cache, outside Git |

## Recorded run — 2026-08-14

| Observation | Value |
| --- | --- |
| Rendered prompt tokens | 43 |
| Generated tokens | 64 (`length` stop) |
| Generation elapsed time | 290.701 ms |
| MLX-LM generated tokens/s | 342.260 |
| MLX-LM prompt tokens/s | 2016.035 |
| Model load elapsed time | 542.927 ms (recorded separately; excluded from generation timing) |
| Process RSS before/after load | 333,725,696 / 785,121,280 bytes |
| Process RSS before measured generation | 796,934,144 bytes |
| MLX Metal active / peak memory after warmup | 281,784,072 / 345,934,496 bytes |
| MLX-LM response peak memory | 0.345934496 GiB |

The generated completion was saved in the direct command output during the run.
It was not evaluated for factual quality and ended because the declared maximum
of 64 tokens was reached.

## Memory method and limitations

The script records three partial views: process resident-set size from `psutil`,
MLX Metal active/peak memory in bytes, and the peak-memory figure emitted by
MLX-LM in GiB. These fields do not add into a reliable total. Apple Silicon's
unified-memory design, allocator caches, other processes, and OS accounting
make a single value insufficient to establish memory use or capacity.

Likewise, the generated-tokens-per-second value is one warmed-up observation
for this one 4-bit model, one prompt, 64-token limit, and exact package
versions. It is **not** comparable with PyTorch MPS, TensorFlow, the Chapter 6
classifier, a different quantization, or a different prompt length. A future
cross-runtime benchmark must normalize model, prompt, output length, warmups,
run count, timing boundary, and memory method first.
