"""Patches Section 8 chi-squared cells into 02_exploratory_analysis.ipynb."""
import json
import nbformat as nbf
from pathlib import Path

nb_path = Path(__file__).resolve().parent.parent / 'src' / 'notebooks' / '02_exploratory_analysis.ipynb'
nb_data = json.loads(nb_path.read_text(encoding='utf-8'))

def md(src): return nbf.v4.new_markdown_cell(src)
def code(src): return nbf.v4.new_code_cell(src)

# ── Cell content (defined as Python strings, no heredoc issues) ───────────

HEADER = r"""---
## Section 8: Chi-Squared Tests & Contingency Tables (Module 4)

Tests whether a categorical variable is **statistically independent** of 180-day mortality.

$$H_0: \text{the variable is independent of death\_180d}$$

$$\chi^2 = \sum \frac{(O - E)^2}{E}$$

Reject $H_0$ when $p < 0.05$.

**Standardized residuals** = $(O - E) / \sqrt{E}$ — cells with $|r| > 2$ deviate significantly from independence and drive the chi-squared result."""

CELL_SUMMARY = """\
import numpy as np
from scipy.stats import chi2_contingency

CAT_COLS = ["sex", "dzgroup", "dzclass", "race", "ca", "dnr"]

rows = []
for col in CAT_COLS:
    ct = pd.crosstab(df[col], df[TARGET_COL])
    chi2, p, dof, _ = chi2_contingency(ct)
    rows.append(
        {
            "Variable": col,
            "Chi2 Stat": round(chi2, 2),
            "df": dof,
            "p-value": f"{p:.2e}",
            "Significant": "Yes" if p < 0.05 else "No",
        }
    )

chi2_df = pd.DataFrame(rows).sort_values("Chi2 Stat", ascending=False)
print("Chi-Squared Test Summary:")
print(chi2_df.to_string(index=False))
"""

CELL_TABLES = """\
# Observed and expected contingency tables for dzgroup and ca
SEP = "=" * 60
for col in ["dzgroup", "ca"]:
    ct = pd.crosstab(df[col], df[TARGET_COL])
    ct.columns = ["Survived (obs)", "Died (obs)"]
    _, _, _, exp = chi2_contingency(pd.crosstab(df[col], df[TARGET_COL]))
    exp_df = pd.DataFrame(
        exp.round(1),
        index=ct.index,
        columns=["Survived (exp)", "Died (exp)"],
    )
    combined = pd.concat([ct, exp_df], axis=1)
    combined["Total"] = combined["Survived (obs)"] + combined["Died (obs)"]
    print()
    print(SEP)
    print(f"Contingency Table: {col} vs death_180d")
    print(SEP)
    print(combined.to_string())
"""

CELL_HEATMAP = """\
# Standardized residuals heatmaps
fig, axes = plt.subplots(1, 2, figsize=(16, 5))

for ax, col in zip(axes, ["dzgroup", "ca"]):
    ct = pd.crosstab(df[col], df[TARGET_COL])
    ct.columns = ["Survived", "Died"]
    _, _, _, exp = chi2_contingency(ct)
    std_resid = (ct.values - exp) / np.sqrt(exp)
    std_resid_df = pd.DataFrame(std_resid, index=ct.index, columns=ct.columns)

    im = ax.imshow(std_resid_df.values, cmap="RdBu_r", vmin=-6, vmax=6, aspect="auto")
    ax.set_xticks(range(len(ct.columns)))
    ax.set_xticklabels(ct.columns)
    ax.set_yticks(range(len(ct.index)))
    ax.set_yticklabels(ct.index, fontsize=9)
    ax.set_title(
        f"Standardized Residuals: {col}\\n|r| > 2 drives chi-squared",
        fontweight="bold",
    )

    for i in range(std_resid_df.shape[0]):
        for j in range(std_resid_df.shape[1]):
            v = std_resid_df.iloc[i, j]
            ax.text(
                j, i, f"{v:.1f}", ha="center", va="center",
                fontsize=9,
                color="black" if abs(v) < 3 else "white",
                fontweight="bold",
            )

    plt.colorbar(im, ax=ax, label="Std. Residual")

fig.suptitle(
    "Standardized Residuals: Cells Driving Chi-Squared",
    fontsize=12, fontweight="bold",
)
plt.tight_layout()
plt.show()
"""

CELL_STACKEDBAR = """\
# Stacked bar charts - visual contingency tables for all 6 variables
fig, axes = plt.subplots(2, 3, figsize=(16, 9))

for ax, col in zip(axes.flat, CAT_COLS):
    ct_norm = pd.crosstab(df[col], df[TARGET_COL], normalize="index") * 100
    ct_norm.columns = ["Survived", "Died"]
    ct_norm[["Survived", "Died"]].plot(
        kind="bar",
        stacked=True,
        ax=ax,
        color=["seagreen", "firebrick"],
        edgecolor="white",
        width=0.7,
    )
    ax.axhline(50, color="black", linestyle="--", linewidth=0.8, alpha=0.5)
    ax.set_title(col, fontweight="bold")
    ax.set_ylabel("% of Group")
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=30)
    ax.legend(fontsize=8, loc="upper right")

fig.suptitle(
    "Stacked Bar: Survival Proportion by Categorical Feature (dashed = 50%)",
    fontsize=12, fontweight="bold",
)
plt.tight_layout()
plt.show()
"""

# ── Remove any previously appended Section 8 cells ───────────────────────
# (identified by the "Section 8" marker in source)
def is_sec8(cell):
    src = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
    return 'Section 8' in src or 'chi2_contingency' in src or 'CAT_COLS' in src

clean_cells = [c for c in nb_data['cells'] if not is_sec8(c)]

# ── Append fresh Section 8 cells ─────────────────────────────────────────
new_cells = [
    md(HEADER),
    code(CELL_SUMMARY),
    code(CELL_TABLES),
    code(CELL_HEATMAP),
    code(CELL_STACKEDBAR),
]

for c in new_cells:
    clean_cells.append(dict(c))

nb_data['cells'] = clean_cells
nb_path.write_text(json.dumps(nb_data, indent=1, ensure_ascii=False), encoding='utf-8')
print(f"Written. Total cells: {len(clean_cells)}")
