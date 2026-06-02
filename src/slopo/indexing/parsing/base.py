import hashlib
from dataclasses import dataclass
from typing import Callable


@dataclass
class CodeUnit:
    name: str
    body: str
    start_line: int
    end_line: int
    body_node_count: int
    body_hash: str


CodeParser = Callable[[bytes], list[CodeUnit]]


def hash_body(body: str) -> str:
    normalized = " ".join(body.split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
