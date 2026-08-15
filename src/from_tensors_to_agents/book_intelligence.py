"""A local, read-only retrieval and review system for this book's corpus."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

CORPUS_DIRECTORIES = ("research", "book/chapters", "experiments", "benchmarks")
ALLOWED_SUFFIXES = {".bib", ".md", ".py", ".txt"}
TOKEN_PATTERN = re.compile(r"[A-Za-z0-9_]{2,}")
CITATION_PATTERN = re.compile(r"@([A-Za-z0-9_-]+)")
BIBTEX_ENTRY_PATTERN = re.compile(r"@\w+\s*\{\s*([^,\s]+)")
LINK_PATTERN = re.compile(r"\[[^]]+\]\(([^)]+)\)")


@dataclass(frozen=True)
class Evidence:
    source: str
    kind: str
    chapter: str | None
    citations: tuple[str, ...]
    text: str
    vector: tuple[float, ...]
    metadata: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class SearchResult:
    evidence: Evidence
    score: float


@dataclass(frozen=True)
class ImprovementPlan:
    objective: str
    evidence_paths: tuple[str, ...]
    steps: tuple[str, ...]
    approval_required: bool = True


def tokens(text: str) -> list[str]:
    return [value.lower() for value in TOKEN_PATTERN.findall(text)]


def embedding(text: str, dimensions: int = 256) -> tuple[float, ...]:
    vector = np.zeros(dimensions, dtype=np.float64)
    for token in tokens(text):
        digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
        value = int.from_bytes(digest, "big")
        vector[value % dimensions] += 1 if value & 1 else -1
    norm = np.linalg.norm(vector)
    return tuple((vector / norm) if norm else vector)


def source_kind(relative_path: Path) -> str:
    return relative_path.parts[0] if relative_path.parts else "unknown"


def chapter_identifier(relative_path: Path) -> str | None:
    if relative_path.parts[:2] == ("book", "chapters"):
        return relative_path.stem.split("-", maxsplit=1)[0]
    return None


def evidence_metadata(relative_path: Path) -> tuple[tuple[str, str], ...]:
    """Keep lightweight, stable provenance available to every retrieval backend."""
    metadata = [("corpus_kind", source_kind(relative_path))]
    chapter = chapter_identifier(relative_path)
    if chapter:
        metadata.append(("chapter", chapter))
    if len(relative_path.parts) > 1 and relative_path.parts[0] in {"experiments", "benchmarks"}:
        metadata.append(("record_group", relative_path.parts[1]))
    return tuple(metadata)


def chunks(text: str, limit: int = 1200) -> list[str]:
    paragraphs = [paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()]
    result: list[str] = []
    current = ""
    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}".strip()
        if current and len(candidate) > limit:
            result.append(current)
            current = paragraph
        else:
            current = candidate
    if current:
        result.append(current)
    return result


def citation_keys(text: str, suffix: str) -> tuple[str, ...]:
    keys = set(CITATION_PATTERN.findall(text))
    if suffix == ".bib":
        keys.update(BIBTEX_ENTRY_PATTERN.findall(text))
        keys.difference_update({"article", "book", "inproceedings", "online"})
    return tuple(sorted(keys))


def corpus_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for directory in CORPUS_DIRECTORIES:
        path = root / directory
        if path.exists():
            files.extend(item for item in path.rglob("*") if item.suffix in ALLOWED_SUFFIXES)
    return sorted(item for item in files if item.is_file())


def build_index(root: Path) -> list[Evidence]:
    root = root.resolve()
    result: list[Evidence] = []
    for path in corpus_files(root):
        text = path.read_text(encoding="utf-8", errors="replace")
        relative = path.relative_to(root)
        for chunk in chunks(text):
            result.append(
                Evidence(
                    source=str(relative),
                    kind=source_kind(relative),
                    chapter=chapter_identifier(relative),
                    citations=citation_keys(chunk, relative.suffix),
                    text=chunk,
                    vector=embedding(chunk),
                    metadata=evidence_metadata(relative),
                )
            )
    return result


def save_index(index: list[Evidence], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps([asdict(item) for item in index], indent=2), encoding="utf-8")


def load_index(path: Path) -> list[Evidence]:
    records = json.loads(path.read_text(encoding="utf-8"))
    return [
        Evidence(
            source=item["source"],
            kind=item["kind"],
            chapter=item["chapter"],
            citations=tuple(item["citations"]),
            text=item["text"],
            vector=tuple(item["vector"]),
            metadata=tuple(tuple(pair) for pair in item.get("metadata", ())),
        )
        for item in records
    ]


def retrieve(index: list[Evidence], query: str, limit: int = 4) -> list[SearchResult]:
    query_vector = np.asarray(embedding(query))
    if not np.any(query_vector):
        return []
    ranked = [
        SearchResult(evidence=item, score=float(np.dot(query_vector, np.asarray(item.vector))))
        for item in index
    ]
    return sorted(ranked, key=lambda item: (-item.score, item.evidence.source))[:limit]


def grounded_answer(index: list[Evidence], query: str, limit: int = 3) -> str:
    results = [item for item in retrieve(index, query, limit) if item.score > 0]
    return grounded_evidence(results)


def grounded_evidence(results: list[SearchResult]) -> str:
    """Render only retrieved corpus evidence; never synthesize an unsupported answer."""
    if not results:
        return "No grounded answer: no indexed evidence matched this question."
    excerpts = []
    for item in results:
        citations = f" citations: {', '.join(item.evidence.citations)}" if item.evidence.citations else ""
        excerpts.append(f"[{item.evidence.source}{citations}]\n{item.evidence.text}")
    return "Grounded evidence only:\n\n" + "\n\n".join(excerpts)


def propose_improvement(index: list[Evidence], objective: str) -> ImprovementPlan:
    results = [item for item in retrieve(index, objective, 4) if item.score > 0]
    sources = tuple(sorted({item.evidence.source for item in results}))
    return ImprovementPlan(
        objective=objective,
        evidence_paths=sources,
        steps=(
            "Verify the cited corpus files and benchmark evidence.",
            "Draft the smallest chapter or experiment change that addresses the objective.",
            "Run the critic and targeted tests before requesting approval.",
            "Apply no source changes until a human explicitly approves the proposal.",
        ),
    )


def review_corpus(root: Path) -> list[str]:
    findings: list[str] = []
    for path in corpus_files(root):
        if path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        relative = path.relative_to(root)
        if relative.parts[:2] == ("book", "chapters") and "## Alternatives" not in text:
            findings.append(f"{relative}: missing Alternatives section")
        for target in LINK_PATTERN.findall(text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target_path = (path.parent / target).resolve()
            if root not in target_path.parents and target_path != root:
                findings.append(f"{relative}: link escapes corpus {target}")
            elif not target_path.exists():
                findings.append(f"{relative}: unresolved link {target}")
    return findings


class ApprovalCheckpoint:
    """Persist approval state separately from the corpus; it never edits sources."""

    def __init__(self, path: Path):
        self.path = path

    def create(self, proposal: ImprovementPlan) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps({"proposal": asdict(proposal), "approved": False}, indent=2),
            encoding="utf-8",
        )

    def approve(self, approved: bool) -> None:
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        payload["approved"] = bool(approved)
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def is_approved(self) -> bool:
        return bool(json.loads(self.path.read_text(encoding="utf-8"))["approved"])
