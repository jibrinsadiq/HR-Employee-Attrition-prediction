from pathlib import Path

from _bootstrap import PROJECT_ROOT  # noqa: F401

from hr_attrition.config import DEFAULT_DATA_PATH
from hr_attrition.data.clean import clean_hr_data
from hr_attrition.data.load import load_hr_data


def main() -> None:
    dataframe = load_hr_data(DEFAULT_DATA_PATH)
    cleaned = clean_hr_data(dataframe)

    output_path = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "hr_attrition_cleaned.csv"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(output_path, index=False)

    print("Raw shape:", dataframe.shape)
    print("Cleaned shape:", cleaned.shape)
    print("Saved cleaned data to:", output_path)


if __name__ == "__main__":
    main()
