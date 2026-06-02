import sqlite3

from slopo.db import rebuild_excluded_units


def _excluded_unit_ids(conn: sqlite3.Connection) -> set[int]:
    rows = conn.execute("SELECT unit_id FROM excluded_units").fetchall()
    return {row[0] for row in rows}


# --- rebuild_excluded_units ---


def test_excludes_only_the_same_units(conn: sqlite3.Connection):
    conn.executescript("""
        INSERT INTO files (id, path, mtime) VALUES (1, 'File.java', 0);
        INSERT INTO code_units (id, file_id, name, body, start_line, end_line, body_node_count, body_hash)
            VALUES (1, 1, 'a', 'a', 1, 2, 3, 'aaa'),
                   (2, 1, 'b', 'b', 1, 2, 3, 'bbb'),
                   (3, 1, 'c', 'c', 1, 2, 3, 'ccc'),
                   (4, 1, 'd', 'd', 1, 2, 3, 'aaa');
    """)

    assert rebuild_excluded_units(conn) == 2
    assert _excluded_unit_ids(conn) == {1, 4}


def test_excludes_nothing_when_all_units_unique(conn: sqlite3.Connection):
    conn.executescript("""
        INSERT INTO files (id, path, mtime) VALUES (1, 'File.java', 0);
        INSERT INTO code_units (id, file_id, name, body, start_line, end_line, body_node_count, body_hash)
            VALUES (1, 1, 'a', 'a', 1, 2, 3, 'aaa'),
                   (2, 1, 'b', 'b', 1, 2, 3, 'bbb'),
                   (3, 1, 'c', 'c', 1, 2, 3, 'ccc');
    """)

    assert rebuild_excluded_units(conn) == 0
    assert _excluded_unit_ids(conn) == set()


def test_rebuild_is_idempotent(conn: sqlite3.Connection):
    conn.executescript("""
        INSERT INTO files (id, path, mtime) VALUES (1, 'File.java', 0);
        INSERT INTO code_units (id, file_id, name, body, start_line, end_line, body_node_count, body_hash)
            VALUES (1, 1, 'a', 'a', 1, 2, 3, 'aaa'),
                   (2, 1, 'b', 'b', 1, 2, 3, 'aaa');
    """)

    rebuild_excluded_units(conn)
    rebuild_excluded_units(conn)

    assert _excluded_unit_ids(conn) == {1, 2}
