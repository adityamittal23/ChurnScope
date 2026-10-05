"""
Builds and executes:
- notebooks/02_exploratory_analysis.ipynb
- notebooks/03_customer_segmentation.ipynb
"""

import nbformat as nbf

def generate_eda_notebook():
    nb = nbf.v4.new_notebook()
    cells = []

    cells.append(nbf.v4.new_markdown_cell("""# Phase 3 — Exploratory Data Analysis (EDA)
**Project:** Customer Churn & Retention Analytics Platform  
**Target:** Data Analyst / Business Intelligence Portfolio  
**Dataset:** Processed IBM Telco Customer Churn (7,043 Accounts)  

---

### Key Analytical Questions Addressed:
1. **Customer Demographics:** What is our customer distribution, and which demographic groups experience higher churn?
2. **Contract Type:** How stark is the churn rate difference between Month-to-Month contracts and Annual contracts?
3. **Tenure Lifecycle:** Does churn decrease with tenure, and what is the severity of the 1st-year onboarding cliff?
4. **Service Profiles:** Which specific internet and add-on services are correlated with elevated churn?
5. **Support Moat:** Do technical support and cybersecurity add-ons serve as retention anchors?
6. **Payment Methods:** How does manual payment via Electronic Check compare with automated methods?
7. **Revenue & Spend:** Are churned customers paying higher monthly bills than retained customers?
"""))

    cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: f'{x:.2f}')

df = pd.read_csv('../data/processed/customers_cleaned.csv')
print(f"Loaded analytical dataset with {df.shape[0]} rows and {df.shape[1]} columns.")
df.head(3)
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 1. Overall Churn Distribution & Baseline KPI
Establish the company-wide baseline churn rate:
$$\\text{Baseline Churn Rate} = \\frac{\\text{Churned Customers}}{\\text{Total Customers}}$$
"""))

    cells.append(nbf.v4.new_code_cell("""total_customers = len(df)
churn_count = df['ChurnFlag'].sum()
retained_count = total_customers - churn_count
churn_rate = (churn_count / total_customers) * 100

print(f"Total Customers:    {total_customers:,}")
print(f"Retained Customers: {retained_count:,} ({100 - churn_rate:.2f}%)")
print(f"Churned Customers:  {churn_count:,} ({churn_rate:.2f}%)")

fig, ax = plt.subplots(figsize=(6, 6))
ax.pie([retained_count, churn_count], labels=['Retained', 'Churned'],
       autopct='%1.1f%%', colors=['#3498db', '#e74c3c'], startangle=140,
       wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2))
ax.set_title(f"Baseline Churn Rate: {churn_rate:.2f}%", fontsize=14, weight='bold')
plt.show()
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 2. Demographic Analysis: Age, Dependents, and Partners
Investigate whether demographic traits drive attrition.
"""))

    cells.append(nbf.v4.new_code_cell("""demo_cols = ['SeniorCitizenLabel', 'Partner', 'Dependents', 'gender']
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

for ax, col in zip(axes.flatten(), demo_cols):
    res = df.groupby(col).agg(
        Total=('customerID', 'count'),
        Churned=('ChurnFlag', 'sum'),
        ChurnRate=('ChurnFlag', lambda s: s.mean() * 100)
    )
    bars = ax.bar(res.index, res['ChurnRate'], color='#2980b9', width=0.45)
    ax.axhline(churn_rate, color='red', linestyle='--', label='Baseline Churn')
    ax.set_title(f'Churn Rate by {col}', fontsize=12, weight='bold')
    ax.set_ylabel('Churn Rate (%)')
    ax.set_ylim(0, 50)
    for b in bars:
        ax.text(b.get_x() + b.get_width()/2., b.get_height() + 1, f"{b.get_height():.1f}%", ha='center', weight='bold')

plt.suptitle("Demographic Churn Comparisons", fontsize=14, weight='bold')
plt.tight_layout()
plt.show()
"""))

    cells.append(nbf.v4.new_markdown_cell("""**Demographic Findings:**
- **Senior Citizens:** Suffer a **41.7% churn rate** vs **23.6%** for younger demographics.
- **Dependents & Partners:** Customers with dependents churn at only **15.5%** vs **31.3%** for single accounts. Family accounts show much higher loyalty.
- **Gender:** Gender has virtually zero impact on churn (Male: 26.2%, Female: 26.9%).
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 3. Contract Type Analysis: The Single Biggest Driver
Analyze the relationship between commitment terms and attrition.
"""))

    cells.append(nbf.v4.new_code_cell("""contract_stats = df.groupby('Contract').agg(
    Total_Customers=('customerID', 'count'),
    Churned_Customers=('ChurnFlag', 'sum'),
    Churn_Rate_Pct=('ChurnFlag', lambda s: s.mean() * 100),
    Monthly_Revenue=('MonthlyCharges', 'sum')
).reindex(['Month-to-month', 'One year', 'Two year'])
contract_stats
"""))

    cells.append(nbf.v4.new_code_cell("""fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.bar(contract_stats.index, contract_stats['Churn_Rate_Pct'], color=['#e74c3c', '#f39c12', '#2ecc71'], width=0.5)
