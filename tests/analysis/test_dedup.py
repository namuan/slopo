from slopo.analysis.dedup import fold_exact_duplicates
from slopo.analysis.models import Cluster, UnitRecord


def _unit(unit_id: int, body_hash: str, line: int = 1) -> UnitRecord:
    return UnitRecord(
        unit_id=unit_id,
        file_path=f"src/file{unit_id}.py",
        name=f"f{unit_id}",
        start_line=line,
        end_line=line + 1,
        body="body",
        body_hash=body_hash,
    )


def test_folds_exact_duplicate():
    units = {1: _unit(1, "a"), 2: _unit(2, "b"), 3: _unit(3, "a")}
    clusters = [Cluster([1, 2, 3], 0.9, 0.95)]

    folded, duplicates = fold_exact_duplicates(clusters, units)

    assert folded[0].unit_ids == [1, 2]
    assert duplicates == {1: [units[3]]}


def test_primary_is_first_in_cluster_not_lowest_id():
    units = {1: _unit(1, "a"), 2: _unit(2, "a"), 3: _unit(3, "b")}
    clusters = [Cluster([2, 1, 3], 0.9, 0.95)]

    folded, duplicates = fold_exact_duplicates(clusters, units)

    assert folded[0].unit_ids == [2, 3]
    assert duplicates == {2: [units[1]]}


def test_collapses_cluster_of_only_exact_copies_to_one_unit():
    units = {1: _unit(1, "a"), 2: _unit(2, "a")}
    clusters = [Cluster([1, 2], 0.9, 0.95)]

    folded, duplicates = fold_exact_duplicates(clusters, units)

    assert folded[0].unit_ids == [1]
    assert duplicates == {1: [units[2]]}


def test_keeps_cluster_of_distinct_units_unchanged():
    units = {1: _unit(1, "a"), 2: _unit(2, "b")}
    clusters = [Cluster([1, 2], 0.9, 0.95)]

    folded, duplicates = fold_exact_duplicates(clusters, units)

    assert folded[0].unit_ids == [1, 2]
    assert duplicates == {}
