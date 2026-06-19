import sqlite3
from dataclasses import dataclass
from pathlib import Path

from slopo.indexing.parsing.base import CodeUnit


@dataclass
class UpsertResult:
    file_id: int
    modified: bool


def list_indexed_paths(conn: sqlite3.Connection) -> dict[str, int]:
    rows = conn.execute("SELECT path, id FROM files").fetchall()
    return {row[0]: row[1] for row in rows}


def delete_files(conn: sqlite3.Connection, file_ids: list[int]) -> None:
    if not file_ids:
        return
    id_placeholders = ",".join("?" * len(file_ids))
    conn.execute(
        f"DELETE FROM code_units WHERE file_id IN ({id_placeholders})", file_ids
    )
    conn.execute(f"DELETE FROM files WHERE id IN ({id_placeholders})", file_ids)


def upsert_file(conn: sqlite3.Connection, path: Path, mtime: float) -> UpsertResult:
    posix_path = path.as_posix()
    row = conn.execute(
        "SELECT id, mtime FROM files WHERE path = ?", (posix_path,)
    ).fetchone()

    if row is not None and row[1] == mtime:
        return UpsertResult(file_id=row[0], modified=False)

    if row is None:
        conn.execute(
            "INSERT INTO files (path, mtime) VALUES (?, ?)", (posix_path, mtime)
        )
        file_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    else:
        conn.execute("UPDATE files SET mtime = ? WHERE id = ?", (mtime, row[0]))
        file_id = row[0]

    return UpsertResult(file_id=file_id, modified=True)


def delete_file_units(conn: sqlite3.Connection, file_id: int) -> None:
    conn.execute("DELETE FROM code_units WHERE file_id = ?", (file_id,))


def prune_orphan_embeddings(conn: sqlite3.Connection) -> None:
    conn.execute(
        "DELETE FROM embeddings"
        " WHERE body_hash NOT IN (SELECT body_hash FROM code_units)"
    )


def insert_file_units(
    conn: sqlite3.Connection, file_id: int, units: list[CodeUnit]
) -> None:
    conn.executemany(
        "INSERT INTO code_units"
        " (file_id, name, body, start_line, end_line, body_node_count, body_hash)"
        " VALUES (?, ?, ?, ?, ?, ?, ?)",
        [
            (
                file_id,
                u.name,
                u.body,
                u.start_line,
                u.end_line,
                u.body_node_count,
                u.body_hash,
            )
            for u in units
        ],
    )
