from typing import NamedTuple


class UnembeddedUnit(NamedTuple):
    unit_id: int
    body: str


class EmbeddedUnit(NamedTuple):
    unit_id: int
    vector: list[float]
