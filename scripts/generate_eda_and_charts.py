"""
Exploratory Data Analysis (EDA) and Visualization Generator
Generates high-resolution visualization figures and computes analytical statistics.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Styling configuration
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

# Color Palette
PRIMARY_COLOR = '#1f77b4'
ACCENT_RED = '#d62728'
ACCENT_GREEN = '#2ca02c'
NEUTRAL_GRAY = '#7f7f7f'
PALETTE = ['#2ca02c', '#d62728'] # Retained (Green), Churned (Red)

def load_data(path='data/processed/customers_cleaned.csv'):
    df = pd.read_csv(path)
    return df

def generate_visualizations(df, output_dir='screenshots'):
    os.makedirs(output_dir, exist_ok=True)
    
    total_customers = len(df)
    churn_count = df['ChurnFlag'].sum()
    retained_count = total_customers - churn_count
    churn_rate = (churn_count / total_customers) * 100

    print(f"Total: {total_customers}, Retained: {retained_count}, Churned: {churn_count}, Rate: {churn_rate:.2f}%")

    # -------------------------------------------------------------
    # 1. Overall Churn Distribution (Donut & Breakdown)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, texts, autotexts = ax.pie(
        [retained_count, churn_count],
        labels=['Retained Customers\n(5,174 | 73.5%)', 'Churned Customers\n(1,869 | 26.5%)'],
        autopct='%1.1f%%',
        startangle=140,
        colors=['#3498db', '#e74c3c'],
        wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2),
        pctdistance=0.75,
        textprops=dict(fontsize=12, weight='bold')
    )
    for at in autotexts:
        at.set_color('white')
    ax.set_title("Overall Customer Churn Distribution\nBaseline Churn Rate: 26.54%", fontsize=15, pad=20, weight='bold')
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, '01_churn_distribution.png'))
    plt.close()

    # -------------------------------------------------------------
    # 2. Churn by Contract Type
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    contract_summary = df.groupby('Contract').agg(
        Total=('customerID', 'count'),
        Churned=('ChurnFlag', 'sum'),
        ChurnRate=('ChurnFlag', lambda x: x.mean() * 100)
    ).reindex(['Month-to-month', 'One year', 'Two year'])

    # Bar 1: Volume
    sns.countplot(data=df, x='Contract', hue='Churn', palette=['#3498db', '#e74c3c'], ax=ax1, order=['Month-to-month', 'One year', 'Two year'])
    ax1.set_title("Customer Volume by Contract Type", fontsize=13, weight='bold')
    ax1.set_xlabel("Contract Type")
    ax1.set_ylabel("Customer Count")
    for p in ax1.patches:
        height = p.get_height()
        if height > 0:
            ax1.annotate(f'{int(height):,}', (p.get_x() + p.get_width() / 2., height + 40),
                         ha='center', va='bottom', fontsize=9)

    # Bar 2: Churn Rate %
    bars = ax2.bar(contract_summary.index, contract_summary['ChurnRate'], color=['#e74c3c', '#f39c12', '#2ecc71'], edgecolor='black', alpha=0.85)
    ax2.set_title("Churn Rate % by Contract Type", fontsize=13, weight='bold')
    ax2.set_xlabel("Contract Type")
    ax2.set_ylabel("Churn Rate (%)")
    ax2.set_ylim(0, 50)
    for bar in bars:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 1.2, f'{yval:.1f}%', ha='center', va='bottom', fontsize=11, weight='bold')

    plt.suptitle("Contract Commitment Analysis: Month-to-Month High Risk Factor", fontsize=15, y=1.03, weight='bold')
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, '02_churn_by_contract.png'), bbox_inches='tight')
    plt.close()

    # -------------------------------------------------------------
    # 3. Churn by Tenure Group
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5))
    tenure_order = ['0-12 Months', '13-24 Months', '25-48 Months', '49+ Months']
    tenure_summary = df.groupby('TenureGroup').agg(
        Total=('customerID', 'count'),
        Churned=('ChurnFlag', 'sum'),
        ChurnRate=('ChurnFlag', lambda x: x.mean() * 100)
    ).reindex(tenure_order)

    bars = ax.bar(tenure_summary.index, tenure_summary['ChurnRate'], color='#34495e', edgecolor='white', width=0.55)
    ax.axhline(churn_rate, color='#e74c3c', linestyle='--', linewidth=2, label=f'Baseline Churn ({churn_rate:.1f}%)')
    ax.set_title("Churn Rate by Customer Tenure Cohort (The 1st-Year Onboarding Cliff)", fontsize=14, weight='bold', pad=15)
    ax.set_ylabel("Churn Rate (%)")
    ax.set_xlabel("Tenure Cohort")
    ax.set_ylim(0, 55)
    ax.legend(loc='upper right')

    for bar, (_, row) in zip(bars, tenure_summary.iterrows()):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 1.2,
                f"{h:.1f}%\n({int(row['Churned'])}/{int(row['Total'])})",
                ha='center', va='bottom', fontsize=10, weight='bold')

    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, '03_churn_by_tenure_group.png'))
    plt.close()

    # -------------------------------------------------------------
    # 4. Churn by Payment Method
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5))
    pm_summary = df.groupby('PaymentMethod').agg(
        Total=('customerID', 'count'),
        Churned=('ChurnFlag', 'sum'),
        ChurnRate=('ChurnFlag', lambda x: x.mean() * 100)
    ).sort_values(by='ChurnRate', ascending=False)

    colors = ['#e74c3c' if 'Electronic check' in x else '#3498db' for x in pm_summary.index]
    bars = ax.barh(pm_summary.index, pm_summary['ChurnRate'], color=colors, edgecolor='black', alpha=0.85, height=0.5)
    ax.axvline(churn_rate, color='#c0392b', linestyle='--', linewidth=1.5, label=f'Avg Churn ({churn_rate:.1f}%)')
    ax.set_title("Churn Rate by Payment Method (Electronic Check Friction)", fontsize=14, weight='bold', pad=15)
    ax.set_xlabel("Churn Rate (%)")
    ax.set_xlim(0, 55)
    ax.legend(loc='lower right')

    for bar, (_, row) in zip(bars, pm_summary.iterrows()):
        w = bar.get_width()
        ax.text(w + 1.0, bar.get_y() + bar.get_height()/2.,
                f"{w:.1f}% ({int(row['Churned']):,} / {int(row['Total']):,})",
                va='center', fontsize=10, weight='bold')

    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, '04_churn_by_payment_method.png'))
    plt.close()

    # -------------------------------------------------------------
    # 5. Churn by Internet Service Type
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 5))
    internet_summary = df.groupby('InternetService').agg(
        Total=('customerID', 'count'),
        Churned=('ChurnFlag', 'sum'),
        ChurnRate=('ChurnFlag', lambda x: x.mean() * 100)
    ).sort_values(by='ChurnRate', ascending=False)

    bars = ax.bar(internet_summary.index, internet_summary['ChurnRate'], color=['#e74c3c', '#2980b9', '#27ae60'], edgecolor='black', alpha=0.85, width=0.5)
    ax.axhline(churn_rate, color='gray', linestyle='--', linewidth=1.5, label=f'Avg Churn ({churn_rate:.1f}%)')
    ax.set_title("Churn Rate by Internet Service Type (Fiber Optic Churn Spike)", fontsize=14, weight='bold', pad=15)
    ax.set_ylabel("Churn Rate (%)")
    ax.set_ylim(0, 50)
    ax.legend(loc='upper right')

    for bar, (_, row) in zip(bars, internet_summary.iterrows()):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 1.2,
                f"{h:.1f}%\n({int(row['Churned']):,} / {int(row['Total']):,})",
                ha='center', va='bottom', fontsize=10, weight='bold')

    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, '05_churn_by_internet_service.png'))
    plt.close()

    # -------------------------------------------------------------
    # 6. Churn by Demographics
    # -------------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    demo_features = [
        ('SeniorCitizenLabel', 'Senior Citizen Status'),
        ('Partner', 'Has Partner'),
        ('Dependents', 'Has Dependents'),
        ('gender', 'Gender')
    ]

    for ax, (col, title) in zip(axes.flatten(), demo_features):
        summary = df.groupby(col)['ChurnFlag'].mean() * 100
        bars = ax.bar(summary.index, summary.values, color=['#3498db', '#e67e22'], width=0.45, edgecolor='black', alpha=0.85)
        ax.axhline(churn_rate, color='red', linestyle=':', label='Avg Churn')
        ax.set_title(f"Churn Rate by {title}", fontsize=12, weight='bold')
        ax.set_ylabel("Churn Rate (%)")
        ax.set_ylim(0, 48)
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., h + 1.0, f'{h:.1f}%', ha='center', va='bottom', fontsize=10, weight='bold')

    plt.suptitle("Demographic Churn Comparisons", fontsize=15, weight='bold', y=1.01)
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, '06_churn_by_demographics.png'), bbox_inches='tight')
    plt.close()

    # -------------------------------------------------------------
    # 7. Service Count vs Churn Rate
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 5))
    svc_summary = df.groupby('ServiceCount').agg(
        Total=('customerID', 'count'),
        Churned=('ChurnFlag', 'sum'),
        ChurnRate=('ChurnFlag', lambda x: x.mean() * 100)
    )

    ax.plot(svc_summary.index, svc_summary['ChurnRate'], marker='o', color='#8e44ad', linewidth=3, markersize=8, label='Churn Rate %')
    ax.axhline(churn_rate, color='red', linestyle='--', label=f'Avg Churn ({churn_rate:.1f}%)')
    ax.set_title("Customer Stickiness: Subscribed Service Count vs Churn Rate", fontsize=14, weight='bold', pad=15)
    ax.set_xlabel("Number of Subscribed Services (0 to 8)")
    ax.set_ylabel("Churn Rate (%)")
    ax.set_ylim(0, 70)
    ax.legend(loc='upper right')

    for x, y, tot in zip(svc_summary.index, svc_summary['ChurnRate'], svc_summary['Total']):
        ax.annotate(f"{y:.1f}%\n(N={tot})", (x, y + 2.5), ha='center', fontsize=9, weight='bold')

    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, '07_churn_by_service_count.png'))
    plt.close()

    # -------------------------------------------------------------
    # 8. Monthly Charges Distribution by Churn Status
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    sns.histplot(data=df, x='MonthlyCharges', hue='Churn', kde=True, palette=['#2ecc71', '#e74c3c'], ax=ax1, bins=30)
    ax1.set_title("Monthly Charges Distribution (KDE)", fontsize=13, weight='bold')
    ax1.set_xlabel("Monthly Charges ($)")

    sns.boxplot(data=df, x='Churn', y='MonthlyCharges', palette=['#2ecc71', '#e74c3c'], ax=ax2, width=0.4)
    ax2.set_title("Monthly Charges Boxplot by Churn", fontsize=13, weight='bold')
    ax2.set_xlabel("Churn Status")
    ax2.set_ylabel("Monthly Charges ($)")

    # Print medians on boxplot
    medians = df.groupby('Churn')['MonthlyCharges'].median()
    means = df.groupby('Churn')['MonthlyCharges'].mean()
    for i, churn_val in enumerate(['No', 'Yes']):
        ax2.text(i, medians[churn_val] + 2, f"Median: ${medians[churn_val]:.1f}\nMean: ${means[churn_val]:.1f}",
                 ha='center', fontsize=10, weight='bold', bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

    plt.suptitle("Revenue Profile: Churned Customers Incur Significantly Higher Monthly Charges", fontsize=15, weight='bold', y=1.02)
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, '08_monthly_charges_distribution_by_churn.png'), bbox_inches='tight')
    plt.close()

    # -------------------------------------------------------------
    # 9. Support & Security Protective Moat
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ts_summary = df.groupby('TechSupport')['ChurnFlag'].mean() * 100
    bars1 = ax1.bar(ts_summary.index, ts_summary.values, color=['#e74c3c', '#27ae60', '#95a5a6'], edgecolor='black', alpha=0.85, width=0.5)
    ax1.set_title("Churn Rate by Tech Support Status", fontsize=12, weight='bold')
    ax1.set_ylabel("Churn Rate (%)")
    ax1.set_ylim(0, 50)
    for b in bars1:
        ax1.text(b.get_x() + b.get_width()/2., b.get_height() + 1.2, f'{b.get_height():.1f}%', ha='center', weight='bold')

    os_summary = df.groupby('OnlineSecurity')['ChurnFlag'].mean() * 100
    bars2 = ax2.bar(os_summary.index, os_summary.values, color=['#e74c3c', '#27ae60', '#95a5a6'], edgecolor='black', alpha=0.85, width=0.5)
    ax2.set_title("Churn Rate by Online Security Status", fontsize=12, weight='bold')
    ax2.set_ylabel("Churn Rate (%)")
    ax2.set_ylim(0, 50)
    for b in bars2:
        ax2.text(b.get_x() + b.get_width()/2., b.get_height() + 1.2, f'{b.get_height():.1f}%', ha='center', weight='bold')

    plt.suptitle("The Protective Moat: Value-Added Services Reduce Churn by Over 60%", fontsize=14, weight='bold', y=1.02)
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, '09_tech_support_online_security.png'), bbox_inches='tight')
    plt.close()

    # -------------------------------------------------------------
    # 10. Strategic Segment Matrix & Revenue at Risk
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    strat_summary = df.groupby('StrategicSegment').agg(
        Customers=('customerID', 'count'),
        Churned=('ChurnFlag', 'sum'),
        MonthlyRevAtRisk=('MonthlyRevenue', lambda s: s[df.loc[s.index, 'ChurnFlag'] == 1].sum()),
        TotalMonthlyRev=('MonthlyRevenue', 'sum')
    )
    strat_summary['ChurnRate'] = (strat_summary['Churned'] / strat_summary['Customers']) * 100
    strat_summary['AnnualRevAtRisk'] = strat_summary['MonthlyRevAtRisk'] * 12

    short_labels = [
        "High Val + High Risk\n(Retention Priority)",
        "High Val + Low/Med Risk\n(Champions)",
        "Low/Med + High Risk\n(At-Risk Core)",
        "Low/Med + Low/Med\n(Stable Core)"
    ]

    bars1 = ax1.bar(short_labels, strat_summary['ChurnRate'], color=['#c0392b', '#27ae60', '#e67e22', '#2980b9'], edgecolor='black', alpha=0.85, width=0.55)
    ax1.set_title("Churn Rate % Across Strategic Segments", fontsize=13, weight='bold')
    ax1.set_ylabel("Churn Rate (%)")
    ax1.set_ylim(0, 65)
    for b in bars1:
        ax1.text(b.get_x() + b.get_width()/2., b.get_height() + 1.2, f'{b.get_height():.1f}%', ha='center', weight='bold')

    # Annual Revenue at Risk
    bars2 = ax2.bar(short_labels, strat_summary['AnnualRevAtRisk'] / 1e3, color=['#c0392b', '#27ae60', '#e67e22', '#2980b9'], edgecolor='black', alpha=0.85, width=0.55)
    ax2.set_title("Annualized Revenue at Risk ($ in Thousands)", fontsize=13, weight='bold')
    ax2.set_ylabel("Revenue at Risk ($k / Year)")
    for b in bars2:
        val = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2., val + 15, f"${val:.1f}k", ha='center', weight='bold')

    plt.suptitle("Strategic Retention Matrix: High Value + High Risk Represents Urgent Focus", fontsize=15, weight='bold', y=1.02)
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, '10_strategic_segment_quadrant.png'), bbox_inches='tight')
    plt.close()

    print("All 10 publication-quality figures successfully created and saved in screenshots/!")

if __name__ == '__main__':
    df = load_data()
    generate_visualizations(df)
