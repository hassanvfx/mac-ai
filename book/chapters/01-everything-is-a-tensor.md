---
sidebar_position: 1
title: Everything Is a Tensor
---

# Everything Is a Tensor

## Intuition

A tensor is a container for numbers plus a shape. The shape tells us how those
numbers relate: one measurement, a list of measurements, an image, or a batch.

## Problem

We need one representation that lets the same program work on a scalar, a
vector, and thousands of examples at once.

## Minimal implementation

Run [the broadcasting experiment](../../experiments/01-tensors/broadcasting.py).

## Experiment

Add a vector to each row of a matrix and predict the resulting shape before
running the program.

## What broke

Write down any shape mismatch before fixing it; shape errors are often the most
useful first signal that a model’s assumptions are wrong.

## Alternatives and takeaway

Arrays are not merely storage. Their dimensions express the structure that
each mathematical operation is allowed to preserve or transform.
