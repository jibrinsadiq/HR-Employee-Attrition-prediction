from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def evaluate_classifier(
    model: Any,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> tuple[dict[str, float], np.ndarray, np.ndarray, str]:
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(
            y_test,
            predictions,
            zero_division=0,
        ),
        "recall": recall_score(
            y_test,
            predictions,
            zero_division=0,
        ),
        "f1_score": f1_score(
            y_test,
            predictions,
            zero_division=0,
        ),
        "roc_auc": roc_auc_score(
            y_test,
            probabilities,
        ),
    }

    report = classification_report(
        y_test,
        predictions,
        zero_division=0,
    )

    return metrics, predictions, probabilities, report


def build_confusion_matrix(
    y_test: pd.Series,
    predictions: np.ndarray,
) -> pd.DataFrame:
    matrix = confusion_matrix(y_test, predictions)

    return pd.DataFrame(
        matrix,
        index=["Actual_No", "Actual_Yes"],
        columns=["Predicted_No", "Predicted_Yes"],
    )
