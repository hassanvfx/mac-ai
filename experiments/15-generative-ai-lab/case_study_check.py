"""Print safe-first boundaries for the external Generative AI Lab case studies."""

from __future__ import annotations


def main() -> None:
    print("Generative AI Lab — safe-first case-study guide")
    print()
    print("Lyrics Refiner")
    print("  Source: https://github.com/hassanvfx/lyrics-refiner")
    print("  Boundary: local-only; never deploy or share a Vite build with an API key.")
    print("  Start: clone, npm install, copy .env.example to local .env, then read the README.")
    print("  Check: inspect every stage and the word-preservation report before export.")
    print()
    print("Newsmusic")
    print("  Source: https://github.com/hassanvfx/newsmusic")
    print("  Boundary: begin in dry-run mode; credentials and OAuth tokens stay local.")
    print("  Start: follow the README and run `orchestrate --until video --dry-run` only.")
    print("  Check: do not spend credits, reuse third-party footage, or upload without review.")
    print()
    print("Never commit credentials. Never publish generated output without human review.")


if __name__ == "__main__":
    main()
