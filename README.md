# Evaluating Early Clinical Indicators for 180-Day Mortality

### A Comparative Analysis Using the SUPPORT2 Dataset — AAI-500 Final Project (Group 3)

## Overview
This repository contains the code and resources for our AAI-500 final team project. The
objective is an end-to-end statistical analysis — data preparation, exploratory data analysis
(EDA), and predictive modeling — culminating in a technical report and a business presentation.

We predict **180-day mortality** (`death_180d`) for seriously ill hospitalized patients from
their day-3 physiology, demographics, and comorbidities, and compare a frequentist baseline
(logistic regression, LASSO, random forest) against a **Bayesian logistic regression** with
uncertainty-aware predictions, benchmarking all models against the original SUPPORT prognostic
score.

## Team Members
*   **Andre Hoth:** 
*   **Michael Valderrama:** 
*   **Tue Truong:** 

*(Note: Work is divided equally. All team members contribute to and review the codebase.)*

## Trello
We track our work using a Trello board:
`https://trello.com/b/Zqe0Wmgq/aai-500-final-project`

## Dataset
*   **Source:** UCI Machine Learning Repository (ID: 880).
*   **Description:** SUPPORT2 — Study to Understand Prognoses, Preferences, Outcomes and Risks of
    Treatment. 9,105 seriously ill hospitalized patients with day-3 physiological measurements,
    demographics, and survival outcomes.
*   **Citation:** Knaus WA, Harrell FE, Lynn J et al. (1995). The SUPPORT prognostic model.
    *Annals of Internal Medicine, 122*, 191–203.

### Data Files
| File | Layer | Description |
|---|---|---|
| `data/support2_raw_complete.csv` | Bronze | Raw download, 9,105 × 48. |
| `data/support2_cleaned.csv` | Silver | Cleaned, imputed, leakage-aware feature set. |

## Project Structure
Our analysis and methodology are broken into the following phases (Parts 1–3 of the notebooks):
*   **Introduction:** Problem statement and objectives.
*   **Data Cleaning & Preparation:** Missing-value imputation, zero-value treatment, leakage handling, feature engineering.
*   **Exploratory Data Analysis:** Distributions, outlier detection, bivariate analysis by outcome.
*   **Model Selection:** Frequentist baselines (LR, LASSO, RF) and a Bayesian logistic regression; justification for each.
*   **Model Analysis:** Discrimination (AUC), calibration (Brier), posterior diagnostics, and benchmark comparison.
*   **Conclusion & Recommendations:** Clinical insights and the case for uncertainty-aware prediction.

### Repository Layout
| Path | Contents |
|---|---|
| `src/master.ipynb` | Consolidated end-to-end notebook (all three parts). |
| `src/notebooks/` | Modular per-section notebooks (`01` cleaning, `02` EDA, `03_*` modeling) that merge into the report deliverable. |
| `scripts/` | Reproducibility scripts (download, merge, figure/HTML/PDF export). |
| `utils/` | Shared helpers (`dataset.py` for I/O, `evaluation.py` for metrics/plots). |
| `experiments/` | Quick feature-set evaluator and exploratory experiment scripts. |
| `data/` | Bronze/Silver CSVs. |
| `artifacts/` | Generated deliverables (`Final-Project-Report-Team-3.{ipynb,html,pdf}`) and exported figures. |
| `docs/` | Reference papers (e.g. the original SUPPORT publication). |

## Key Results
Held-out (20% stratified test) discrimination for 180-day mortality:

| Model | Test AUC |
|---|---|
| SUPPORT (`surv6m`, benchmark) | 0.790 |
| Random Forest | 0.768 |
| Bayesian LR (B-spline) | 0.754 |
| Bayesian LR (linear) | 0.751 |
| Logistic Regression / LASSO | 0.748 |

The Bayesian model matches the frequentist baselines on discrimination while additionally
providing per-patient predictive uncertainty (posterior credible intervals) and per-prediction
reason codes — the primary advantage for clinical risk communication.

## Setup and Execution
This project is written in Python (≥ 3.10) and follows PEP 8 style guidelines.

1. **Clone the repository:**
   ```bash
   git clone [repository_url]
   cd usd-aai-500-final
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **(Optional) Download the raw dataset** (a copy is already committed under `data/`):
   ```bash
   python scripts/download_support2_dataset.py
   ```
4. **Run the analysis** — open `src/master.ipynb` (or the modular notebooks in `src/notebooks/`)
   and run all cells. Notebooks resolve the project root automatically, so they can be run from
   any working directory.

### Generating the Deliverables
| Command | Output |
|---|---|
| `python scripts/merge_notebooks.py` | Merges `src/notebooks/NN_*.ipynb` → `artifacts/Final-Project-Report-Team-3.ipynb` (+ PDF). |
| `python scripts/export_html.py` | `src/master.ipynb` → `artifacts/Final-Project-Report-Team-3.html` (self-contained). |
| `python scripts/export_pdf.py` | Report HTML → PDF via headless Chromium (highest fidelity). |
| `python scripts/export_bayesian_figures.py` | Re-renders the slide-ready Bayesian figures to `artifacts/bayesian/`. |

> The PDF/HTML exporters need an **executed** notebook (with saved outputs) to capture figures,
> and the PDF path requires Playwright's Chromium: `python -m playwright install chromium`.

## Notebook Hygiene (nbstripout)
We strip all outputs from working notebooks in `src/` so PR diffs stay readable.

*   **Install:** `pip install nbstripout`
*   **Enable for this repo:** run `nbstripout --install` in the repo root.

`.gitattributes` scopes nbstripout to the `src/` directory, so the executed deliverables in
`artifacts/` keep their outputs.
