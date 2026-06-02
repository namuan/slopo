import sqlite3

import numpy as np

from slopo.embedding.db import (
    count_unembedded_units,
    load_embeddings,
    load_next_batch,
    save_embeddings,
)
from slopo.embedding.models import EmbeddedUnit

# --- count_unembedded_units ---


def test_count_unembedded_units_ignores_excluded_units(conn: sqlite3.Connection):
    conn.executescript("""
        INSERT INTO files (id, path, mtime) VALUES (1, 'File.java', 0);
        INSERT INTO code_units (id, file_id, name, body, start_line, end_line, body_node_count, body_hash)
            VALUES (1, 1, 'a', 'a', 1, 2, 3, 'a');
        INSERT INTO code_units (id, file_id, name, body, start_line, end_line, body_node_count, body_hash)
            VALUES (2, 1, 'b', 'b', 1, 2, 3, 'b');
        INSERT INTO excluded_units (unit_id) VALUES (2);
    """)

    assert count_unembedded_units(conn) == 1


def test_count_unembedded_units_ignores_embedded_units(conn: sqlite3.Connection):
    conn.executescript("""
        INSERT INTO files (id, path, mtime) VALUES (1, 'File.java', 0);
        INSERT INTO code_units (id, file_id, name, body, start_line, end_line, body_node_count, body_hash)
            VALUES (1, 1, 'a', 'a', 1, 2, 3, 'a');
        INSERT INTO code_units (id, file_id, name, body, start_line, end_line, body_node_count, body_hash, embedding)
            VALUES (2, 1, 'b', 'b', 1, 2, 3, 'b', X'0000803f');
    """)

    assert count_unembedded_units(conn) == 1


# --- load_next_batch ---


def test_load_next_batch_skips_excluded_units(conn: sqlite3.Connection):
    conn.executescript("""
        INSERT INTO files (id, path, mtime) VALUES (1, 'File.java', 0);
        INSERT INTO code_units (id, file_id, name, body, start_line, end_line, body_node_count, body_hash)
            VALUES (1, 1, 'a', 'a', 1, 2, 3, 'a');
        INSERT INTO code_units (id, file_id, name, body, start_line, end_line, body_node_count, body_hash)
            VALUES (2, 1, 'b', 'b', 1, 2, 3, 'b');
        INSERT INTO excluded_units (unit_id) VALUES (2);
    """)

    batch = load_next_batch(conn, max_items=10, max_chars=10_000)

    assert [u.unit_id for u in batch] == [1]


def test_load_next_batch_skips_already_embedded_units(conn: sqlite3.Connection):
    conn.executescript("""
        INSERT INTO files (id, path, mtime) VALUES (1, 'File.java', 0);
        INSERT INTO code_units (id, file_id, name, body, start_line, end_line, body_node_count, body_hash, embedding)
            VALUES (1, 1, 'a', 'a', 1, 2, 3, 'a', X'0000803f');
        INSERT INTO code_units (id, file_id, name, body, start_line, end_line, body_node_count, body_hash)
            VALUES (2, 1, 'b', 'b', 1, 2, 3, 'b');
    """)

    batch = load_next_batch(conn, max_items=10, max_chars=10_000)

    assert [u.unit_id for u in batch] == [2]


# --- load_embeddings ---


def test_load_embeddings_skips_unembedded_units(conn: sqlite3.Connection):
    conn.executescript("""
        INSERT INTO files (id, path, mtime) VALUES (1, 'File.java', 0);
        INSERT INTO code_units (id, file_id, name, body, start_line, end_line, body_node_count, body_hash, embedding)
            VALUES (1, 1, 'a', 'a', 1, 2, 3, 'a', X'0000803f');
        INSERT INTO code_units (id, file_id, name, body, start_line, end_line, body_node_count, body_hash)
            VALUES (2, 1, 'b', 'b', 1, 2, 3, 'b');
    """)

    assert list(load_embeddings(conn)) == [1]


def test_load_embeddings_skips_excluded_units(conn: sqlite3.Connection):
    conn.executescript("""
        INSERT INTO files (id, path, mtime) VALUES (1, 'File.java', 0);
        INSERT INTO code_units (id, file_id, name, body, start_line, end_line, body_node_count, body_hash, embedding)
            VALUES (1, 1, 'a', 'a', 1, 2, 3, 'a', X'0000803f');
        INSERT INTO code_units (id, file_id, name, body, start_line, end_line, body_node_count, body_hash, embedding)
            VALUES (2, 1, 'b', 'b', 1, 2, 3, 'b', X'0000803f');
        INSERT INTO excluded_units (unit_id) VALUES (1);
    """)

    assert list(load_embeddings(conn)) == [2]


# --- save_embeddings ---


def test_save_then_load_embeddings_round_trips_the_vector(conn: sqlite3.Connection):
    conn.executescript("""
        INSERT INTO files (id, path, mtime) VALUES (1, 'File.java', 0);
        INSERT INTO code_units (id, file_id, name, body, start_line, end_line, body_node_count, body_hash)
            VALUES (1, 1, 'a', 'a', 1, 2, 3, 'a');
    """)

    save_embeddings(conn, [EmbeddedUnit(unit_id=1, vector=[1.0, 2.0, 3.0])])

    loaded = load_embeddings(conn)
    assert np.array_equal(loaded[1], np.array([1.0, 2.0, 3.0], dtype=np.float32))
