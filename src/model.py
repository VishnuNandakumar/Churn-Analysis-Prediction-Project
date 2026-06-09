"""
model.py
────────
Trains a Logistic Regression churn classifier with SMOTE balancing,
evaluates performance, and serialises the artefacts.

Usage:
    python src/model.py
"""

import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, roc_auc_score, classification_report,
    confusion_matrix, RocCurveDisplay
)
from imblearn.over_sampling import SMOTE

DATA_PATH  = "data/processed/telco_churn_clean.csv"
MODEL_DIR  = "models"
REPORT_DIR = "reports/figures"
RANDOM_STATE = 42


# ── Data loading ─────────────────────────────────────────────────────────────

def load_data(path: str = DATA_PATH):
    df = pd.read_csv(path)
    X = df.drop(columns=["Churn"])
    y = df["Churn"]
    print(f"[data]  X: {X.shape}  |  Churn rate: {y.mean():.1%}")
    return X, y


# ── Training ──────────────────────────────────────────────────────────────────

def train(X_train, y_train):
    # Scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_train)

    # SMOTE to address class imbalance (~73% non-churn)
    sm = SMOTE(random_state=RANDOM_STATE)
    X_res, y_res = sm.fit_resample(X_scaled, y_train)
    print(f"[smote] Resampled: {np.bincount(y_res)} (class 0, class 1)")

    # Logistic Regression
    clf = LogisticRegression(
        C=0.5,
        max_iter=1000,
        class_weight="balanced",
        random_state=RANDOM_STATE
    )
    clf.fit(X_res, y_res)

    # Cross-validation sanity check
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    cv_scores = cross_val_score(clf, X_scaled, y_train, cv=cv, scoring="roc_auc")
    print(f"[cv]    5-fold ROC-AUC: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

    return clf, scaler


# ── Evaluation ────────────────────────────────────────────────────────────────

def evaluate(clf, scaler, X_test, y_test):
    X_scaled = scaler.transform(X_test)
    y_pred   = clf.predict(X_scaled)
    y_prob   = clf.predict_proba(X_scaled)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)

    print("\n" + "="*55)
    print(f"  Accuracy : {acc:.2%}")
    print(f"  ROC-AUC  : {auc:.3f}")
    print("="*55)
    print(classification_report(y_test, y_pred, target_names=["Stay", "Churn"]))

    return y_pred, y_prob, acc, auc


# ── Plots ─────────────────────────────────────────────────────────────────────

def plot_confusion_matrix(y_test, y_pred, out_dir: str = REPORT_DIR):
    os.makedirs(out_dir, exist_ok=True)
    cm = confusion_matrix(y_test, y_pred)

    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Stay", "Churn"],
                yticklabels=["Stay", "Churn"], ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix — Logistic Regression")
    fig.tight_layout()
    path = os.path.join(out_dir, "confusion_matrix.png")
    fig.savefig(path, dpi=150)
    plt.close()
    print(f"[plot]  Confusion matrix → {path}")


def plot_feature_importance(clf, feature_names, top_n: int = 15, out_dir: str = REPORT_DIR):
    os.makedirs(out_dir, exist_ok=True)
    coefs = pd.Series(clf.coef_[0], index=feature_names).abs().nlargest(top_n)

    fig, ax = plt.subplots(figsize=(7, 5))
    coefs.sort_values().plot.barh(ax=ax, color="#3B82F6")
    ax.set_title(f"Top {top_n} Churn Drivers (|Coefficient|)")
    ax.set_xlabel("Absolute Coefficient")
    fig.tight_layout()
    path = os.path.join(out_dir, "feature_importance.png")
    fig.savefig(path, dpi=150)
    plt.close()
    print(f"[plot]  Feature importance → {path}")


def plot_roc_curve(clf, scaler, X_test, y_test, out_dir: str = REPORT_DIR):
    os.makedirs(out_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(5, 5))
    RocCurveDisplay.from_estimator(clf, scaler.transform(X_test), y_test, ax=ax)
    ax.set_title("ROC Curve — Logistic Regression")
    fig.tight_layout()
    path = os.path.join(out_dir, "roc_curve.png")
    fig.savefig(path, dpi=150)
    plt.close()
    print(f"[plot]  ROC curve → {path}")


# ── Serialise ─────────────────────────────────────────────────────────────────

def save_artifacts(clf, scaler, feature_names, out_dir: str = MODEL_DIR):
    os.makedirs(out_dir, exist_ok=True)
    joblib.dump(clf,           os.path.join(out_dir, "churn_model.pkl"))
    joblib.dump(scaler,        os.path.join(out_dir, "scaler.pkl"))
    joblib.dump(feature_names, os.path.join(out_dir, "feature_names.pkl"))
    print(f"[save]  Artifacts → {out_dir}/")


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )

    clf, scaler = train(X_train, y_train)
    y_pred, y_prob, acc, auc = evaluate(clf, scaler, X_test, y_test)

    plot_confusion_matrix(y_test, y_pred)
    plot_feature_importance(clf, X.columns.tolist())
    plot_roc_curve(clf, scaler, X_test, y_test)
    save_artifacts(clf, scaler, X.columns.tolist())
