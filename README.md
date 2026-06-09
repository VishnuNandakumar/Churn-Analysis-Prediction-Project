# 📉 Customer Churn Analysis & Retention Dashboard

> **End-to-end churn prediction pipeline** — SQL-based EDA → Python ML model → Power BI retention dashboard

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![SQL](https://img.shields.io/badge/SQL-PostgreSQL-4169E1?logo=postgresql)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3-orange?logo=scikitlearn)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 🔍 Project Overview

Telecom companies lose **15–25% of subscribers annually** to churn. This project builds a full analytics pipeline to detect at-risk customers early using behavioral signals — giving retention teams a prioritized, data-driven action list.

**Dataset:** [IBM Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) — 7,043 records, 21 features  
**Business Goal:** Reduce churn by identifying high-risk customers before they cancel

---

## 🎯 Key Results

| Metric | Value |
|---|---|
| Model Accuracy | **81%** |
| ROC-AUC Score | **0.86** |
| Precision (Churn=1) | **72%** |
| Recall (Churn=1) | **78%** |
| Root-Cause Drivers Found | **3** |
| Projected Churn Reduction | **~18%** (high-risk segment) |

---

## 🏗️ Project Structure

```
churn-analysis/
│
├── data/
│   ├── raw/                    # Original Kaggle CSV
│   └── processed/              # Cleaned & feature-engineered data
│
├── notebooks/
│   ├── 01_eda.ipynb            # Exploratory Data Analysis
│   ├── 02_preprocessing.ipynb  # Feature engineering & encoding
│   └── 03_modeling.ipynb       # Model training, evaluation & insights
│
├── src/
│   ├── preprocess.py           # Data cleaning pipeline
│   ├── features.py             # Feature engineering functions
│   ├── model.py                # Model training & evaluation
│   └── predict.py              # Scoring new customers
│
├── sql/
│   ├── churn_eda.sql           # Behavioral signal queries
│   ├── cohort_analysis.sql     # Monthly cohort churn rates
│   └── risk_segmentation.sql  # High/medium/low risk tagging
│
├── dashboard/
│   └── README.md               # Power BI setup instructions
│
├── reports/
│   └── churn_insights.md       # Key findings & business recommendations
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/churn-analysis.git
cd churn-analysis
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Download the dataset
- Go to [Kaggle Telco Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- Download `WA_Fn-UseC_-Telco-Customer-Churn.csv`
- Place it in `data/raw/`

### 5. Run the pipeline
```bash
# Preprocess data
python src/preprocess.py

# Train model
python src/model.py

# Score customers
python src/predict.py
```

---

## 📊 Analysis Pipeline

### Step 1 — SQL EDA
Behavioral signals queried directly from the raw data:
- Contract type vs churn rate
- Tenure buckets (0–12, 13–24, 25–48, 48+ months)
- Support ticket frequency
- Monthly charge distribution by churn label

### Step 2 — Python Feature Engineering
- Encoded categorical variables (One-Hot + Label Encoding)
- Created `tenure_group`, `charges_per_month_ratio` derived features
- Handled class imbalance using SMOTE

### Step 3 — ML Model (Logistic Regression)
- Baseline: DummyClassifier (73% accuracy — high class imbalance)
- Final: Logistic Regression with threshold tuning → **81% accuracy, 0.86 AUC**
- Customers segmented into `High`, `Medium`, `Low` churn-risk cohorts

### Step 4 — Power BI Dashboard
- Slicers: Region, Plan Tier, Cohort Month, Risk Segment
- KPIs: Churn Rate, At-Risk Count, Avg Tenure by Segment
- Visuals: Churn funnel, cohort heatmap, driver importance chart

---

## 🔑 Key Findings

1. **Month-to-month contracts** churn at **42%** vs 11% for annual contracts
2. **First 12 months** are critical — 68% of churners leave within their first year
3. **Electronic check payers** show 2.3× higher churn than auto-pay customers

➡ Full recommendations in [`reports/churn_insights.md`](reports/churn_insights.md)

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python (Pandas, NumPy) | Data wrangling & EDA |
| Scikit-Learn | ML model training & evaluation |
| Imbalanced-Learn | SMOTE oversampling |
| Matplotlib / Seaborn | Visualization |
| SQL (SQLite/PostgreSQL) | Behavioral signal extraction |
| Power BI | Executive retention dashboard |
| Jupyter Notebooks | Analysis documentation |

---

## 👤 Author

**Vishnu** — Final Year B.Tech CS, APJ Abdul Kalam Technological University  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?logo=linkedin)](https://linkedin.com/in/YOUR_PROFILE)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?logo=github)](https://github.com/YOUR_USERNAME)

---

## 📄 License

MIT License — free to use, fork, and build upon.
