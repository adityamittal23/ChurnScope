"""
Master Pipeline Runner — Customer Churn & Retention Analytics Platform
Executes the entire end-to-end analytics workflow with a single command:
1. Cleans raw data and engineers analytical features
2. Builds analytical SQLite database
3. Executes and verifies all 6 SQL query suites
4. Generates 10 publication-quality exploratory charts
5. Renders 3-page Power BI dashboard mockups
6. Runs the 8-point automated validation test suite
"""

import subprocess
import sys
import time

def run_step(step_num, title, command):
    print(f"\n[{step_num}/6] >>> {title}...")
    start_time = time.time()
    result = subprocess.run([sys.executable] + command.split()[1:], capture_output=True, text=True)
    elapsed = time.time() - start_time
    
    if result.returncode == 0:
        print(f"        [OK] Completed successfully in {elapsed:.2f}s")
        if result.stdout.strip():
            # Print brief preview of output
            lines = result.stdout.strip().split('\n')
            preview = lines[0] if len(lines) == 1 else f"{lines[0]} ... {lines[-1]}"
            print(f"        Output: {preview}")
    else:
        print(f"        [ERROR] Error during execution (code {result.returncode})")
        print(result.stderr)
        sys.exit(1)

def main():
    print("=" * 65)
    print(" CUSTOMER CHURN & RETENTION ANALYTICS — FULL PIPELINE EXECUTION")
    print("=" * 65)

    # Step 1: Clean raw data and engineer features
    run_step(1, "Data Cleaning & Feature Engineering", "python scripts/clean_data.py")

    # Step 2: Build SQLite database
    run_step(2, "Building SQLite Analytical Database", "python scripts/build_sql_database.py")

    # Step 3: Run and log SQL queries
    run_step(3, "Executing SQL Analytics Engine & Questions Q1-Q10", "python scripts/run_sql_analysis.py")

    # Step 4: Generate exploratory analysis visualizations
    run_step(4, "Generating Publication-Quality Charts", "python scripts/generate_eda_and_charts.py")

    # Step 5: Render Power BI dashboard screenshots
    run_step(5, "Rendering Power BI 3-Page Dashboard Mockups", "python scripts/generate_dashboard_screenshots.py")

    # Step 6: Run full validation suite
    run_step(6, "Executing 8-Point Quality Assurance Test Suite", "python scripts/validate_pipeline.py")

    print("\n" + "=" * 65)
    print(" PIPELINE COMPLETE! All datasets, databases, SQL reports,")
    print(" visual assets, and dashboards are generated and validated.")
    print("=" * 65)
    print("\nDeliverables to explore:")
    print("  * Cleaned Dataset: data/processed/customers_cleaned.csv")
    print("  * SQLite Database: data/customer_churn.db")
    print("  * Verified SQL Output: reports/sql_query_results.md")
    print("  * Strategic Report: reports/business_insights.md")
    print("  * Visual Screenshots: screenshots/")
    print("  * Power BI DAX Library: powerbi/dax_measures.md\n")

if __name__ == '__main__':
    main()
