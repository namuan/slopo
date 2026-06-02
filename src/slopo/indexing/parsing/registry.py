from pathlib import Path

from slopo.indexing.parsing.lang import (
    javascript,
    csharp,
    rust,
    go,
    python,
    typescript,
    kotlin,
    java,
)
from slopo.indexing.parsing.base import CodeParser

_REGISTRY: dict[str, CodeParser] = {
    ".cs": csharp.parse,
    ".go": go.parse,
    ".java": java.parse,
    ".js": javascript.parse,
    ".kt": kotlin.parse,
    ".py": python.parse,
    ".rs": rust.parse,
    ".ts": typescript.parse,
}


def get_parser(path: Path) -> CodeParser:
    suffix = path.suffix.lower()
    parser = _REGISTRY.get(suffix)
    if parser is None:
        raise ValueError(f"No parser registered for '{suffix}' files")
    return parser


def supported_extensions() -> list[str]:
    return list(_REGISTRY)
