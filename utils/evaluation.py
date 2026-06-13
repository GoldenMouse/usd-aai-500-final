"""Reusable held-out evaluation helpers for the modeling notebooks.

Each model only needs to produce its test-set predicted P(death) array, then pass
it to these helpers for the standard benchmark comparison (AUC table + ROC plot).
All functions operate on ``{label: predicted P(death) array}`` dicts so any model
plugs in the same way.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, roc_curve

# Legacy SUPPORT benchmarks. (column, invert): invert=True means the column is a
# survival probability, so P(death) = 1 - col; aps is already a severity score.
BENCHMARK_SPEC = {
    "SUPPORT (surv6m)": ("surv6m", True),
    "Physician (prg6m)": ("prg6m", True),
    "APACHE III (aps)": ("aps", False),
}


def get_benchmark_preds(df, idx_test, spec=BENCHMARK_SPEC):
    """Return ``{label: P(death) array}`` for the legacy benchmarks on the test rows."""
    out = {}
    for label, (col, invert) in spec.items():
        v = df.iloc[idx_test][col].to_numpy()
        out[label] = 1 - v if invert else v
    return out


def auc_table(y_test, model_preds, benchmark_preds=None):
    """Sorted AUC table for one+ models plus optional benchmarks.

    ``model_preds`` / ``benchmark_preds`` are ``{label: predicted P(death) array}``.
    """
    rows = {**model_preds, **(benchmark_preds or {})}
    data = [(name, roc_auc_score(y_test, p)) for name, p in rows.items()]
    return (
        pd.DataFrame(data, columns=["model", "AUC"])
        .sort_values("AUC", ascending=False)
        .reset_index(drop=True)
    )


def plot_roc(y_test, preds, title="ROC Curves", ax=None):
    """Overlay ROC curves for every ``{label: P(death)}`` in preds; AUC in the legend."""
    if ax is None:
        _, ax = plt.subplots(figsize=(7, 6))
    for name, p in preds.items():
        fpr, tpr, _ = roc_curve(y_test, p)
        ax.plot(
            fpr,
            tpr,
            linewidth=1.8,
            label=f"{name} (AUC={roc_auc_score(y_test, p):.3f})",
        )
    ax.plot([0, 1], [0, 1], "k--", linewidth=1, label="Random (AUC=0.500)")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title(title, fontweight="bold")
    ax.legend(fontsize=9)
    return ax


def brier_score(y_test, p):
    """Mean squared error of predicted probabilities (lower = better)."""
    return float(np.mean((np.asarray(p) - np.asarray(y_test)) ** 2))
