---
sidebar_position: 10
title: From LLM Calls to AI Systems
---

# From LLM Calls to AI Systems

## Intuition

LangChain is integration and orchestration around a model, not the intelligence itself.

## Problem

Connect models, messages, structured output, retrievers, and tools without
losing visibility into the Book Intelligence Assistant’s evidence.

## Minimal implementation

The companion project will compare a direct structured plan/review call with a
LangChain composition over the same retrieved book evidence.

## Experiment

Compare direct SDK calls with the composed workflow.

## What broke

Record schema, tool-call, and context failures.

## Alternatives and takeaway

Use an abstraction only when it makes the system easier to change or observe.
