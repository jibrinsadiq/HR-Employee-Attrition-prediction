import json
import os
from functools import lru_cache
from pathlib import Path


MODEL_DIR = Path(os.getenv("MODEL_DIR", "artifacts"))
PERSONA_FILENAME = os.getenv(
    "PERSONA_MAPPING_NAME",
    "persona_mapping.json",
)
ACTION_FILENAME = os.getenv(
    "RETENTION_ACTIONS_NAME",
    "retention_actions.json",
)


@lru_cache(maxsize=1)
def load_persona_mapping() -> dict[str, str]:
    path = MODEL_DIR / PERSONA_FILENAME
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


@lru_cache(maxsize=1)
def load_retention_actions() -> dict[str, str]:
    path = MODEL_DIR / ACTION_FILENAME
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_persona_and_action(cluster_id: int) -> tuple[str, str]:
    key = str(cluster_id)

    persona = load_persona_mapping().get(
        key,
        f"Employee segment {cluster_id}",
    )

    action = load_retention_actions().get(
        key,
        "Arrange an HR review before selecting a retention intervention.",
    )

    return persona, action
