# MLX and local-inference notes

The local-inference experiment is intentionally a single, inspectable MLX-LM
observation. It uses `mlx-community/Qwen2.5-0.5B-Instruct-4bit`, not the
MLX-LM default 3B model, so the project can begin with a modest cache while
preserving space for later fixtures. The runnable script and exact observation
are `experiments/07-mlx/run_local_model.py` and
`benchmarks/04-mlx/README.md`.

Important boundaries:

- The `4bit` portion of the model identifier is the model publisher's declared
  quantization, not a measurement by this project.
- The model response is an example of local generation, not an answer-quality
  evaluation. It ends at the requested token limit and is not judged correct.
- MLX reports Metal active and peak memory in bytes. MLX-LM's stream response
  exposes a separate peak-memory field in GiB. Process RSS is another partial
  observation. Unified memory means none of these fields alone is total system
  memory use.
- A single warmed-up generation rate is an observation for the exact model,
  prompt, max token count, and package versions. It must not be compared to the
  PyTorch classifier's two-sentence forward pass.

API and usage details follow [@mlx_lm2026].
