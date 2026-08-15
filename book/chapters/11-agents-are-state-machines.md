---
sidebar_position: 11
title: Agents Are State Machines with an LLM Inside
---

# Agents Are State Machines with an LLM Inside

## Intuition

An agentic system is state plus steps plus decisions; an LLM is one possible
decision-maker inside that graph.

## Problem

Build a routed book-maintenance flow with explicit state and conditional edges.

## Minimal implementation

Run [approval_checkpoint.py](../../experiments/11-langgraph/approval_checkpoint.py).
The baseline flow persists a proposal and cannot edit source files; the
LangGraph implementation will preserve that same approval boundary.

## Experiment

Compare deterministic routing with LLM-selected routing.

## What broke

Record loops, invalid state, and ambiguous routing.

## Alternatives and takeaway

Use a workflow when the path is known; use an agentic graph only when judgment helps.
