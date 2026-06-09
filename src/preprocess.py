"""
preprocess.py
─────────────
Cleans the raw Telco Churn CSV and outputs a model-ready DataFrame.

Usage:
    python src/preprocess.py
"""

import pandas as pd
import numpy as np
import os

RAW_PATH = "data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv"
OUT_PATH  = "data/processed/telco_churn_clean.csv"


# ── Helpers ──────────────────────────────────────────────────────────────────

def load_raw(path: str = RAW_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"[load]  {df.shape[0]:,} rows × {df.shape[1]} cols")
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Fix TotalCharges — arrives as string with blank spaces
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    blank_tc = df["TotalCharges"].isna().sum()
    print(f"[clean] {blank_tc} blank TotalCharges filled with 0 (new customers)")
    df["TotalCharges"].fillna(0, inplace=True)

    # Drop customerID — not a feature
    df.drop(columns=["customerID"], inplace=True)

    # Binary target
    df["Churn"] = (df["Churn"] == "Yes").astype(int)

    print(f"[clean] Churn rate: {df['Churn'].mean():.1%}")
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Tenure groups — business-meaningful buckets
    bins   = [0, 12, 24, 48, df["tenure"].max() + 1]
    labels = ["0–12 mo", "13–24 mo", "25–48 mo", "48+ mo"]
    df["tenure_group"] = pd.cut(df["tenure"], bins=bins, labels=labels, right=False)

    # Monthly charge ratio (how much of total spend is recent?)
    df["charges_ratio"] = np.where(
        df["TotalCharges"] > 0,
        df["MonthlyCharges"] / df["TotalCharges"],
        1.0
    )

    # Flag high-spend customers
    monthly_p75 = df["MonthlyCharges"].quantile(0.75)
    df["high_spend"] = (df["MonthlyCharges"] >= monthly_p75).astype(int)

    print(f"[feat]  Added tenure_group, charges_ratio, high_spend")
    return df


def encode(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Binary Yes/No columns → 1/0
    binary_cols = [
        "Partner", "Dependents", "PhoneService", "PaperlessBilling",
        "MultipleLines", "OnlineSecurity", "OnlineBackup",
        "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"
    ]
    for col in binary_cols:
        if col in df.columns:
            df[col] = df[col].map({"Yes": 1, "No": 0, "No phone service": 0,
                                   "No internet service": 0}).fillna(0).astype(int)

    # One-hot encode remaining categoricals
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    if cat_cols:
        df = pd.get_dummies(df, columns=cat_cols, drop_first=True)
        print(f"[enc]   One-hot encoded: {cat_cols}")

    return df


def save(df: pd.DataFrame, path: str = OUT_PATH) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"[save]  Written → {path}  ({df.shape[0]:,} rows × {df.shape[1]} cols)")


# ── Main ─────────────────────────────────────────────────────────────────────

def run_pipeline() -> pd.DataFrame:
    df = load_raw()
    df = clean(df)
    df = engineer_features(df)
    df = encode(df)
    save(df)
    return df


if __name__ == "__main__":
    run_pipeline()
