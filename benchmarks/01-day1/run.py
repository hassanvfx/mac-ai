"""Measure the fixed Day 1 PyTorch training workload on CPU or Apple MPS.

Examples:

    uv run python benchmarks/01-day1/run.py --device auto
    uv run python benchmarks/01-day1/run.py --device cpu --runs 5

The runner intentionally reports a small synthetic workload. Its timings are
useful for documenting the learning example on one machine, not for making
general framework or hardware performance claims.
"""

from __future__ import annotations

import argparse
import platform
import statistics
import time

import torch

from from_tensors_to_agents.training import train_tiny_regressor


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", choices=("auto", "cpu", "mps"), default="auto")
    parser.add_argument("--epochs", type=int, default=250)
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--seed", type=int, default=7)
    return parser.parse_args()


def select_device(requested: str) -> torch.device:
    if requested == "cpu":
        return torch.device("cpu")
    if requested == "mps":
        if not torch.backends.mps.is_available():
            raise RuntimeError("MPS was requested but is not available in this PyTorch build.")
        return torch.device("mps")
    return torch.device("mps" if torch.backends.mps.is_available() else "cpu")


def synchronize(device: torch.device) -> None:
    """Wait for queued MPS work so elapsed time covers the full workload."""
    if device.type == "mps":
        torch.mps.synchronize()


def main() -> None:
    args = parse_args()
    if args.epochs < 1 or args.runs < 1:
        raise ValueError("--epochs and --runs must both be at least 1")

    device = select_device(args.device)
    # One warmup prevents one-time device setup from contaminating timed runs.
    train_tiny_regressor(epochs=args.epochs, seed=args.seed, device=device)
    synchronize(device)

    durations_ms: list[float] = []
    final_losses: list[float] = []
    for _ in range(args.runs):
        synchronize(device)
        started = time.perf_counter()
        losses = train_tiny_regressor(epochs=args.epochs, seed=args.seed, device=device)
        synchronize(device)
        durations_ms.append((time.perf_counter() - started) * 1_000)
        final_losses.append(losses[-1])

    print("--- Day 1 benchmark metadata ---")
    print(f"platform={platform.platform()}")
    print(f"python={platform.python_version()} torch={torch.__version__}")
    print(f"device={device.type} mps_available={torch.backends.mps.is_available()}")
    print(f"seed={args.seed} epochs={args.epochs} timed_runs={args.runs}")
    print(f"median_wall_time_ms={statistics.median(durations_ms):.3f}")
    print(f"all_wall_time_ms={[round(value, 3) for value in durations_ms]}")
    print(f"final_loss={final_losses[-1]:.6f} deterministic={len(set(final_losses)) == 1}")


if __name__ == "__main__":
    main()
