from slopo.config import Config
from slopo.embedding.models import UnembeddedUnit, EmbeddedUnit


def embed_units(batch: list[UnembeddedUnit], config: Config) -> list[EmbeddedUnit]:
    import litellm  # type: ignore[import-untyped]

    response = litellm.embedding(
        model=config.embedding_model,
        input=[u.body for u in batch],
        dimensions=config.embedding_dimensions,
        api_key=config.embedding_api_key,
    )
    return [
        EmbeddedUnit(unit_id=unit.unit_id, vector=item["embedding"])
        for unit, item in zip(batch, response.data)
    ]
