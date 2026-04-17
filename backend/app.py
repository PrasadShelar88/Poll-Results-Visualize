from __future__ import annotations

from pathlib import Path
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from src.data_generator import create_dataset
from src.preprocess import clean_poll_data
from src.analyze import vote_share_summary, generate_insights

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_FILE = DATA_DIR / "poll_data.csv"
CLEAN_FILE = DATA_DIR / "cleaned_poll_data.csv"

st.set_page_config(page_title="Poll Results Visualizer", layout="wide")
sns.set_theme(style="whitegrid")


@st.cache_data
def load_data() -> pd.DataFrame:
    DATA_DIR.mkdir(exist_ok=True)
    if not RAW_FILE.exists():
        create_dataset(RAW_FILE, n_rows=500, seed=42)
    if not CLEAN_FILE.exists():
        clean_poll_data(RAW_FILE, CLEAN_FILE)
    return pd.read_csv(CLEAN_FILE)


def filtered_data(df: pd.DataFrame) -> pd.DataFrame:
    regions = st.sidebar.multiselect("Select Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
    age_groups = st.sidebar.multiselect("Select Age Group", sorted(df["Age Group"].unique()), default=sorted(df["Age Group"].unique()))
    tools = st.sidebar.multiselect("Select Preferred Tool", sorted(df["Preferred Tool"].unique()), default=sorted(df["Preferred Tool"].unique()))
    return df[df["Region"].isin(regions) & df["Age Group"].isin(age_groups) & df["Preferred Tool"].isin(tools)]


def main() -> None:
    st.title("📊 Poll Results Visualizer")
    st.caption("Analyze poll responses, compare preferences, and generate decision-ready insights.")

    df = load_data()
    df = filtered_data(df)
    insights = generate_insights(df)

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Responses", insights["total_responses"])
    c2.metric("Top Tool", insights["top_tool"])
    c3.metric("Average Satisfaction", insights["average_satisfaction"])

    if st.checkbox("Show filtered dataset preview"):
        st.dataframe(df, use_container_width=True)

    st.subheader("Vote Share Summary")
    st.dataframe(vote_share_summary(df), use_container_width=True)

    left, right = st.columns(2)

    with left:
        st.subheader("Tool Preference")
        tool_counts = df["Preferred Tool"].value_counts()
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x=tool_counts.index, y=tool_counts.values, hue=tool_counts.index, legend=False, ax=ax)
        ax.set_xlabel("Tool")
        ax.set_ylabel("Votes")
        ax.tick_params(axis="x", rotation=20)
        st.pyplot(fig)

    with right:
        st.subheader("Satisfaction Distribution")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(df["Satisfaction (1-5)"], bins=5, kde=True, ax=ax, color="skyblue")
        st.pyplot(fig)

    left, right = st.columns(2)

    with left:
        st.subheader("Region-wise Comparison")
        region_summary = pd.crosstab(df["Region"], df["Preferred Tool"])
        st.bar_chart(region_summary)

    with right:
        st.subheader("Responses Over Time")
        trend = df.groupby("Date").size()
        st.line_chart(trend)

    st.subheader("Feedback Word Cloud")
    text = " ".join(df["Feedback"].astype(str).tolist())
    if text.strip():
        wc = WordCloud(width=1000, height=400, background_color="white").generate(text)
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.info("No feedback text available for the current filters.")


if __name__ == "__main__":
    main()
