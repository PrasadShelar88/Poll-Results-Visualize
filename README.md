# 📊 Poll Results Visualizer

## 🚀 Overview

The **Poll Results Visualizer** is a data analytics project that processes poll/survey data and transforms it into meaningful insights using visualizations and dashboards.

This project helps users quickly understand trends, preferences, and feedback through interactive charts and reports.

---

## 🎯 Objective

* Import poll/survey data (CSV, Google Forms, synthetic data)
* Clean and preprocess responses
* Analyze voting patterns and feedback
* Visualize results using charts
* Provide insights for decision-making
* (Optional) Display results via an interactive dashboard

---

## 🧠 Problem Statement

Raw survey data is:

* Difficult to interpret
* Time-consuming to analyze
* Not decision-friendly

This project solves that by converting raw data into:

* Visual charts
* Summary insights
* Interactive dashboards

---

## ✨ Features

* 📥 CSV Upload Support
* 🧹 Data Cleaning & Preprocessing
* 📊 Vote Count & Percentage Analysis
* 📈 Visualizations:

  * Bar Charts
  * Pie Charts
  * Histograms
  * Trend Analysis
* 🌍 Demographic Analysis (Age, Gender, Region)
* ☁️ Word Cloud for Feedback
* 🖥️ Streamlit Dashboard (Backend)
* ⚛️ React Dashboard (Frontend)

---

## 🛠️ Tech Stack

### Backend

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Streamlit
* WordCloud

### Frontend

* React (Vite)
* JavaScript
* Chart Libraries (Chart.js / Recharts)

---

## 📁 Project Structure

```
Poll-Results-Visualizer/
│
├── backend/
│   ├── data/
│   ├── outputs/
│   ├── src/
│   ├── main.py
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── README.md
│
└── README.md
```

---

## ⚙️ Installation Guide

### 🔹 Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

---

### 🔹 Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## ▶️ How to Run

### Run Backend (Analysis Script)

```bash
python main.py
```

### Run Streamlit Dashboard

```bash
streamlit run app.py
```

### Run Frontend

```bash
npm run dev
```

---

## 📊 Expected Outputs

* 📁 Cleaned dataset (`cleaned_poll_data.csv`)
* 📊 Bar chart → tool popularity
* 🥧 Pie chart → vote share
* 📈 Histogram → satisfaction distribution
* 🌍 Demographic comparison charts
* ☁️ Word cloud → feedback analysis
* 🖥️ Dashboard UI

---

---

## 📈 Example Insights

* 🔥 Most preferred tool identified
* 📊 Percentage share of each option
* 📉 Trends over time
* 🧠 Feedback patterns via word cloud

---

## 💼 Industry Relevance

Used in:

* Market Research
* Election Polling
* Customer Feedback Analysis
* Employee Satisfaction Surveys
* Education Feedback Systems

Companies using similar systems:

* Google Forms + Looker Studio
* SurveyMonkey
* Qualtrics
* YouGov

---

## 🧪 Virtual Simulation

* Synthetic poll data generation
* Random response distribution
* Demographic segmentation
* Automated insight generation

---

## 🔮 Future Improvements

* Real-time polling system
* API-based backend integration
* Sentiment analysis (NLP)
* Power BI / Tableau dashboard
* Live dashboard updates
* User authentication system

---

## ❗ Troubleshooting

### Module Not Found

```bash
pip install <module_name>
```

### CSV Not Loading

* Check file path
* Ensure correct filename

### Charts Not Showing

```python
plt.show()
```

---

## 🧑‍💻 Author

**Prasad Shelar**
B.Tech CSE | 

---

## ⭐ Contribute

Feel free to fork, improve, and submit pull requests!

---

