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
from hr_attrition.evaluation.classification_metrics import (
    build_confusion_matrix,
    evaluate_classifier,
)
from hr_attrition.features.classification_features import (
    CLASSIFICATION_FEATURES,
    CLASSIFICATION_TARGET,
)
from hr_attrition.models.classification import (
    build_xgboost_pipeline,
)
from hr_attrition.models.classification_tuning import (
    build_xgboost_random_search,
)
from hr_attrition.tracking.mlflow_tracking import (
    configure_mlflow,
    log_classification_run,
)


def main() -> None:
    dataframe = clean_hr_data(
        load_hr_data(DEFAULT_DATA_PATH)
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

    negative_count = int((y_train == 0).sum())
    positive_count = int((y_train == 1).sum())
    scale_pos_weight = negative_count / positive_count

    base_pipeline = build_xgboost_pipeline(
        scale_pos_weight=scale_pos_weight
    )

    search = build_xgboost_random_search(
        base_pipeline,
        n_iter=30,
    )
    search.fit(X_train, y_train)

    best_pipeline = search.best_estimator_

    metrics, predictions, _, report = evaluate_classifier(
        best_pipeline,
        X_test,
        y_test,
    )

    matrix = build_confusion_matrix(
        y_test,
        predictions,
    )

    best_parameters = {
        key.replace("model__", ""): value
        for key, value in search.best_params_.items()
    }

    configure_mlflow(
        DEFAULT_MLFLOW_TRACKING_URI,
        DEFAULT_MLFLOW_EXPERIMENT,
    )

    run_id = log_classification_run(
        run_name="xgboost_random_search_raw_pipeline",
        model_name="XGBClassifier",
        model=best_pipeline,
        parameters={
            "tuning_method": "RandomizedSearchCV",
            "search_iterations": 30,
            "cv_folds": 5,
            "scoring": "roc_auc",
            "scale_pos_weight": scale_pos_weight,
            "best_cv_roc_auc": search.best_score_,
            **best_parameters,
        },
        metrics=metrics,
        input_example=X_train.head(5),
        classification_report_text=report,
        confusion_matrix=matrix,
        report_directory=DEFAULT_REPORT_DIR,
    )

    print("Run ID:", run_id)
    print("Best parameters:", best_parameters)
    print("Best CV ROC-AUC:", search.best_score_)
    print("Test metrics:", metrics)


if __name__ == "__main__":
    main()
