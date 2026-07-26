from datetime import date

import pandas as pd

from _bootstrap import PROJECT_ROOT  # noqa: F401

from hr_attrition.artifacts.model_artifacts import (
    save_joblib_model,
    save_json,
)
from hr_attrition.config import (
    DEFAULT_ARTIFACT_DIR,
    DEFAULT_DATA_PATH,
    DEFAULT_REPORT_DIR,
)
from hr_attrition.data.clean import clean_hr_data
from hr_attrition.data.load import load_hr_data
from hr_attrition.features.classification_features import (
    CLASSIFICATION_FEATURES,
    CLASSIFICATION_TARGET,
)
from hr_attrition.features.clustering_features import (
    CLUSTERING_FEATURES,
)
from hr_attrition.models.classification import (
    build_logistic_regression_pipeline,
)
from hr_attrition.models.clustering import (
    build_kmeans_pipeline,
)


def build_persona_mapping(
    dataframe: pd.DataFrame,
    labels,
) -> tuple[dict[str, str], pd.DataFrame]:
    profiled = dataframe.copy()
    profiled["Cluster"] = labels

    profile = (
        profiled
        .groupby("Cluster")[
            CLUSTERING_FEATURES
            + [
                "OverTime_encoded",
                "Attrition_encoded",
            ]
        ]
        .mean()
    )

    profile["Employee_Count"] = (
        profiled.groupby("Cluster").size()
    )

    commute_cluster = int(
        profile["DistanceFromHome"].idxmax()
    )

    remaining = [
        int(cluster_id)
        for cluster_id in profile.index
        if int(cluster_id) != commute_cluster
    ]

    veteran_cluster = int(
        profile.loc[
            remaining,
            "YearsAtCompany",
        ].idxmax()
    )

    newcomer_cluster = next(
        cluster_id
        for cluster_id in remaining
        if cluster_id != veteran_cluster
    )

    mapping = {
        str(commute_cluster):
            "Commute-burdened mid-career employees",
        str(newcomer_cluster):
            "Flight-risk newcomers",
        str(veteran_cluster):
            "Stable high-earning veterans",
    }

    profile["Persona"] = [
        mapping[str(int(cluster_id))]
        for cluster_id in profile.index
    ]

    return mapping, profile.reset_index()


def main() -> None:
    dataframe = clean_hr_data(
        load_hr_data(DEFAULT_DATA_PATH)
    )

    # Raw-input production classifier
    classifier = build_logistic_regression_pipeline()
    classifier.fit(
        dataframe[CLASSIFICATION_FEATURES],
        dataframe[CLASSIFICATION_TARGET],
    )

    classifier_path = save_joblib_model(
        classifier,
        DEFAULT_ARTIFACT_DIR
        / "attrition_classifier.joblib",
    )

    # Final seven-feature, three-cluster persona model
    segmenter = build_kmeans_pipeline(n_clusters=3)
    segment_labels = segmenter.fit_predict(
        dataframe[CLUSTERING_FEATURES]
    )

    segmenter_path = save_joblib_model(
        segmenter,
        DEFAULT_ARTIFACT_DIR
        / "employee_segmenter.joblib",
    )

    # Derived fields used only for profiling
    dataframe["OverTime_encoded"] = (
        dataframe["OverTime"]
        .map({"No": 0, "Yes": 1})
    )

    persona_mapping, profile = build_persona_mapping(
        dataframe,
        segment_labels,
    )

    retention_actions = {
        cluster_id: action
        for cluster_id, action in [
            (
                next(
                    key
                    for key, value
                    in persona_mapping.items()
                    if value.startswith("Commute")
                ),
                (
                    "Review flexible-working, scheduling, "
                    "and commute-support options."
                ),
            ),
            (
                next(
                    key
                    for key, value
                    in persona_mapping.items()
                    if value.startswith("Flight-risk")
                ),
                (
                    "Prioritise an early manager check-in, "
                    "compensation review, and a visible "
                    "career-development plan."
                ),
            ),
            (
                next(
                    key
                    for key, value
                    in persona_mapping.items()
                    if value.startswith("Stable")
                ),
                (
                    "Focus on recognition, succession planning, "
                    "leadership opportunities, and mentoring."
                ),
            ),
        ]
    }

    save_json(
        persona_mapping,
        DEFAULT_ARTIFACT_DIR
        / "persona_mapping.json",
    )

    save_json(
        retention_actions,
        DEFAULT_ARTIFACT_DIR
        / "retention_actions.json",
    )

    save_json(
        {
            "classifier_name": "LogisticRegression",
            "classifier_version": "1.0",
            "classification_threshold": 0.50,
            "segmenter_name": "KMeans",
            "number_of_clusters": 3,
            "training_date": date.today().isoformat(),
            "classification_features":
                CLASSIFICATION_FEATURES,
            "clustering_features":
                CLUSTERING_FEATURES,
        },
        DEFAULT_ARTIFACT_DIR
        / "model_metadata.json",
    )

    DEFAULT_REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )
    profile.to_csv(
        DEFAULT_REPORT_DIR
        / "production_cluster_profile.csv",
        index=False,
    )

    print("Classifier saved:", classifier_path)
    print("Segmenter saved:", segmenter_path)
    print("Persona mapping:", persona_mapping)
    print(
        "Cluster profile saved:",
        DEFAULT_REPORT_DIR
        / "production_cluster_profile.csv",
    )


if __name__ == "__main__":
    main()
