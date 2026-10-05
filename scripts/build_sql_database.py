"""
Database Initializer & SQL Table Builder
Creates analytical SQLite database: data/customer_churn.db
Loads cleaned customer records and creates views for analytical queries.
"""

import sqlite3
import pandas as pd
import os

def build_database(csv_path='data/processed/customers_cleaned.csv', db_path='data/customer_churn.db'):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    if os.path.exists(db_path):
        os.remove(db_path)
        
    print(f"Creating database at: {db_path}")
    conn = sqlite3.connect(db_path)
    
    # Read processed CSV
    df = pd.read_csv(csv_path)
    
    import re
    def to_snake_case(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        return s2.replace('__', '_')
    
    df.columns = [to_snake_case(c) for c in df.columns]
    # Specific standard name overrides
    df = df.rename(columns={'customer_i_d': 'customer_id'})
    
    # Write to primary analytical table 'customers'
    df.to_sql('customers', conn, index=False, if_exists='replace')
    print(f"Loaded {len(df)} rows into 'customers' table.")
    
    # Create indexes for optimal query performance
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX idx_customers_contract ON customers(contract);")
    cursor.execute("CREATE INDEX idx_customers_tenure_group ON customers(tenure_group);")
    cursor.execute("CREATE INDEX idx_customers_churn ON customers(churn);")
    cursor.execute("CREATE INDEX idx_customers_value_segment ON customers(customer_value_segment);")
    cursor.execute("CREATE INDEX idx_customers_payment ON customers(payment_method);")
    conn.commit()
    
    # Verify row count and schema
    cursor.execute("SELECT COUNT(*) FROM customers;")
    count = cursor.fetchone()[0]
    print(f"Verification: 'customers' table contains {count} records.")
    
    conn.close()
    print("Database build completed successfully!")

if __name__ == '__main__':
    build_database()
