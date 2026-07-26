from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.mixture import GaussianMixture
from sklearn.pipeline import Pipeline

from hr_attrition.preprocessing.clustering_preprocessor import (
    build_clustering_preprocessor,
)


def build_kmeans_pipeline(
    n_clusters: int = 3,
) -> Pipeline:
    return Pipeline(
        steps=[
            (
                "preprocessor",
                build_clustering_preprocessor(),
            ),
            (
                "model",
                KMeans(
                    n_clusters=n_clusters,
                    random_state=42,
                    n_init=20,
                ),
            ),
        ]
    )


def build_agglomerative_pipeline(
    n_clusters: int = 3,
) -> Pipeline:
    return Pipeline(
        steps=[
            (
                "preprocessor",
                build_clustering_preprocessor(),
            ),
            (
                "model",
                AgglomerativeClustering(
                    n_clusters=n_clusters,
                    linkage="ward",
                ),
            ),
        ]
    )


def build_gaussian_mixture_pipeline(
    n_components: int = 3,
) -> Pipeline:
    return Pipeline(
        steps=[
            (
                "preprocessor",
                build_clustering_preprocessor(),
            ),
            (
                "model",
                GaussianMixture(
                    n_components=n_components,
                    covariance_type="full",
                    n_init=5,
                    random_state=42,
                ),
            ),
        ]
    )
