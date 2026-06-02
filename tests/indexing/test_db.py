import sqlite3

from slopo.indexing.db import delete_file_units, delete_files, insert_file_units
from slopo.indexing.parsing.base import CodeUnit


def _insert_file(conn: sqlite3.Connection) -> int:
    conn.execute("INSERT INTO files (path, mtime) VALUES ('Calculator.java', 0)")
    return conn.execute("SELECT last_insert_rowid()").fetchone()[0]


def test_inserts_unit_fields_into_matching_columns(conn: sqlite3.Connection):
    file_id = _insert_file(conn)
    unit = CodeUnit(
        name="increment",
        body="int increment(int a) { return a + 1; }",
        start_line=2,
        end_line=4,
        body_node_count=7,
        body_hash="abc123",
    )

    insert_file_units(conn, file_id, [unit])

    row = conn.execute(
        "SELECT file_id, name, body, start_line, end_line, body_node_count, body_hash"
        " FROM code_units"
    ).fetchone()
    assert row == (
        file_id,
        "increment",
        "int increment(int a) { return a + 1; }",
        2,
        4,
        7,
        "abc123",
    )


def test_inserts_all_units_with_sequential_ids(conn: sqlite3.Connection):
    file_id = _insert_file(conn)
    units = [
        CodeUnit("increment", "body1", 1, 2, 3, "hash1"),
        CodeUnit("decrement", "body2", 4, 5, 6, "hash2"),
    ]

    insert_file_units(conn, file_id, units)

    rows = conn.execute("SELECT id, name FROM code_units ORDER BY id").fetchall()
    assert rows == [(1, "increment"), (2, "decrement")]


def test_deletes_file_whose_units_are_excluded(conn: sqlite3.Connection):
    file_id = _insert_file(conn)
    insert_file_units(conn, file_id, [CodeUnit("dup", "body", 1, 2, 3, "hash")])
    unit_id = conn.execute("SELECT id FROM code_units").fetchone()[0]
    conn.execute("INSERT INTO excluded_units (unit_id) VALUES (?)", (unit_id,))

    delete_files(conn, [file_id])

    assert conn.execute("SELECT COUNT(*) FROM files").fetchone()[0] == 0
    assert conn.execute("SELECT COUNT(*) FROM code_units").fetchone()[0] == 0
    assert conn.execute("SELECT COUNT(*) FROM excluded_units").fetchone()[0] == 0


def test_deletes_units_of_modified_file_that_are_excluded(conn: sqlite3.Connection):
    file_id = _insert_file(conn)
    insert_file_units(conn, file_id, [CodeUnit("dup", "body", 1, 2, 3, "hash")])
    unit_id = conn.execute("SELECT id FROM code_units").fetchone()[0]
    conn.execute("INSERT INTO excluded_units (unit_id) VALUES (?)", (unit_id,))

    delete_file_units(conn, file_id)

    assert conn.execute("SELECT COUNT(*) FROM code_units").fetchone()[0] == 0
    assert conn.execute("SELECT COUNT(*) FROM excluded_units").fetchone()[0] == 0
