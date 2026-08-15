---
sidebar_position: 2
title: Learning Is Just Error Correction
---

# Learning Is Just Error Correction

## Intuition

A loss names the error; a gradient describes how that error changes locally.

## Problem

How can a program change a parameter in a direction that reduces error?

## Minimal implementation

Run [the autograd experiment](../../experiments/02-gradients/autograd.py).

## Experiment

Change the initial weight and target, calculate the gradient by hand, then
compare it with autograd.

## What broke

Gradients accumulate by default. Explain why an optimizer clears them before a
new training step.

## Alternatives and takeaway

Backpropagation is efficient bookkeeping for the chain rule, not magic.
