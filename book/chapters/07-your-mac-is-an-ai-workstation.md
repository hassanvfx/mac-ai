---
sidebar_position: 7
title: Your Mac Is an AI Workstation
---

# Your Mac Is an AI Workstation

## Intuition

Apple Silicon uses unified memory: the CPU and GPU-accessible parts of a system
share a memory pool rather than copying every model tensor through a separate
GPU memory space. That can make local inference practical, but it does not make
memory infinite or a model automatically fast. Model size, quantization, prompt
length, generated tokens, allocator behavior, and other applications all still
matter.

Unified memory changes a systems boundary, not the laws of capacity. A local
model, its tokenizer, generated-token cache, application process, browser, and
the operating system all compete for one finite pool. Quantization stores some
model weights with fewer bits, but it does not remove every runtime allocation
or make a model's context free. The practical question is therefore not whether
an advertised parameter count sounds small, but whether this exact model and
workload leave enough headroom for the rest of the machine.

Storage and memory are separate constraints. The first model download needs
disk space for weights and tokenizer files; a later generation needs available
unified memory for the loaded model, runtime buffers, prompt, key/value cache,
and everything else running on the Mac. Checking `df -h .` before an optional
download prevents a simple disk failure, but it says nothing about whether a
long prompt will fit comfortably at inference time.

## Problem

Run one local MLX-LM inference workload whose inputs and measurement boundary
are visible. A fair PyTorch-MPS-versus-MLX comparison comes later, after the
same generative model and protocol are available in both runtimes.

That restraint prevents an invalid comparison. Chapter 3 measures a tiny
PyTorch training loop; Chapter 6 runs a classifier; this chapter streams a
quantized instruction model. Their elapsed times represent different tasks,
token counts, warm-up behavior, and memory methods. A “fastest runtime” table
would look precise while answering no coherent engineering question.

## Minimal implementation

Install the Apple-Silicon-only optional group and run the complete example:

```bash
uv sync --group mlx
uv run --group mlx python experiments/07-mlx/run_local_model.py
```

The initial experiment uses
`mlx-community/Qwen2.5-0.5B-Instruct-4bit`: a local instruction model whose
identifier declares 4-bit quantization. It sends one fixed prompt through the
model's chat template, performs an unmeasured four-token warm-up, and measures
one deterministic (`temperature=0`) streamed generation capped at 64 tokens.
The MLX-LM package provides model loading and generation on Apple Silicon
[@mlx_lm2026].

Read the model identifier as experiment configuration. `Qwen2.5-0.5B` names a
particular model family and approximate parameter scale; `Instruct` signals a
chat-oriented variant; `4bit` describes the published quantized artifact. None
of those words guarantees factual output, a particular memory footprint, or
compatibility with another runtime. Record the complete identifier rather than
shortening it to a family name, because a later revision or quantization can
materially change the workload.

## Real implementation: state the measurement boundary

`experiments/07-mlx/run_local_model.py` records model/package versions, model
identifier, prompt, rendered prompt-token count, token limit, temperature,
warm-up, load time, generation time, and token rates. It also records process
RSS and two MLX memory views: Metal active/peak memory in bytes and MLX-LM's
reported peak memory in GiB. The output labels the units rather than adding
them together, because they are different partial observations.

The measurement boundary matters as much as the number. Download and model
load are user-visible costs for an application, but they answer a different
question from warmed-up generation throughput. The script records them
separately. It also resets MLX peak memory after the warm-up so the reported
generation peak does not accidentally include first-use initialization. That is
not a universal memory accounting method; it is a declared observation method
that a reader can reproduce and improve.

Interpret the fields as a timeline. Model load is the cold-start cost after
weights are locally cached. The warm-up triggers lazy setup but is excluded from
measured generation. The generation timer begins immediately before streaming
and ends after the final response. If an application cares about a first
interactive response, record first-token latency separately; if it cares about
batch throughput, declare batch size and queueing. Do not reuse this one token
rate for either question.

The memory fields are observations with different owners. Process RSS includes
what the operating system attributes to Python; Metal active and peak fields
describe MLX allocator views; MLX-LM returns its own peak figure. They may move
together without being additive. For a longer-context experiment, preserve all
three labels and record a pressure event rather than estimate capacity from one
successful run.

## Experiment

On the recorded Mac, MLX 0.31.2 and MLX-LM 0.31.3 generated 64 tokens after a
43-token rendered prompt in 290.701 ms, reporting 342.260 generated tokens/s.
The model load took 542.927 ms and was deliberately excluded from the generation
timing. MLX Metal reported 281,784,072 active bytes and 345,934,496 peak bytes;
MLX-LM reported 0.345934496 GiB peak memory. The model's local cache occupied
approximately 276 MiB after download. The full contract is recorded at
`benchmarks/04-mlx/README.md`.

These are observations for one exact model, prompt, token limit, package
versions, and warmed-up run. They are not a claim that MLX is faster than
PyTorch MPS, that 4-bit models always fit a given Mac, or that the completion
is correct. The response stopped at the declared 64-token limit and was not
quality-scored.

The fixed prompt exercises chat-template rendering, tokenization, generation,
and stop behavior without claiming to measure reasoning, factuality, safety, or
instruction following. It ends at the configured length limit, so completion
length is a workload parameter rather than a quality signal. A future quality
evaluation needs a versioned prompt set, scoring rubric, and human or task-based
judgments.

## What broke

The first issue was dependency compatibility: MLX-LM 0.31 requires Transformers
5, while the first Chapter 6 draft capped Transformers below 5. The project
resolved this by upgrading the optional Transformers group and rerunning the
Chapter 6 MPS and CPU checks before relying on it. This is why optional groups
still need an integrated lockfile, not isolated installation instructions.

Model download is another boundary. The first run uses the Hugging Face cache
outside Git and may show an unauthenticated-request warning when no Hugging Face
token is configured. A token can improve download limits, but no token or
credential is needed for this public model and none belongs in the repository.

Finally, a memory field is not a capacity guarantee. Unified-memory pressure
can depend on other work running on the computer, caches, and longer prompts.
Check available storage before downloading models and use an explicit workload
before increasing model size or context length.

Classify a local failure before changing frameworks. A missing optional package
is an installation problem; a cache/download error is a storage or network
problem; a chat-template error is a model-interface problem; memory pressure is
a workload/capacity problem; and an unhelpful completion is an evaluation
problem. Each needs a different record and remedy. Collapsing them into “the
model does not work on my Mac” makes the project impossible to reproduce.

## Alternatives and when to use them

Use MLX-LM when you want a native local inference path and can make model,
quantization, cache, memory, and evaluation limits explicit. Use a hosted API
when a model, scale, or operational capability is unavailable locally—but keep
credentials environment-configured and preserve the same evidence discipline.
PyTorch MPS is a valuable alternative for models and training workflows already
expressed in PyTorch. Do not choose on a slogan: choose after measuring the
actual workload.

Smaller task-specific models can be better local choices than a general
instruction model for classification, extraction, or embedding. Quantized
GGUF-style toolchains are another alternative with their own formats and
measurement rules. A remote service can simplify distribution but changes
privacy, cost, latency, and outage behavior. State which trade-off matters
before choosing a runtime.

## Evidence trail

The local-inference note is `research/04-mlx/notes.md`. Run
`experiments/07-mlx/run_local_model.py` only after the documented optional
install, then interpret its one workload through `benchmarks/04-mlx/README.md`.

## Takeaway

Local inference is a systems decision, not only a privacy preference. The
responsible first question is not “how many tokens per second?” but “which model
and quantization, on what prompt, with what cache, memory method, warm-up, and
quality boundary?”