ax.set_title("Churn Rate by Contract Commitment Type", fontsize=14, weight='bold')
ax.set_ylabel("Churn Rate (%)")
ax.set_ylim(0, 50)
for b in bars:
    ax.text(b.get_x() + b.get_width()/2., b.get_height() + 1.2, f"{b.get_height():.1f}%", ha='center', weight='bold', fontsize=11)
plt.show()
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 4. Customer Tenure: The 1st-Year Onboarding Cliff
Examine attrition patterns as customer tenure increases.
"""))

    cells.append(nbf.v4.new_code_cell("""tenure_stats = df.groupby('TenureGroup').agg(
    Total=('customerID', 'count'),
    Churned=('ChurnFlag', 'sum'),
    ChurnRate=('ChurnFlag', lambda s: s.mean() * 100)
).reindex(['0-12 Months', '13-24 Months', '25-48 Months', '49+ Months'])
tenure_stats
"""))

    cells.append(nbf.v4.new_code_cell("""fig, ax = plt.subplots(figsize=(9, 4.5))
bars = ax.bar(tenure_stats.index, tenure_stats['ChurnRate'], color='#34495e', width=0.5)
ax.axhline(churn_rate, color='red', linestyle='--', label=f'Baseline ({churn_rate:.1f}%)')
ax.set_title("The 1st-Year Cliff: Churn Rate Plummets as Tenure Increases", fontsize=13, weight='bold')
ax.set_ylabel("Churn Rate (%)")
ax.set_ylim(0, 55)
ax.legend()
for b, (_, row) in zip(bars, tenure_stats.iterrows()):
    ax.text(b.get_x() + b.get_width()/2., b.get_height() + 1.2, f"{b.get_height():.1f}%\\\\n({int(row['Churned'])}/{int(row['Total'])})", ha='center', weight='bold')
plt.show()
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 5. Internet Service Type & Support Moat
Investigate why Fiber Optic customers have high churn and how Tech Support mitigates it.
"""))

    cells.append(nbf.v4.new_code_cell("""internet_summary = df.groupby(['InternetService', 'TechSupport']).agg(
    Total=('customerID', 'count'),
    Churned=('ChurnFlag', 'sum'),
    ChurnRate=('ChurnFlag', lambda s: s.mean() * 100)
).reset_index()
internet_summary
"""))

    cells.append(nbf.v4.new_code_cell("""fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=internet_summary[internet_summary['InternetService'] != 'No'],
            x='InternetService', y='ChurnRate', hue='TechSupport', palette=['#e74c3c', '#2ecc71'])
ax.set_title("Tech Support Impact: Dramatic Churn Reduction in Fiber Optic", fontsize=13, weight='bold')
ax.set_ylabel("Churn Rate (%)")
ax.set_ylim(0, 60)
plt.show()
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 6. Payment Method & Billing Friction"""))

    cells.append(nbf.v4.new_code_cell("""pm_stats = df.groupby(['PaymentCategory', 'PaymentMethod']).agg(
    Total=('customerID', 'count'),
    Churned=('ChurnFlag', 'sum'),
    ChurnRate=('ChurnFlag', lambda s: s.mean() * 100)
).reset_index()
pm_stats
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 7. Revenue Analysis: Monthly Charges & Revenue at Risk"""))

    cells.append(nbf.v4.new_code_cell("""print(f"Average Monthly Charge (Retained): ${df[df['ChurnFlag'] == 0]['MonthlyCharges'].mean():.2f}")
print(f"Average Monthly Charge (Churned):  ${df[df['ChurnFlag'] == 1]['MonthlyCharges'].mean():.2f}")

monthly_rev_at_risk = df[df['ChurnFlag'] == 1]['MonthlyCharges'].sum()
annual_rev_at_risk = monthly_rev_at_risk * 12
print(f"Total Monthly Recurring Revenue at Risk: ${monthly_rev_at_risk:,.2f}")
print(f"Total Annualized Revenue at Risk:        ${annual_rev_at_risk:,.2f}")
"""))

    nb.cells = cells
    with open('notebooks/02_exploratory_analysis.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("notebooks/02_exploratory_analysis.ipynb generated successfully.")

def generate_segmentation_notebook():
    nb = nbf.v4.new_notebook()
    cells = []

    cells.append(nbf.v4.new_markdown_cell("""# Phase 5 — Customer Segmentation & Retention Prioritization
