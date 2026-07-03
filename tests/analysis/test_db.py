import sqlite3

import pytest

from slopo import db
from slopo.analysis.db import count_exact_copies, load_duplicate_hashes, load_units
from slopo.analysis.models import UnitRecord

_SETUP = """
    INSERT INTO files (id, path, mtime) VALUES (1, 'File.java', 0);
    INSERT INTO code_units (id, file_id, name, body, start_line, end_line, body_node_count, body_hash)
        VALUES (1, 1, 'a', 'body-a', 1, 2, 3, 'dup'),
               (2, 1, 'b', 'body-b', 1, 2, 3, 'dup'),
               (3, 1, 'c', 'body-c', 1, 2, 3, 'dup'),
               (4, 1, 'd', 'body-d', 1, 2, 3, 'unique');
"""


def test_counts_every_member_of_a_duplicate_group(conn: sqlite3.Connection):
    conn.executescript(_SETUP)

    assert count_exact_copies(conn) == 3


def test_counts_zero_when_all_units_unique(conn: sqlite3.Connection):
    conn.executescript("""
        INSERT INTO files (id, path, mtime) VALUES (1, 'File.java', 0);
        INSERT INTO code_units (id, file_id, name, body, start_line, end_line, body_node_count, body_hash)
            VALUES (1, 1, 'a', 'a', 1, 2, 3, 'x'),
                   (2, 1, 'b', 'b', 1, 2, 3, 'y');
    """)

    assert count_exact_copies(conn) == 0


def test_returns_only_hashes_shared_by_more_than_one_unit(conn: sqlite3.Connection):
    conn.executescript(_SETUP)

    assert load_duplicate_hashes(conn) == {"dup"}


def test_loads_only_the_requested_units(conn: sqlite3.Connection):
    conn.executescript(_SETUP)

    units = load_units(conn, {1, 3})

    assert set(units.keys()) == {1, 3}
    assert units[1] == UnitRecord(
        unit_id=1,
        file_path="File.java",
        name="a",
        start_line=1,
        end_line=2,
        body="body-a",
        body_hash="dup",
    )


def test_loads_units_spanning_multiple_chunks(
    conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr(db, "_MAX_SQL_VARIABLES", 2)
    conn.executescript(_SETUP)

    units = load_units(conn, {1, 2, 3, 4})

    assert set(units.keys()) == {1, 2, 3, 4}
