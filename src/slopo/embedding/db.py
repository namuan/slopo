import sqlite3

import numpy as np

from slopo.embedding.batching import trim_to_char_limit
from slopo.embedding.models import EmbeddedUnit, UnembeddedUnit


def count_unembedded_units(conn: sqlite3.Connection) -> int:
    row = conn.execute(
        """
        SELECT COUNT(*) FROM code_units
        WHERE embedding IS NULL
          AND id NOT IN (SELECT unit_id FROM excluded_units)
        """
    ).fetchone()
    return row[0]


def load_next_batch(
    conn: sqlite3.Connection, max_items: int, max_chars: int
) -> list[UnembeddedUnit]:
    rows = conn.execute(
        """
        SELECT id, body
        FROM code_units
        WHERE embedding IS NULL
          AND id NOT IN (SELECT unit_id FROM excluded_units)
        LIMIT ?
    """,
        (max_items,),
    ).fetchall()

    units = [UnembeddedUnit(unit_id=row[0], body=row[1]) for row in rows]
    return trim_to_char_limit(units, max_chars)


def save_embeddings(conn: sqlite3.Connection, embeddings: list[EmbeddedUnit]) -> None:
    conn.executemany(
        "UPDATE code_units SET embedding = ? WHERE id = ?",
        [
            (np.asarray(e.vector, dtype=np.float32).tobytes(), e.unit_id)
            for e in embeddings
        ],
    )


def load_embeddings(conn: sqlite3.Connection) -> dict[int, np.ndarray]:
    rows = conn.execute(
        """
        SELECT id, embedding FROM code_units
        WHERE embedding IS NOT NULL
          AND id NOT IN (SELECT unit_id FROM excluded_units)
        """
    ).fetchall()
    return {row[0]: np.frombuffer(row[1], dtype=np.float32) for row in rows}
