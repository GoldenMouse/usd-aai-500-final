"""
Feature Lab — quickly try feature sets and see test-set performance.

HOW TO USE
----------
1. Edit the three lists in the CONFIG block below (add/remove feature names).
2. Run it:
       python experiments/feature_lab.py            # fast: sklearn logistic (~1 sec)
       python experiments/feature_lab.py --bayes     # faithful: PyMC Bayesian LR (~20 sec)
3. Read the printed test AUC + odds-ratio table; compare against the `surv6m` benchmark.

Notes
-----
- Continuous features are z-score standardized (fit on TRAIN only). Binary 0/1 columns and
  one-hot categoricals are left unstandardized.
- Same conventions as the notebooks: target `death_180d`, RANDOM_SEED=42, 80/20 stratified
  split. AUC is identical whichever category is the one-hot reference, so don't worry about
  reference levels when comparing feature sets.
- The fast sklearn logistic regression and the PyMC Bayesian LR give essentially the same AUC
  for feature comparison; use --bayes when you want the exact notebook-style number.
"""

import argparse
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

_root = Path(__file__).resolve().parent
while _root != _root.parent and not (_root / "pyproject.toml").exists():
    _root = _root.parent
sys.path.insert(0, str(_root))
from utils.dataset import load_csv  # noqa: E402

warnings.filterwarnings("ignore")
RANDOM_SEED = 42

# ============================ CONFIG — EDIT THESE ============================
# Continuous measurements (z-score standardized):
CONTINUOUS = [
    "age",
    "meanbp",
    "bili",
    "bun",
    "alb",
    "adlsc",
    "scoma",
    "pafi",
    "hrt",
    "resp",
    "temp",
    "sod",
]

# Binary 0/1 columns (used as-is). e.g. "diabetes", "dementia"
BINARY = ["diabetes"]

# Categorical columns (one-hot encoded, first level dropped as reference).
# e.g. "dzclass", "ca", "income", "race"
CATEGORICAL = ["dzclass", "ca", "income"]
# ===========================================================================

TARGET = "death_180d"


def build_design(df):
    """Assemble the model matrix from the CONFIG lists; return (DataFrame, continuous_cols)."""
    blocks = []
    if CONTINUOUS:
        blocks.append(df[CONTINUOUS].astype(float))
    if BINARY:
        blocks.append(df[BINARY].astype(float))
    for col in CATEGORICAL:
        blocks.append(
            pd.get_dummies(df[col], prefix=col, drop_first=True).astype(float)
        )
    X = pd.concat(blocks, axis=1)
    return X


def fit_sklearn(Xtr, ytr, Xte):
    # C=1.0 L2 ~ the Normal(0,1) prior used in the notebook's Bayesian LR
    model = LogisticRegression(max_iter=5000, C=1.0)
    model.fit(Xtr, ytr)
    pred = model.predict_proba(Xte)[:, 1]
    return pred, model.coef_.ravel()


def fit_bayes(Xtr, ytr, Xte):
    import pymc as pm
    from scipy.special import expit as sigmoid

    n = Xtr.shape[1]
    with pm.Model():
        b0 = pm.Normal("intercept", 0, 2)
        b = pm.Normal("betas", 0, 1, shape=n)
        pm.Bernoulli("obs", logit_p=b0 + pm.math.dot(Xtr, b), observed=ytr)
        tr = pm.sample(
            draws=1000,
            tune=500,
            chains=2,
            cores=1,
            target_accept=0.9,
            random_seed=RANDOM_SEED,
            progressbar=False,
        )
    pi = tr.posterior["intercept"].values.flatten()
    pb = tr.posterior["betas"].values.reshape(-1, n)
    pred = sigmoid(pi[:, None] + pb @ Xte.T).mean(axis=0)
    return pred, pb.mean(axis=0)


def main(bayes=False):
    df = load_csv("support2_cleaned.csv")
    y = df[TARGET].values
    X = build_design(df)

    if X.isna().any().any():
        bad = X.columns[X.isna().any()].tolist()
        sys.exit(
            f"ERROR: missing values in feature(s) {bad} — impute/handle them first."
        )

    names = list(X.columns)
    Xv = X.values.astype(float)
    idx = np.arange(len(df))
    Xtr, Xte, ytr, yte, _, idx_te = train_test_split(
        Xv, y, idx, test_size=0.2, random_state=RANDOM_SEED, stratify=y
    )

    # standardize continuous columns only, fit on TRAIN
    cont_idx = [names.index(c) for c in CONTINUOUS]
    if cont_idx:
        sc = StandardScaler().fit(Xtr[:, cont_idx])
        Xtr[:, cont_idx] = sc.transform(Xtr[:, cont_idx])
        Xte[:, cont_idx] = sc.transform(Xte[:, cont_idx])

    pred, coef = fit_bayes(Xtr, ytr, Xte) if bayes else fit_sklearn(Xtr, ytr, Xte)
    auc = roc_auc_score(yte, pred)
    auc_surv6m = roc_auc_score(yte, 1 - df.iloc[idx_te]["surv6m"].values)

    engine = "PyMC Bayesian LR" if bayes else "sklearn logistic (fast)"
    print(f"\n=== Feature-set evaluation ({engine}) ===")
    print(
        f"Continuous ({len(CONTINUOUS)}, standardized): {', '.join(CONTINUOUS) or '-'}"
    )
    print(f"Binary ({len(BINARY)}): {', '.join(BINARY) or '-'}")
    print(f"Categorical ({len(CATEGORICAL)}, one-hot): {', '.join(CATEGORICAL) or '-'}")
    print(f"Total model features: {len(names)}")

    odds = np.exp(coef)
    order = np.argsort(-np.abs(coef))
    print("\nOdds ratios (continuous = per 1 SD; sorted by strength):")
    for i in order:
        direction = "higher risk" if odds[i] > 1 else "lower risk"
        print(f"  {names[i]:30s} OR={odds[i]:6.3f}  {direction}")

    print(f"\nTest AUC:          {auc:.4f}")
    print(f"surv6m benchmark:  {auc_surv6m:.4f}   (gap {auc_surv6m - auc:+.4f})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Quick feature-set evaluator.")
    ap.add_argument(
        "--bayes",
        action="store_true",
        help="use the PyMC Bayesian LR (~20s) instead of fast sklearn logistic",
    )
    args = ap.parse_args()
    main(bayes=args.bayes)
