# Day 1 benchmark record

## Purpose and limitations

This record measures the fixed synthetic regressor used in Chapter 3. It is a
teaching workload—64 scalar samples, a `1 → 8 → 1` network, SGD, and 250
epochs—not a general comparison of hardware, frameworks, or real-world model
training. Values from another machine, dependency version, power mode, or
workload are not directly comparable.

## Reproduction command

```bash
uv run python benchmarks/01-day1/run.py --device auto --epochs 250 --runs 5 --seed 7
```

The runner performs one unmeasured warmup, synchronizes MPS immediately before
and after each timed run, and reports the median of five `perf_counter` wall
times. It selects CPU when MPS is unavailable. Use `--device cpu` or
`--device mps` only when a device-specific observation is intended.

## Recorded observation

| Field | Value |
| --- | --- |
| Date | 2026-08-14 |
| Host platform | macOS 26.1, arm64 |
| Python / PyTorch | 3.11.9 / 2.13.0 |
| Requested / selected device | `auto` / `mps` |
| MPS available | `True` |
| Seed / epochs / timed runs | `7 / 250 / 5` |
| Dataset / model | 64 synthetic scalar pairs; `Linear(1, 8) → Tanh → Linear(8, 1)` |
| Optimizer / loss | SGD (`lr=0.08`) / mean squared error |
| Initial / final loss | `1.892602 / 0.000994` |
| Timed wall-clock values | 120.537, 122.571, 119.637, 121.099, 119.836 ms |
| Median wall-clock time | **120.537 ms** |
| Determinism check | All five timed runs reached final loss `0.000994` |
| Memory observation | Not collected; this small workload is not evidence for unified-memory claims. |

## Interpretation

The example converged deterministically for this fixed seed and environment,
and Apple MPS was available. The measurement says only that this exact
educational workload completed with the recorded timing on this machine. It
does not establish that MPS is faster than CPU, that results generalize to
larger models, or that all PyTorch operations are MPS-compatible.
