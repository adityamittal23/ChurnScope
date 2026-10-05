"""
Data Cleaning & Feature Engineering Pipeline
Customer Churn & Retention Analytics Platform
"""

import os
import pandas as pd
import numpy as np

def clean_and_prepare_data(input_path: str, output_path: str) -> pd.DataFrame:
    print(f"Loading raw data from: {input_path}")
    df = pd.read_csv(input_path)
    initial_shape = df.shape
    print(f"Initial dataset shape: {initial_shape}")

    # 1. Check for duplicates
    dup_count = df.duplicated(subset=['customerID']).sum()
    print(f"Duplicate customerID count: {dup_count}")
    if dup_count > 0:
        df = df.drop_duplicates(subset=['customerID'])

    # 2. Handle TotalCharges blank values and type conversion
    # In raw Telco dataset, 11 records have tenure == 0 and TotalCharges == ' '
    blank_total_charges = df['TotalCharges'].str.strip() == ''
    print(f"Number of blank TotalCharges records (tenure == 0): {blank_total_charges.sum()}")
    
    # Replace blank strings with '0.0' and cast to float
    df['TotalCharges'] = df['TotalCharges'].str.strip().replace('', '0.0')
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0.0)

    # 3. Create Senior Citizen Label
    df['SeniorCitizenLabel'] = df['SeniorCitizen'].map({0: 'No', 1: 'Yes'})

    # 4. Create Churn Flag (Binary integer 1/0 for mathematical operations and SQL aggregations)
    df['ChurnFlag'] = (df['Churn'] == 'Yes').astype(int)

    # 5. Tenure Group (as required by PRD Section Phase 2 line 220)
    # Buckets: '0-12 Months', '13-24 Months', '25-48 Months', '49+ Months'
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

    # Tenure Cohort Lifecycle
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

    # 6. Revenue Metrics
    df['MonthlyRevenue'] = df['MonthlyCharges']
    df['AnnualRevenue'] = (df['MonthlyCharges'] * 12).round(2)

    # 7. Customer Value Segment (Low, Medium, High Value)
    # Low Value (< $35), Medium Value ($35 - $70), High Value (> $70)
    def get_revenue_segment(monthly):
        if monthly < 35.0:
            return 'Low Value'
        elif monthly <= 70.0:
            return 'Medium Value'
        else:
            return 'High Value'

    df['CustomerValueSegment'] = df['MonthlyCharges'].apply(get_revenue_segment)

    # 8. Contract Category
    df['ContractCategory'] = df['Contract']

    # 9. Payment Category (Automatic vs Manual)
    def get_payment_category(pm):
        if 'automatic' in pm.lower():
            return 'Automatic'
        else:
            return 'Manual'

    df['PaymentCategory'] = df['PaymentMethod'].apply(get_payment_category)

    # 10. Service Count (Number of active subscribed services)
    service_cols = [
        'PhoneService', 'MultipleLines', 'OnlineSecurity', 'OnlineBackup',
        'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies'
    ]
    df['ServiceCount'] = df[service_cols].apply(
        lambda row: sum(val == 'Yes' for val in row), axis=1
    )

    # Key Service Flags
    df['HasInternet'] = (df['InternetService'] != 'No').astype(int)
    df['HasTechSupport'] = (df['TechSupport'] == 'Yes').astype(int)
    df['HasOnlineSecurity'] = (df['OnlineSecurity'] == 'Yes').astype(int)

    # 11. Churn Risk Segment (Rule-based risk scoring)
    # Risk factors identified from business analysis:
    # - Month-to-month contract (+2 pts)
    # - Fiber Optic internet without tech support (+2 pts)
    # - Tenure <= 12 months (+1 pt)
    # - Electronic check payment (+1 pt)
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

    # 12. Strategic Segment (Value + Risk 2x2 Matrix)
    # High Value + High Risk (Retention Priority)
    # High Value + Low Risk (Loyal Champions)
    # Low/Medium Value + High Risk (At-Risk Accounts)
    # Low/Medium Value + Low Risk (Stable Base)
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

    # 13. Create normalized column names for SQL compatibility (lower_snake_case)
    # Keep original PascalCase columns as well as standard lowercase aliases for SQL queries
    column_mapping = {
        'customerID': 'customer_id',
        'gender': 'gender',
        'SeniorCitizen': 'senior_citizen',
        'Partner': 'partner',
        'Dependents': 'dependents',
        'tenure': 'tenure',
        'PhoneService': 'phone_service',
        'MultipleLines': 'multiple_lines',
        'InternetService': 'internet_service',
        'OnlineSecurity': 'online_security',
        'OnlineBackup': 'online_backup',
        'DeviceProtection': 'device_protection',
        'TechSupport': 'tech_support',
        'StreamingTV': 'streaming_tv',
        'StreamingMovies': 'streaming_movies',
        'Contract': 'contract',
        'PaperlessBilling': 'paperless_billing',
        'PaymentMethod': 'payment_method',
        'MonthlyCharges': 'monthly_charges',
        'TotalCharges': 'total_charges',
        'Churn': 'churn',
        'ChurnFlag': 'churn_flag',
        'SeniorCitizenLabel': 'senior_citizen_label',
        'TenureGroup': 'tenure_group',
        'TenureCohort': 'tenure_cohort',
        'MonthlyRevenue': 'monthly_revenue',
        'AnnualRevenue': 'annual_revenue',
        'CustomerValueSegment': 'customer_value_segment',
        'ContractCategory': 'contract_category',
        'PaymentCategory': 'payment_category',
        'ServiceCount': 'service_count',
        'HasInternet': 'has_internet',
        'HasTechSupport': 'has_tech_support',
        'HasOnlineSecurity': 'has_online_security',
        'RiskScore': 'risk_score',
        'ChurnRiskSegment': 'churn_risk_segment',
        'StrategicSegment': 'strategic_segment'
    }

    # Save processed dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned dataset saved successfully to: {output_path}")
    print(f"Processed dataset shape: {df.shape}")
    print("Features summary:")
    print(df[['tenure_group' if 'tenure_group' in df else 'TenureGroup', 
              'CustomerValueSegment', 'ChurnRiskSegment', 'StrategicSegment']].value_counts())
    
    return df

if __name__ == '__main__':
    raw_path = 'data/raw/customer_churn.csv'
    proc_path = 'data/processed/customers_cleaned.csv'
    clean_and_prepare_data(raw_path, proc_path)
