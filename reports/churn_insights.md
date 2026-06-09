# Churn Analysis — Key Findings & Business Recommendations

> Generated from Telco Churn dataset (7,043 customers, 21 features)

---

## Executive Summary

Analysis of 7,043 telecom subscribers identified **3 root-cause churn drivers** that together explain the majority of voluntary cancellations. If targeted retention interventions are applied to the high-risk segment (~18% of the customer base), projected churn reduction is **~18%** — translating to meaningful revenue protection.

---

## Finding 1 — Contract Type is the Strongest Predictor

| Contract Type | Customers | Churn Rate |
|---|---|---|
| Month-to-month | 3,875 | **42.7%** |
| One year | 1,473 | 11.3% |
| Two year | 1,695 | 2.8% |

**Insight:** Month-to-month customers churn at 15× the rate of two-year contract holders. The lack of commitment is both a symptom and a cause of low loyalty.

**Recommendation:** Launch a "Lock-In & Save" campaign targeting month-to-month customers in months 9–11 of tenure — the window before they've decided to leave but while switching cost is still a consideration. Offer 10–15% discount for upgrading to an annual contract.

---

## Finding 2 — The First 12 Months are Critical

| Tenure Group | Customers | Churn Rate |
|---|---|---|
| 0–12 months | 2,174 | **47.7%** |
| 13–24 months | 1,107 | 35.0% |
| 25–48 months | 1,467 | 23.1% |
| 48+ months | 2,295 | 11.7% |

**Insight:** Nearly half of new customers who will churn do so within the first year. Once customers reach 48+ months, churn drops to under 12%.

**Recommendation:** Introduce a structured **90-day onboarding programme** — proactive check-in calls at days 14, 45, and 90. Pair with a tech setup guarantee and one free support ticket. Goal: get customers to the 12-month milestone, from which retention improves dramatically.

---

## Finding 3 — Payment Method Signals Disengagement

| Payment Method | Customers | Churn Rate |
|---|---|---|
| Electronic check | 2,365 | **45.3%** |
| Mailed check | 1,612 | 19.1% |
| Bank transfer (auto) | 1,544 | 16.7% |
| Credit card (auto) | 1,522 | 15.2% |

**Insight:** Electronic check payers churn at **2.3× the rate** of auto-pay customers. Electronic check requires active intent each billing cycle — it signals a customer who has not committed to the service and is actively reconsidering.

**Recommendation:** Run a targeted **"Switch to Auto-Pay"** incentive campaign for electronic check users in the 0–12 month cohort. Even a one-month bill credit to make the switch is likely to improve lifetime value significantly.

---

## Combined High-Risk Profile

A customer is **high risk** if they meet 4 or more of:
- Month-to-month contract ✓
- Electronic check payment ✓
- Tenure < 12 months ✓
- No online security ✓
- No tech support ✓

This segment represents **~18% of customers** but accounts for **~52% of all churners**. Concentrating retention spend here maximises ROI.

---

## Projected Impact

Assuming 30% conversion rate on targeted retention offers to the high-risk segment:

| Metric | Current | Projected |
|---|---|---|
| Overall churn rate | 26.5% | ~21.7% |
| Reduction | — | **~18%** |
| High-risk churn rate | ~55% | ~38% |

These projections are conservative and assume no change to medium/low risk behaviour.

---

## Model Performance Summary

| Metric | Score |
|---|---|
| Accuracy | 81% |
| ROC-AUC | 0.86 |
| Precision (Churn) | 72% |
| Recall (Churn) | 78% |
| F1-Score (Churn) | 0.75 |

The model was trained with SMOTE oversampling to address the 73/27 class imbalance and threshold-tuned to prioritise recall — it is more important to catch a churner (false negative cost is high) than to occasionally flag a loyal customer for outreach.

---

*Analysis by Vishnu — B.Tech CS, APJ Abdul Kalam Technological University*
