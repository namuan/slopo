from pathlib import Path
from unittest.mock import MagicMock, patch

from slopo.config import Config
from slopo.embedding.embeddings import embed_units
from slopo.embedding.models import EmbeddedUnit, UnembeddedUnit

_CONFIG = Config(
    source_dir=Path("src"),
    source_dir_exclude=[],
    db_file=Path("slopo.db"),
    report_dir=Path("slopo-report"),
    ignore_file=Path("slopo.ignore.txt"),
    embedding_model="openai/text-embedding-3-small",
    embedding_dimensions=3,
    embedding_api_key="test-key",
    embedding_batch_size=100,
    embedding_batch_chars=10000,
    similarity_threshold=0.9,
    rerank_threshold=0.93,
    body_node_count_threshold=10,
    exclude_exact_duplicates=True,
)


def _mock_response(vectors: list[list[float]]) -> MagicMock:
    response = MagicMock()
    response.data = [{"embedding": v} for v in vectors]
    return response


def test_single_unit_mapped():
    units = [UnembeddedUnit(unit_id=7, body="def foo(): pass")]
    with patch(
        "litellm.embedding",
        return_value=_mock_response([[1.0, 2.0, 3.0]]),
    ):
        result = embed_units(units, _CONFIG)

    assert result == [EmbeddedUnit(unit_id=7, vector=[1.0, 2.0, 3.0])]


def test_multiple_units_preserve_order():
    units = [
        UnembeddedUnit(unit_id=1, body="def foo(): pass"),
        UnembeddedUnit(unit_id=2, body="def bar(): pass"),
        UnembeddedUnit(unit_id=3, body="def baz(): pass"),
    ]
    with patch(
        "litellm.embedding",
        return_value=_mock_response(
            [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        ),
    ):
        result = embed_units(units, _CONFIG)

    assert result == [
        EmbeddedUnit(unit_id=1, vector=[1.0, 0.0, 0.0]),
        EmbeddedUnit(unit_id=2, vector=[0.0, 1.0, 0.0]),
        EmbeddedUnit(unit_id=3, vector=[0.0, 0.0, 1.0]),
    ]
