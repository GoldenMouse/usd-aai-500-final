# Data frame: `support2`
**Overview:** 9,105 observations, 47 variables (maximum NAs: 5,641)

### Variables & Metadata

| Name | Label | Storage | NAs |
| :--- | :--- | :--- | :--- |
| `age` | Age | double | 0 |
| `death` | Death at any time up to NDI date: 31DEC94 | double | 0 |
| `sex` | *See levels below* (2 levels) | integer | 0 |
| `hospdead` | Death in Hospital | double | 0 |
| `slos` | Days from Study Entry to Discharge | double | 0 |
| `d.time` | Days of Follow-Up | double | 0 |
| `dzgroup` | *See levels below* (8 levels) | integer | 0 |
| `dzclass` | *See levels below* (4 levels) | integer | 0 |
| `num.co` | Number of comorbidities | double | 0 |
| `edu` | Years of Education | double | 1634 |
| `income` | *See levels below* (4 levels) | integer | 2982 |
| `scoma` | SUPPORT Coma Score based on Glasgow D3 | double | 1 |
| `charges` | Hospital Charges | double | 172 |
| `totcst` | Total RCC cost | double | 888 |
| `totmcst` | Total micro-cost | double | 3475 |
| `avtisst` | Average TISS, Days 3-25 | double | 82 |
| `race` | *See levels below* (5 levels) | integer | 42 |
| `sps` | SUPPORT physiology score day 3 | double | 1 |
| `aps` | APS III no coma, imp bun, uout for ph1, D3 | double | 1 |
| `surv2m` | 2M model survival prediction at day 3 | double | 1 |
| `surv6m` | 6M model survival prediction at day 3 | double | 1 |
| `hday` | Day in Hospital at Study Admit | double | 0 |
| `diabetes` | Diabetes (Com 27-28, Dx 73) | double | 0 |
| `dementia` | Dementia (Comorbidity 6) | double | 0 |
| `ca` | *See levels below* (3 levels) | integer | 0 |
| `prg2m` | MD 2 Month Survival Estimate | double | 1649 |
| `prg6m` | MD 6 Month Survival Estimate | double | 1633 |
| `dnr` | *See levels below* (3 levels) | integer | 30 |
| `dnrday` | Days to DNR, <0: DNR before study | double | 30 |
| `meanbp` | Mean Arterial Blood Pressure Day 3 | double | 1 |
| `wblc` | White Blood Cell Count Day 3 | double | 212 |
| `hrt` | Heart Rate Day 3 | double | 1 |
| `resp` | Respiration Rate Day 3 | double | 1 |
| `temp` | Temperature (celcius) Day 3 | double | 1 |
| `pafi` | PaO2/(.01*FiO2) Day 3 | double | 2325 |
| `alb` | Serum Albumin Day 3 | double | 3372 |
| `bili` | Bilirubin Day 3 | double | 2601 |
| `crea` | Serum creatinine Day 3 | double | 67 |
| `sod` | Serum sodium Day 3 | double | 1 |
| `ph` | Serum pH (arterial) Day 3 | double | 2284 |
| `glucose` | Glucose Day 3 | double | 4500 |
| `bun` | BUN Day 3 | double | 4352 |
| `urine` | Urine Output Day 3 | double | 4862 |
| `adlp` | ADL Patient Day 3 (patient reported their Activities of Daily Living) | double | 5641 |
| `adls` | ADL Surrogate Day 3 (surrogate reported ADL) | double | 2867 |
| `sfdm2` | *See levels below* (5 levels) | integer | 1400 |
| `adlsc` | Imputed ADL Calibrated to Surrogate (this based from adlp and adls, use this) | double | 0 |

### Categorical Variable Levels

| Variable | Levels |
| :--- | :--- |
| `sex` | female, male |
| `dzgroup` | ARF/MOSF w/Sepsis, COPD, CHF, Cirrhosis, Coma, Colon Cancer, Lung Cancer, MOSF w/Malig |
| `dzclass` | ARF/MOSF, COPD/CHF/Cirrhosis, Coma, Cancer |
| `income` | under $11k, $11-$25k, $25-$50k, >$50k |
| `race` | white, black, asian, other, hispanic |
| `ca` | no, yes, metastatic |
| `dnr` | no dnr, dnr before sadm, dnr after sadm |
| `sfdm2` | no(M2 and SIP pres), adl>=4 (>=5 if sur), SIP>=30, Coma or Intub, <2 mo. follow-up |
