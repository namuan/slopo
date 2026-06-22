## (10) score 0.93-0.95

Hash: `6cbaa611475c`

---

- `slopo/analysis/rerank.py` lines 30-46

```python
def rerank_cluster_pairs(
    pairs_in_cluster: list[SimilarPair],
    units: dict[int, UnitRecord],
) -> list[SimilarPair]:
    reranked: list[SimilarPair] = []
    for pair in pairs_in_cluster:
        unit_a = units[pair.unit_id_a]
        unit_b = units[pair.unit_id_b]
        new_score = rerank_pair_score(pair, unit_a, unit_b)
        reranked.append(
            SimilarPair(
                similarity=new_score,
                unit_id_a=pair.unit_id_a,
                unit_id_b=pair.unit_id_b,
            )
        )
    return reranked
```

---

- `slopo/analysis/rerank.py` lines 49-61

```python
def rerank_all_clusters(
    clusters: list[Cluster],
    pairs: list[SimilarPair],
    units: dict[int, UnitRecord],
) -> list[SimilarPair]:
    reranked: list[SimilarPair] = []
    for cluster in clusters:
        members = set(cluster.unit_ids)
        in_cluster = [
            p for p in pairs if p.unit_id_a in members and p.unit_id_b in members
        ]
        reranked.extend(rerank_cluster_pairs(in_cluster, units))
    return reranked
```

---

- `slopo/analysis/clustering.py` lines 68-87

```python
def reorder_clusters(
    clusters: list[Cluster], reranked_pairs: list[SimilarPair]
) -> list[Cluster]:
    result: list[Cluster] = []
    for cluster in clusters:
        members = set(cluster.unit_ids)
        in_cluster = [
            p
            for p in reranked_pairs
            if p.unit_id_a in members and p.unit_id_b in members
        ]
        ordered = sort_cluster(members, in_cluster)
        sims = [p.similarity for p in in_cluster]
        min_sim = min(sims)
        max_sim = max(sims)
        result.append(
            Cluster(unit_ids=ordered, min_similarity=min_sim, max_similarity=max_sim)
        )
    result.sort(key=lambda c: c.max_similarity, reverse=True)
    return result
```
