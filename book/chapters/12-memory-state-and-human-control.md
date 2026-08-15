---
sidebar_position: 12
title: Memory, State and Human Control
---

# Memory, State and Human Control

## Intuition

Thread state, long-term memory, and checkpoints solve different continuity problems.

## Problem

Add proposal persistence and a human approval point without confusing retrieved
book evidence with the current task state.

## Minimal implementation

The companion graph will checkpoint retrieval, plan, critique, and approval
state separately from the read-only book corpus.

## Experiment

Compare an interrupted run with an uninterrupted one.

## What broke

Record stale memory, unsafe approval bypasses, and migration issues.

## Alternatives and takeaway

Human control is a designed transition, not an afterthought.
