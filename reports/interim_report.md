# Interim Report: Insurance Risk Analytics

**Project:** Insurance Risk Analytics  
**Branch:** task-2  
**Date:** May 2026

---

## 1. Business Understanding

### Objective

The goal of this project is to build an end-to-end insurance risk analytics pipeline for a South African motor insurance portfolio. The pipeline covers exploratory data analysis (EDA), hypothesis testing, and predictive modeling to support data-driven decisions in underwriting and pricing.

### Business Context

Insurance companies rely on accurate risk assessment to price policies fairly and remain profitable. Key business questions this project addresses:

- Which provinces, vehicle types, or demographics are associated with higher claim rates?
- Is there a significant difference in risk (loss ratio) across customer segments?
- Can we predict total claims or flag high-risk policies before underwriting?

### Key Metric: Loss Ratio

The primary business metric used throughout this analysis is the **Loss Ratio**:

```
Loss Ratio = TotalClaims / TotalPremium
```

A loss ratio > 1 means the insurer is paying out more in claims than it collects in premiums — a direct indicator of underpricing or high-risk segments.

---

## 2. Dataset Overview

| Property | Value |
|----------|-------|
| Source file | `data/insurance_data.csv` |
| Format | Pipe-delimited (`\|`) CSV |
| Raw rows | ~1,000,099 |
| Columns | 52 |
| Cleaned rows | 1,000,098 (1 duplicate removed) |
| Date range | 2014 – 2015 (TransactionMonth) |

### Key Columns

| Column | Description |
|--------|-------------|
| `TotalPremium` | Monthly premium collected |
| `TotalClaims` | Claims paid out |
| `Province` | South African province of the policyholder |
| `VehicleType` | Type of insured vehicle |
| `make` | Vehicle manufacturer |
| `Gender` | Policyholder gender |
| `RegistrationYear` | Year the vehicle was registered |
| `CustomValueEstimate` | Estimated vehicle value |
| `SumInsured` | Total insured amount |

---

## 3. EDA Findings

### 3.1 Missing Values

Several columns have significant missing data:

| Column | Missing Count |
|--------|--------------|
| `NumberOfVehiclesInFleet` | 1,000,098 (100%) — effectively empty |
| `CrossBorder` | 999,400 |
| `CustomValueEstimate` | 779,642 |
| `Rebuilt` / `Converted` / `WrittenOff` | ~641,901 each |
| `Bank` / `AccountType` | ~40,000–145,000 |
| `Gender` / `MaritalStatus` | ~8,000–9,500 |
| Vehicle attributes (`make`, `Model`, etc.) | 552 each |

`NumberOfVehiclesInFleet` is entirely null and should be dropped before modeling.  
`CustomValueEstimate` is missing in ~78% of rows — imputation or exclusion will be required.

### 3.2 Numerical Summary (Key Columns)

| Metric | TotalPremium | TotalClaims | CustomValueEstimate |
|--------|-------------|-------------|---------------------|
| Mean | 61.91 | 64.86 | 225,531 |
| Std | 230.28 | 2,384.08 | 564,516 |
| Min | -782.58 | -12,002.41 | 20,000 |
| 25% | 0.00 | 0.00 | 135,000 |
| Median | 2.18 | 0.00 | 220,000 |
| 75% | 21.93 | 0.00 | 280,000 |
| Max | 65,282.60 | 393,092.10 | 26,550,000 |

**Notable observations:**
- The median `TotalClaims` is **0** — the majority of policies had no claims in a given month, which is expected for insurance data (right-skewed distribution).
- Negative values exist in both `TotalPremium` and `TotalClaims`, likely representing adjustments or refunds. These need investigation before modeling.
- `TotalPremium` and `TotalClaims` have very high standard deviations relative to their means, indicating heavy-tailed distributions with extreme outliers.
- `CustomValueEstimate` ranges from R20,000 to R26.5 million, reflecting a wide mix of vehicle types.

### 3.3 Distribution Analysis

- `TotalPremium`, `TotalClaims`, and `CustomValueEstimate` are all **heavily right-skewed** — a small number of policies account for a disproportionate share of premiums and claims.
- Gender distribution shows three categories: `Male`, `Female`, and `Not specified`. A large portion of records fall under `Not specified`, which may reflect commercial/fleet policies.

### 3.4 Geographic Analysis (Province)

Preliminary grouping by `Province` shows variation in average premiums and claims across South Africa's provinces. Provinces such as Gauteng and Western Cape are expected to show higher average premiums due to higher vehicle values and traffic density.

### 3.5 Vehicle Analysis

- The fleet is dominated by **4-cylinder, 4-door passenger vehicles** (median: 2,694cc, 111kW).
- Vehicle registration years range from 1987 to 2015, with the bulk of the fleet registered between 2008 and 2013.
- Top vehicle makes by average claims can be identified — certain commercial vehicle makes show disproportionately high average claim values.

### 3.6 Temporal Trends

Transaction data spans 2014–2015. Monthly aggregation of average claims reveals seasonal or temporal patterns that may inform pricing adjustments.

### 3.7 Loss Ratio

The overall portfolio loss ratio is approximately **1.05** (TotalClaims / TotalPremium), meaning the portfolio is marginally unprofitable at the aggregate level. Segment-level analysis (by province, vehicle type, cover type) is needed to identify which segments are driving losses.

---

## 4. Data Version Control (DVC) Setup

### Overview

DVC (Data Version Control) is used to track large data files outside of Git, enabling reproducible pipelines and auditability — critical requirements in regulated industries.

### What Was Done

| Step | Detail |
|------|--------|
| DVC initialized | `dvc init` run in project root |
| Remote storage configured | Local directory at `C:/Users/ephra/dvc_local_storage` |
| Raw data tracked | `data/insurance_data.csv` tracked via `dvc add` |
| Cleaned data created | `src/clean_data.py` drops duplicates and null `TotalPremium`/`TotalClaims` rows |
| Cleaned data tracked | `data/insurance_data_cleaned.csv` tracked via `dvc add` |
| Both versions pushed | `dvc push` — 2 files pushed to local remote |
| `.dvc` files committed | `data/insurance_data.csv.dvc` and `data/insurance_data_cleaned.csv.dvc` committed to Git |

### Data Versions

| File | Rows | Description |
|------|------|-------------|
| `data/insurance_data.csv` | 1,000,099 | Raw dataset |
| `data/insurance_data_cleaned.csv` | 1,000,098 | Duplicates removed, nulls in TotalPremium/TotalClaims dropped |

### How to Reproduce the Pipeline

```bash
# 1. Clone the repository
git clone https://github.com/EphrataTech/insurance-risk-analytics.git
cd insurance-risk-analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure DVC remote (update path for your machine)
dvc remote add -d localstorage /path/to/your/dvc_storage

# 4. Pull tracked datasets
dvc pull

# 5. (Optional) Re-run the cleaning step
python src/clean_data.py
```

---

## 5. Next Steps

- **Hypothesis Testing (Task 3):** Test whether risk differences across provinces, vehicle types, and gender are statistically significant using chi-square and t-tests.
- **Modeling (Task 4):** Build predictive models (e.g., linear regression for `TotalClaims`, classification for high-risk flag) using the cleaned dataset.
- **Data Quality:** Investigate negative premium/claim values and decide on treatment strategy.
- **Feature Engineering:** Derive features such as vehicle age, loss ratio per policy, and claim frequency.
