from pathlib import Path

import mlflow
import pandas as pd


def latest_finished_classification_runs(
    experiment_name: str = "attrition",
) -> pd.DataFrame:
    experiment = mlflow.get_experiment_by_name(
        experiment_name
    )

    if experiment is None:
        raise ValueError(
            f"MLflow experiment not found: {experiment_name}"
        )

    runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["start_time DESC"],
    )

    if runs.empty:
        return runs

    results = pd.DataFrame(
        {
            "Run_ID": runs.get("run_id"),
            "Run_Name": runs.get("tags.mlflow.runName"),
            "Model": runs.get("params.model"),
            "Accuracy": runs.get("metrics.accuracy"),
            "Precision": runs.get("metrics.precision"),
            "Recall": runs.get("metrics.recall"),
            "F1_Score": runs.get("metrics.f1_score"),
            "ROC_AUC": runs.get("metrics.roc_auc"),
            "Status": runs.get("status"),
            "Start_Time": runs.get("start_time"),
        }
    )

    return (
        results[results["Status"] == "FINISHED"]
        .sort_values("Start_Time", ascending=False)
        .drop_duplicates(subset="Model", keep="first")
        .reset_index(drop=True)
    )


def export_results(
    results: pd.DataFrame,
    output_directory: str | Path,
) -> None:
    output_dir = Path(output_directory)
    output_dir.mkdir(parents=True, exist_ok=True)

    results.to_csv(
        output_dir / "classification_results.csv",
        index=False,
    )

    (output_dir / "classification_results.txt").write_text(
        results.round(4).to_string(index=False),
        encoding="utf-8",
    )
