import sqlite3

from slopo.analysis.models import UnitRecord


def load_units(conn: sqlite3.Connection, unit_ids: set[int]) -> dict[int, UnitRecord]:
    if not unit_ids:
        return {}
    ids = list(unit_ids)
    id_placeholders = ",".join("?" * len(ids))
    rows = conn.execute(
        f"""
        SELECT cu.id, f.path, cu.name, cu.start_line, cu.end_line, cu.body, cu.body_hash
        FROM code_units cu
        JOIN files f ON f.id = cu.file_id
        WHERE cu.id IN ({id_placeholders})
        """,
        ids,
    ).fetchall()
    return {
        row[0]: UnitRecord(
            unit_id=row[0],
            file_path=row[1],
            name=row[2],
            start_line=row[3],
            end_line=row[4],
            body=row[5],
            body_hash=row[6],
        )
        for row in rows
    }
