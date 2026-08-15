.PHONY: test lint audit-book site book provisional-pdf preflight cover release-manifest

test:
	uv run pytest

lint:
	uv run ruff check .

audit-book:
	python3 scripts/audit_book.py

site:
	cd site && npm run build

book:
	./scripts/build-book.sh

preflight:
	uv run python scripts/preflight_pdf.py book/build/ai-from-tensors-to-agents-on-mac-silicon-provisional.pdf --kind interior

provisional-pdf: book
	./scripts/export-provisional-pdf.sh

cover:
	uv run python scripts/build-cover.py

release-manifest:
	uv run python scripts/release_manifest.py
