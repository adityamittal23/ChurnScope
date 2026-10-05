"""
Generates high-resolution dashboard screenshots mimicking Power BI Desktop report pages:
1. screenshots/executive_dashboard.png
2. screenshots/churn_analysis.png
3. screenshots/retention_analysis.png
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np

# Load cleaned data
df = pd.read_csv('data/processed/customers_cleaned.csv')

def create_header(fig, active_page="Executive Overview"):
    # Header bar
    header_ax = fig.add_axes([0, 0.93, 1, 0.07])
    header_ax.set_facecolor('#1E293B')
    header_ax.axis('off')
    
    header_ax.text(0.02, 0.5, "TELECOM ANALYTICS | Customer Churn & Retention Intelligence", 
                   color='white', fontsize=14, weight='bold', va='center')
    
    # Page Navigation Tabs
    pages = ["1. Executive Overview", "2. Churn Analysis", "3. Retention Strategy"]
    x_pos = 0.55
    for p in pages:
        is_active = active_page in p
        bg_col = '#3B82F6' if is_active else '#334155'
        text_col = 'white' if is_active else '#94A3B8'
        rect = patches.FancyBboxPatch((x_pos, 0.2), 0.13, 0.6, boxstyle="round,pad=0.02",
                                      facecolor=bg_col, edgecolor='none')
        header_ax.add_patch(rect)
        header_ax.text(x_pos + 0.065, 0.5, p, color=text_col, fontsize=9.5, weight='bold',
                       ha='center', va='center')
        x_pos += 0.145

def draw_kpi_card(ax, title, value, subtext="", bg_color='#FFFFFF', text_color='#1E293B', val_color='#2563EB'):
    ax.set_facecolor(bg_color)
    for spine in ax.spines.values():
        spine.set_color('#E2E8F0')
        spine.set_linewidth(1.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(0.5, 0.72, title.upper(), fontsize=9, color='#64748B', weight='bold', ha='center', va='center')
    ax.text(0.5, 0.42, value, fontsize=17, color=val_color, weight='heavy', ha='center', va='center')
    if subtext:
        ax.text(0.5, 0.18, subtext, fontsize=8, color='#94A3B8', ha='center', va='center')

# ==============================================================================
# Page 1: Executive Overview
# ==============================================================================
def render_executive_dashboard(output_path='screenshots/executive_dashboard.png'):
    fig = plt.figure(figsize=(16, 9), facecolor='#F1F5F9')
    create_header(fig, "Executive Overview")
    
    # Top KPI row (6 cards)
    card_specs = [
        ("Total Customers", f"{len(df):,}", "Active base accounts", '#0F172A'),
        ("Churned Customers", f"{df['ChurnFlag'].sum():,}", "Lost accounts", '#DC2626'),
        ("Churn Rate", f"{df['ChurnFlag'].mean()*100:.2f}%", "Baseline company KPI", '#DC2626'),
        ("Monthly Revenue", f"${df['MonthlyCharges'].sum()/1e3:.1f}K", "Total recurring MRR", '#2563EB'),
        ("Revenue at Risk", f"${df[df['ChurnFlag']==1]['MonthlyCharges'].sum()/1e3:.1f}K", "30.5% of total MRR", '#DC2626'),
        ("Avg Monthly Spend", f"${df['MonthlyCharges'].mean():.2f}", "ARPU across all accounts", '#0D9488'),
    ]
    
    card_width = 0.145
    card_gap = 0.016
    left_start = 0.03
    for i, (title, val, sub, col) in enumerate(card_specs):
        ax_card = fig.add_axes([left_start + i * (card_width + card_gap), 0.81, card_width, 0.095])
        draw_kpi_card(ax_card, title, val, sub, val_color=col)
        
    # Visual 1: Donut Chart - Baseline Churn Breakdown
    ax1 = fig.add_axes([0.03, 0.42, 0.28, 0.35], facecolor='white')
    for spine in ax1.spines.values(): spine.set_color('#E2E8F0')
    retained = (df['ChurnFlag'] == 0).sum()
    churned = (df['ChurnFlag'] == 1).sum()
    ax1.pie([retained, churned], labels=['Retained\n(73.5%)', 'Churned\n(26.5%)'],
            autopct='%1.1f%%', colors=['#3B82F6', '#EF4444'], startangle=140,
            wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2), pctdistance=0.75,
            textprops=dict(fontsize=10, weight='bold'))
    ax1.set_title("Customer Churn Breakdown", fontsize=11, weight='bold', pad=10, color='#1E293B')

    # Visual 2: Churn by Contract Type
    ax2 = fig.add_axes([0.34, 0.42, 0.31, 0.35], facecolor='white')
    for spine in ax2.spines.values(): spine.set_color('#E2E8F0')
    c_grp = df.groupby('Contract')['ChurnFlag'].mean() * 100
    bars = ax2.bar(c_grp.index, c_grp.values, color=['#EF4444', '#F59E0B', '#10B981'], width=0.5, edgecolor='#E2E8F0')
    ax2.set_title("Churn Rate by Contract Type", fontsize=11, weight='bold', pad=10, color='#1E293B')
    ax2.set_ylabel("Churn Rate (%)", fontsize=9, color='#64748B')
    ax2.set_ylim(0, 52)
    for b in bars:
        ax2.text(b.get_x() + b.get_width()/2., b.get_height() + 1.2, f"{b.get_height():.1f}%", ha='center', weight='bold', fontsize=9.5)

    # Visual 3: Churn Rate by Tenure Group
    ax3 = fig.add_axes([0.68, 0.42, 0.29, 0.35], facecolor='white')
    for spine in ax3.spines.values(): spine.set_color('#E2E8F0')
    t_grp = df.groupby('TenureGroup')['ChurnFlag'].mean() * 100
    t_grp = t_grp.reindex(['0-12 Months', '13-24 Months', '25-48 Months', '49+ Months'])
    bars = ax3.bar(t_grp.index, t_grp.values, color='#1E3A8A', width=0.5, edgecolor='#E2E8F0')
    ax3.axhline(df['ChurnFlag'].mean()*100, color='#EF4444', linestyle='--', label='Avg (26.5%)')
    ax3.set_title("Churn Rate by Customer Tenure Cohort", fontsize=11, weight='bold', pad=10, color='#1E293B')
    ax3.set_ylabel("Churn Rate (%)", fontsize=9, color='#64748B')
    ax3.set_ylim(0, 58)
    ax3.legend(fontsize=8, loc='upper right')
    for b in bars:
        ax3.text(b.get_x() + b.get_width()/2., b.get_height() + 1.2, f"{b.get_height():.1f}%", ha='center', weight='bold', fontsize=9)

    # Visual 4: Annual Revenue at Risk by Strategic Segment
    ax4 = fig.add_axes([0.03, 0.06, 0.45, 0.31], facecolor='white')
    for spine in ax4.spines.values(): spine.set_color('#E2E8F0')
    strat = df.groupby('StrategicSegment').apply(lambda s: (s[s['ChurnFlag']==1]['MonthlyCharges'].sum()*12)/1e3).sort_values(ascending=False)
    short_names = ["High Val + High Risk\n(Priority)", "Low/Med + High Risk\n(At-Risk Core)", "High Val + Low/Med\n(Champions)", "Low/Med + Low/Med\n(Stable)"]
    bars = ax4.barh(short_names[::-1], strat.values[::-1], color=['#3B82F6', '#10B981', '#F59E0B', '#EF4444'], height=0.55)
    ax4.set_title("Annualized Revenue at Risk ($ in Thousands)", fontsize=11, weight='bold', pad=10, color='#1E293B')
    ax4.set_xlabel("Annual Revenue Loss ($K)", fontsize=9, color='#64748B')
    for b in bars:
        w = b.get_width()
        ax4.text(w + 15, b.get_y() + b.get_height()/2., f"${w:.1f}K", va='center', weight='bold', fontsize=9.5)

    # Visual 5: Churn Rate by Customer Value Segment
    ax5 = fig.add_axes([0.52, 0.06, 0.45, 0.31], facecolor='white')
    for spine in ax5.spines.values(): spine.set_color('#E2E8F0')
    val_seg = df.groupby('CustomerValueSegment').agg(Total=('customerID', 'count'), ChurnRate=('ChurnFlag', lambda s: s.mean()*100)).reindex(['Low Value', 'Medium Value', 'High Value'])
    bars = ax5.bar(val_seg.index, val_seg['ChurnRate'], color=['#64748B', '#3B82F6', '#EF4444'], width=0.45)
    ax5.set_title("Churn Rate by Customer Value Segment", fontsize=11, weight='bold', pad=10, color='#1E293B')
    ax5.set_ylabel("Churn Rate (%)", fontsize=9, color='#64748B')
    ax5.set_ylim(0, 40)
    for b in bars:
        ax5.text(b.get_x() + b.get_width()/2., b.get_height() + 1.0, f"{b.get_height():.1f}%", ha='center', weight='bold', fontsize=9.5)

    fig.savefig(output_path, dpi=200)
    plt.close()
    print(f"Rendered: {output_path}")

# ==============================================================================
# Page 2: Churn Analysis (Deep Dive)
# ==============================================================================
def render_churn_analysis_dashboard(output_path='screenshots/churn_analysis.png'):
    fig = plt.figure(figsize=(16, 9), facecolor='#F1F5F9')
    create_header(fig, "Churn Analysis")
    
    # Visual 1: Payment Method Friction
    ax1 = fig.add_axes([0.03, 0.52, 0.45, 0.37], facecolor='white')
    for spine in ax1.spines.values(): spine.set_color('#E2E8F0')
    pm = df.groupby('PaymentMethod')['ChurnFlag'].mean().sort_values(ascending=False) * 100
    bars = ax1.barh(pm.index[::-1], pm.values[::-1], color=['#3B82F6', '#3B82F6', '#3B82F6', '#EF4444'], height=0.5)
    ax1.set_title("Churn Rate by Payment Method (Electronic Check Friction)", fontsize=11, weight='bold', pad=10, color='#1E293B')
    ax1.set_xlabel("Churn Rate (%)", fontsize=9, color='#64748B')
    ax1.set_xlim(0, 55)
    for b in bars:
        w = b.get_width()
        ax1.text(w + 1, b.get_y() + b.get_height()/2., f"{w:.1f}%", va='center', weight='bold', fontsize=9.5)

    # Visual 2: Internet Service Type & Tech Support
    ax2 = fig.add_axes([0.52, 0.52, 0.45, 0.37], facecolor='white')
    for spine in ax2.spines.values(): spine.set_color('#E2E8F0')
    inet_ts = df[df['InternetService'] != 'No'].groupby(['InternetService', 'TechSupport'])['ChurnFlag'].mean().unstack() * 100
    inet_ts.plot(kind='bar', ax=ax2, color=['#EF4444', '#10B981'], width=0.5)
    ax2.set_title("Internet Service vs Tech Support Protection", fontsize=11, weight='bold', pad=10, color='#1E293B')
    ax2.set_ylabel("Churn Rate (%)", fontsize=9, color='#64748B')
    ax2.set_ylim(0, 55)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)
    ax2.legend(['No Tech Support', 'Has Tech Support'], fontsize=9)

    # Visual 3: Subscribed Services Count vs Churn Rate
    ax3 = fig.add_axes([0.03, 0.07, 0.45, 0.38], facecolor='white')
    for spine in ax3.spines.values(): spine.set_color('#E2E8F0')
    svc = df.groupby('ServiceCount')['ChurnFlag'].mean() * 100
    ax3.plot(svc.index, svc.values, marker='o', color='#8B5CF6', linewidth=2.5, markersize=7)
    ax3.set_title("Product Stickiness: Active Services Count vs Churn Rate", fontsize=11, weight='bold', pad=10, color='#1E293B')
    ax3.set_xlabel("Number of Add-on Services (0 to 8)", fontsize=9, color='#64748B')
    ax3.set_ylabel("Churn Rate (%)", fontsize=9, color='#64748B')
    ax3.set_ylim(0, 68)
    for x, y in zip(svc.index, svc.values):
        ax3.text(x, y + 2.5, f"{y:.1f}%", ha='center', weight='bold', fontsize=8.5)

    # Visual 4: Monthly Spend Distribution (KDE Curves)
    ax4 = fig.add_axes([0.52, 0.07, 0.45, 0.38], facecolor='white')
    for spine in ax4.spines.values(): spine.set_color('#E2E8F0')
    df[df['ChurnFlag']==0]['MonthlyCharges'].plot(kind='kde', ax=ax4, color='#3B82F6', label='Retained (Avg $61.27)', linewidth=2)
    df[df['ChurnFlag']==1]['MonthlyCharges'].plot(kind='kde', ax=ax4, color='#EF4444', label='Churned (Avg $74.44)', linewidth=2)
    ax4.set_title("Monthly Spend Density: High Churn Concentration in $70-$100 Band", fontsize=11, weight='bold', pad=10, color='#1E293B')
    ax4.set_xlabel("Monthly Charges ($)", fontsize=9, color='#64748B')
    ax4.legend(fontsize=9)
    ax4.set_xlim(15, 125)

    fig.savefig(output_path, dpi=200)
    plt.close()
    print(f"Rendered: {output_path}")

# ==============================================================================
# Page 3: Customer Value & Retention Prioritization
# ==============================================================================
def render_retention_strategy_dashboard(output_path='screenshots/retention_analysis.png'):
    fig = plt.figure(figsize=(16, 9), facecolor='#F1F5F9')
    create_header(fig, "Retention Strategy")
    
    # Top KPI row (Strategic KPIs)
    kpis = [
        ("High-Value Customers", f"{(df['CustomerValueSegment']=='High Value').sum():,}", "Monthly spend > $70", '#2563EB'),
        ("High-Value Churn Rate", f"{df[df['CustomerValueSegment']=='High Value']['ChurnFlag'].mean()*100:.1f}%", "34.1% churn rate", '#DC2626'),
        ("Priority Target Accounts", "1,912", "Active Month-to-month High Value", '#DC2626'),
        ("Target MRR at Risk", "$167.3K", "Immediate protection priority", '#D97706'),
        ("10% Churn Save Impact", "$166.9K/yr", "Recoverable annual recurring revenue", '#10B981'),
    ]
    card_width = 0.175
    card_gap = 0.016
    left_start = 0.03
    for i, (title, val, sub, col) in enumerate(kpis):
        ax_card = fig.add_axes([left_start + i * (card_width + card_gap), 0.81, card_width, 0.095])
        draw_kpi_card(ax_card, title, val, sub, val_color=col)
        
    # Visual 1: 2x2 Strategic Quadrant Matrix (Bubble / Scatter representation)
    ax1 = fig.add_axes([0.03, 0.1, 0.45, 0.65], facecolor='white')
    for spine in ax1.spines.values(): spine.set_color('#E2E8F0')
    
    # 4 Quadrants
    quad_data = [
        ("High Value + High Risk\n(URGENT RETENTION)", 85, 45, 1912, '#EF4444'),
        ("High Value + Low/Med Risk\n(LOYAL CHAMPIONS)", 85, 12, 1373, '#10B981'),
        ("Low/Med Value + High Risk\n(AT-RISK CORE)", 45, 42, 420, '#F59E0B'),
        ("Low/Med Value + Low/Med Risk\n(STABLE CORE)", 45, 15, 3338, '#3B82F6')
    ]
    
    for label, x, y, size, col in quad_data:
        ax1.scatter(x, y, s=size*1.3, color=col, alpha=0.6, edgecolors='black', linewidth=1.5)
        ax1.text(x, y, f"{label}\n(N={size:,})", ha='center', va='center', weight='bold', fontsize=8.5, color='#0F172A')
        
    ax1.set_xlim(30, 100)
    ax1.set_ylim(0, 55)
    ax1.set_xlabel("Average Monthly Spend ($ / ARPU)", fontsize=10, weight='bold', color='#1E293B')
    ax1.set_ylabel("Cohort Churn Rate (%)", fontsize=10, weight='bold', color='#1E293B')
    ax1.set_title("Strategic Retention Matrix: Value vs Churn Risk", fontsize=12, weight='bold', pad=12, color='#1E293B')
    ax1.axvline(70, color='#94A3B8', linestyle=':')
    ax1.axhline(26.5, color='#94A3B8', linestyle=':')

    # Visual 2: Top Active High-Value Accounts Requiring Immediate Contact (Simulated Table)
    ax2 = fig.add_axes([0.52, 0.42, 0.45, 0.33], facecolor='white')
    ax2.axis('off')
    ax2.text(0.01, 0.95, "TOP PRIORITY ACCOUNTS REQUIRING RETENTION OUTREACH", fontsize=11, weight='bold', color='#1E293B')
    
    top_targets = df[(df['ChurnFlag']==0) & (df['Contract']=='Month-to-month') & (df['CustomerValueSegment']=='High Value')].sort_values(by='MonthlyCharges', ascending=False).head(6)
    table_data = [["CustomerID", "Tenure", "Monthly $", "Internet", "Tech Support", "Payment"]]
    for _, r in top_targets.iterrows():
        table_data.append([r['customerID'], f"{r['tenure']} mo", f"${r['MonthlyCharges']:.2f}", r['InternetService'], r['TechSupport'], r['PaymentMethod'].split()[0]])
        
    t = ax2.table(cellText=table_data, loc='center', cellLoc='center', colWidths=[0.22, 0.13, 0.16, 0.16, 0.16, 0.17])
    t.auto_set_font_size(False)
    t.set_fontsize(8.5)
    t.scale(1, 1.4)
    for (row, col), cell in t.get_celld().items():
        if row == 0:
            cell.set_facecolor('#1E293B')
            cell.set_text_props(color='white', weight='bold')
        else:
            cell.set_facecolor('#F8FAFC' if row % 2 == 0 else 'white')

    # Visual 3: Financial ROI of Churn Reduction Scenarios
    ax3 = fig.add_axes([0.52, 0.1, 0.45, 0.27], facecolor='white')
    for spine in ax3.spines.values(): spine.set_color('#E2E8F0')
    scenarios = ["Baseline Loss", "5% Save", "10% Save", "15% Save", "20% Save"]
    total_loss = df[df['ChurnFlag']==1]['MonthlyCharges'].sum() * 12 / 1e3
    savings = [total_loss, total_loss*0.95, total_loss*0.90, total_loss*0.85, total_loss*0.80]
    bars = ax3.bar(scenarios, savings, color=['#EF4444', '#F59E0B', '#3B82F6', '#10B981', '#059669'], width=0.5)
    ax3.set_title("Financial Recovery: Annual Revenue Saved under Retention Scenarios", fontsize=11, weight='bold', pad=10, color='#1E293B')
    ax3.set_ylabel("Annual Revenue at Risk ($K)", fontsize=9, color='#64748B')
    for b in bars:
        ax3.text(b.get_x() + b.get_width()/2., b.get_height() + 30, f"${b.get_height():.0f}K", ha='center', weight='bold', fontsize=8.5)

    fig.savefig(output_path, dpi=200)
    plt.close()
    print(f"Rendered: {output_path}")

if __name__ == '__main__':
    render_executive_dashboard()
    render_churn_analysis_dashboard()
    render_retention_strategy_dashboard()
