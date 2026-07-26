import mlflow
import pandas as pd

mlflow.set_tracking_uri("sqlite:///mlflow_attrition.db")

experiment = mlflow.get_experiment_by_name("attrition")

if experiment is None:
    raise ValueError("The MLflow experiment 'attrition' was not found.")

runs_df = mlflow.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["start_time DESC"]
)

print("Number of runs found:", len(runs_df))


def get_column(dataframe, column_name):
    if column_name in dataframe.columns:
        return dataframe[column_name]

    return pd.Series(
        [None] * len(dataframe),
        index=dataframe.index
    )


classification_results = pd.DataFrame({
    "Run_ID": get_column(runs_df, "run_id"),

    "Run_Name": get_column(
        runs_df,
        "tags.mlflow.runName"
    ),

    "Model": get_column(
        runs_df,
        "params.model"
    ),

    "Accuracy": get_column(
        runs_df,
        "metrics.accuracy"
    ).combine_first(
        get_column(runs_df, "metrics.test_accuracy")
    ),

    "Precision": get_column(
        runs_df,
        "metrics.precision"
    ).combine_first(
        get_column(runs_df, "metrics.test_precision")
    ),

    "Recall": get_column(
        runs_df,
        "metrics.recall"
    ).combine_first(
        get_column(runs_df, "metrics.test_recall")
    ),

    "F1_Score": get_column(
        runs_df,
        "metrics.f1_score"
    ).combine_first(
        get_column(runs_df, "metrics.test_f1_score")
    ),

    "ROC_AUC": get_column(
        runs_df,
        "metrics.roc_auc"
    ).combine_first(
        get_column(runs_df, "metrics.test_roc_auc")
    ),

    "Status": get_column(
        runs_df,
        "status"
    ),

    "Start_Time": get_column(
        runs_df,
        "start_time"
    )
})

classification_results

with open(
    "mlflow_classification_results.txt",
    "w",
    encoding="utf-8"
) as file:
    file.write(
        classification_results
        .round(4)
        .to_string(index=False)
    )