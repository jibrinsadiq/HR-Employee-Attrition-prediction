from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline


XGBOOST_PARAM_DISTRIBUTIONS = {
    "model__n_estimators": [100, 200, 300, 400, 500],
    "model__learning_rate": [0.01, 0.03, 0.05, 0.10, 0.20],
    "model__max_depth": [2, 3, 4, 5, 6, 8],
    "model__min_child_weight": [1, 2, 3, 5, 7],
    "model__subsample": [0.60, 0.70, 0.80, 0.90, 1.00],
    "model__colsample_bytree": [
        0.60,
        0.70,
        0.80,
        0.90,
        1.00,
    ],
    "model__gamma": [0, 0.10, 0.20, 0.50, 1.00],
    "model__reg_alpha": [0, 0.001, 0.01, 0.10, 1.00],
    "model__reg_lambda": [0.50, 1.00, 2.00, 5.00, 10.00],
}


def build_xgboost_random_search(
    pipeline: Pipeline,
    n_iter: int = 30,
) -> RandomizedSearchCV:
    stratified_cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42,
    )

    return RandomizedSearchCV(
        estimator=pipeline,
        param_distributions=XGBOOST_PARAM_DISTRIBUTIONS,
        n_iter=n_iter,
        scoring="roc_auc",
        cv=stratified_cv,
        random_state=42,
        n_jobs=-1,
        verbose=2,
        return_train_score=True,
    )
