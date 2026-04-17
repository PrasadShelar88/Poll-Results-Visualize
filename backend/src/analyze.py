from __future__ import annotations

from pathlib import Path
import json
import pandas as pd



def vote_share_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = df["Preferred Tool"].value_counts().rename_axis("Preferred Tool").reset_index(name="Votes")
    summary["Share %"] = (summary["Votes"] / summary["Votes"].sum() * 100).round(2)
    return summary



def region_wise_summary(df: pd.DataFrame) -> pd.DataFrame:
    pivot = pd.crosstab(df["Region"], df["Preferred Tool"])
    return pivot



def demographic_summary(df: pd.DataFrame) -> pd.DataFrame:
    pivot = pd.crosstab(df["Age Group"], df["Preferred Tool"])
    return pivot



def daily_trend(df: pd.DataFrame) -> pd.DataFrame:
    trend = df.groupby("Date").size().reset_index(name="Responses")
    return trend



def generate_insights(df: pd.DataFrame) -> dict:
    vote_summary = vote_share_summary(df)
    top_tool = vote_summary.iloc[0]["Preferred Tool"]
    top_share = float(vote_summary.iloc[0]["Share %"])
    avg_rating = float(df["Satisfaction (1-5)"].mean().round(2))

    region_pref = (
        df.groupby(["Region", "Preferred Tool"])
        .size()
        .reset_index(name="Votes")
        .sort_values(["Region", "Votes"], ascending=[True, False])
        .drop_duplicates(subset=["Region"])
    )

    insights = {
        "top_tool": top_tool,
        "top_share_percent": top_share,
        "average_satisfaction": avg_rating,
        "region_leaders": region_pref.to_dict(orient="records"),
        "total_responses": int(len(df)),
    }
    return insights



def save_analysis_outputs(df: pd.DataFrame, output_dir: str | Path) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    vote_share_summary(df).to_csv(output_dir / "vote_share_summary.csv", index=False)
    region_wise_summary(df).to_csv(output_dir / "region_wise_summary.csv")
    demographic_summary(df).to_csv(output_dir / "age_group_summary.csv")
    daily_trend(df).to_csv(output_dir / "daily_response_trend.csv", index=False)

    with open(output_dir / "insights.json", "w", encoding="utf-8") as f:
        json.dump(generate_insights(df), f, indent=2)


if __name__ == "__main__":
    data = pd.read_csv("data/cleaned_poll_data.csv")
    save_analysis_outputs(data, "outputs")
    print("Analysis outputs saved in outputs/")
