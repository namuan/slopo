import sqlite3
from typing import Iterator

import pytest

from slopo.schema import create_schema


@pytest.fixture
def conn() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    create_schema(conn)
    yield conn
    conn.close()