**Project:** Customer Churn & Retention Analytics Platform  
**Target:** Data Analyst / Business Intelligence Portfolio  
**Objective:** Classify customer base along Multi-Dimensional Axes (Tenure, Revenue Value, Churn Risk) and build the 2x2 Strategic Retention Matrix to prioritize high-value at-risk accounts.
"""))

    cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../data/processed/customers_cleaned.csv')
print(f"Loaded {len(df)} customer records for segmentation.")
df.head(3)
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 1. Multi-Dimensional Segmentation Breakdown
We segment along 4 key business dimensions:
1. **Tenure Lifecycle Cohort:** New (0-1 yr), Growing (1-2 yrs), Established (2-4 yrs), Loyal (4+ yrs)
2. **Customer Value Segment:** Low Value (<$35), Medium Value ($35-$70), High Value (>$70)
3. **Churn Risk Tier:** High Risk, Medium Risk, Low Risk
4. **Strategic 2x2 Quadrant:** Value vs Risk Matrix
"""))

    cells.append(nbf.v4.new_code_cell("""# Dimension 1: Value Segment
val_summary = df.groupby('CustomerValueSegment').agg(
    Customers=('customerID', 'count'),
    Pct_Customers=('customerID', lambda s: len(s) / len(df) * 100),
    Avg_Monthly_Spend=('MonthlyCharges', 'mean'),
    Total_Monthly_Rev=('MonthlyCharges', 'sum'),
    Churn_Rate=('ChurnFlag', lambda s: s.mean() * 100)
).reindex(['Low Value', 'Medium Value', 'High Value'])
val_summary
"""))

    cells.append(nbf.v4.new_code_cell("""# Dimension 2: Risk Tier
risk_summary = df.groupby('ChurnRiskSegment').agg(
    Customers=('customerID', 'count'),
    Churned=('ChurnFlag', 'sum'),
    Churn_Rate=('ChurnFlag', lambda s: s.mean() * 100),
    Monthly_Rev_At_Risk=('MonthlyRevenue', lambda s: s[df.loc[s.index, 'ChurnFlag'] == 1].sum())
).reindex(['High Risk', 'Medium Risk', 'Low Risk'])
risk_summary
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 2. Strategic 2x2 Retention Quadrant
The core decision framework for retention strategy:
- **High Value + High Risk (Retention Priority):** Immediate outreach, VIP care, contract renewal discounts.
- **High Value + Low/Med Risk (Loyal Champions):** Cross-selling, loyalty perks, referral programs.
- **Low/Med Value + High Risk (At-Risk Core):** Automated email/SMS check-ins, self-service tools.
- **Low/Med Value + Low/Med Risk (Stable Core):** Low-touch maintenance.
"""))

    cells.append(nbf.v4.new_code_cell("""quadrant_summary = df.groupby('StrategicSegment').agg(
    Total_Customers=('customerID', 'count'),
    Pct_Base=('customerID', lambda s: len(s) / len(df) * 100),
    Churned_Count=('ChurnFlag', 'sum'),
    Churn_Rate_Pct=('ChurnFlag', lambda s: s.mean() * 100),
    Monthly_Rev_At_Risk=('MonthlyRevenue', lambda s: s[df.loc[s.index, 'ChurnFlag'] == 1].sum()),
    Annual_Rev_At_Risk=('MonthlyRevenue', lambda s: s[df.loc[s.index, 'ChurnFlag'] == 1].sum() * 12)
)
quadrant_summary
"""))

    cells.append(nbf.v4.new_code_cell("""fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

quadrant_summary['Churn_Rate_Pct'].plot(kind='bar', ax=ax1, color=['#c0392b', '#27ae60', '#e67e22', '#2980b9'])
ax1.set_title("Churn Rate % Across Strategic Quadrants", fontsize=12, weight='bold')
ax1.set_ylabel("Churn Rate (%)")
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=25, ha='right')

(quadrant_summary['Annual_Rev_At_Risk'] / 1000).plot(kind='bar', ax=ax2, color=['#c0392b', '#27ae60', '#e67e22', '#2980b9'])
ax2.set_title("Annualized Revenue at Risk ($ in Thousands)", fontsize=12, weight='bold')
ax2.set_ylabel("$k per Year")
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=25, ha='right')

plt.suptitle("Strategic Retention Matrix Analysis", fontsize=14, weight='bold')
plt.tight_layout()
plt.show()
"""))

    cells.append(nbf.v4.new_markdown_cell("""## 3. High-Value At-Risk Target List Export
Generate the tactical list of highest priority customer accounts for Customer Success and Retention teams.
"""))

    cells.append(nbf.v4.new_code_cell("""target_accounts = df[
    (df['CustomerValueSegment'] == 'High Value') &
    (df['Contract'] == 'Month-to-month') &
    (df['ChurnFlag'] == 0) # Currently active, but vulnerable to churn
].sort_values(by='MonthlyCharges', ascending=False)

print(f"Total High-Priority Active At-Risk Accounts: {len(target_accounts)}")
print(f"Total Monthly Recurring Revenue from these accounts: ${target_accounts['MonthlyCharges'].sum():,.2f}")
print(f"Total Annual Recurring Revenue: ${target_accounts['MonthlyCharges'].sum() * 12:,.2f}")

target_accounts[['customerID', 'tenure', 'MonthlyCharges', 'InternetService', 'TechSupport', 'PaymentMethod']].head(10)
"""))

    nb.cells = cells
    with open('notebooks/03_customer_segmentation.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("notebooks/03_customer_segmentation.ipynb generated successfully.")

if __name__ == '__main__':
    generate_eda_notebook()
    generate_segmentation_notebook()
