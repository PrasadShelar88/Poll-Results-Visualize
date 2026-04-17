from __future__ import annotations

from pathlib import Path
import random
import numpy as np
import pandas as pd


AGE_GROUPS = ["18-24", "25-34", "35-44", "45-54", "55+"]
GENDERS = ["Male", "Female", "Other"]
REGIONS = ["North", "South", "East", "West", "Central"]
QUESTIONS = [
    "Which data tool do you prefer for analytics tasks?",
    "How satisfied are you with your current analytics workflow?",
]
TOOLS = ["Python", "Excel", "Power BI", "Tableau", "R"]
COMMENTS = {
    "Python": [
        "Python is flexible and powerful",
        "Great for automation and analysis",
        "Best for data science projects",
    ],
    "Excel": [
        "Easy for quick reports",
        "Useful for beginners",
        "Great for day to day analysis",
    ],
    "Power BI": [
        "Strong dashboard experience",
        "Useful for business reporting",
        "Interactive visuals are helpful",
    ],
    "Tableau": [
        "Very good for storytelling",
        "Beautiful dashboards",
        "Fast for interactive charts",
    ],
    "R": [
        "Good for statistics",
        "Helpful for research analysis",
        "Useful for academic work",
    ],
}


def weighted_choice(region: str, age_group: str) -> str:
    base = {
        "Python": 0.32,
        "Excel": 0.22,
        "Power BI": 0.18,
        "Tableau": 0.16,
        "R": 0.12,
    }

    if age_group == "18-24":
        base["Python"] += 0.08
        base["Excel"] -= 0.03
    elif age_group == "45-54":
        base["Excel"] += 0.05
        base["Power BI"] += 0.02
    elif age_group == "55+":
        base["Excel"] += 0.06
        base["R"] -= 0.02

    if region == "West":
        base["Power BI"] += 0.04
    elif region == "South":
        base["Python"] += 0.04
    elif region == "North":
        base["Tableau"] += 0.03

    options = list(base.keys())
    weights = np.array(list(base.values()), dtype=float)
    weights = weights / weights.sum()
    return str(np.random.choice(options, p=weights))



def create_dataset(output_path: str | Path, n_rows: int = 500, seed: int = 42) -> pd.DataFrame:
    random.seed(seed)
    np.random.seed(seed)

    start_date = pd.Timestamp("2025-01-01")
    rows: list[dict] = []

    for i in range(1, n_rows + 1):
        age_group = random.choice(AGE_GROUPS)
        gender = random.choice(GENDERS)
        region = random.choice(REGIONS)
        timestamp = start_date + pd.to_timedelta(random.randint(0, 119), unit="D") + pd.to_timedelta(random.randint(0, 86399), unit="s")
        preferred_tool = weighted_choice(region, age_group)
        satisfaction = int(np.clip(np.random.normal(loc=4.0, scale=0.9), 1, 5))
        feedback = random.choice(COMMENTS[preferred_tool])

        rows.append(
            {
                "Respondent ID": f"R{i:04d}",
                "Timestamp": timestamp,
                "Age Group": age_group,
                "Gender": gender,
                "Region": region,
                "Question": QUESTIONS[0],
                "Preferred Tool": preferred_tool,
                "Satisfaction (1-5)": satisfaction,
                "Feedback": feedback,
            }
        )

    df = pd.DataFrame(rows)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    path = Path("data/poll_data.csv")
    df = create_dataset(path)
    print(f"Dataset created: {path} ({len(df)} rows)")
