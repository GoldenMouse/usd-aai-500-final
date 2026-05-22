# Project Dataset Proposals:

## Michael
Option 1: ISIC 2024 Skin Cancer (Metadata-Only Prediction)
About 400,000 rows from the ISIC archive at isic-archive.com, one row per skin lesion exam. Usable columns: patient age, sex, body region, clinical lesion size in millimeters, imaging context (tile type, image type), biopsy plan, source hospital. The 0/1 malignant flag comes from a separate Ground Truth file, joined on the lesion ID. Direct download from the ISIC Archive Collections page, no API key, no Kaggle account.

Problem: How much of skin cancer risk can you predict from patient metadata alone, before any imaging? Binary classification (malignant vs benign), about 4% positive class.

The use case is pre-screening triage for a dermatologist. Given basic patient metadata before a biopsy, what is the chance it is malignant? Useful when imaging is not available (telemedicine, low-resource clinics, biopsy queue prioritization). Since missing a cancer costs way more than an unnecessary biopsy, the approach would prioritize recall over accuracy.
Why metadata-only when the original challenge used images? Two reasons that go in the assumptions section. (a) Statistical: the goal is to see what is predictable from just the patient and lesion fields, before adding anything image-based. (b) Practical: a lot of clinical settings just do not have imaging (telemed, low-resource, pre-imaging triage), so a metadata-only model is actually useful.

-----------------------

Option 2: FDA FAERS GLP-1 Adverse Event Triage
FDA Adverse Event Reporting System data at fis.fda.gov, one row per adverse event report. Each quarter has 200K-400K total reports across 6-7 normalized tables joined on a case ID. Filtering to GLP-1 drugs (Ozempic, Wegovy, Mounjaro, etc.) gives tens of thousands of GLP-1-specific reports per quarter. Features: patient age, sex, weight, reporter type, indication, concomitant drugs, reaction terms at the System Organ Class level. Outcome is a serious/non-serious flag. Direct download, no API key needed.

Problem: given a GLP-1 adverse event report, predict whether it is a serious event (death, hospitalization, life-threatening, disability, etc.) or not. Binary classification with about a 40-50% positive class, so the imbalance is not bad.
The use case is pharmacovigilance triage. FDA, drug manufacturers, and big health systems all have to decide which reports to investigate first, and GLP-1 reports have been flooding in since 2022. Missing a real safety signal is the expensive mistake, so the approach would prioritize recall.

Why triage classification rather than estimating the true incidence rate? Two reasons that go in the assumptions section. (a) Statistical: FAERS only has the reports people actually filed, not every adverse event that happened. So a model trained on this data could predict whether a filed report is serious, but it would not tell you anything about the overall rate of serious events in GLP-1 users. (b) Practical: triage is the actual job pharmacovigilance teams do every day, so a classifier built for it is what is useful.
FAERS' voluntary-reporting selection bias is real (sicker patients and more attentive providers report more), and that would go in the assumptions section of the writeup rather than get papered over btw.

## Andre
Problem 1: Identify which contextual and behavioral factors are most strongly associated with significant glucose excursions (rapid highs/lows or increased glucose variability) in people with Type 1 Diabetes. Rather than attempting to build a black-box prediction model, the project focuses on statistically explainable relationships between glucose outcomes and variables such as carbohydrate intake, insulin dosing, time-of-day, exercise, and sleep.

Dataset: Use the Ohio University OhioT1DM Dataset, a publicly available multimodal diabetes dataset containing continuous glucose monitor (CGM) readings, insulin events, meal/carbohydrate data, exercise/activity information, sleep data, and other contextual variables collected from individuals with Type 1 Diabetes over extended periods of time.

Approach:

Define glucose excursion metrics such as:
hyperglycemia (>180 mg/dL),
hypoglycemia (<70 mg/dL),
or glucose variability (standard deviation/range).

Perform exploratory statistical analysis and visualization to understand distributions and trends.
Use correlation analysis, hypothesis testing, and regression techniques to evaluate relationships between contextual variables and glucose outcomes.
Compare which variables show statistically significant associations with increased glucose variability or excursion frequency.
Discuss findings, limitations of observational/self-reported data, and implications for future explainable AI systems in diabetes management.


-----------------------

Problem 2: Determine whether contextual and behavioral variables improve the ability to identify impending glucose excursions compared to using CGM trends alone. The project investigates whether adding factors such as meals, insulin dosing, sleep, exercise, and time-of-day provides statistically meaningful improvement over glucose-only analysis.

Dataset: Use the Ohio University OhioT1DM Dataset, which includes continuous glucose monitor (CGM) readings along with insulin delivery, meal/carbohydrate intake, exercise/activity data, sleep information, and additional contextual variables collected from individuals with Type 1 Diabetes.

Approach:

Define target outcomes such as:
hypoglycemic events (<70 mg/dL),
hyperglycemic events (>180 mg/dL),
or significant glucose excursions within a future prediction window.

Build a baseline statistical model using only CGM-derived variables (current glucose, rate-of-change, recent trends).
Build a second model incorporating contextual variables such as insulin, carbohydrates, exercise, sleep, and time-of-day.
Compare model performance using statistical measures such as accuracy, sensitivity, specificity, correlation strength, or regression fit metrics.
Evaluate whether contextual variables provide statistically significant improvement in identifying glucose excursions and discuss implications for personalized diabetes monitoring systems.


## Tue
Project: SUPPORT2 (Day-3 Clinical Survival Prediction) About 9,105 rows from the UCI Machine Learning Repository, one row per critically ill ICU patient. Usable columns: patient age, sex, primary disease group, comorbidities, and day-3 physiological lab results (mean blood pressure, white blood cell count, bilirubin, albumin, creatinine, etc.). The 0/1 180-day mortality target is engineered by combining the follow-up time and death indicator columns. Direct download via the ucimlrepo

Problem: How accurately can 180-day patient survival be predicted using early (day-3) clinical data? Binary classification (180-day mortality vs survival), imbalanced class. The use case is automated pre-screening for palliative care triage. Given day-3 clinical data, what is the probability the patient will not survive 6 months? Useful for triggering automated alerts in Electronic Health Records (EHR) to pivot from aggressive, expensive ICU intervention to comfortable hospice care. Since missing a terminal prognosis (a false negative) subjects patients to painful, prolonged, and often unwanted end-of-life treatments, the approach prioritizes recall and AUROC over basic accuracy.

Why build this when the dataset already contains legacy survival predictions? Two reasons that go in the assumptions section. (a) Statistical: the goal is to benchmark a modern machine learning pipeline directly against the 1990s SUPPORT prognostic model (surv6m) to demonstrate improved predictive power on the same cohort. (b) Practical: the original Phase II study proved that handing static survival probabilities to physicians fails to change clinical behavior; a modern model must be pitched as an automated workflow integration to effectively reduce futile care and honor patient autonomy.