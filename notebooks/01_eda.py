"""
01_eda.py  →  convert to notebook:  jupytext --to notebook 01_eda.py
─────────────────────────────────────────────────────────────────────
Exploratory Data Analysis — Telco Customer Churn
"""

# %% [markdown]
# # 📊 Exploratory Data Analysis — Telco Customer Churn
#
# **Goal:** Understand the data structure, identify behavioral signals,
# and surface the root-cause drivers of churn before modelling.

# %% Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.dpi"] = 120

# %% Load data
df = pd.read_csv("../data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")
print(f"Shape: {df.shape}")
df.head()

# %% Basic info
df.info()

# %% Fix TotalCharges dtype
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["Churn_binary"] = (df["Churn"] == "Yes").astype(int)

print(f"\nChurn rate: {df['Churn_binary'].mean():.1%}")
print(f"Missing values:\n{df.isna().sum()[df.isna().sum() > 0]}")

# %% [markdown]
# ## 1. Churn Rate by Contract Type

# %%
fig, ax = plt.subplots(figsize=(7, 4))
contract_churn = df.groupby("Contract")["Churn_binary"].mean().sort_values(ascending=False)
contract_churn.mul(100).plot.bar(ax=ax, color=["#EF4444", "#F59E0B", "#10B981"], edgecolor="white")
ax.set_title("Churn Rate by Contract Type", fontsize=13, fontweight="bold")
ax.set_ylabel("Churn Rate (%)")
ax.set_xlabel("")
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
for bar in ax.patches:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f"{bar.get_height():.1f}%", ha="center", fontsize=10)
plt.tight_layout()
plt.savefig("../reports/figures/churn_by_contract.png")
plt.show()

# %% [markdown]
# **Finding:** Month-to-month contracts churn at ~42% — 15× the two-year rate.

# %% Tenure distribution
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Tenure histogram split by churn
for label, colour in [("No", "#3B82F6"), ("Yes", "#EF4444")]:
    df[df["Churn"] == label]["tenure"].plot.hist(
        bins=30, alpha=0.6, color=colour, label=label, ax=axes[0]
    )
axes[0].set_title("Tenure Distribution by Churn")
axes[0].set_xlabel("Tenure (months)")
axes[0].legend(title="Churned")

# Churn rate by tenure bucket
bins = [0, 12, 24, 48, df["tenure"].max() + 1]
labels = ["0–12", "13–24", "25–48", "48+"]
df["tenure_group"] = pd.cut(df["tenure"], bins=bins, labels=labels, right=False)
tenure_churn = df.groupby("tenure_group")["Churn_binary"].mean().mul(100)
tenure_churn.plot.bar(ax=axes[1], color="#3B82F6", edgecolor="white")
axes[1].set_title("Churn Rate by Tenure Group")
axes[1].set_ylabel("Churn Rate (%)")
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=0)

plt.tight_layout()
plt.savefig("../reports/figures/tenure_analysis.png")
plt.show()

# %% Payment method analysis
payment_churn = (
    df.groupby("PaymentMethod")["Churn_binary"]
    .agg(["mean", "count"])
    .rename(columns={"mean": "churn_rate", "count": "customers"})
    .sort_values("churn_rate", ascending=False)
)
payment_churn["churn_rate_pct"] = payment_churn["churn_rate"].mul(100).round(1)
print(payment_churn)

# %% Monthly charges — churned vs retained
fig, ax = plt.subplots(figsize=(7, 4))
for label, colour in [("No", "#3B82F6"), ("Yes", "#EF4444")]:
    df[df["Churn"] == label]["MonthlyCharges"].plot.kde(
        ax=ax, color=colour, label=f"Churned: {label}", linewidth=2
    )
ax.set_title("Monthly Charges Distribution — Churned vs Retained")
ax.set_xlabel("Monthly Charges ($)")
ax.legend()
plt.tight_layout()
plt.savefig("../reports/figures/monthly_charges_distribution.png")
plt.show()

# %% Correlation heatmap (numeric features)
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(
    df[numeric_cols].corr(),
    annot=True, fmt=".2f", cmap="coolwarm", center=0,
    linewidths=0.5, ax=ax
)
ax.set_title("Correlation Matrix — Numeric Features")
plt.tight_layout()
plt.savefig("../reports/figures/correlation_heatmap.png")
plt.show()

# %% [markdown]
# ## Summary — Top EDA Findings
#
# | Driver | Signal | Churn Impact |
# |---|---|---|
# | Contract type | Month-to-month | ~42% churn rate |
# | Tenure | First 12 months | ~48% churn rate |
# | Payment method | Electronic check | 2.3× average |
#
# These 3 drivers will be the primary features in the ML model.
