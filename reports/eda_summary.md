# Exploratory Data Analysis (EDA) Summary Report
**Project:** Customer Churn & Retention Analytics Platform  
**Target:** Business Intelligence & Stakeholder Briefing  
**Dataset:** Processed IBM Telco Customer Churn (7,043 Records)  
**Author:** Data Analytics Team  

---

## 1. Executive Summary

This exploratory data analysis investigates the behavioral, transactional, and demographic drivers of customer attrition across **7,043 customer accounts**. 

### Core Baseline Metrics
- **Total Customer Accounts:** 7,043
- **Active Retained Customers:** 5,174 (73.46%)
- **Churned Customers:** 1,869 (26.54%)
- **Total Monthly Recurring Revenue (MRR):** $456,116.60
- **Monthly Revenue at Risk (Churned MRR):** $139,130.85 (30.50% of total MRR)
- **Annualized Revenue at Risk (ARR):** **$1,669,570.20**
- **Average Monthly Charges (Retained):** $61.27
- **Average Monthly Charges (Churned):** **$74.44** (+$13.17 / +21.5% higher)

The empirical analysis reveals that churn is **heavily concentrated in specific operational and contract segments** rather than distributed uniformly across the customer base.

---

## 2. Key Findings by Dimension

### 2.1 Contract Commitment: The Single Strongest Predictor
Contract commitment length represents the most powerful differentiator in customer retention:

| Contract Type | Total Customers | Churned Customers | Churn Rate (%) | Monthly Revenue |
|---|---|---|---|---|
| **Month-to-month** | 3,875 (55.0%) | 1,655 | **42.71%** | $263,018.60 |
| **One year** | 1,473 (20.9%) | 166 | **11.27%** | $95,683.40 |
| **Two year** | 1,695 (24.1%) | 48 | **2.83%** | $97,414.60 |

- **Observation:** Month-to-month customers represent **88.55% of all churned accounts** (1,655 out of 1,869). Customers with two-year contracts have virtually negligible churn (2.83%).
- **Business Rationale:** Absence of contractual switching costs combined with monthly billing review points leaves month-to-month customers vulnerable to competitor promotional offers.

---

### 2.2 Customer Tenure: The "1st-Year Onboarding Cliff"
Attrition is drastically front-loaded within the first 12 months of customer acquisition:

| Tenure Cohort | Tenure Range | Customer Count | Churned Count | Churn Rate (%) |
|---|---|---|---|---|
| **New (0-1 yr)** | 0–12 Months | 2,186 (31.0%) | 1,042 | **47.68%** |
| **Growing (1-2 yrs)** | 13–24 Months | 1,024 (14.5%) | 294 | **28.71%** |
| **Established (2-4 yrs)**| 25–48 Months | 1,594 (22.6%) | 328 | **20.58%** |
| **Loyal (4+ yrs)** | 49+ Months | 2,239 (31.8%) | 205 | **9.16%** |

- **Observation:** Nearly half (**47.68%**) of all customers in their first 12 months leave the company. After crossing the 24-month mark, churn drops to 20.6%, and customers with 4+ years of loyalty exhibit single-digit churn (9.16%).
- **Business Rationale:** The first 90–180 days suffer from onboarding friction, initial technical setup hurdles, and buyer's remorse before product habituation solidifies.

---

### 2.3 Product & Service Mix: Fiber Optic Anomaly & The Support Moat

| Service Dimension | Category | Total Accounts | Churn Rate (%) |
|---|---|---|---|
| **Internet Service** | Fiber Optic | 3,096 | **41.89%** |
| | DSL | 2,421 | 18.96% |
| | No Internet | 1,526 | 7.40% |
| **Tech Support** | No Tech Support | 3,473 | **41.64%** |
| | With Tech Support | 2,044 | **15.17%** |
| **Online Security** | No Online Security | 3,498 | **41.77%** |
| | With Online Security | 2,019 | **14.61%** |

- **Observation 1 (Fiber Optic Spike):** Despite being a premium high-speed offering, Fiber Optic exhibits a startling **41.89% churn rate**, generating over $100,000 in monthly churned revenue.
- **Observation 2 (The Protective Moat):** Subscribing to value-added protection services (Tech Support and Online Security) slashes customer churn by **over 63%** (from ~41.7% down to ~14.8%).
- **Observation 3 (Service Bundling):** Customers who subscribe to 5 or more services have a churn rate below **15%**, compared to **35%+** for customers with only 1–2 disconnected services.

---

### 2.4 Payment Methods: Electronic Check Friction

| Payment Method | Automation | Customers | Churn Rate (%) | Churned Volume |
|---|---|---|---|---|
| **Electronic Check** | Manual | 2,365 | **45.29%** | 1,071 |
| **Mailed Check** | Manual | 1,612 | 19.11% | 308 |
| **Bank Transfer** | Automatic | 1,544 | 16.71% | 258 |
| **Credit Card** | Automatic | 1,522 | 15.24% | 232 |

- **Observation:** Customers paying via manual Electronic Check churn at **45.29%**—nearly **triple** the churn rate of customers enrolled in automated bank debit (16.71%) or credit card auto-pay (15.24%).
- **Business Rationale:** Manual payment requires an active payment action every month, giving the customer recurring opportunities to re-evaluate their service cost, while experiencing payment gateway errors or late payment friction.

---

### 2.5 Demographics & Customer Segments

- **Senior Citizens:** Represent 16.2% of the base but exhibit an elevated **41.68% churn rate** (compared to 23.61% for non-seniors).
- **Family Accounts:** Customers with partners and dependents churn at only **15.5%**, compared to **31.3%** for single-person households. Multi-member households exhibit substantial structural inertia.
- **Gender:** Gender has **no statistically significant relationship** with customer churn (Males: 26.16%, Females: 26.92%).

---

### 2.6 Revenue Impact: High-Payer Paradox
- Churned customers have a **mean monthly spend of $74.44**, compared to **$61.27** for retained customers.
- Customers paying between **$70 and $100 per month** experience the highest concentration of churn. These are predominantly Fiber Optic customers paying high rates who lack bundled tech support or contract discounts.

---

## 3. Summary of Visualizations

All high-resolution figures have been saved to `screenshots/`:

1. `01_churn_distribution.png`: Baseline churn breakdown (26.54% vs 73.46%).
2. `02_churn_by_contract.png`: Contract volume and churn rate comparison.
3. `03_churn_by_tenure_group.png`: The 1st-year tenure drop curve.
4. `04_churn_by_payment_method.png`: Electronic Check vs Auto-pay channels.
5. `05_churn_by_internet_service.png`: Fiber Optic vs DSL vs No Internet.
6. `06_churn_by_demographics.png`: 4-quadrant demographic distribution.
7. `07_churn_by_service_count.png`: Customer stickiness vs service count.
8. `08_monthly_charges_distribution_by_churn.png`: Spend density and boxplots.
9. `09_tech_support_online_security.png`: Protective moat analysis.
10. `10_strategic_segment_quadrant.png`: Revenue at risk across the 2x2 matrix.

---

## 4. Next Steps
These findings directly inform the **SQL Analytics queries** in Phase 4 and the **Power BI Dashboard design** in Phase 7.
