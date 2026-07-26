from _bootstrap import PROJECT_ROOT  # noqa: F401

from sklearn.model_selection import train_test_split

from hr_attrition.config import (
    DEFAULT_DATA_PATH,
    DEFAULT_MLFLOW_EXPERIMENT,
    DEFAULT_MLFLOW_TRACKING_URI,
    DEFAULT_REPORT_DIR,
)
from hr_attrition.data.clean import clean_hr_data
from hr_attrition.data.load import load_hr_data
from hr_attrition.data.validate import require_columns
from hr_attrition.evaluation.classification_metrics import (
    build_confusion_matrix,
    evaluate_classifier,
)
from hr_attrition.features.classification_features import (
    CLASSIFICATION_FEATURES,
    CLASSIFICATION_TARGET,
)
from hr_attrition.models.classification import (
    build_logistic_regression_pipeline,
    build_random_forest_pipeline,
)
from hr_attrition.tracking.mlflow_tracking import (
    configure_mlflow,
    log_classification_run,
)


def train_and_log(
    run_name,
    model_name,
    pipeline,
    parameters,
    X_train,
    X_test,
    y_train,
    y_test,
):
    pipeline.fit(X_train, y_train)

    metrics, predictions, _, report = evaluate_classifier(
        pipeline,
        X_test,
        y_test,
    )

    matrix = build_confusion_matrix(
        y_test,
        predictions,
    )

    run_id = log_classification_run(
        run_name=run_name,
        model_name=model_name,
        model=pipeline,
        parameters=parameters,
        metrics=metrics,
        input_example=X_train.head(5),
        classification_report_text=report,
        confusion_matrix=matrix,
        report_directory=DEFAULT_REPORT_DIR,
    )

    print(f"\n{model_name}")
    print("Run ID:", run_id)
    print(metrics)


def main() -> None:
    dataframe = clean_hr_data(
        load_hr_data(DEFAULT_DATA_PATH)
    )

    require_columns(
        dataframe,
        CLASSIFICATION_FEATURES
        + [CLASSIFICATION_TARGET],
    )

    X = dataframe[CLASSIFICATION_FEATURES]
    y = dataframe[CLASSIFICATION_TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    configure_mlflow(
        DEFAULT_MLFLOW_TRACKING_URI,
        DEFAULT_MLFLOW_EXPERIMENT,
    )

    train_and_log(
        run_name="logistic_regression_raw_pipeline",
        model_name="LogisticRegression",
        pipeline=build_logistic_regression_pipeline(),
        parameters={
            "class_weight": "balanced",
            "max_iter": 1000,
            "test_size": 0.20,
            "random_state": 42,
        },
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
    )

    train_and_log(
        run_name="random_forest_raw_pipeline",
        model_name="RandomForestClassifier",
        pipeline=build_random_forest_pipeline(),
        parameters={
            "n_estimators": 200,
            "class_weight": "balanced",
            "test_size": 0.20,
            "random_state": 42,
        },
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
    )


if __name__ == "__main__":
    main()
