.PHONY: test lint site book preflight

test:
	uv run pytest

lint:
	uv run ruff check .

site:
	cd site && npm run build

book:
	./scripts/build-book.sh

preflight:
	uv run python scripts/preflight_pdf.py book/build/from-tensors-to-agents.pdf
