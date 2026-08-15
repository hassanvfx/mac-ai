---
sidebar_position: 3
title: Building a Neural Network with PyTorch
---

# Building a Neural Network with PyTorch

## Intuition

Parameters become useful only inside a repeatable train–measure–adjust loop.

## Problem

Build the smallest model that learns a known relationship without hiding the
training loop behind a high-level API.

## Minimal implementation

Run [the tiny network experiment](../../experiments/03-pytorch/train_tiny_network.py).

## Experiment

Compare initial and final loss on MPS and CPU; record results in the Day 1
benchmark log in the companion repository.

## What broke

Record device availability, seed effects, and any operation that cannot run on
MPS.

## Alternatives and takeaway

PyTorch makes the training loop explicit, so its abstractions remain visible
while we learn.
