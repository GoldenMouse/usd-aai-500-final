# [Project Title] - AAI-500 Final Project

## Overview
This repository contains the code and resources for our AAI-500 final team project. The objective is to perform an end-to-end statistical analysis, including data preparation, exploratory data analysis (EDA), and predictive modeling, culminating in a technical report and a business presentation.

## Team Members
*   **Andre Hoth (lead)**: [Specific Contributions]
*   **Michael Valderrama**: [Specific Contributions]
*   **Tue Truong**: [Specific Contributions]

*(Note: Work is divided equally. All team members contribute to and review the codebase.)*

## Trello 
We track our work using a Trello board:
`https://trello.com/b/Zqe0Wmgq/aai-500-final-project`


## Dataset
*   **Source:** UCI Machine Learning Repository (ID: 880)
*   **Description:** SUPPORT2 - Study to Understand Prognoses, Preferences, Outcomes and Risks of Treatment. 9,105 seriously ill hospitalized patients with day-3 physiological measurements, demographics, and survival outcomes.
*   **Citation:** Knaus WA, Harrell FE, Lynn J et al. (1995). The SUPPORT prognostic model. *Annals of Internal Medicine*, 122, 191-203.

## Nbstripout
We remove all outputs from working notebooks to allow us to see diffs better in PRs
Usage:

Installation: Run `pip install nbstripout`
Setup: Run `nbstripout --install` in your terminal.

We setup .gitattributes to only target Nbstripout in src/ directory

### Data Files

| File | Layer |
|---|---|
| `data/support2_raw_complete.csv` | Bronze |
| `data/support2_cleaned.csv` | Silver |

## Project Structure
Our analysis and methodology are broken down into the following key phases:
*   **Introduction:** Problem statement and objectives.
*   **Data Cleaning & Preparation:** Handling missing values, formatting, and feature engineering.
*   **Exploratory Data Analysis:** Visualizations and initial statistical findings.
*   **Model Selection:** Justification for the chosen statistical/machine learning models.
*   **Model Analysis:** Evaluation metrics, validity, and statistical backing.
*   **Conclusion & Recommendations:** Actionable business insights derived from the model.

## Setup and Execution
This project is written in Python and follows PEP 8 style guidelines.

1. Clone this repository:
```bash
   git clone [repository_url]
```
2. Install dependencies
```bash
   pip install -r requirements.txt
```


