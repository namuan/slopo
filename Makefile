.PHONY: install install-server serve init show-config index embed analyze \
        pipeline clean test lint typecheck setup-env

EMBED_PORT ?= 8000
EMBED_MODEL ?= all-MiniLM-L6-v2
VENV := .venv
PYTHON := $(VENV)/bin/python3
UV := uv

# ── Setup ────────────────────────────────────────────────────────

install: $(VENV)
	$(UV) sync

$(VENV):
	$(UV) venv

install-server: install
	$(UV) pip install sentence-transformers fastapi uvicorn

# ── Local embedding server ───────────────────────────────────────

serve: export OPENAI_API_BASE ?= http://localhost:$(EMBED_PORT)/v1
serve: export LITELLM_DROP_PARAMS ?= true
serve:
	$(PYTHON) local-embed-server.py --port $(EMBED_PORT) --model $(EMBED_MODEL)

# ── Configuration ────────────────────────────────────────────────

init:
	$(UV) run slopo init

show-config:
	$(UV) run slopo show-config

# ── Pipeline (requires running server + env vars set) ────────────

index:
	$(UV) run slopo index

embed:
	$(UV) run slopo embed

analyze:
	$(UV) run slopo analyze

pipeline: index embed analyze

# ── Clean ────────────────────────────────────────────────────────

clean:
	rm -rf slopo.db slopo-report/ slopo.ignore.txt

# ── Quality ──────────────────────────────────────────────────────

test:
	$(UV) run pytest

lint:
	$(UV) run ruff check

typecheck:
	$(UV) run mypy src

# ── Help ─────────────────────────────────────────────────────────

help:
	@echo "Usage:"
	@echo "  make install         Create venv and install all dependencies"
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
