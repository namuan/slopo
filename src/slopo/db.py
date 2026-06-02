import sqlite3
from pathlib import Path

from slopo.config import Config
from slopo.schema import SCHEMA_VERSION, create_schema


class DatabaseNotFoundError(Exception):
    pass


class ConfigurationMismatchError(Exception):
    def __init__(self, field: str, stored: str, current: str) -> None:
        super().__init__(f"{field}: stored={stored}, current={current}")
        self.field = field
        self.stored = stored
        self.current = current


class SchemaVersionMismatchError(Exception):
    pass


def open_db(cfg: Config) -> sqlite3.Connection:
    if not cfg.db_file.exists():
        raise DatabaseNotFoundError
    conn = _connect(cfg.db_file)
    _check_schema_version(conn)
    _check_metadata(conn, cfg)
    return conn


def create_db(cfg: Config) -> sqlite3.Connection:
    conn = _connect(cfg.db_file)
    create_schema(conn)
    conn.execute(
        "INSERT INTO metadata"
        " (id, source_dir, embedding_model, embedding_dimensions, body_node_count_threshold)"
        " VALUES (1, ?, ?, ?, ?)",
        (
            str(cfg.source_dir.resolve()),
            cfg.embedding_model,
            cfg.embedding_dimensions,
            cfg.body_node_count_threshold,
        ),
    )
    conn.commit()
    return conn


def rebuild_excluded_units(conn: sqlite3.Connection) -> int:
    clear_excluded_units(conn)
    conn.execute(
        """
        INSERT INTO excluded_units (unit_id)
        SELECT id FROM code_units
        WHERE body_hash IN (
            SELECT body_hash FROM code_units
            GROUP BY body_hash HAVING COUNT(*) > 1
        )
        """
    )
    return conn.execute("SELECT COUNT(*) FROM excluded_units").fetchone()[0]


def clear_excluded_units(conn: sqlite3.Connection) -> None:
    conn.execute("DELETE FROM excluded_units")


def verify_source_dir(conn: sqlite3.Connection, source_dir: Path) -> None:
    resolved = str(source_dir.resolve())
    stored = conn.execute("SELECT source_dir FROM metadata WHERE id = 1").fetchone()
    if stored[0] != resolved:
        raise ConfigurationMismatchError("source_dir", stored[0], resolved)


def _connect(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _check_schema_version(conn: sqlite3.Connection) -> None:
    row = conn.execute("SELECT version FROM schema_version").fetchone()
    if row[0] != SCHEMA_VERSION:
        raise SchemaVersionMismatchError(
            f"schema version mismatch: database is v{row[0]}, this version expects v{SCHEMA_VERSION}."
        )


def _check_metadata(conn: sqlite3.Connection, cfg: Config) -> None:
    stored = conn.execute(
        "SELECT embedding_model, embedding_dimensions, body_node_count_threshold"
        " FROM metadata WHERE id = 1"
    ).fetchone()

    if stored is None:
        raise sqlite3.OperationalError

    if stored[0] != cfg.embedding_model:
        raise ConfigurationMismatchError(
            "embedding_model", stored[0], cfg.embedding_model
        )
    if stored[1] != cfg.embedding_dimensions:
        raise ConfigurationMismatchError(
            "embedding_dimensions", str(stored[1]), str(cfg.embedding_dimensions)
        )
    if stored[2] != cfg.body_node_count_threshold:
        raise ConfigurationMismatchError(
            "body_node_count_threshold",
            str(stored[2]),
            str(cfg.body_node_count_threshold),
        )
