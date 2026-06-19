import sqlite3
from dataclasses import dataclass
from pathlib import Path

from slopo.indexing.db import (
    delete_file_units,
    delete_files,
    insert_file_units,
    list_indexed_paths,
    prune_orphan_embeddings,
    upsert_file,
)
from slopo.indexing.scanner import scan_directory


@dataclass
class SyncStats:
    indexed_files: int
    skipped_files: int
    indexed_units: int
    removed_files: int


def sync_index(
    conn: sqlite3.Connection,
    directory: Path,
    body_node_count_threshold: int,
    exclude: list[str],
) -> SyncStats:
    indexed_files = 0
    skipped_files = 0
    indexed_units = 0

    previously_indexed = list_indexed_paths(conn)
    for scanned_file in scan_directory(directory, body_node_count_threshold, exclude):
        mtime = (directory / scanned_file.path).stat().st_mtime
        result = upsert_file(conn, scanned_file.path, mtime)
        previously_indexed.pop(scanned_file.path.as_posix(), None)
        if not result.modified:
            skipped_files += 1
            continue
        delete_file_units(conn, result.file_id)
        insert_file_units(conn, result.file_id, scanned_file.units)
        indexed_files += 1
        indexed_units += len(scanned_file.units)

    removed_ids = list(previously_indexed.values())
    delete_files(conn, removed_ids)

    prune_orphan_embeddings(conn)

    return SyncStats(
        indexed_files=indexed_files,
        skipped_files=skipped_files,
        indexed_units=indexed_units,
        removed_files=len(removed_ids),
    )
