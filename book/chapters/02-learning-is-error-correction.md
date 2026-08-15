---
sidebar_position: 2
title: Learning Is Error Correction
---

# Learning Is Error Correction

## Intuition

Learning begins with a disagreement: a model makes a prediction, a target says
what should have happened, and a loss function turns their difference into one
number. A gradient then answers a local question: if a parameter moves a tiny
amount, how does that loss change? It is not a learning rule by itself. It is
the measurement used by an optimizer to choose a corrective step
[@goodfellow2016deep].

## Problem

Take the one-parameter model `prediction = 2 × weight`, target `10`, and
squared error loss `(prediction - target)²`. With `weight = 3`, the prediction
is `6`, the loss is `16`, and the analytic derivative is:

```text
d/d(weight) (2 × weight - 10)² = 4 × (2 × weight - 10) = -16
```

The negative value means that a small increase in this particular weight
reduces the loss locally. The goal is to verify that PyTorch’s autograd system
constructs the same derivative from ordinary tensor operations.

![The forward pass computes a loss; the backward pass propagates its gradient to the parameter.](../assets/day1/gradient-flow.png)

## Minimal implementation

```bash
uv run python experiments/02-gradients/autograd.py
```

The expected output is a prediction of `6.0`, a loss of `16.0`, and
`d(loss)/d(weight)=-16.0`. The automated test independently verifies that
analytic result in `tests/test_day1.py`.

## A more realistic implementation

Real models contain many parameters and nested functions. Rather than writing
one derivative per parameter, PyTorch records the operations used to produce a
loss. Calling `loss.backward()` applies the chain rule through that recorded
computation. An optimizer then reads each parameter’s `.grad` value and
updates it. The common training-loop order is:

```text
zero old gradients → forward pass → loss → backward pass → optimizer step
```

The order matters. Gradients accumulate by default because accumulation is
useful for some workloads. In ordinary minibatch training, failing to clear
them combines the current gradient with stale work from previous steps.

## Experiment

Change the starting weight and target in the autograd script. Calculate the
derivative on paper before execution, then compare it with `weight.grad`.
Next, call `backward()` twice without clearing the gradient and observe the
accumulation. Finally, reset the gradient and explain why the normal training
loop performs that reset before every forward pass.

## What broke

Two beginner errors reveal important boundaries. A tensor without
`requires_grad=True` does not request a derivative with respect to itself.
And calling `backward()` after discarding or mutating a computation graph can
produce an error because autograd needs the original operations. The repair is
not to memorize error messages; it is to identify which values are parameters,
which values are observations, and which loss produced the gradient.

## Alternatives and when to use them

For a one-variable function, symbolic or hand differentiation is clearer and
often safer. Finite differences are useful as a slow diagnostic check. Use
reverse-mode automatic differentiation when one scalar loss depends on many
parameters—the standard setting for neural-network training.

## Takeaway

Loss measures error, gradients measure local sensitivity, and an optimizer
chooses the update. Keeping those roles separate makes backpropagation
understandable rather than magical.
