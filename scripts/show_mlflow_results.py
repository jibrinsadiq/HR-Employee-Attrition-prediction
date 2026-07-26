from _bootstrap import PROJECT_ROOT  # noqa: F401

import mlflow

from hr_attrition.config import (
    DEFAULT_MLFLOW_EXPERIMENT,
    DEFAULT_MLFLOW_TRACKING_URI,
    DEFAULT_REPORT_DIR,
)
from hr_attrition.evaluation.reports import (
    export_results,
    latest_finished_classification_runs,
)


def main() -> None:
    mlflow.set_tracking_uri(
        DEFAULT_MLFLOW_TRACKING_URI
    )

    results = latest_finished_classification_runs(
        DEFAULT_MLFLOW_EXPERIMENT
    )

    if results.empty:
        print("No completed MLflow runs were found.")
        return

    export_results(
        results,
        DEFAULT_REPORT_DIR,
    )

    print(
        results[
            [
                "Model",
                "Accuracy",
                "Precision",
                "Recall",
                "F1_Score",
                "ROC_AUC",
                "Start_Time",
            ]
        ].round(4).to_string(index=False)
    )

    print("\nSaved reports to:", DEFAULT_REPORT_DIR)


if __name__ == "__main__":
    main()
