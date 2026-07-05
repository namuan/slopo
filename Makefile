.PHONY: install install-server serve init show-config index embed analyze \
        pipeline clean test lint typecheck help

EMBED_PORT ?= 8000
EMBED_MODEL ?= all-MiniLM-L6-v2

# ── Setup ────────────────────────────────────────────────────────

install:
	uv sync

install-server: install
	uv add --dev sentence-transformers fastapi uvicorn

# ── Local embedding server ───────────────────────────────────────

serve:
	uv run local-embed-server.py --port $(EMBED_PORT) --model $(EMBED_MODEL)

# ── Slopo commands ───────────────────────────────────────────────

init:
	uv run slopo init

show-config:
	uv run slopo show-config

index:
	uv run slopo index

embed:
	uv run slopo embed

analyze:
	uv run slopo analyze

pipeline: index embed analyze

# ── Clean ────────────────────────────────────────────────────────

clean:
	rm -rf slopo.db slopo-report/ slopo.ignore.txt

# ── Quality ──────────────────────────────────────────────────────

test:
	uv run pytest

lint:
	uv run ruff check

typecheck:
	uv run mypy src

# ── Help ─────────────────────────────────────────────────────────

help:
	@echo "Usage:"
	@echo "  make install         Install all dependencies"
	@echo "  make install-server  Also install deps for the local embedding server"
	@echo "  make serve           Start local embedding server (port: $(EMBED_PORT))"
	@echo "  make init            Create slopo.conf.yaml template"
	@echo "  make show-config     Validate and show current config"
	@echo "  make index           Index source files"
	@echo "  make embed           Compute embeddings"
	@echo "  make analyze         Generate duplication report"
	@echo "  make pipeline        Run index + embed + analyze"
	@echo "  make clean           Remove slopo.db, reports, and ignore file"
	@echo "  make test            Run tests"
	@echo "  make lint            Run ruff linter"
	@echo "  make typecheck       Run mypy type checker"
	@echo ""
	@echo "Environment variables:"
	@echo "  EMBED_PORT=8000      Port for the local embedding server"
	@echo "  EMBED_MODEL=all-MiniLM-L6-v2  Model name to serve"
