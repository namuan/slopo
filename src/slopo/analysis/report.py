import re
from datetime import datetime
from pathlib import Path

from slopo.analysis.ignore import cluster_hash
from slopo.analysis.models import Cluster, UnitRecord

_LANG_MAP = {
    ".cs": "csharp",
    ".go": "go",
    ".java": "java",
    ".js": "javascript",
    ".kt": "kotlin",
    ".py": "python",
    ".rs": "rust",
    ".ts": "typescript",
}

_CLUSTER_FILE_RE = re.compile(r"cluster-\d+\.md")


def write_report(
    clusters: list[Cluster], units: dict[int, UnitRecord], output_dir: Path
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _clean_report_dir(output_dir)

    total = len(clusters)
    (output_dir / "index.md").write_text(
        build_index_markdown(clusters, units), encoding="utf-8"
    )
    for i, cluster in enumerate(clusters, 1):
        filename = cluster_filename(i, total)
        (output_dir / filename).write_text(
            build_cluster_markdown(i, cluster, units), encoding="utf-8"
        )


def build_index_markdown(clusters: list[Cluster], units: dict[int, UnitRecord]) -> str:
    total = len(clusters)
    headers = ["Cluster", "Hash", "Score", "Code units", "Unique files"]
    rows: list[list[str]] = []
    for i, cluster in enumerate(clusters, 1):
        link = f"[Cluster {i}]({cluster_filename(i, total)})"
        unit_count = len(cluster.unit_ids)
        unique_files = len({units[uid].file_path for uid in cluster.unit_ids})
        rows.append(
            [
                link,
                cluster_hash(cluster, units),
                _similarity_range(cluster),
                str(unit_count),
                str(unique_files),
            ]
        )
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Generated {timestamp}\n\n{_format_table(headers, rows)}"


def build_cluster_markdown(
    number: int, cluster: Cluster, units: dict[int, UnitRecord]
) -> str:
    lines: list[str] = [
        f"## ({number}) score {_similarity_range(cluster)}\n",
        f"Hash: `{cluster_hash(cluster, units)}`\n",
    ]
    for unit_id in cluster.unit_ids:
        unit = units[unit_id]
        lang = _lang_tag(unit.file_path)
        lines.append(f"`{unit.file_path}` lines {unit.start_line}-{unit.end_line}\n")
        lines.append(f"```{lang}\n{unit.body}\n```\n")
    return "\n".join(lines)


def cluster_filename(number: int, total: int) -> str:
    width = len(str(total))
    return f"cluster-{number:0{width}d}.md"


def _clean_report_dir(output_dir: Path) -> None:
    index = output_dir / "index.md"
    if index.is_file():
        index.unlink()
    for path in output_dir.glob("cluster-*.md"):
        if _CLUSTER_FILE_RE.fullmatch(path.name):
            path.unlink()


def _format_table(headers: list[str], rows: list[list[str]]) -> str:
    widths = [
        max(len(headers[col]), *(len(row[col]) for row in rows))
        if rows
        else len(headers[col])
        for col in range(len(headers))
    ]

    def render(cells: list[str]) -> str:
        padded = [cells[col].ljust(widths[col]) for col in range(len(cells))]
        return "| " + " | ".join(padded) + " |"

    separator = "|" + "|".join("-" * (w + 2) for w in widths) + "|"
    lines = [render(headers), separator]
    lines.extend(render(row) for row in rows)
    return "\n".join(lines) + "\n"


def _similarity_range(cluster: Cluster) -> str:
    if cluster.min_similarity == cluster.max_similarity:
        return f"{cluster.min_similarity:.2f}"
    return f"{cluster.min_similarity:.2f}-{cluster.max_similarity:.2f}"


def _lang_tag(file_path: str) -> str:
    return _LANG_MAP.get(Path(file_path).suffix, "")
