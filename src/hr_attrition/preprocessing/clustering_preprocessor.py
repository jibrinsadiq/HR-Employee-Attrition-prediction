import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler

from hr_attrition.features.clustering_features import (
    OTHER_CLUSTERING_FEATURES,
    SKEWED_CLUSTERING_FEATURES,
)


def build_clustering_preprocessor() -> ColumnTransformer:
    """Build the preprocessing used by the final persona model."""
    skewed_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            (
                "log_transform",
                FunctionTransformer(
                    np.log1p,
                    feature_names_out="one-to-one",
                ),
            ),
            ("scaler", StandardScaler()),
        ]
    )

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    return ColumnTransformer(
        transformers=[
            (
                "skewed",
                skewed_pipeline,
                SKEWED_CLUSTERING_FEATURES,
            ),
            (
                "numeric",
                numeric_pipeline,
                OTHER_CLUSTERING_FEATURES,
            ),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )
