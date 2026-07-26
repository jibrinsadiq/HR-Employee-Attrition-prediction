import pandas as pd


TARGET_MAPPING = {
    "No": 0,
    "Yes": 1,
}


def clean_hr_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Apply lightweight, reusable cleaning.

    Encoding is deliberately kept out of this function because the
    production scikit-learn pipeline handles categorical encoding.
    """
    cleaned = dataframe.copy()
    cleaned.columns = cleaned.columns.str.strip()

    if "Attrition" not in cleaned.columns:
        raise KeyError("Required target column 'Attrition' is missing.")

    cleaned["Attrition"] = cleaned["Attrition"].astype(str).str.strip()
    cleaned["Attrition_encoded"] = cleaned["Attrition"].map(
        TARGET_MAPPING
    )

    invalid_target_rows = cleaned["Attrition_encoded"].isna()
    if invalid_target_rows.any():
        invalid_values = sorted(
            cleaned.loc[
                invalid_target_rows,
                "Attrition",
            ].unique().tolist()
        )
        raise ValueError(
            "Unexpected Attrition values found: "
            f"{invalid_values}"
        )

    return cleaned
