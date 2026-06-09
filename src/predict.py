"""
predict.py
──────────
Loads the trained model and scores a customer DataFrame,
appending churn probability and risk segment.

Usage:
    python src/predict.py                         # scores processed test slice
    python src/predict.py --input my_customers.csv
"""

import argparse
import os
import joblib
import pandas as pd
import numpy as np

MODEL_DIR = "models"
DATA_PATH = "data/processed/telco_churn_clean.csv"
OUT_PATH  = "data/processed/churn_scores.csv"


def load_artifacts(model_dir: str = MODEL_DIR):
    clf   = joblib.load(os.path.join(model_dir, "churn_model.pkl"))
    scaler = joblib.load(os.path.join(model_dir, "scaler.pkl"))
    feats  = joblib.load(os.path.join(model_dir, "feature_names.pkl"))
    return clf, scaler, feats


def align_features(df: pd.DataFrame, feature_names: list) -> pd.DataFrame:
    """Ensure column alignment with training set."""
    for col in feature_names:
        if col not in df.columns:
            df[col] = 0
    return df[feature_names]


def risk_segment(prob: float) -> str:
    if prob >= 0.65:
        return "High"
    elif prob >= 0.35:
        return "Medium"
    return "Low"


def score(input_path: str = DATA_PATH, out_path: str = OUT_PATH) -> pd.DataFrame:
    clf, scaler, feats = load_artifacts()

    df_raw = pd.read_csv(input_path)

    # Drop target if present
    target_col = "Churn"
    actual = df_raw.pop(target_col) if target_col in df_raw.columns else None

    X = align_features(df_raw.copy(), feats)
    X_scaled = scaler.transform(X)

    probs = clf.predict_proba(X_scaled)[:, 1]
    preds = clf.predict(X_scaled)

    results = df_raw.copy()
    results["churn_probability"] = probs.round(4)
    results["churn_prediction"]  = preds
    results["risk_segment"]      = [risk_segment(p) for p in probs]

    if actual is not None:
        results["actual_churn"] = actual.values

    seg_counts = results["risk_segment"].value_counts()
    print("\n── Risk Segment Distribution ──────────────────────")
    for seg in ["High", "Medium", "Low"]:
        n = seg_counts.get(seg, 0)
        pct = n / len(results) * 100
        print(f"  {seg:<8} {n:>5,}  ({pct:.1f}%)")
    print("────────────────────────────────────────────────────\n")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    results.to_csv(out_path, index=False)
    print(f"[score] Saved → {out_path}")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Score customers for churn risk")
    parser.add_argument("--input", default=DATA_PATH, help="Path to input CSV")
    parser.add_argument("--output", default=OUT_PATH,  help="Path to output CSV")
    args = parser.parse_args()
    score(args.input, args.output)
