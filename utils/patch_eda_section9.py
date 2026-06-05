"""Patches Section 9 (Feature Selection) into 02_exploratory_analysis.ipynb."""
import json
import nbformat as nbf
from pathlib import Path

nb_path = Path(__file__).resolve().parent.parent / 'src' / 'notebooks' / '02_exploratory_analysis.ipynb'
nb_data = json.loads(nb_path.read_text(encoding='utf-8'))

def md(src): return nbf.v4.new_markdown_cell(src)
def code(src): return nbf.v4.new_code_cell(src)

HEADER = """\
---
## Section 9: Feature Selection for Modeling

Not every feature in the cleaned dataset adds meaningful predictive signal for 180-day mortality.
Including low-signal features adds noise without benefit, and can hurt model generalization.

**Criteria for dropping:**
- Weak effect size in EDA (small mortality gap between groups)
- Administrative/financial data with no clinical mechanism
- High imputation rate with weak underlying signal

**Signal metric for categorical features:** Mortality rate spread — the difference between the
highest and lowest 180-day mortality rate across the categories of that variable.
A large spread means the variable strongly separates high-risk from low-risk patients."""

CELL_SIGNAL = """\
# Categorical features - mortality rate spread (max - min across categories)
CAT_EVAL = ["sex", "dzgroup", "dzclass", "race", "ca", "income", "sfdm2"]

cat_rows = []
for col in CAT_EVAL:
    if col not in df.columns:
        continue
    rate = df.groupby(col, observed=True)[TARGET_COL].mean()
    cat_rows.append({
        "Feature": col,
        "Rate Spread (%)": round(float((rate.max() - rate.min()) * 100), 1),
        "Max Rate": f"{rate.max():.1%}",
        "Min Rate": f"{rate.min():.1%}",
    })

cat_signal = pd.DataFrame(cat_rows).sort_values("Rate Spread (%)", ascending=True)
print(cat_signal.to_string(index=False))

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(cat_signal["Feature"], cat_signal["Rate Spread (%)"],
        color="steelblue", edgecolor="white")
ax.axvline(5, color="orange", linestyle="--", linewidth=1.2,
           label="5% spread threshold")
ax.set_title("Categorical Features — Mortality Rate Spread", fontweight="bold")
ax.set_xlabel("Max - Min Mortality Rate (%)")
ax.legend(fontsize=9)
plt.tight_layout()
plt.show()
"""

CELL_DECISIONS = """\
decisions = pd.DataFrame([
    {"Feature": "sex",     "Decision": "Drop", "Signal": "Weak",
     "Rationale": "~1-2% mortality gap between male/female; barely above baseline"},
    {"Feature": "edu",     "Decision": "Drop", "Signal": "Weak",
     "Rationale": "Weak gradient; 18% of values imputed (median=12 inflated)"},
    {"Feature": "hday",    "Decision": "Drop", "Signal": "Weak",
     "Rationale": "Day entered study; no clear causal link to 180-day mortality"},
    {"Feature": "charges", "Decision": "Drop", "Signal": "None",
     "Rationale": "Hospital charges — administrative, not a clinical predictor"},
    {"Feature": "totcst",  "Decision": "Drop", "Signal": "None",
     "Rationale": "Total RCC cost — administrative, not a clinical predictor"},
    {"Feature": "totmcst", "Decision": "Drop", "Signal": "None",
     "Rationale": "Total micro-cost — administrative, 38% imputed"},
    {"Feature": "All day-3 labs",    "Decision": "Keep", "Signal": "Strong",
     "Rationale": "Primary clinical predictors per Knaus et al. (1995)"},
    {"Feature": "age, adlsc, scoma", "Decision": "Keep", "Signal": "Strong",
     "Rationale": "Strong EDA effect sizes and clear clinical mechanism"},
    {"Feature": "dzgroup / dzclass", "Decision": "Keep", "Signal": "Strong",
     "Rationale": "Largest mortality spread of any categorical feature"},
    {"Feature": "ca, diabetes, dementia", "Decision": "Keep", "Signal": "Moderate",
     "Rationale": "Comorbidities with known mortality associations"},
    {"Feature": "income, race",      "Decision": "Keep", "Signal": "Moderate",
     "Rationale": "Socioeconomic signal; moderate mortality gradient in EDA"},
])

print("Feature Selection Decisions:")
print(decisions.to_string(index=False))
"""

CELL_FINAL = """\
DROP_COLS = ["sex", "edu", "hday", "charges", "totcst", "totmcst"]

MODEL_FEATURE_COLS = [c for c in FEATURE_COLS if c not in DROP_COLS]

print(f"Features available in FEATURE_COLS : {len(FEATURE_COLS)}")
print(f"Features dropped                   : {len(DROP_COLS)}  {DROP_COLS}")
print(f"Final model feature count          : {len(MODEL_FEATURE_COLS)}")
print()
print("Final model features:")
for col in MODEL_FEATURE_COLS:
    print(f"  {col}")
"""

# ── Remove stale Section 9 cells ─────────────────────────────────────────
CELL_SAVE = """\
OUTPUT_MODEL = _proj_root / "data" / "support2_model_features.csv"
df[MODEL_FEATURE_COLS + [TARGET_COL]].to_csv(OUTPUT_MODEL, index=False)

n_feat = len(MODEL_FEATURE_COLS)
print(f"Saved : {OUTPUT_MODEL}")
print(f"Shape : {df.shape[0]:,} rows  x  {n_feat + 1} columns")
print(f"  Features : {n_feat}  |  Target : {TARGET_COL}")
print()
print("Data layers:")
print(f"  Bronze : support2_raw_complete.csv  (raw download)")
print(f"  Silver : support2_cleaned.csv       (imputed, all columns)")
print(f"  Gold   : support2_model_features.csv (feature-selected, model-ready)")
"""


def is_sec9(cell):
    src = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
    return ('Section 9' in src or 'DROP_COLS' in src
            or 'MODEL_FEATURE_COLS' in src or "Cohen" in src
            or 'support2_model_features' in src or 'CAT_EVAL' in src)

clean = [c for c in nb_data['cells'] if not is_sec9(c)]

for c in [md(HEADER), code(CELL_SIGNAL), code(CELL_DECISIONS), code(CELL_FINAL), code(CELL_SAVE)]:
    clean.append(dict(c))

nb_data['cells'] = clean
nb_path.write_text(json.dumps(nb_data, indent=1, ensure_ascii=False), encoding='utf-8')
print(f"Written. Total cells: {len(clean)}")
