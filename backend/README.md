# Poll Results Visualizer Backend

A complete beginner-friendly yet professional Python project for analyzing poll or survey data, generating charts, exporting summary files, and running an interactive Streamlit dashboard.

## Features
- Synthetic poll dataset generation
- CSV cleaning and preprocessing
- Vote/share analysis
- Region-wise and age-group comparisons
- Satisfaction distribution analysis
- Feedback word cloud
- Streamlit dashboard
- Exported charts and summary CSV/JSON files

## Project Structure
```
poll_results_visualizer_backend/
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── data/
├── outputs/
└── src/
    ├── __init__.py
    ├── data_generator.py
    ├── preprocess.py
    ├── analyze.py
    └── visualize.py
```

## Setup
### Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Mac/Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run main pipeline
```bash
python main.py
```

## Run dashboard
```bash
streamlit run app.py
```

## Outputs generated
- `data/poll_data.csv`
- `data/cleaned_poll_data.csv`
- `outputs/vote_share_summary.csv`
- `outputs/region_wise_summary.csv`
- `outputs/age_group_summary.csv`
- `outputs/daily_response_trend.csv`
- `outputs/insights.json`
- chart PNG files in `outputs/`

## Ideal for
- Data Analyst portfolio
- Business Analyst practice
- Survey and feedback analytics demos
- Placement and internship GitHub proof projects
