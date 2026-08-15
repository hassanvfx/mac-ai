---
sidebar_position: 3
title: Building a Neural Network with PyTorch
---

# Building a Neural Network with PyTorch

## Intuition

A neural network becomes useful only when its parameters participate in a
repeatable cycle: make a prediction, measure error, compute gradients, and
update the parameters. PyTorch exposes that cycle directly. That visibility is
valuable at the start because it lets us connect the tensor shapes from Chapter
1 and gradients from Chapter 2 to an actual learning system.

![The explicit six-step PyTorch training loop.](../assets/day1/training-loop.png)

## Problem

Build the smallest network that can learn a known relationship without hiding
the training loop behind a high-level trainer. The fixed task is 64 synthetic
pairs generated from `target = 2 × input + 0.5`. The model is:

```text
Linear(1, 8) → Tanh → Linear(8, 1)
```

This network has more capacity than the linear target requires. That is
intentional: it demonstrates the standard PyTorch components while retaining a
small, deterministic workload whose behavior is easy to inspect.

## Minimal implementation

Run the complete training example:

```bash
uv run python experiments/03-pytorch/train_tiny_network.py
```

The script selects Apple MPS when the installed PyTorch build reports it as
available; otherwise it falls back safely to CPU. It fixes the random seed to
`7`, trains for 250 epochs with SGD and mean squared error, and prints the
first and final losses.

## Real implementation: make the observation reproducible

The benchmark runner makes device selection, warmup, synchronization, number
of timed runs, and seed explicit:

```bash
uv run python benchmarks/01-day1/run.py --device auto --epochs 250 --runs 5 --seed 7
```

On the recorded M4 Pro environment (macOS 26.1, Python 3.11.9, PyTorch 2.13.0),
MPS was available. Five timed runs reached the same final loss, `0.000994`,
from an initial loss of `1.892602`; their median wall time was 120.537 ms.
The complete workload, individual values, and limitations are recorded at
`benchmarks/01-day1/README.md` in the companion repository.

This is evidence about one tiny synthetic workload on one machine. It is not a
claim that MPS is faster than CPU, nor a prediction about larger networks.

## Experiment

Run the benchmark once with `--device cpu` and, on an MPS-capable Mac, once
with `--device mps`. Do not compare only the median number: first confirm the
same seed, epochs, versions, warmup procedure, and final loss. Then increase
the epoch count and observe whether setup time becomes a smaller fraction of
the measurement. Record every changed condition rather than overwriting the
existing observation.

## What broke

Accelerator availability is conditional. The example must run on CPU-only
machines, and an explicit `--device mps` request fails clearly if MPS is
unavailable. Also, accelerator work may be queued: timing without an MPS
synchronization can stop the clock before all device work finishes. The
benchmark runner synchronizes before and after each timed run for that reason.

## Alternatives and when to use them

For a first prototype, an explicit loop is the best choice because every step
is inspectable. Higher-level PyTorch training frameworks can reduce repetition
after the fundamentals are understood. For a strictly linear relationship, a
single `Linear(1, 1)` model is simpler; the small hidden layer here exists to
teach composition, not because the data demands it.

## Takeaway

PyTorch training is a controlled feedback loop. A useful result is not merely a
lower loss: it is a lower loss tied to a known seed, dataset, model, device,
measurement method, and record of what the result does *not* prove.
