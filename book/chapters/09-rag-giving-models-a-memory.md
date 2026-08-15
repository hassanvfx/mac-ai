---
sidebar_position: 9
title: "RAG: Giving Models a Memory They Never Learned"
---

# RAG: Giving Models a Memory They Never Learned

## Intuition

Retrieval gives a model relevant external context at answer time.

## Problem

Construct the book-corpus document-to-answer pipeline explicitly before hiding
it behind APIs.

## Minimal implementation

Run [grounded_answer.py](../../experiments/09-rag/grounded_answer.py). It returns
only retrieved excerpts and source paths; a query without evidence is refused.

## Experiment

Compare prompting alone, retrieved evidence, and a deliberately weak retrieval
setup with missing context.

## What broke

Record missing context, poor chunks, and unsupported answers.

## Alternatives and takeaway

RAG changes available context; it does not train new model weights. Grounding is
only meaningful when a reader can inspect the cited evidence.
