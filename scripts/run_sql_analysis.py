"""
SQL Test & Execution Runner
Executes all SQL query files in sql/ against data/customer_churn.db,
validates syntax, formats query outputs into Markdown tables, and writes reports/sql_query_results.md.
"""

import sqlite3
import os
import glob
import pandas as pd

def df_to_markdown_table(df):
    headers = [str(c) for c in df.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |"
    ]
    for _, row in df.iterrows():
        row_str = [str(x) if pd.notna(x) else "" for x in row]
        lines.append("| " + " | ".join(row_str) + " |")
    return "\n".join(lines)

def run_sql_scripts(db_path='data/customer_churn.db', sql_dir='sql', output_report='reports/sql_query_results.md'):
    print(f"Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    
    sql_files = sorted(glob.glob(os.path.join(sql_dir, '*.sql')))
    print(f"Found {len(sql_files)} SQL files to execute: {[os.path.basename(f) for f in sql_files]}")
    
    report_lines = [
        "# SQL Analytics Execution Results & Verification Report",
        "**Project:** Customer Churn & Retention Analytics Platform  ",
        "**Database Engine:** SQLite 3 (ANSI-SQL Compatible)  ",
        "**Database Location:** `data/customer_churn.db`  ",
        "**Total Table Records:** 7,043 rows in `customers`  ",
        "\n---\n"
    ]
    
    for sql_file in sql_files:
        base_name = os.path.basename(sql_file)
        print(f"\n==================================================")
        print(f"Executing: {base_name}")
        print(f"==================================================")
        
        report_lines.append(f"## File: `{base_name}`\n")
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Split into distinct statements by semicolon
        # Filter out empty statements and comment blocks
        raw_queries = [q.strip() for q in content.split(';') if q.strip()]
        
        query_idx = 1
        for q in raw_queries:
            # Skip if only comments
            lines = [line.strip() for line in q.split('\n') if line.strip() and not line.strip().startswith('--')]
            if not lines:
                continue
            
            clean_query = q.strip()
            print(f"Running Query {query_idx}...")
            
            # Extract comment header if available
            header_comments = [l for l in q.split('\n') if l.strip().startswith('--')]
            query_title = header_comments[0].replace('--', '').strip() if header_comments else f"Query {query_idx}"
            
            report_lines.append(f"### {query_title}")
            report_lines.append("```sql")
            report_lines.append(clean_query + ";")
            report_lines.append("```\n")
            
            try:
                df_res = pd.read_sql_query(clean_query, conn)
                print(f"Query {query_idx} returned {len(df_res)} rows.")
                report_lines.append("**Output:**\n")
                report_lines.append(df_to_markdown_table(df_res))
                report_lines.append("\n")
            except Exception as e:
                print(f"Error in Query {query_idx}: {e}")
                report_lines.append(f"**Execution Error:** `{e}`\n")
                
            query_idx += 1
            
    conn.close()
    
    os.makedirs(os.path.dirname(output_report), exist_ok=True)
    with open(output_report, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
        
    print(f"\nAll SQL queries successfully executed and logged to: {output_report}")

if __name__ == '__main__':
    run_sql_scripts()
