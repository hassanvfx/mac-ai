# Milestone 5 workflow-shape comparison

The frozen fixture compares deterministic, single-planner, and
researcher/critic/writer workflows on one book-maintenance task. Each path
retrieved `research/embeddings.md`, flagged the draft chapter's missing
Alternatives section, required approval, and performed no write. The result is
contract coverage only—not model quality, latency, or multi-agent performance.

Run:

```bash
uv run --group agents python experiments/13-workflows/compare_workflows.py
```
