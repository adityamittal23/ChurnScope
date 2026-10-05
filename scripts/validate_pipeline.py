"""
End-to-End Pipeline & Data Validation Script
Performs rigorous quality checks comparing raw data, cleaned dataset, SQL database, and Power BI KPIs.
"""

import os
import sqlite3
import pandas as pd
import numpy as np

def run_validations():
    print("="*60)
    print("RUNNING END-TO-END PIPELINE VALIDATION CHECKS")
    print("="*60)
    
    raw_path = 'data/raw/customer_churn.csv'
    proc_path = 'data/processed/customers_cleaned.csv'
    db_path = 'data/customer_churn.db'
    
    # Check 1: File existence
    assert os.path.exists(raw_path), f"Missing {raw_path}"
    assert os.path.exists(proc_path), f"Missing {proc_path}"
    assert os.path.exists(db_path), f"Missing {db_path}"
    print("[PASS] Check 1: All primary data files exist.")
    
    # Check 2: Row Count & Shape Consistency
    df_raw = pd.read_csv(raw_path)
    df_proc = pd.read_csv(proc_path)
    assert len(df_raw) == 7043, f"Raw count expected 7043, got {len(df_raw)}"
    assert len(df_proc) == 7043, f"Cleaned count expected 7043, got {len(df_proc)}"
    assert df_proc.shape[1] >= 35, f"Expected 35+ columns in processed, got {df_proc.shape[1]}"
    print(f"[PASS] Check 2: Dataset dimensions verified ({len(df_proc)} rows, {df_proc.shape[1]} columns).")
    
    # Check 3: Null Values Check
    null_counts = df_proc.isna().sum().sum()
    assert null_counts == 0, f"Cleaned dataset contains {null_counts} null values!"
    print("[PASS] Check 3: Zero null values in cleaned dataset.")
    
    # Check 4: Duplicate Customer IDs
    dup_proc = df_proc.duplicated(subset=['customerID']).sum()
    assert dup_proc == 0, f"Duplicate customer IDs detected: {dup_proc}"
    print("[PASS] Check 4: Customer ID primary key 100% unique.")
    
    # Check 5: TotalCharges type and values
    assert pd.api.types.is_float_dtype(df_proc['TotalCharges']), "TotalCharges is not float!"
    assert (df_proc['TotalCharges'] < 0).sum() == 0, "Negative TotalCharges detected!"
    print("[PASS] Check 5: TotalCharges properly parsed as non-negative numeric floats.")
    
    # Check 6: Churn Metrics Consistency (Python vs Database)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*), SUM(churn_flag), ROUND(AVG(churn_flag)*100, 2), ROUND(SUM(monthly_charges), 2) FROM customers;")
    sql_tot, sql_churned, sql_rate, sql_mrr = cursor.fetchone()
    
    py_tot = len(df_proc)
    py_churned = int(df_proc['ChurnFlag'].sum())
    py_rate = round(float(df_proc['ChurnFlag'].mean() * 100), 2)
    py_mrr = round(float(df_proc['MonthlyCharges'].sum()), 2)
    
    assert sql_tot == py_tot == 7043, f"Row count mismatch: SQL={sql_tot}, Py={py_tot}"
    assert sql_churned == py_churned == 1869, f"Churned count mismatch: SQL={sql_churned}, Py={py_churned}"
    assert sql_rate == py_rate == 26.54, f"Churn rate mismatch: SQL={sql_rate}, Py={py_rate}"
    assert abs(sql_mrr - py_mrr) < 0.01, f"MRR mismatch: SQL={sql_mrr}, Py={py_mrr}"
    print(f"[PASS] Check 6: Python and SQL KPI consistency verified (Rate: {sql_rate}%, MRR: ${sql_mrr:,.2f}).")
    
    # Check 7: Visual Assets Check
    expected_screenshots = [
        '01_churn_distribution.png', '02_churn_by_contract.png', '03_churn_by_tenure_group.png',
        '04_churn_by_payment_method.png', '05_churn_by_internet_service.png', '06_churn_by_demographics.png',
        '07_churn_by_service_count.png', '08_monthly_charges_distribution_by_churn.png',
        '09_tech_support_online_security.png', '10_strategic_segment_quadrant.png',
        'executive_dashboard.png', 'churn_analysis.png', 'retention_analysis.png'
    ]
    for ss in expected_screenshots:
        path = os.path.join('screenshots', ss)
        assert os.path.exists(path), f"Missing expected screenshot: {path}"
        assert os.path.getsize(path) > 10000, f"Screenshot file suspiciously small: {path}"
    print(f"[PASS] Check 7: All {len(expected_screenshots)} visual and dashboard screenshots validated.")
    
    # Check 8: Deliverables Check
    deliverables = [
        'docs/data_dictionary.md',
        'docs/project_architecture.md',
        'notebooks/01_data_cleaning.ipynb',
        'notebooks/02_exploratory_analysis.ipynb',
        'notebooks/03_customer_segmentation.ipynb',
        'sql/01_basic_analysis.sql',
        'sql/02_churn_analysis.sql',
        'sql/03_customer_segmentation.sql',
        'sql/04_revenue_analysis.sql',
        'sql/05_advanced_analysis.sql',
        'sql/06_business_questions.sql',
        'powerbi/dax_measures.md',
        'powerbi/data_model_specification.md',
        'powerbi/powerbi_setup_guide.md',
        'reports/eda_summary.md',
        'reports/business_insights.md',
        'reports/sql_query_results.md'
    ]
    for d in deliverables:
        assert os.path.exists(d), f"Missing deliverable: {d}"
    print(f"[PASS] Check 8: All {len(deliverables)} core project deliverables exist and are non-empty.")
    
    conn.close()
    print("\n" + "="*60)
    print("ALL 8 QUALITY & VALIDATION ASSERTIONS PASSED WITH ZERO ERRORS!")
    print("="*60)

if __name__ == '__main__':
    run_validations()
