import warnings
warnings.filterwarnings("ignore")

from pathlib import Path

import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd

from mlflow.models import infer_signature
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
MLFLOW_DB_PATH = BASE_DIR / "mlflow_attrition.db"


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_PATH}\n"
        "Place WA_Fn-UseC_-HR-Employee-Attrition.csv "
        "in the same folder as this script."
    )

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully.")
print("Dataset shape:", df.shape)


# ---------------------------------------------------------
# Encode target and categorical features
# ---------------------------------------------------------

df["Attrition_encoded"] = df["Attrition"].map({
    "No": 0,
    "Yes": 1,
})

travel_mapping = {
    "Non-Travel": 0,
    "Travel_Rarely": 1,
    "Travel_Frequently": 2,
}

df["BusinessTravel_encoded"] = df["BusinessTravel"].map(travel_mapping)

df["Gender_encoded"] = df["Gender"].map({
    "Female": 0,
    "Male": 1,
})

df["OverTime_encoded"] = df["OverTime"].map({
    "No": 0,
    "Yes": 1,
})

df = pd.get_dummies(
    df,
    columns=[
        "MaritalStatus",
        "JobRole",
        "Department",
        "EducationField",
    ],
    dtype=int,
)


# ---------------------------------------------------------
# Feature groups
# ---------------------------------------------------------

target_feature = "Attrition_encoded"

skewed_features = [
    "MonthlyIncome",
    "NumCompaniesWorked",
    "TotalWorkingYears",
    "YearsAtCompany",
    "YearsSinceLastPromotion",
]

numerical_features = [
    "Age",
    "DailyRate",
    "DistanceFromHome",
    "Education",
    "EnvironmentSatisfaction",
    "HourlyRate",
    "JobInvolvement",
    "JobLevel",
    "JobSatisfaction",
    "MonthlyRate",
    "PercentSalaryHike",
    "PerformanceRating",
    "RelationshipSatisfaction",
    "StockOptionLevel",
    "TrainingTimesLastYear",
    "WorkLifeBalance",
    "YearsInCurrentRole",
    "YearsWithCurrManager",
]

ordinal_features = [
    "BusinessTravel_encoded",
]

encoded_categorical_features = [
    # Binary encoded
    "Gender_encoded",
    "OverTime_encoded",

    # Marital status
    "MaritalStatus_Divorced",
    "MaritalStatus_Married",
    "MaritalStatus_Single",

    # Job roles
    "JobRole_Healthcare Representative",
    "JobRole_Human Resources",
    "JobRole_Laboratory Technician",
    "JobRole_Manager",
    "JobRole_Manufacturing Director",
    "JobRole_Research Director",
    "JobRole_Research Scientist",
    "JobRole_Sales Executive",
    "JobRole_Sales Representative",

    # Departments
    "Department_Human Resources",
    "Department_Research & Development",
    "Department_Sales",

    # Education fields
    "EducationField_Human Resources",
    "EducationField_Life Sciences",
    "EducationField_Marketing",
    "EducationField_Medical",
    "EducationField_Other",
    "EducationField_Technical Degree",
]

hr_features = (
    skewed_features
    + numerical_features
    + ordinal_features
    + encoded_categorical_features
)


# ---------------------------------------------------------
# Validate required columns
# ---------------------------------------------------------

missing_features = [
    feature
    for feature in hr_features + [target_feature]
    if feature not in df.columns
]

if missing_features:
    raise KeyError(
        "The following required columns are missing:\n"
        + "\n".join(missing_features)
    )

if df[target_feature].isna().any():
    raise ValueError(
        "Attrition_encoded contains missing values. "
        "Check the original Attrition values."
    )


# ---------------------------------------------------------
# Prepare X and y
# ---------------------------------------------------------

X = df[hr_features]
y = df[target_feature]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
print("y_train shape:", y_train.shape)
print("y_test shape:", y_test.shape)


# ---------------------------------------------------------
# Preprocessing pipelines
# ---------------------------------------------------------

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

ordinal_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
    ]
)

categorical_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("skewed", skewed_pipeline, skewed_features),
        ("numeric", numeric_pipeline, numerical_features),
        ("ordinal", ordinal_pipeline, ordinal_features),
        (
            "categorical",
            categorical_pipeline,
            encoded_categorical_features,
        ),
    ],
    remainder="drop",
    verbose_feature_names_out=False,
)


# ---------------------------------------------------------
# Complete model pipeline
# ---------------------------------------------------------

model_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
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


# ---------------------------------------------------------
# Configure MLflow
# ---------------------------------------------------------

tracking_uri = f"sqlite:///{MLFLOW_DB_PATH.as_posix()}"

mlflow.set_tracking_uri(tracking_uri)
experiment = mlflow.set_experiment("attrition")

print("\nMLflow version:", mlflow.__version__)
print("Tracking URI:", mlflow.get_tracking_uri())
print("Experiment name:", experiment.name)
print("Experiment ID:", experiment.experiment_id)
print("Database location:", MLFLOW_DB_PATH)


# ---------------------------------------------------------
# Train, evaluate, and log model
# ---------------------------------------------------------

with mlflow.start_run(run_name="logistic_regression") as run:
    model_pipeline.fit(X_train, y_train)

    y_pred = model_pipeline.predict(X_test)
    y_prob = model_pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(
            y_test,
            y_pred,
            zero_division=0,
        ),
        "recall": recall_score(
            y_test,
            y_pred,
            zero_division=0,
        ),
        "f1_score": f1_score(
            y_test,
            y_pred,
            zero_division=0,
        ),
        "roc_auc": roc_auc_score(y_test, y_prob),
        "average_precision": average_precision_score(
            y_test,
            y_prob,
        ),
    }

    parameters = {
        "model": "LogisticRegression",
        "class_weight": "balanced",
        "max_iter": 1000,
        "test_size": 0.20,
        "random_state": 42,
        "number_of_features": len(hr_features),
    }

    mlflow.log_params(parameters)
    mlflow.log_metrics(metrics)

    input_example = X_train.head(5)
    model_signature = infer_signature(
        X_train,
        model_pipeline.predict(X_train),
    )

    mlflow.sklearn.log_model(
        sk_model=model_pipeline,
        name="attrition_model",
        signature=model_signature,
        input_example=input_example,
    )

    report = classification_report(
        y_test,
        y_pred,
        zero_division=0,
    )

    matrix = confusion_matrix(y_test, y_pred)

    report_path = BASE_DIR / "classification_report.txt"
    matrix_path = BASE_DIR / "confusion_matrix.csv"

    report_path.write_text(report, encoding="utf-8")

    pd.DataFrame(
        matrix,
        index=["Actual_No", "Actual_Yes"],
        columns=["Predicted_No", "Predicted_Yes"],
    ).to_csv(matrix_path)

    mlflow.log_artifact(str(report_path))
    mlflow.log_artifact(str(matrix_path))

    print("\nRun ID:", run.info.run_id)
    print("\nMetrics:")
    for metric_name, metric_value in metrics.items():
        print(f"{metric_name}: {metric_value:.4f}")

    print("\nConfusion Matrix:")
    print(matrix)

    print("\nClassification Report:")
    print(report)

print("\nModel training and MLflow logging completed successfully.")
