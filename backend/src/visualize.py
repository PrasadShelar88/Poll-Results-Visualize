from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from wordcloud import WordCloud

sns.set_theme(style="whitegrid")



def save_charts(df: pd.DataFrame, output_dir: str | Path) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    tool_counts = df["Preferred Tool"].value_counts()

    plt.figure(figsize=(9, 5))
    sns.barplot(x=tool_counts.index, y=tool_counts.values, hue=tool_counts.index, legend=False)
    plt.title("Most Preferred Tools")
    plt.xlabel("Tool")
    plt.ylabel("Votes")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(output_dir / "bar_chart_tool_preference.png")
    plt.close()

    plt.figure(figsize=(7, 7))
    plt.pie(tool_counts.values, labels=tool_counts.index, autopct="%1.1f%%", startangle=90)
    plt.title("Vote Share by Tool")
    plt.tight_layout()
    plt.savefig(output_dir / "pie_chart_vote_share.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.histplot(df["Satisfaction (1-5)"], bins=5, kde=True, color="skyblue")
    plt.title("Satisfaction Rating Distribution")
    plt.xlabel("Rating")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(output_dir / "histogram_satisfaction.png")
    plt.close()

    region_summary = pd.crosstab(df["Region"], df["Preferred Tool"])
    region_summary.plot(kind="bar", stacked=True, figsize=(10, 6))
    plt.title("Region-wise Tool Preference")
    plt.xlabel("Region")
    plt.ylabel("Responses")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_dir / "stacked_region_preference.png")
    plt.close()

    trend = df.groupby("Date").size()
    plt.figure(figsize=(10, 5))
    trend.plot(marker="o")
    plt.title("Daily Poll Submissions")
    plt.xlabel("Date")
    plt.ylabel("Responses")
    plt.tight_layout()
    plt.savefig(output_dir / "line_daily_trend.png")
    plt.close()

    text = " ".join(df["Feedback"].astype(str).tolist())
    wordcloud = WordCloud(width=1000, height=500, background_color="white").generate(text)
    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Feedback Word Cloud")
    plt.tight_layout()
    plt.savefig(output_dir / "wordcloud_feedback.png")
    plt.close()


if __name__ == "__main__":
    data = pd.read_csv("data/cleaned_poll_data.csv")
    save_charts(data, "outputs")
    print("Charts saved in outputs/")
