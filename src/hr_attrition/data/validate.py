import pandas as pd


def require_columns(
    dataframe: pd.DataFrame,
    required_columns: list[str],
) -> None:
    """Raise a clear error when expected model columns are missing."""
    missing = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing:
        raise KeyError(
            "The following required columns are missing: "
            + ", ".join(missing)
        )
