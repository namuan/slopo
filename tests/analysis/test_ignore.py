from pathlib import Path

from slopo.analysis.ignore import (
    cluster_hash,
    ensure_ignore_file,
    load_ignored,
)
from slopo.analysis.models import Cluster, UnitRecord


def unit(unit_id: int, file_path: str, body_hash: str) -> UnitRecord:
    return UnitRecord(
        unit_id=unit_id,
        file_path=file_path,
        name="",
        start_line=1,
        end_line=10,
        body="",
        body_hash=body_hash,
    )


# --- cluster_hash ---


def test_same_units_in_different_order_produce_the_same_hash():
    units = {1: unit(1, "src/A.java", "h1"), 2: unit(2, "src/B.java", "h2")}
    a = cluster_hash(Cluster([1, 2], 0.9, 0.9), units)
    b = cluster_hash(Cluster([2, 1], 0.9, 0.9), units)
    assert a == b


def test_different_body_hash_produces_a_different_hash():
    units = {1: unit(1, "src/A.java", "h1"), 2: unit(2, "src/A.java", "h2")}
    a = cluster_hash(Cluster([1], 0.9, 0.9), units)
    b = cluster_hash(Cluster([2], 0.9, 0.9), units)
    assert a != b


def test_different_file_path_produces_a_different_hash():
    units = {1: unit(1, "src/A.java", "h1"), 2: unit(2, "src/B.java", "h1")}
    a = cluster_hash(Cluster([1], 0.9, 0.9), units)
    b = cluster_hash(Cluster([2], 0.9, 0.9), units)
    assert a != b


def test_hash_is_shortened_to_the_configured_length():
    units = {1: unit(1, "src/A.java", "h1")}
    assert len(cluster_hash(Cluster([1], 0.9, 0.9), units)) == 12


# --- load_ignored ---


def test_missing_file_yields_an_empty_set(tmp_path: Path):
    assert load_ignored(tmp_path / "absent.txt") == set()


def test_reads_hashes_skipping_blank_and_comment_lines(tmp_path: Path):
    path = tmp_path / "ignore.txt"
    path.write_text("# header\n\nabc123\n\n# note\ndef456\n", encoding="utf-8")
    assert load_ignored(path) == {"abc123", "def456"}


def test_strips_inline_comments_and_surrounding_whitespace(tmp_path: Path):
    path = tmp_path / "ignore.txt"
    path.write_text("  abc123  # reviewed\n", encoding="utf-8")
    assert load_ignored(path) == {"abc123"}


# --- ensure_ignore_file ---


def test_writes_header_when_absent(tmp_path: Path):
    path = tmp_path / "ignore.txt"
    ensure_ignore_file(path)
    content = path.read_text(encoding="utf-8")
    assert content.startswith("#")


def test_leaves_an_existing_file_untouched(tmp_path: Path):
    path = tmp_path / "ignore.txt"
    path.write_text("my-hash\n", encoding="utf-8")
    ensure_ignore_file(path)
    assert path.read_text(encoding="utf-8") == "my-hash\n"
