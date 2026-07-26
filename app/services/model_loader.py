import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib


MODEL_DIR = Path(os.getenv("MODEL_DIR", "artifacts"))
CLASSIFIER_FILENAME = os.getenv(
    "CLASSIFIER_MODEL_NAME",
    "attrition_classifier.joblib",
)
SEGMENTER_FILENAME = os.getenv(
    "SEGMENTER_MODEL_NAME",
    "employee_segmenter.joblib",
)
METADATA_FILENAME = os.getenv(
    "MODEL_METADATA_NAME",
    "model_metadata.json",
)


@lru_cache(maxsize=1)
def get_classifier() -> Any:
    path = MODEL_DIR / CLASSIFIER_FILENAME
    if not path.exists():
        raise FileNotFoundError(f"Classifier artifact not found: {path}")
    return joblib.load(path)


@lru_cache(maxsize=1)
def get_segmenter() -> Any:
    path = MODEL_DIR / SEGMENTER_FILENAME
    if not path.exists():
        raise FileNotFoundError(f"Segmenter artifact not found: {path}")
    return joblib.load(path)


@lru_cache(maxsize=1)
def get_model_metadata() -> dict[str, Any]:
    path = MODEL_DIR / METADATA_FILENAME
    if not path.exists():
        return {
            "classifier_name": "LogisticRegression",
            "classifier_version": "unversioned",
            "classification_threshold": 0.50,
            "segmenter_name": "KMeans",
        }

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_model_status() -> dict[str, bool]:
    classifier_path = MODEL_DIR / CLASSIFIER_FILENAME
    segmenter_path = MODEL_DIR / SEGMENTER_FILENAME

    return {
        "classifier_loaded": classifier_path.exists(),
        "segmenter_loaded": segmenter_path.exists(),
    }
