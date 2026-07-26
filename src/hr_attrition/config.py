from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
)

DEFAULT_ARTIFACT_DIR = PROJECT_ROOT / "artifacts"
DEFAULT_REPORT_DIR = PROJECT_ROOT / "reports"

DEFAULT_MLFLOW_DB_PATH = PROJECT_ROOT / "mlflow_attrition.db"
DEFAULT_MLFLOW_TRACKING_URI = (
    f"sqlite:///{DEFAULT_MLFLOW_DB_PATH.as_posix()}"
)
DEFAULT_MLFLOW_EXPERIMENT = "attrition"
