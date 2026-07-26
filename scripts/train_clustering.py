import pandas as pd

from _bootstrap import PROJECT_ROOT  # noqa: F401

from hr_attrition.config import (
    DEFAULT_DATA_PATH,
    DEFAULT_REPORT_DIR,
)
from hr_attrition.data.clean import clean_hr_data
from hr_attrition.data.load import load_hr_data
from hr_attrition.evaluation.clustering_metrics import (
    evaluate_clustering,
)
from hr_attrition.features.clustering_features import (
    CLUSTERING_FEATURES,
)
from hr_attrition.models.clustering import (
    build_agglomerative_pipeline,
    build_gaussian_mixture_pipeline,
    build_kmeans_pipeline,
)


def main() -> None:
    dataframe = clean_hr_data(
        load_hr_data(DEFAULT_DATA_PATH)
    )
    X = dataframe[CLUSTERING_FEATURES]

    results = []

    for cluster_count in range(2, 7):
        candidates = {
            "K-Means": build_kmeans_pipeline(cluster_count),
            "Agglomerative":
                build_agglomerative_pipeline(cluster_count),
            "Gaussian Mixture":
                build_gaussian_mixture_pipeline(cluster_count),
        }

        for model_name, pipeline in candidates.items():
            labels = pipeline.fit_predict(X)
            processed = pipeline.named_steps[
                "preprocessor"
            ].transform(X)

            metrics = evaluate_clustering(
                processed,
                labels,
            )

            results.append(
                {
                    "Model": model_name,
                    "Clusters": cluster_count,
                    **metrics,
                    "Smallest_Cluster":
                        pd.Series(labels).value_counts().min(),
                }
            )

    results_df = (
        pd.DataFrame(results)
        .sort_values(
            "silhouette",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    DEFAULT_REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        DEFAULT_REPORT_DIR
        / "clustering_model_comparison.csv"
    )
    results_df.to_csv(output_path, index=False)

    print(results_df.head(15).round(4))
    print("\nSaved:", output_path)


if __name__ == "__main__":
    main()
