.PHONY: test lint audit-book site book provisional-pdf pdf-online preflight cover qrcodes release-manifest validate-reader-bridge validate-publication publish-review

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

pdf-online: provisional-pdf
	uv run python scripts/build_online_pdf.py

cover:
	uv run python scripts/build-cover.py

qrcodes:
	uv run python scripts/generate_qr_codes.py

validate-reader-bridge:
	uv run python scripts/validate_reader_bridge.py

validate-publication:
	uv run python scripts/validate_publication.py

publish-review: validate-reader-bridge qrcodes book provisional-pdf pdf-online preflight validate-publication

release-manifest:
	uv run python scripts/release_manifest.py
