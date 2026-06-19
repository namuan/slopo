import sqlite3

import numpy as np

from slopo.analysis.clustering import build_clusters, filter_clusters, reorder_clusters
from slopo.analysis.db import count_exact_copies, load_duplicate_hashes, load_units
from slopo.analysis.dedup import fold_exact_duplicates
from slopo.analysis.ignore import cluster_hash, ensure_ignore_file, load_ignored
from slopo.analysis.models import Cluster, UnitRecord
from slopo.analysis.overlap import exclude_overlapping_pairs
from slopo.analysis.rerank import rerank_all_clusters
from slopo.analysis.report.filesystem import write_report
from slopo.analysis.similarity import find_similar_pairs
from slopo.config import Config
from slopo.embedding.db import load_embeddings
from slopo.progress import ProgressReporter

# Rows of the similarity matrix computed per iteration. Caps the size of
# the intermediate (block_size, n) product so it doesn't blow up at large n.
_BLOCK_SIZE = 1000


def run_analyze(
    conn: sqlite3.Connection,
    cfg: Config,
    log: ProgressReporter,
) -> None:
    embeddings = load_embeddings(conn)
    if not embeddings:
        log("No embedded code units found. Run `embed` first.")
        return

    log("Calculating similarity...")
    pairs = find_similar_pairs(embeddings, cfg.similarity_threshold, _BLOCK_SIZE)

    if not pairs:
        log("No similar pairs found.")
        return

    referenced_ids = {uid for p in pairs for uid in (p.unit_id_a, p.unit_id_b)}
    units = load_units(conn, referenced_ids)
    pairs = exclude_overlapping_pairs(pairs, units)

    if not pairs:
        log("No similar pairs found.")
        return

    log("Clustering and ranking...")
    clusters = build_clusters(pairs)

    reranked_pairs = rerank_all_clusters(clusters, pairs, units)
    clusters = reorder_clusters(clusters, reranked_pairs)
    clusters = filter_clusters(clusters, cfg.rerank_threshold)

    clusters, duplicates = fold_exact_duplicates(clusters, units)

    if not clusters:
        log(
            "No similar code units found for configured similarity and rerank thresholds."
        )
        return

    ensure_ignore_file(cfg.ignore_file)

    ignored = load_ignored(cfg.ignore_file)
    if ignored:
        kept = [c for c in clusters if cluster_hash(c, units) not in ignored]
        ignored_count = len(clusters) - len(kept)
        clusters = kept
        if ignored_count:
            log(f"Ignored {ignored_count} previously reviewed clusters.")

    if not clusters:
        log("All similar code clusters are in the ignore list.")
        return

    write_report(clusters, units, cfg.report_dir, duplicates)
    log(f"Report written to {cfg.report_dir} directory.")

    _report_ratios(conn, embeddings, clusters, duplicates, units, log)


def _report_ratios(
    conn: sqlite3.Connection,
    embeddings: dict[int, np.ndarray],
    clusters: list[Cluster],
    duplicates: dict[int, list[UnitRecord]],
    units: dict[int, UnitRecord],
    log: ProgressReporter,
) -> None:
    duplicate_hashes = load_duplicate_hashes(conn)
    exact_copies = count_exact_copies(conn)

    kept = {uid for c in clusters for uid in c.unit_ids}
    folded = {dup.unit_id for dups in duplicates.values() for dup in dups}
    flagged_with = kept | folded
    flagged_without = {
        uid for uid in flagged_with if units[uid].body_hash not in duplicate_hashes
    }

    total_with = len(embeddings)
    total_without = total_with - exact_copies

    log(f"Exact copies: {exact_copies} of {total_with} units.")
    log(
        "Similarity ratio (excluding exact copies):"
        f" {_ratio(len(flagged_without), total_without)}"
    )
    log(
        "Similarity ratio (including exact copies):"
        f" {_ratio(len(flagged_with), total_with)}"
    )


def _ratio(flagged: int, total: int) -> str:
    ratio = flagged / total if total > 0 else 0.0
    return f"{ratio:.2%} ({flagged}/{total} units flagged as similar)"
