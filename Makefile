.PHONY: test lint audit-book site book print-art master-pdf provisional-pdf pdf-online preflight cover qrcodes release-manifest validate-reader-bridge validate-publication validate-lulu validate-lulu-interior publish-review

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

print-art:
	uv run python scripts/build_print_art.py

preflight:
	uv run python scripts/preflight_pdf.py book/build/pdf-online.pdf --kind interior
	uv run python scripts/prepare_lulu_pdf.py book/build/pdf-online.pdf --audit-only

master-pdf: print-art book validate-lulu-interior
	./scripts/export-provisional-pdf.sh

provisional-pdf: master-pdf
	@echo "Compatibility target: the single beta master is book/build/pdf-online.pdf."

pdf-online: master-pdf
	@echo "The online reading edition is the same beta master PDF."

cover:
	uv run python scripts/build-cover.py

qrcodes:
	uv run python scripts/generate_qr_codes.py

validate-reader-bridge:
	uv run python scripts/validate_reader_bridge.py

validate-publication:
	uv run python scripts/validate_publication.py

validate-lulu:
	uv run python scripts/validate_lulu_distribution.py

validate-lulu-interior:
	uv run python scripts/validate_lulu_distribution.py --interior book/build/ai-from-tensors-to-agents-on-mac-silicon.docx

publish-review: validate-reader-bridge qrcodes master-pdf preflight validate-publication

release-manifest:
	uv run python scripts/release_manifest.py
