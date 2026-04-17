from __future__ import annotations

from pathlib import Path
import pandas as pd


REQUIRED_COLUMNS = [
    "Respondent ID",
    "Timestamp",
    "Age Group",
    "Gender",
    "Region",
    "Question",
    "Preferred Tool",
    "Satisfaction (1-5)",
    "Feedback",
]



def clean_poll_data(input_path: str | Path, output_path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(input_path)

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    df = df.drop_duplicates().copy()
    df = df.dropna(subset=["Preferred Tool", "Satisfaction (1-5)", "Region", "Age Group"])

    df["Preferred Tool"] = df["Preferred Tool"].astype(str).str.strip().str.title()
    df["Region"] = df["Region"].astype(str).str.strip().str.title()
    df["Age Group"] = df["Age Group"].astype(str).str.strip()
    df["Gender"] = df["Gender"].astype(str).str.strip().str.title()
    df["Feedback"] = df["Feedback"].fillna("No feedback")

    df["Satisfaction (1-5)"] = pd.to_numeric(df["Satisfaction (1-5)"], errors="coerce")
    df = df.dropna(subset=["Satisfaction (1-5)"])
    df["Satisfaction (1-5)"] = df["Satisfaction (1-5)"].clip(lower=1, upper=5).astype(int)

    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    df = df.dropna(subset=["Timestamp"])
    df["Date"] = df["Timestamp"].dt.date
    df["Feedback Length"] = df["Feedback"].astype(str).str.len()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    cleaned = clean_poll_data("data/poll_data.csv", "data/cleaned_poll_data.csv")
    print(f"Cleaned dataset saved with {len(cleaned)} rows")
