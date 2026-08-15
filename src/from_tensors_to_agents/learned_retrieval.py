"""Optional local learned-embedding retrieval over existing book evidence."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

import numpy as np

from from_tensors_to_agents.book_intelligence import Evidence, SearchResult, grounded_evidence

DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class Encoder(Protocol):
    def encode(self, sentences: Sequence[str], **kwargs: object) -> np.ndarray: ...


@dataclass(frozen=True)
class LearnedIndex:
    evidence: tuple[Evidence, ...]
    vectors: np.ndarray
    model_id: str


def normalize_rows(vectors: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return np.divide(vectors, norms, out=np.zeros_like(vectors), where=norms != 0)


def build_learned_index(evidence: Sequence[Evidence], encoder: Encoder, model_id: str) -> LearnedIndex:
    items = tuple(evidence)
    if not items:
        return LearnedIndex(items, np.empty((0, 0), dtype=np.float64), model_id)
    vectors = np.asarray(encoder.encode([item.text for item in items]), dtype=np.float64)
    if vectors.ndim != 2 or vectors.shape[0] != len(items):
        raise ValueError("encoder must return one two-dimensional vector per evidence item")
    return LearnedIndex(items, normalize_rows(vectors), model_id)


def retrieve_learned(index: LearnedIndex, query: str, encoder: Encoder, limit: int = 4) -> list[SearchResult]:
    if not index.evidence or not query.strip():
        return []
    query_vector = normalize_rows(np.asarray(encoder.encode([query]), dtype=np.float64))[0]
    scores = index.vectors @ query_vector
    ranked = [SearchResult(evidence=item, score=float(scores[position])) for position, item in enumerate(index.evidence)]
    return sorted(ranked, key=lambda item: (-item.score, item.evidence.source))[:limit]


def learned_grounded_answer(
    index: LearnedIndex,
    query: str,
    encoder: Encoder,
    limit: int = 3,
    minimum_score: float = 0.25,
) -> str:
    """Return retrieved excerpts only, or explicitly refuse weak learned retrieval."""
    results = [
        result
        for result in retrieve_learned(index, query, encoder, limit)
        if result.score >= minimum_score
    ]
    return grounded_evidence(results)


def load_encoder(model_id: str = DEFAULT_EMBEDDING_MODEL) -> Encoder:
    """Load a local/cached sentence-transformer only when the optional path runs."""
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(model_id)
