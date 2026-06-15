# Customer Churn Prediction

Interview-ready end-to-end churn project built on the IBM Telco Customer Churn dataset.

## Project goals

- Understand churn patterns with focused EDA
- Build a SQL layer for business questions and segmentation
- Train explainable and higher-performing churn models
- Produce assets that can flow into Power BI and a business report

## Repository structure

```text
customerchurn/
|-- artifacts/
|   |-- figures/            # EDA and model charts
|   |-- metrics/            # JSON metrics, CSV outputs
|   `-- models/             # Serialized sklearn models
|-- dashboard/              # Power BI guidance and page plan
|-- data/
|   |-- Telco-Customer-Churn.csv
|   `-- processed/          # Cleaned CSV + SQLite database
|-- notebooks/              # Notebook notes / conversion targets
|-- report/                 # Business recommendation report
|-- sql/                    # DDL + business analysis queries
|-- src/                    # Python pipeline scripts
|-- requirements.txt
`-- README.md
```

## What is included

### 1. Data setup + EDA

- Cleans `TotalCharges`, encodes churn flags, and creates analysis fields
- Produces summary statistics, churn rates, and key charts
- Highlights churn by contract, tenure bucket, and monthly charge bucket

### 2. SQL layer + feature engineering

- Loads cleaned data into SQLite
- Includes business-facing SQL for churn rate, revenue at risk, and segmentation
- Creates a Power BI-ready view/table definition

### 3. ML model

- Baseline: Logistic Regression
- Improved: Random Forest
- Optional class balancing with SMOTE when `imbalanced-learn` is installed
- Saves metrics, confusion matrix, predictions, and feature importance

### 4. Dashboard + report

- Power BI page plan and suggested KPIs
- Business recommendation report with actions, risks, and a 30/60/90-day roadmap

## Quick start

```bash
python src/data_prep.py
python src/eda.py
python src/train_model.py
```

## Main outputs

- Clean data: `data/processed/telco_churn_clean.csv`
- SQLite database: `data/processed/telco_churn.db`
- EDA summary: `artifacts/metrics/eda_summary.json`
- Model metrics: `artifacts/metrics/model_metrics.json`
- Predictions: `artifacts/metrics/test_predictions.csv`
- Figures: `artifacts/figures/`

## Interview talking points

- Logistic Regression is the baseline for interpretability.
- Random Forest is the stronger non-linear benchmark for business accuracy.
- Contract type, tenure, monthly charges, and add-on service adoption are likely churn drivers.
- Revenue-at-risk can be estimated directly from predicted churn probability and monthly charges.
