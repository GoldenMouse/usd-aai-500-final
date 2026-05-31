The 47 variables fall into seven functional groups:

| Group | Columns | Role in Analysis |
|---|---|---|
| **Identifiers** | `id` | Row key — not a feature |
| **Demographics** | `age`, `sex`, `race`, `edu`, `income` | Patient background |
| **Disease / Comorbidities** | `dzgroup`, `dzclass`, `num.co`, `ca`, `diabetes`, `dementia` | Diagnosis & comorbidities |
| **Day-3 Physiology** | `meanbp`, `wblc`, `hrt`, `resp`, `temp`, `pafi`, `alb`, `bili`, `crea`, `sod`, `ph`, `glucose`, `bun`, `urine` | Lab measurements at day 3 of ICU stay — **primary predictors** |
| **Severity Scores** | `scoma`, `aps`, `sps`, `avtisst` | Clinical severity indices |
| **Functional Status** | `adlp`, `adls`, `adlsc`, `sfdm2` | Activities of Daily Living |
| **Outcomes / Timing** | `death`, `hospdead`, `d.time`, `slos`, `hday` | Mortality indicators and timing |
| **Legacy Benchmarks** | `surv2m`, `surv6m`, `prg2m`, `prg6m` | 1990s SUPPORT model predictions |
| **DNR Orders** | `dnr`, `dnrday` | Do-Not-Resuscitate information |
| **Administrative** | `charges`, `totcst`, `totmcst` | Hospital cost data |