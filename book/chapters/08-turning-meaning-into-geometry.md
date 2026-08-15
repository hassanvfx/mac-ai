---
sidebar_position: 8
title: Turning Meaning Into Geometry
---

# Turning Meaning Into Geometry

## Intuition

Embeddings map text into a space where distance can approximate semantic relation.

## Problem

Build semantic search over the book corpus before introducing an orchestration
framework or external vector database.

## Minimal implementation

Run [book_search.py](../../experiments/08-embeddings/book_search.py). It creates
a deterministic local index and preserves each result’s repository path,
chapter identifier, citation keys, and corpus kind.

## Experiment

Compare the deterministic hashed embedding ranking with keyword retrieval on
questions about experiments, benchmarks, and citations.

## What broke

Capture misleading neighbors and chunk-boundary effects.

## Alternatives and takeaway

Semantic similarity is useful evidence, not a fact guarantee. The later RAG
system must expose the evidence it used.
