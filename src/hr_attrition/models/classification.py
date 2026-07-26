from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

from hr_attrition.preprocessing.classification_preprocessor import (
    build_classification_preprocessor,
)


def build_logistic_regression_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            (
                "preprocessor",
                build_classification_preprocessor(),
            ),
            (
                "model",
                LogisticRegression(
                    class_weight="balanced",
                    max_iter=1000,
                    random_state=42,
                ),
            ),
        ]
    )


def build_random_forest_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            (
                "preprocessor",
                build_classification_preprocessor(),
            ),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=200,
                    class_weight="balanced",
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )


def build_xgboost_pipeline(
    scale_pos_weight: float,
) -> Pipeline:
    return Pipeline(
        steps=[
            (
                "preprocessor",
                build_classification_preprocessor(),
            ),
            (
                "model",
                XGBClassifier(
                    objective="binary:logistic",
                    eval_metric="logloss",
                    tree_method="hist",
                    scale_pos_weight=scale_pos_weight,
                    random_state=42,
                    n_jobs=1,
                ),
            ),
        ]
    )
