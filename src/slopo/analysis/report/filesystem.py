from datetime import datetime
from pathlib import Path

from slopo.analysis.models import Cluster, UnitRecord
from slopo.analysis.report.markdown import (
    build_cluster_markdown,
    build_index_markdown,
)
from slopo.analysis.report.naming import (
    CLUSTER_FILE_GLOB,
    CLUSTER_FILE_RE,
    cluster_filename,
)


def write_report(
    clusters: list[Cluster],
    units: dict[int, UnitRecord],
    output_dir: Path,
    duplicates: dict[int, list[UnitRecord]],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _clean_report_dir(output_dir)

    total = len(clusters)
    (output_dir / "index.md").write_text(
        build_index_markdown(clusters, units, duplicates, datetime.now()),
        encoding="utf-8",
    )
    for i, cluster in enumerate(clusters, 1):
        filename = cluster_filename(i, total)
        (output_dir / filename).write_text(
            build_cluster_markdown(i, cluster, units, duplicates), encoding="utf-8"
        )


def _clean_report_dir(output_dir: Path) -> None:
    index = output_dir / "index.md"
    if index.is_file():
        index.unlink()
    for path in output_dir.glob(CLUSTER_FILE_GLOB):
        if CLUSTER_FILE_RE.fullmatch(path.name):
            path.unlink()
