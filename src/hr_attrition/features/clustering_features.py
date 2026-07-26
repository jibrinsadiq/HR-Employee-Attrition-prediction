CLUSTERING_FEATURES = [
    "YearsAtCompany",
    "MonthlyIncome",
    "JobSatisfaction",
    "EnvironmentSatisfaction",
    "JobInvolvement",
    "WorkLifeBalance",
    "DistanceFromHome",
]

SKEWED_CLUSTERING_FEATURES = [
    "YearsAtCompany",
    "MonthlyIncome",
]

OTHER_CLUSTERING_FEATURES = [
    feature
    for feature in CLUSTERING_FEATURES
    if feature not in SKEWED_CLUSTERING_FEATURES
]
