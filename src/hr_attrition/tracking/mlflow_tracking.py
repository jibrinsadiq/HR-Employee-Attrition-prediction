from pathlib import Path
from typing import Any

import mlflow
import mlflow.sklearn
import pandas as pd


def configure_mlflow(
    tracking_uri: str,
    experiment_name: str,
) -> None:
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)


def log_classification_run(
    *,
    run_name: str,
    model_name: str,
    model: Any,
    parameters: dict[str, Any],
    metrics: dict[str, float],
    input_example: pd.DataFrame,
    classification_report_text: str,
    confusion_matrix: pd.DataFrame,
    report_directory: str | Path,
) -> str:
    report_dir = Path(report_directory)
    report_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / f"{run_name}_report.txt"
    matrix_path = report_dir / f"{run_name}_confusion_matrix.csv"

    report_path.write_text(
        classification_report_text,
        encoding="utf-8",
    )
    confusion_matrix.to_csv(matrix_path)

    with mlflow.start_run(run_name=run_name) as run:
        mlflow.log_params(
            {
                "model": model_name,
                **parameters,
            }
        )
        mlflow.log_metrics(metrics)

        mlflow.log_artifact(
            str(report_path),
            artifact_path="reports",
        )
        mlflow.log_artifact(
            str(matrix_path),
            artifact_path="reports",
        )

        mlflow.sklearn.log_model(
            sk_model=model,
            name="model",
            input_example=input_example,
            serialization_format=(
                mlflow.sklearn
                .SERIALIZATION_FORMAT_CLOUDPICKLE
            ),
        )

        return run.info.run_id
