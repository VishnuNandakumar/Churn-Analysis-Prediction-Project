# Power BI Dashboard — Setup Guide

## Overview

The Churn Retention Dashboard provides retention teams with a live, filterable view of customer risk segments, churn drivers, and cohort trends.

---

## Data Sources to Connect

Once you've run the full Python pipeline, connect Power BI to:

| Source | File / Table | Purpose |
|---|---|---|
| CSV | `data/processed/churn_scores.csv` | Main customer risk table |
| CSV | `data/processed/telco_churn_clean.csv` | Feature-level analysis |
| SQL Output | `sql/risk_segmentation.sql` result | Segment summary card |

---

## Dashboard Pages

### Page 1 — Executive Summary
**KPI Cards:**
- Total customers
- Overall churn rate (%)
- High-risk customer count
- Projected monthly revenue at risk

**Visuals:**
- Donut: Churn vs Retained
- Bar: Churn rate by Contract Type
- Line: Churn rate by Tenure Group

---

### Page 2 — Risk Segment Explorer
**Visuals:**
- Clustered bar: Customer count by Risk Segment (High / Medium / Low)
- Scatter: Monthly Charges vs Tenure, coloured by Churn Prediction
- Table: Top 100 high-risk customers (customerID, risk score, monthly charge)

**Slicers:**
- Risk Segment
- Contract Type
- Payment Method
- Tenure Group

---

### Page 3 — Cohort Analysis
**Visuals:**
- Matrix (heatmap): Churn rate by Cohort Bucket × Contract Type
- Waterfall: Cumulative churn by tenure milestone
- Line: Avg monthly charge trend across cohorts

---

### Page 4 — Driver Insights
**Visuals:**
- Horizontal bar: Top 10 churn drivers (from feature importance)
- Card: "If high-risk customers are retained → ~18% churn reduction"
- Grouped bar: Actual churn rate by Payment Method

---

## Slicers (Global — applies to all pages)

| Slicer | Field |
|---|---|
| Region | `InternetService` (proxy) |
| Plan Tier | `Contract` |
| Cohort Month | `tenure_group` |
| Risk Segment | `risk_segment` |

---

## DAX Measures

```dax
-- Churn Rate
Churn Rate = 
    DIVIDE(
        COUNTROWS(FILTER('churn_scores', 'churn_scores'[churn_prediction] = 1)),
        COUNTROWS('churn_scores')
    )

-- Monthly Revenue at Risk (High Risk only)
Revenue At Risk = 
    CALCULATE(
        SUM('churn_scores'[MonthlyCharges]),
        'churn_scores'[risk_segment] = "High"
    )

-- Avg Churn Probability
Avg Churn Prob = AVERAGE('churn_scores'[churn_probability])
```

---

## Colour Scheme

| Segment | Hex |
|---|---|
| High Risk | `#EF4444` |
| Medium Risk | `#F59E0B` |
| Low Risk | `#10B981` |
| Brand Blue | `#3B82F6` |
| Background | `#F8FAFC` |
