#!/usr/bin/env python3
"""
Local OpenAI-compatible embedding server using a cached HuggingFace model.

Serves /v1/embeddings so LiteLLM (and Slopo) can use it as an "openai" provider.

Usage:
    python local-embed-server.py [--port 8000] [--model all-MiniLM-L6-v2]
"""

import argparse
import os
import sys

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


app = FastAPI(title="Local Embedding Server")

# ── Lazy-load model on first request ─────────────────────────────
_model = None
_model_name = None


def _load_model(model_name: str):
    global _model
    from sentence_transformers import SentenceTransformer

    # HF cache path – SentenceTransformer will auto-detect the cache
    os.environ.setdefault(
        "HF_HOME",
        os.path.expanduser("~/.cache/huggingface"),
    )
    model_path = f"sentence-transformers/{model_name}"
    print(f"Loading {model_path} from cache...", file=sys.stderr)
    _model = SentenceTransformer(model_path)
    print(f"Model loaded (dim={_model.get_embedding_dimension()})", file=sys.stderr)


# ── API types ────────────────────────────────────────────────────


class EmbeddingRequest(BaseModel):
    model: str
    input: str | list[str]
    dimensions: int | None = None


class EmbeddingData(BaseModel):
    object: str = "embedding"
    index: int
    embedding: list[float]


class Usage(BaseModel):
    prompt_tokens: int = 0
    total_tokens: int = 0


class EmbeddingResponse(BaseModel):
    object: str = "list"
    data: list[EmbeddingData]
    model: str
    usage: Usage = Usage()


# ── Endpoint ─────────────────────────────────────────────────────


@app.post("/v1/embeddings")
async def embeddings(req: EmbeddingRequest):
    if _model is None:
        _load_model(_model_name or "all-MiniLM-L6-v2")

    inputs = req.input if isinstance(req.input, list) else [req.input]
    dim = req.dimensions or _model.get_embedding_dimension()

    # Compute embeddings
    embeddings = _model.encode(inputs, normalize_embeddings=True)
    # Truncate if dimensions requested is smaller
    if dim < embeddings.shape[1]:
        embeddings = embeddings[:, :dim]

    data = [
        EmbeddingData(index=i, embedding=emb.tolist())
        for i, emb in enumerate(embeddings)
    ]
    return EmbeddingResponse(data=data, model=req.model)


# ── CLI ──────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Local embedding server")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on")
    parser.add_argument(
        "--model",
        default="all-MiniLM-L6-v2",
        help="Model name under sentence-transformers/ on HuggingFace",
    )
    args = parser.parse_args()

    global _model_name
    _model_name = args.model

    print(
        f"Starting local embedding server on http://localhost:{args.port}",
        file=sys.stderr,
    )
    print(f"Model: sentence-transformers/{args.model}", file=sys.stderr)
    print(f"Cache: {os.path.expanduser('~/.cache/huggingface')}", file=sys.stderr)
    uvicorn.run(app, host="0.0.0.0", port=args.port, log_level="info")


if __name__ == "__main__":
    main()
