from pathlib import Path

import pandas as pd


def load_hr_data(path: str | Path) -> pd.DataFrame:
    """Load the IBM HR attrition CSV with basic path validation."""
    data_path = Path(path)

    if not data_path.exists():
        raise FileNotFoundError(
            f"HR dataset not found: {data_path.resolve()}"
        )

    dataframe = pd.read_csv(data_path)

    if dataframe.empty:
        raise ValueError("The HR dataset is empty.")

    return dataframe
