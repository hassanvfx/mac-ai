"""Audit canonical chapters for editorial sections, citations, links, and word budget."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "book" / "chapters"
BIBLIOGRAPHY = ROOT / "research" / "references.bib"
REQUIRED = ("Intuition", "Problem", "Minimal implementation", "Experiment", "What broke", "Takeaway")
CITATION = re.compile(r"@([A-Za-z0-9_-]+)")
BIB_KEY = re.compile(r"@\w+\s*\{\s*([^,\s]+)")
LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")
CODE_PATH = re.compile(r"`((?:experiments|src|benchmarks|research)/[^`\s]+\.(?:py|md|bib|txt))`")
EXPECTED_RESEARCH = {
    "01": "research/01-tensors/notes.md",
    "02": "research/01-tensors/notes.md",
    "03": "research/01-tensors/notes.md",
    "04": "research/02-vision-and-frameworks/notes.md",
    "05": "research/02-vision-and-frameworks/notes.md",
    "06": "research/03-transformers/notes.md",
    "07": "research/04-mlx/notes.md",
    "08": "research/05-embeddings-and-rag/notes.md",
    "09": "research/05-embeddings-and-rag/notes.md",
    "10": "research/06-structured-ai-systems/notes.md",
    "11": "research/07-workflow-graphs/notes.md",
    "12": "research/07-workflow-graphs/notes.md",
    "13": "research/07-workflow-graphs/notes.md",
    "14": "research/07-workflow-graphs/notes.md",
}


def main() -> None:
    bibliography = set(BIB_KEY.findall(BIBLIOGRAPHY.read_text(encoding="utf-8")))
    total_words = 0
    findings: list[str] = []
    for chapter in sorted(CHAPTERS.glob("[0-9][0-9]-*.md")):
        text = chapter.read_text(encoding="utf-8")
        words = len(re.findall(r"\b[\w'-]+\b", text))
        total_words += words
        if not chapter.name.startswith("00-"):
            headings = {line[3:].strip() for line in text.splitlines() if line.startswith("## ")}
            missing = [section for section in REQUIRED if section not in headings]
            if missing:
                findings.append(f"{chapter.relative_to(ROOT)}: missing sections: {', '.join(missing)}")
        unknown = sorted(set(CITATION.findall(text)) - bibliography)
        if unknown:
            findings.append(f"{chapter.relative_to(ROOT)}: unknown citation keys: {', '.join(unknown)}")
        for target in LINK.findall(text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            if not (chapter.parent / target).resolve().exists():
                findings.append(f"{chapter.relative_to(ROOT)}: unresolved link: {target}")
        for path_reference in CODE_PATH.findall(text):
            if not (ROOT / path_reference).is_file():
                findings.append(f"{chapter.relative_to(ROOT)}: unresolved repository path: {path_reference}")
        chapter_number = chapter.name[:2]
        expected_research = EXPECTED_RESEARCH.get(chapter_number)
        if expected_research and expected_research not in text:
            findings.append(f"{chapter.relative_to(ROOT)}: missing research evidence reference: {expected_research}")
        print(f"{chapter.name}: {words} words")
    print(f"TOTAL: {total_words} words (beta target: 45,000–55,000)")
    if findings:
        print("FINDINGS:")
        print("\n".join(findings))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
