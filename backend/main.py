from __future__ import annotations

from pathlib import Path
import pandas as pd

from src.data_generator import create_dataset
from src.preprocess import clean_poll_data
from src.analyze import save_analysis_outputs, generate_insights, vote_share_summary
from src.visualize import save_charts


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
RAW_FILE = DATA_DIR / "poll_data.csv"
CLEAN_FILE = DATA_DIR / "cleaned_poll_data.csv"



def run_pipeline() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("[1/4] Generating synthetic poll data...")
    create_dataset(RAW_FILE, n_rows=500, seed=42)

    print("[2/4] Cleaning dataset...")
    df = clean_poll_data(RAW_FILE, CLEAN_FILE)

    print("[3/4] Saving analysis outputs...")
    save_analysis_outputs(df, OUTPUT_DIR)

    print("[4/4] Saving charts...")
    save_charts(df, OUTPUT_DIR)

    insights = generate_insights(df)
    summary = vote_share_summary(df)

    print("\n===== POLL RESULTS SUMMARY =====")
    print(summary.to_string(index=False))
    print("\n===== KEY INSIGHTS =====")
    print(f"Total responses: {insights['total_responses']}")
    print(f"Top tool: {insights['top_tool']} ({insights['top_share_percent']}%)")
    print(f"Average satisfaction: {insights['average_satisfaction']}")
    print("\nAll outputs saved in outputs/")


if __name__ == "__main__":
    run_pipeline()
