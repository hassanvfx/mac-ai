---
sidebar_position: 1
title: Everything Is a Tensor
---

# Everything Is a Tensor

## Intuition

A tensor is a collection of numbers with a shape. The numbers carry values;
the shape says how to interpret them. A scalar has shape `()`, a list of three
measurements has shape `(3,)`, a two-row table has shape `(2, 3)`, and a batch
of color images commonly has four axes: `(batch, height, width, channels)` or
`(batch, channels, height, width)`. The central habit of machine learning is
to ask what every axis means before asking which model to use.

This is more than vocabulary. Linear algebra lets one operation describe many
examples at once, and tensor libraries make that operation executable on CPUs
and accelerators. The representation is therefore the bridge between a
mathematical expression and a training program [@goodfellow2016deep].

## Problem

Suppose two examples each have three features and we want to add a different
offset to each feature. We want one vector of offsets to apply to every row,
not a manual loop that can quietly confuse examples with features. The desired
calculation is:

```text
(2, 3) batch + (3,) bias → (2, 3) result
```

The second operand is *broadcast* across the leading batch axis. Broadcasting
is concise, but it is also a common source of silent mistakes: `(3,)` means
something very different from `(3, 1)`.

## Minimal implementation

Run the complete example:

```bash
uv run python experiments/01-tensors/broadcasting.py
```

The program adds `[0.1, 0.2, 0.3]` to each row of a `(2, 3)` tensor. Predict
the result before running it. The expected first row is `[1.1, 2.2, 3.3]`; if
you instead expected each number in the first column to change by `0.1`, you
have correctly identified the feature axis.

## A more realistic implementation

Neural-network batches use the same idea at larger scale. A linear layer maps
an input batch `X` with shape `(batch, input_features)` to an output with
shape `(batch, output_features)`:

```text
X @ Wᵀ + b
```

Here `b` has shape `(output_features,)` and broadcasts once per example. The
operation preserves the batch axis, replaces the feature axis, and gives one
output vector per input. Writing those shapes beside the expression prevents
many errors before Python runs.

## Experiment

Change the bias in `experiments/01-tensors/broadcasting.py` from `(3,)` to
`(2, 1)`. First predict the new result. Then deliberately try an incompatible
shape such as `(2,)` and read PyTorch’s error message. Record which axes you
thought were aligned and which axes PyTorch attempted to align.

## What broke

The most useful early failure is a shape mismatch. Do not immediately reshape
until the error disappears. State the intended meaning of each axis and verify
that the reshape preserves it. A technically valid reshape can still be a
conceptual bug—for example, mixing examples across a batch or treating image
width as channels.

## Alternatives and when to use them

Python lists work for tiny demonstrations, and NumPy uses the same broad
array-and-broadcasting model. Use PyTorch tensors when the next step needs
automatic differentiation, neural-network modules, or accelerator placement.
Avoid a tensor library abstraction only when the data is truly irregular and a
named record or graph structure communicates the domain better.

## Takeaway

Tensors are not merely containers. Their shapes are part of the program’s
meaning. Before changing an operation, name every axis, write the input and
output shapes, and decide exactly which axes may broadcast.
