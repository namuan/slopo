import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from pathspec import PathSpec

from slopo.indexing.parsing.base import CodeUnit
from slopo.indexing.parsing.registry import get_parser, supported_extensions

logger = logging.getLogger(__name__)

_MAX_BODY_CHARS = 10_000


@dataclass
class ScannedFile:
    path: Path
    units: list[CodeUnit]


def scan_directory(
    root: Path,
    body_node_count_threshold: int,
    exclude: list[str],
) -> Iterator[ScannedFile]:
    spec = PathSpec.from_lines("gitignore", exclude)
    for path in _source_files(root, spec):
        relative = path.relative_to(root)
        units = _parse_file(path)
        if units is not None:
            units = [
                u
                for u in units
                if u.body_node_count >= body_node_count_threshold
                and len(u.body) <= _MAX_BODY_CHARS
            ]
            yield ScannedFile(path=relative, units=units)


def _source_files(root: Path, spec: PathSpec) -> Iterator[Path]:
    for extension in supported_extensions():
        for path in root.rglob(f"*{extension}"):
            if not spec.match_file(path.relative_to(root)):
                yield path


def _parse_file(path: Path) -> list[CodeUnit] | None:
    try:
        parser = get_parser(path)
        return parser(path.read_bytes())
    except Exception as e:
        logger.warning("Skipping %s: %s", path, e)
        return None
