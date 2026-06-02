import hashlib
from pathlib import Path

from slopo.analysis.models import Cluster, UnitRecord

_HASH_LENGTH = 12

_HEADER = """\
# Cluster hashes reviewed and dismissed. One hash per line.
#
# A hash covers each unit's code body and its path relative to the index root.
# It changes when the code or that path changes, so the cluster re-surfaces.
# Re-indexing from a different root shifts every path, changing the hashes.

"""


def cluster_hash(cluster: Cluster, units: dict[int, UnitRecord]) -> str:
    pairs = sorted(
        (units[uid].file_path, units[uid].body_hash) for uid in cluster.unit_ids
    )
    canonical = "\n".join(f"{path}\0{body_hash}" for path, body_hash in pairs)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return digest[:_HASH_LENGTH]


def load_ignored(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    hashes: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.split("#", 1)[0].strip()
        if stripped:
            hashes.add(stripped)
    return hashes


def ensure_ignore_file(path: Path) -> None:
    if path.exists():
        return
    path.write_text(_HEADER, encoding="utf-8")
