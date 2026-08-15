# Milestone 5 structured-adapter observation

## Contract

This record compares the *contract handling* of the direct SDK and LangChain
paths. It does not compare model quality, API latency, token usage, price, or
provider reliability, because no configured remote model was invoked.

| Field | Value |
| --- | --- |
| Script | `experiments/10-systems/compare_structured_planning.py` |
| Dependency group | `agents` |
| Direct package | `openai` 2.54.0 |
| Composed packages | `langchain` 1.3.15; `langchain-openai` 1.5.1 |
| Model endpoint | no network endpoint used in the recorded fixture run |
| Input | the same deterministically retrieved book-corpus paths for both adapters |
| Output policy | Pydantic schema, allowed-path filtering, warning on unsupported paths, approval always required |
| Writes | none; checkpoint/index output remains local only |

## Recorded no-network run — 2026-08-14

```bash
uv run --group agents python experiments/10-systems/compare_structured_planning.py
```

Both fixture adapters returned
`book/chapters/08-turning-meaning-into-geometry.md` as their allowed path and
reported `approval required: True`. Unit tests additionally verified that an
invented `outside.md` path is rejected, an empty evidence set receives no
implementation steps, malformed LangChain output stops the workflow, and a
missing environment configuration stops before a network call.

## Limits and next experiment

This proves only local adapter behavior using fixtures. A later controlled API
experiment must declare provider, endpoint type, model revision, prompt,
schema mode, retries, timing boundary, token accounting, redaction policy, and
sampled results before drawing a model/provider comparison.
