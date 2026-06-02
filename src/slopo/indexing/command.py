import sqlite3

from slopo.config import Config
from slopo.db import clear_excluded_units, rebuild_excluded_units
from slopo.indexing.sync import sync_index
from slopo.progress import ProgressReporter


def run_index(
    conn: sqlite3.Connection,
    cfg: Config,
    log: ProgressReporter,
) -> None:
    log("Indexing code...")

    with conn:
        stats = sync_index(
            conn, cfg.source_dir, cfg.body_node_count_threshold, cfg.source_dir_exclude
        )
        if cfg.exclude_exact_duplicates:
            excluded = rebuild_excluded_units(conn)
        else:
            clear_excluded_units(conn)

    log(
        f"Indexed {stats.indexed_units} code units from {stats.indexed_files} files"
        f" ({stats.skipped_files} unchanged, {stats.removed_files} removed)."
    )

    if cfg.exclude_exact_duplicates:
        log(f" ({excluded} units are excluded as exact-duplicates)")
