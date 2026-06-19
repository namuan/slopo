from slopo.analysis.models import Cluster, UnitRecord


def fold_exact_duplicates(
    clusters: list[Cluster], units: dict[int, UnitRecord]
) -> tuple[list[Cluster], dict[int, list[UnitRecord]]]:
    folded: list[Cluster] = []
    duplicates: dict[int, list[UnitRecord]] = {}

    for cluster in clusters:
        kept_ids: list[int] = []
        first_of_hash: dict[str, int] = {}
        for unit_id in cluster.unit_ids:
            body_hash = units[unit_id].body_hash
            primary = first_of_hash.get(body_hash)
            if primary is None:
                first_of_hash[body_hash] = unit_id
                kept_ids.append(unit_id)
            else:
                duplicates.setdefault(primary, []).append(units[unit_id])

        folded.append(cluster._replace(unit_ids=kept_ids))

    return folded, duplicates
