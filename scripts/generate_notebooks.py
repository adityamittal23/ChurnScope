"""
Script to generate reproducible Jupyter Notebooks for:
1. 01_data_cleaning.ipynb
2. 02_exploratory_analysis.ipynb
3. 03_customer_segmentation.ipynb
"""

import os
import nbformat as nbf

def generate_cleaning_notebook():
    nb = nbf.v4.new_notebook()
    cells = []

    cells.append(nbf.v4.new_markdown_cell("""# Phase 2 — Data Cleaning & Preparation
**Project:** Customer Churn & Retention Analytics Platform  
**Target:** Data Analyst / Business Intelligence Portfolio  
**Dataset:** IBM Telco Customer Churn (7,043 Records)  

---

### Objectives
1. Load and inspect the raw customer churn dataset.
2. Check for duplicate records and validate primary key uniqueness.
3. Identify and impute missing/blank values in `TotalCharges`.
4. Validate correct data types across numeric and categorical variables.
5. Engineer business-aligned derived variables (Tenure Buckets, Revenue Tiers, Service Counts, Risk Scores, and 2x2 Strategic Quadrant).
6. Export the reliable analytical dataset to `data/processed/customers_cleaned.csv`.
"""))

    cells.append(nbf.v4.new_code_cell("""import os
import pandas as pd
import numpy as np

# Configure display options
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: f'{x:.2f}')
print('Libraries loaded successfully.')
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 1. Load Raw Dataset & Inspect Dimensions"""))

    cells.append(nbf.v4.new_code_cell("""raw_path = '../data/raw/customer_churn.csv'
df_raw = pd.read_csv(raw_path)
print(f'Raw dataset shape: {df_raw.shape[0]} rows, {df_raw.shape[1]} columns')
df_raw.head()
"""))

    cells.append(nbf.v4.new_code_cell("""# Check column types and non-null values
df_raw.info()
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 2. Check for Duplicate Records & Verify Primary Key"""))

    cells.append(nbf.v4.new_code_cell("""dup_count = df_raw.duplicated(subset=['customerID']).sum()
print(f'Number of duplicate customerID entries: {dup_count}')
assert dup_count == 0, 'Duplicate records detected!'
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 3. Handle Blank Values in TotalCharges
Notice that `TotalCharges` is parsed as `object` (string) because 11 records have blank space `' '`.
All 11 records have `tenure == 0` (brand-new customers signed up in current cycle).
We impute these to `0.0` and cast the column to `float64`.
"""))

    cells.append(nbf.v4.new_code_cell("""blank_mask = df_raw['TotalCharges'].str.strip() == ''
print(f'Number of blank TotalCharges records: {blank_mask.sum()}')
df_raw[blank_mask][['customerID', 'tenure', 'MonthlyCharges', 'TotalCharges', 'Churn']]
"""))

    cells.append(nbf.v4.new_code_cell("""df = df_raw.copy()
df['TotalCharges'] = df['TotalCharges'].str.strip().replace('', '0.0')
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0.0)

print(f'TotalCharges dtype: {df["TotalCharges"].dtype}')
print(f'Null count in TotalCharges: {df["TotalCharges"].isna().sum()}')
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 4. Feature Engineering & Derived Variables
According to the PRD specifications, we construct:
- `SeniorCitizenLabel`: 'Yes' / 'No'
- `ChurnFlag`: 1 (Churned) / 0 (Retained)
- `TenureGroup`: '0-12 Months', '13-24 Months', '25-48 Months', '49+ Months'
- `TenureCohort`: 'New (0-1 yr)', 'Growing (1-2 yrs)', 'Established (2-4 yrs)', 'Loyal (4+ yrs)'
- `MonthlyRevenue`: Alias of MonthlyCharges
- `AnnualRevenue`: MonthlyCharges * 12
- `CustomerValueSegment`: Low Value (<$35), Medium Value ($35-$70), High Value (>$70)
- `ContractCategory`: Standard contract type
- `PaymentCategory`: Automatic vs Manual
- `ServiceCount`: Count of subscribed services across 8 products
- `ChurnRiskSegment`: Rule-based risk tier (High, Medium, Low Risk)
- `StrategicSegment`: 2x2 Value & Risk Quadrant
"""))

    cells.append(nbf.v4.new_code_cell("""# 1. Senior Citizen Label
df['SeniorCitizenLabel'] = df['SeniorCitizen'].map({0: 'No', 1: 'Yes'})

# 2. Binary Churn Flag
df['ChurnFlag'] = (df['Churn'] == 'Yes').astype(int)

# 3. Tenure Group
def get_tenure_group(tenure):
    if tenure <= 12:
        return '0-12 Months'
    elif tenure <= 24:
        return '13-24 Months'
    elif tenure <= 48:
        return '25-48 Months'
    else:
        return '49+ Months'

df['TenureGroup'] = df['tenure'].apply(get_tenure_group)

# 4. Tenure Cohort
def get_tenure_cohort(tenure):
    if tenure <= 12:
        return 'New (0-1 yr)'
    elif tenure <= 24:
        return 'Growing (1-2 yrs)'
    elif tenure <= 48:
        return 'Established (2-4 yrs)'
    else:
        return 'Loyal (4+ yrs)'

df['TenureCohort'] = df['tenure'].apply(get_tenure_cohort)

# 5. Revenue Metrics
df['MonthlyRevenue'] = df['MonthlyCharges']
df['AnnualRevenue'] = (df['MonthlyCharges'] * 12).round(2)

# 6. Customer Value Segment
def get_revenue_segment(monthly):
    if monthly < 35.0:
        return 'Low Value'
    elif monthly <= 70.0:
        return 'Medium Value'
    else:
        return 'High Value'

df['CustomerValueSegment'] = df['MonthlyCharges'].apply(get_revenue_segment)

# 7. Contract & Payment Categories
df['ContractCategory'] = df['Contract']
df['PaymentCategory'] = df['PaymentMethod'].apply(lambda pm: 'Automatic' if 'automatic' in pm.lower() else 'Manual')

# 8. Service Count
service_cols = [
    'PhoneService', 'MultipleLines', 'OnlineSecurity', 'OnlineBackup',
    'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies'
]
df['ServiceCount'] = df[service_cols].apply(lambda row: sum(val == 'Yes' for val in row), axis=1)

# Service Specific Flags
df['HasInternet'] = (df['InternetService'] != 'No').astype(int)
df['HasTechSupport'] = (df['TechSupport'] == 'Yes').astype(int)
df['HasOnlineSecurity'] = (df['OnlineSecurity'] == 'Yes').astype(int)

# 9. Churn Risk Scoring
def calculate_risk_score(row):
    score = 0
    if row['Contract'] == 'Month-to-month':
        score += 2
    if row['InternetService'] == 'Fiber optic' and row['TechSupport'] != 'Yes':
        score += 2
    elif row['InternetService'] == 'Fiber optic':
        score += 1
    if row['tenure'] <= 12:
        score += 1
    if row['PaymentMethod'] == 'Electronic check':
        score += 1
    return score

df['RiskScore'] = df.apply(calculate_risk_score, axis=1)

def get_risk_tier(score):
    if score >= 4:
        return 'High Risk'
    elif score >= 2:
        return 'Medium Risk'
    else:
        return 'Low Risk'

df['ChurnRiskSegment'] = df['RiskScore'].apply(get_risk_tier)

# 10. Strategic Segment (2x2 Matrix)
def get_strategic_segment(row):
    is_high_val = row['CustomerValueSegment'] == 'High Value'
    risk = row['ChurnRiskSegment']
    if is_high_val and risk == 'High Risk':
        return 'High Value + High Risk (Retention Priority)'
    elif is_high_val and risk in ['Low Risk', 'Medium Risk']:
        return 'High Value + Low/Med Risk (Loyal Champions)'
    elif not is_high_val and risk == 'High Risk':
        return 'Low/Med Value + High Risk (At-Risk Core)'
    else:
        return 'Low/Med Value + Low/Med Risk (Stable Core)'

df['StrategicSegment'] = df.apply(get_strategic_segment, axis=1)
print(f'Feature engineering complete. Total columns: {df.shape[1]}')
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 5. Cleaned Dataset Validation & Persistence"""))

    cells.append(nbf.v4.new_code_cell("""# Quality Assertions
assert df.isna().sum().sum() == 0, 'Cleaned dataset contains null values!'
assert len(df) == 7043, 'Cleaned dataset row count unexpected!'

output_file = '../data/processed/customers_cleaned.csv'
os.makedirs(os.path.dirname(output_file), exist_ok=True)
df.to_csv(output_file, index=False)
print(f'Successfully persisted cleaned dataset to: {output_file}')
df.head()
"""))

    nb.cells = cells
    with open('notebooks/01_data_cleaning.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Generated notebooks/01_data_cleaning.ipynb successfully.")

if __name__ == '__main__':
    generate_cleaning_notebook()
