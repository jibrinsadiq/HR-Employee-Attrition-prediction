import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    FunctionTransformer,
    OneHotEncoder,
    OrdinalEncoder,
    StandardScaler,
)

from hr_attrition.features.classification_features import (
    BINARY_CATEGORICAL_FEATURES,
    NOMINAL_CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    ORDINAL_FEATURES,
    SKEWED_NUMERIC_FEATURES,
)


def build_classification_preprocessor() -> ColumnTransformer:
    """Build a raw-input preprocessing graph for classification."""
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

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

    business_travel_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="most_frequent"),
            ),
            (
                "encoder",
                OrdinalEncoder(
                    categories=[
                        [
                            "Non-Travel",
                            "Travel_Rarely",
                            "Travel_Frequently",
                        ]
                    ],
                    handle_unknown="use_encoded_value",
                    unknown_value=-1,
                ),
            ),
        ]
    )

    binary_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="most_frequent"),
            ),
            (
                "encoder",
                OrdinalEncoder(
                    categories=[
                        ["Female", "Male"],
                        ["No", "Yes"],
                    ],
                    handle_unknown="use_encoded_value",
                    unknown_value=-1,
                ),
            ),
        ]
    )

    nominal_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="most_frequent"),
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
            ),
        ]
    )

    return ColumnTransformer(
        transformers=[
            (
                "skewed",
                skewed_pipeline,
                SKEWED_NUMERIC_FEATURES,
            ),
            (
                "numeric",
                numeric_pipeline,
                NUMERIC_FEATURES,
            ),
            (
                "business_travel",
                business_travel_pipeline,
                ORDINAL_FEATURES,
            ),
            (
                "binary",
                binary_pipeline,
                BINARY_CATEGORICAL_FEATURES,
            ),
            (
                "nominal",
                nominal_pipeline,
                NOMINAL_CATEGORICAL_FEATURES,
            ),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )
