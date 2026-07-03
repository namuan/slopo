import pytest

from slopo import db
from slopo.db import chunked


def test_yields_nothing_for_empty_input():
    assert list(chunked([])) == []


def test_yields_single_chunk_when_input_fits(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(db, "_MAX_SQL_VARIABLES", 3)

    assert list(chunked([1, 2])) == [[1, 2]]


def test_splits_input_across_chunks(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(db, "_MAX_SQL_VARIABLES", 2)

    assert list(chunked([1, 2, 3, 4, 5])) == [[1, 2], [3, 4], [5]]


def test_exact_multiple_leaves_no_trailing_empty_chunk(
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(db, "_MAX_SQL_VARIABLES", 2)

    assert list(chunked([1, 2, 3, 4])) == [[1, 2], [3, 4]]
