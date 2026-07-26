from typing import Any

import numpy as np
from sklearn.metrics import (
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)


def evaluate_clustering(
    processed_data: np.ndarray,
    labels: np.ndarray,
) -> dict[str, float]:
    return {
        "silhouette": silhouette_score(
            processed_data,
            labels,
        ),
        "calinski_harabasz": calinski_harabasz_score(
            processed_data,
            labels,
        ),
        "davies_bouldin": davies_bouldin_score(
            processed_data,
            labels,
        ),
    }


def get_pipeline_cluster_labels(
    pipeline: Any,
    raw_data: Any,
) -> tuple[np.ndarray, np.ndarray]:
    processed = pipeline.named_steps[
        "preprocessor"
    ].transform(raw_data)

    model = pipeline.named_steps["model"]

    if hasattr(model, "labels_"):
        labels = model.labels_
    else:
        labels = model.predict(processed)

    return processed, labels
