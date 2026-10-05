# SQL Analytics Execution Results & Verification Report
**Project:** Customer Churn & Retention Analytics Platform  
**Database Engine:** SQLite 3 (ANSI-SQL Compatible)  
**Database Location:** `data/customer_churn.db`  
**Total Table Records:** 7,043 rows in `customers`  

---

## File: `01_basic_analysis.sql`

### ====================================================================
```sql
-- ====================================================================
-- Script: 01_basic_analysis.sql
-- Project: Customer Churn & Retention Analytics
-- Description: Basic exploratory queries, baseline KPIs, and distributions
-- ====================================================================

-- 1. Total Customer Base Overview
SELECT 
    COUNT(customer_id) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    SUM(CASE WHEN churn = 'No' THEN 1 ELSE 0 END) AS active_customers,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1.0 ELSE 0.0 END) / COUNT(customer_id) * 100, 2) AS churn_rate_pct
FROM customers;
```

**Output:**

| total_customers | churned_customers | active_customers | churn_rate_pct |
| --- | --- | --- | --- |
| 7043.0 | 1869.0 | 5174.0 | 26.54 |


### 2. Demographic Breakdown (Gender and Senior Citizens)
```sql
-- 2. Demographic Breakdown (Gender and Senior Citizens)
SELECT 
    gender,
    senior_citizen_label,
    COUNT(customer_id) AS customer_count,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM customers), 2) AS pct_of_total_base,
    SUM(churn_flag) AS churned_count,
    ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct
FROM customers
GROUP BY gender, senior_citizen_label
ORDER BY churn_rate_pct DESC;
```

**Output:**

| gender | senior_citizen_label | customer_count | pct_of_total_base | churned_count | churn_rate_pct |
| --- | --- | --- | --- | --- | --- |
| Female | Yes | 568 | 8.06 | 240 | 42.25 |
| Male | Yes | 574 | 8.15 | 236 | 41.11 |
| Female | No | 2920 | 41.46 | 699 | 23.94 |
| Male | No | 2981 | 42.33 | 694 | 23.28 |


### 3. Household Composition (Partner and Dependents)
```sql
-- 3. Household Composition (Partner and Dependents)
SELECT 
    partner,
    dependents,
    COUNT(customer_id) AS total_customers,
    SUM(churn_flag) AS churned_count,
    ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges
FROM customers
GROUP BY partner, dependents
ORDER BY churn_rate_pct DESC;
```

**Output:**

| partner | dependents | total_customers | churned_count | churn_rate_pct | avg_monthly_charges |
| --- | --- | --- | --- | --- | --- |
| No | No | 3280 | 1123 | 34.24 | 62.98 |
| Yes | No | 1653 | 420 | 25.41 | 74.98 |
| No | Yes | 361 | 77 | 21.33 | 52.51 |
| Yes | Yes | 1749 | 249 | 14.24 | 60.97 |


### 4. Contract Distribution & High-Level Churn
```sql
-- 4. Contract Distribution & High-Level Churn
SELECT 
    contract,
    COUNT(customer_id) AS total_customers,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM customers), 2) AS contract_share_pct,
    SUM(churn_flag) AS churned_customers,
    ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct
FROM customers
GROUP BY contract
ORDER BY churn_rate_pct DESC;
```

**Output:**

| contract | total_customers | contract_share_pct | churned_customers | churn_rate_pct |
| --- | --- | --- | --- | --- |
| Month-to-month | 3875 | 55.02 | 1655 | 42.71 |
| One year | 1473 | 20.91 | 166 | 11.27 |
| Two year | 1695 | 24.07 | 48 | 2.83 |


### 5. Summary Statistics for Monthly and Total Charges
```sql
-- 5. Summary Statistics for Monthly and Total Charges
SELECT 
    churn,
    COUNT(customer_id) AS customer_count,
    ROUND(MIN(monthly_charges), 2) AS min_monthly_charges,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges,
    ROUND(MAX(monthly_charges), 2) AS max_monthly_charges,
    ROUND(AVG(total_charges), 2) AS avg_total_charges,
    ROUND(AVG(tenure), 1) AS avg_tenure_months
FROM customers
GROUP BY churn;
```

**Output:**

| churn | customer_count | min_monthly_charges | avg_monthly_charges | max_monthly_charges | avg_total_charges | avg_tenure_months |
| --- | --- | --- | --- | --- | --- | --- |
| No | 5174 | 18.25 | 61.27 | 118.75 | 2549.91 | 37.6 |
| Yes | 1869 | 18.85 | 74.44 | 118.35 | 1531.8 | 18.0 |


## File: `02_churn_analysis.sql`

### ====================================================================
```sql
-- ====================================================================
-- Script: 02_churn_analysis.sql
-- Project: Customer Churn & Retention Analytics
-- Description: Deep-dive churn analysis across contracts, tenure, services, and payments
-- ====================================================================

-- 1. Churn by Contract Type with Revenue Contribution
SELECT 
    contract,
    COUNT(customer_id) AS total_customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct,
    ROUND(SUM(monthly_charges), 2) AS total_monthly_revenue,
    ROUND(SUM(CASE WHEN churn_flag = 1 THEN monthly_charges ELSE 0 END), 2) AS monthly_revenue_at_risk
FROM customers
GROUP BY contract
ORDER BY churn_rate_pct DESC;
```

**Output:**

| contract | total_customers | churned_customers | churn_rate_pct | total_monthly_revenue | monthly_revenue_at_risk |
| --- | --- | --- | --- | --- | --- |
| Month-to-month | 3875 | 1655 | 42.71 | 257294.15 | 120847.1 |
| One year | 1473 | 166 | 11.27 | 95816.6 | 14118.45 |
| Two year | 1695 | 48 | 2.83 | 103005.85 | 4165.3 |


### 2. Churn by Tenure Cohort (Testing the 1st-Year Onboarding Cliff)
```sql
-- 2. Churn by Tenure Cohort (Testing the 1st-Year Onboarding Cliff)
SELECT 
    tenure_group,
    tenure_cohort,
    COUNT(customer_id) AS cohort_size,
    SUM(churn_flag) AS churned_count,
    ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges,
    ROUND(SUM(CASE WHEN churn_flag = 1 THEN monthly_charges ELSE 0 END), 2) AS lost_monthly_revenue
FROM customers
GROUP BY tenure_group, tenure_cohort
ORDER BY 
    CASE tenure_group
        WHEN '0-12 Months' THEN 1
        WHEN '13-24 Months' THEN 2
        WHEN '25-48 Months' THEN 3
        ELSE 4
    END;
```

**Output:**

| tenure_group | tenure_cohort | cohort_size | churned_count | churn_rate_pct | avg_monthly_charges | lost_monthly_revenue |
| --- | --- | --- | --- | --- | --- | --- |
| 0-12 Months | New (0-1 yr) | 2186 | 1037 | 47.44 | 56.1 | 68954.25 |
| 13-24 Months | Growing (1-2 yrs) | 1024 | 294 | 28.71 | 61.36 | 23081.65 |
| 25-48 Months | Established (2-4 yrs) | 1594 | 325 | 20.39 | 65.93 | 27462.5 |
| 49+ Months | Loyal (4+ yrs) | 2239 | 213 | 9.51 | 73.95 | 19632.45 |


### 3. Churn by Internet Service Provider Type
```sql
-- 3. Churn by Internet Service Provider Type
SELECT 
    internet_service,
    COUNT(customer_id) AS total_customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges,
    ROUND(SUM(CASE WHEN churn_flag = 1 THEN monthly_charges ELSE 0 END), 2) AS lost_monthly_revenue
FROM customers
GROUP BY internet_service
ORDER BY churn_rate_pct DESC;
```

**Output:**

| internet_service | total_customers | churned_customers | churn_rate_pct | avg_monthly_charges | lost_monthly_revenue |
| --- | --- | --- | --- | --- | --- |
| Fiber optic | 3096 | 1297 | 41.89 | 91.5 | 114300.05 |
| DSL | 2421 | 459 | 18.96 | 58.1 | 22529.2 |
| No | 1526 | 113 | 7.4 | 21.08 | 2301.6 |


### 4. Protective Service Moat: Tech Support & Online Security Impact
```sql
-- 4. Protective Service Moat: Tech Support & Online Security Impact
SELECT 
    has_internet,
    tech_support,
    online_security,
    COUNT(customer_id) AS customer_count,
    SUM(churn_flag) AS churned_count,
    ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_spend
FROM customers
WHERE internet_service != 'No'
GROUP BY has_internet, tech_support, online_security
ORDER BY churn_rate_pct DESC;
```

**Output:**

| has_internet | tech_support | online_security | customer_count | churned_count | churn_rate_pct | avg_monthly_spend |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | No | No | 2553 | 1250 | 48.96 | 74.19 |
| 1 | Yes | No | 945 | 211 | 22.33 | 79.76 |
| 1 | No | Yes | 920 | 196 | 21.3 | 75.69 |
| 1 | Yes | Yes | 1099 | 99 | 9.01 | 81.47 |


### 5. Payment Method & Billing Channel Comparison
```sql
-- 5. Payment Method & Billing Channel Comparison
SELECT 
    payment_category,
    payment_method,
    COUNT(customer_id) AS total_accounts,
    SUM(churn_flag) AS churned_accounts,
    ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN churn_flag = 1 THEN monthly_charges ELSE 0 END), 2) AS monthly_revenue_at_risk
FROM customers
GROUP BY payment_category, payment_method
ORDER BY churn_rate_pct DESC;
```

**Output:**

| payment_category | payment_method | total_accounts | churned_accounts | churn_rate_pct | monthly_revenue_at_risk |
| --- | --- | --- | --- | --- | --- |
| Manual | Electronic check | 2365 | 1071 | 45.29 | 84288.75 |
| Manual | Mailed check | 1612 | 308 | 19.11 | 16803.6 |
| Automatic | Bank transfer (automatic) | 1544 | 258 | 16.71 | 20091.9 |
| Automatic | Credit card (automatic) | 1522 | 232 | 15.24 | 17946.6 |


### 6. Interaction: Contract x Payment Method Matrix
```sql
-- 6. Interaction: Contract x Payment Method Matrix
SELECT 
    contract,
    payment_category,
    COUNT(customer_id) AS total_customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct
FROM customers
GROUP BY contract, payment_category
ORDER BY contract, churn_rate_pct DESC;
```

**Output:**

| contract | payment_category | total_customers | churned_customers | churn_rate_pct |
| --- | --- | --- | --- | --- |
| Month-to-month | Manual | 2743 | 1276 | 46.52 |
| Month-to-month | Automatic | 1132 | 379 | 33.48 |
| One year | Manual | 684 | 87 | 12.72 |
| One year | Automatic | 789 | 79 | 10.01 |
| Two year | Manual | 550 | 16 | 2.91 |
| Two year | Automatic | 1145 | 32 | 2.79 |


## File: `03_customer_segmentation.sql`

### ====================================================================
```sql
-- ====================================================================
-- Script: 03_customer_segmentation.sql
-- Project: Customer Churn & Retention Analytics
-- Description: Customer value segmentation, tenure segmentation, and strategic matrix
-- ====================================================================

-- 1. Value Tier Segmentation (Low, Medium, High Value)
SELECT 
    customer_value_segment,
    COUNT(customer_id) AS total_customers,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM customers), 2) AS customer_share_pct,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges,
    ROUND(SUM(monthly_charges), 2) AS total_monthly_revenue,
    SUM(churn_flag) AS churned_customers,
    ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN churn_flag = 1 THEN monthly_charges ELSE 0 END), 2) AS monthly_revenue_at_risk
FROM customers
GROUP BY customer_value_segment
ORDER BY avg_monthly_charges DESC;
```

**Output:**

| customer_value_segment | total_customers | customer_share_pct | avg_monthly_charges | total_monthly_revenue | churned_customers | churn_rate_pct | monthly_revenue_at_risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| High Value | 3583 | 50.87 | 90.23 | 323302.3 | 1267 | 35.36 | 112491.0 |
| Medium Value | 1729 | 24.55 | 54.79 | 94737.15 | 414 | 23.94 | 22216.8 |
| Low Value | 1731 | 24.58 | 22.0 | 38077.15 | 188 | 10.86 | 4423.05 |


### 2. Multi-Play Service Adoption Depth Segmentation
```sql
-- 2. Multi-Play Service Adoption Depth Segmentation
-- Classifying accounts based on the number of active services
WITH service_tier_cte AS (
    SELECT 
        customer_id,
        monthly_charges,
        churn_flag,
        service_count,
        CASE 
            WHEN service_count = 0 THEN '0 - No Add-on Services'
            WHEN service_count BETWEEN 1 AND 2 THEN '1 - Low Adoption (1-2 Services)'
            WHEN service_count BETWEEN 3 AND 5 THEN '2 - Moderate Adoption (3-5 Services)'
            ELSE '3 - Power Bundle (6+ Services)'
        END AS adoption_tier
    FROM customers
)
SELECT 
    adoption_tier,
    COUNT(customer_id) AS account_count,
    ROUND(AVG(service_count), 1) AS avg_services_used,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_spend,
    SUM(churn_flag) AS churned_count,
    ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct
FROM service_tier_cte
GROUP BY adoption_tier
ORDER BY adoption_tier;
```

**Output:**

| adoption_tier | account_count | avg_services_used | avg_monthly_spend | churned_count | churn_rate_pct |
| --- | --- | --- | --- | --- | --- |
| 0 - No Add-on Services | 80 | 0.0 | 24.9 | 35 | 43.75 |
| 1 - Low Adoption (1-2 Services) | 2889 | 1.4 | 38.73 | 749 | 25.93 |
| 2 - Moderate Adoption (3-5 Services) | 2795 | 4.0 | 77.95 | 873 | 31.23 |
| 3 - Power Bundle (6+ Services) | 1279 | 6.6 | 97.22 | 212 | 16.58 |


### 3. The 2x2 Strategic Retention Matrix
```sql
-- 3. The 2x2 Strategic Retention Matrix
-- Combining Customer Value Segment and Churn Risk Segment
SELECT 
    strategic_segment,
    COUNT(customer_id) AS total_customers,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM customers), 2) AS pct_of_base,
    SUM(churn_flag) AS churned_customers,
    ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN churn_flag = 1 THEN monthly_charges ELSE 0 END), 2) AS monthly_revenue_at_risk,
    ROUND(SUM(CASE WHEN churn_flag = 1 THEN monthly_charges ELSE 0 END) * 12, 2) AS annual_revenue_at_risk
FROM customers
GROUP BY strategic_segment
ORDER BY annual_revenue_at_risk DESC;
```

**Output:**

| strategic_segment | total_customers | pct_of_base | churned_customers | churn_rate_pct | monthly_revenue_at_risk | annual_revenue_at_risk |
| --- | --- | --- | --- | --- | --- | --- |
| High Value + High Risk (Retention Priority) | 1912 | 27.15 | 1071 | 56.01 | 93343.5 | 1120122.0 |
| High Value + Low/Med Risk (Loyal Champions) | 1671 | 23.73 | 196 | 11.73 | 19147.5 | 229770.0 |
| Low/Med Value + Low/Med Risk (Stable Core) | 3040 | 43.16 | 386 | 12.7 | 15750.35 | 189004.2 |
| Low/Med Value + High Risk (At-Risk Core) | 420 | 5.96 | 216 | 51.43 | 10889.5 | 130674.0 |


### 4. Cross-Tabulation: Tenure Cohort x Customer Value Segment
```sql
-- 4. Cross-Tabulation: Tenure Cohort x Customer Value Segment
SELECT 
    tenure_cohort,
    customer_value_segment,
    COUNT(customer_id) AS total_customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct,
    ROUND(SUM(monthly_charges), 2) AS segment_mrr
FROM customers
GROUP BY tenure_cohort, customer_value_segment
ORDER BY 
    CASE tenure_cohort
        WHEN 'New (0-1 yr)' THEN 1
        WHEN 'Growing (1-2 yrs)' THEN 2
        WHEN 'Established (2-4 yrs)' THEN 3
        ELSE 4
    END,
    segment_mrr DESC;
```

**Output:**

| tenure_cohort | customer_value_segment | total_customers | churned_customers | churn_rate_pct | segment_mrr |
| --- | --- | --- | --- | --- | --- |
| New (0-1 yr) | High Value | 875 | 594 | 67.89 | 72693.55 |
| New (0-1 yr) | Medium Value | 672 | 291 | 43.3 | 35938.85 |
| New (0-1 yr) | Low Value | 639 | 152 | 23.79 | 13997.35 |
| Growing (1-2 yrs) | High Value | 478 | 218 | 45.61 | 41774.35 |
| Growing (1-2 yrs) | Medium Value | 276 | 62 | 22.46 | 15189.1 |
| Growing (1-2 yrs) | Low Value | 270 | 14 | 5.19 | 5866.4 |
| Established (2-4 yrs) | High Value | 839 | 269 | 32.06 | 75988.55 |
| Established (2-4 yrs) | Medium Value | 381 | 40 | 10.5 | 20873.35 |
| Established (2-4 yrs) | Low Value | 374 | 16 | 4.28 | 8231.4 |
| Loyal (4+ yrs) | High Value | 1391 | 186 | 13.37 | 132845.85 |
| Loyal (4+ yrs) | Medium Value | 400 | 21 | 5.25 | 22735.85 |
| Loyal (4+ yrs) | Low Value | 448 | 6 | 1.34 | 9982.0 |


## File: `04_revenue_analysis.sql`

### ====================================================================
```sql
-- ====================================================================
-- Script: 04_revenue_analysis.sql
-- Project: Customer Churn & Retention Analytics
-- Description: Financial impact, revenue at risk, ARPU analysis, and high-value churn
-- ====================================================================

-- 1. High-Level Revenue Summary: Retained vs Churned
SELECT 
    churn,
    COUNT(customer_id) AS total_customers,
    ROUND(SUM(monthly_charges), 2) AS total_monthly_revenue,
    ROUND(SUM(monthly_charges) * 100.0 / (SELECT SUM(monthly_charges) FROM customers), 2) AS pct_of_total_mrr,
    ROUND(AVG(monthly_charges), 2) AS arpu_monthly,
    ROUND(SUM(total_charges), 2) AS total_historical_charges,
    ROUND(AVG(total_charges), 2) AS avg_historical_charges_per_account
FROM customers
GROUP BY churn;
```

**Output:**

| churn | total_customers | total_monthly_revenue | pct_of_total_mrr | arpu_monthly | total_historical_charges | avg_historical_charges_per_account |
| --- | --- | --- | --- | --- | --- | --- |
| No | 5174 | 316985.75 | 69.5 | 61.27 | 13193241.8 | 2549.91 |
| Yes | 1869 | 139130.85 | 30.5 | 74.44 | 2862926.9 | 1531.8 |


### 2. Revenue at Risk by Contract Type
```sql
-- 2. Revenue at Risk by Contract Type
SELECT 
    contract,
    COUNT(customer_id) AS total_customers,
    SUM(churn_flag) AS churned_count,
    ROUND(SUM(monthly_charges), 2) AS total_segment_mrr,
    ROUND(SUM(CASE WHEN churn_flag = 1 THEN monthly_charges ELSE 0 END), 2) AS monthly_revenue_at_risk,
    ROUND(SUM(CASE WHEN churn_flag = 1 THEN monthly_charges ELSE 0 END) * 12, 2) AS annual_revenue_at_risk,
    ROUND(SUM(CASE WHEN churn_flag = 1 THEN monthly_charges ELSE 0 END) * 100.0 / SUM(monthly_charges), 2) AS pct_segment_mrr_lost
FROM customers
GROUP BY contract
ORDER BY annual_revenue_at_risk DESC;
```

**Output:**

| contract | total_customers | churned_count | total_segment_mrr | monthly_revenue_at_risk | annual_revenue_at_risk | pct_segment_mrr_lost |
| --- | --- | --- | --- | --- | --- | --- |
| Month-to-month | 3875 | 1655 | 257294.15 | 120847.1 | 1450165.2 | 46.97 |
| One year | 1473 | 166 | 95816.6 | 14118.45 | 169421.4 | 14.73 |
| Two year | 1695 | 48 | 103005.85 | 4165.3 | 49983.6 | 4.04 |


### 3. Top High-Value Accounts that Churned (Individual Account Deep-Dive)
```sql
-- 3. Top High-Value Accounts that Churned (Individual Account Deep-Dive)
SELECT 
    customer_id,
    tenure,
    contract,
    internet_service,
    monthly_charges,
    total_charges,
    payment_method,
    service_count
FROM customers
WHERE churn = 'Yes' AND monthly_charges >= 100.0
ORDER BY monthly_charges DESC, tenure DESC
LIMIT 20;
```

**Output:**

| customer_id | tenure | contract | internet_service | monthly_charges | total_charges | payment_method | service_count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 8199-ZLLSA | 67 | One year | Fiber optic | 118.35 | 7804.15 | Bank transfer (automatic) | 8 |
| 2889-FPWRM | 72 | One year | Fiber optic | 117.8 | 8684.8 | Bank transfer (automatic) | 8 |
| 2302-ANTDP | 48 | Month-to-month | Fiber optic | 117.45 | 5438.9 | Electronic check | 8 |
| 9053-JZFKV | 67 | Two year | Fiber optic | 116.2 | 7752.3 | Credit card (automatic) | 8 |
| 1444-VVSGW | 70 | One year | Fiber optic | 115.65 | 7968.85 | Credit card (automatic) | 8 |
| 0201-OAMXR | 70 | One year | Fiber optic | 115.55 | 8127.6 | Credit card (automatic) | 8 |
| 4361-BKAXE | 41 | Month-to-month | Fiber optic | 114.5 | 4527.45 | Bank transfer (automatic) | 8 |
| 1555-DJEQW | 70 | Two year | Fiber optic | 114.2 | 7723.9 | Bank transfer (automatic) | 8 |
| 9158-VCTQB | 41 | Month-to-month | Fiber optic | 113.6 | 4594.95 | Bank transfer (automatic) | 8 |
| 7279-BUYWN | 41 | Month-to-month | Fiber optic | 113.2 | 4689.5 | Electronic check | 7 |
| 5271-YNWVR | 68 | Two year | Fiber optic | 113.15 | 7856.0 | Electronic check | 8 |
| 5236-PERKL | 57 | Two year | Fiber optic | 112.95 | 6465.0 | Bank transfer (automatic) | 7 |
| 1583-IHQZE | 12 | Month-to-month | Fiber optic | 112.95 | 1384.75 | Mailed check | 7 |
| 6664-FPDAC | 56 | One year | Fiber optic | 111.95 | 6418.9 | Electronic check | 7 |
| 2403-BCASL | 41 | One year | Fiber optic | 111.95 | 4534.9 | Electronic check | 7 |
| 3090-HAWSU | 61 | Two year | Fiber optic | 111.6 | 6876.05 | Credit card (automatic) | 7 |
| 2659-VXMWZ | 67 | One year | Fiber optic | 111.3 | 7482.1 | Electronic check | 7 |
| 9249-FXSCK | 52 | One year | Fiber optic | 111.25 | 5916.45 | Credit card (automatic) | 7 |
| 0115-TFERT | 21 | Month-to-month | Fiber optic | 111.2 | 2317.1 | Electronic check | 7 |
| 9079-YEXQJ | 54 | Month-to-month | Fiber optic | 111.1 | 6014.85 | Electronic check | 7 |


### 4. Revenue Decile Analysis using NTILE Window Function
```sql
-- 4. Revenue Decile Analysis using NTILE Window Function
-- Dividing customer base into 10 revenue deciles to inspect churn concentration
WITH decile_cte AS (
    SELECT 
        customer_id,
        monthly_charges,
        churn_flag,
        NTILE(10) OVER (ORDER BY monthly_charges ASC) AS revenue_decile
    FROM customers
)
SELECT 
    revenue_decile,
    COUNT(customer_id) AS customer_count,
    ROUND(MIN(monthly_charges), 2) AS min_monthly_charge,
    ROUND(MAX(monthly_charges), 2) AS max_monthly_charge,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charge,
    ROUND(SUM(monthly_charges), 2) AS total_decile_mrr,
    SUM(churn_flag) AS churned_count,
    ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN churn_flag = 1 THEN monthly_charges ELSE 0 END), 2) AS monthly_rev_at_risk
FROM decile_cte
GROUP BY revenue_decile
ORDER BY revenue_decile;
```

**Output:**

| revenue_decile | customer_count | min_monthly_charge | max_monthly_charge | avg_monthly_charge | total_decile_mrr | churned_count | churn_rate_pct | monthly_rev_at_risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.0 | 705.0 | 18.25 | 20.05 | 19.62 | 13833.85 | 61.0 | 8.65 | 1196.95 |
| 2.0 | 705.0 | 20.05 | 25.05 | 21.74 | 15324.8 | 66.0 | 9.36 | 1442.85 |
| 3.0 | 705.0 | 25.05 | 45.85 | 35.56 | 25069.05 | 180.0 | 25.53 | 6854.35 |
| 4.0 | 704.0 | 45.9 | 58.85 | 52.57 | 37008.7 | 172.0 | 24.43 | 8935.25 |
| 5.0 | 704.0 | 58.9 | 70.35 | 65.34 | 45999.7 | 153.0 | 21.73 | 10316.05 |
| 6.0 | 704.0 | 70.35 | 79.1 | 74.64 | 52543.95 | 267.0 | 37.93 | 19943.05 |
| 7.0 | 704.0 | 79.1 | 85.5 | 82.15 | 57833.0 | 267.0 | 37.93 | 21950.15 |
| 8.0 | 704.0 | 85.5 | 94.25 | 89.85 | 63256.25 | 241.0 | 34.23 | 21662.4 |
| 9.0 | 704.0 | 94.3 | 102.6 | 98.05 | 69025.95 | 288.0 | 40.91 | 28242.8 |
| 10.0 | 704.0 | 102.65 | 118.75 | 108.27 | 76221.35 | 174.0 | 24.72 | 18587.0 |


### 5. Cumulative Revenue at Risk Analysis (Running Totals)
```sql
-- 5. Cumulative Revenue at Risk Analysis (Running Totals)
WITH segment_rev AS (
    SELECT 
        contract,
        internet_service,
        ROUND(SUM(CASE WHEN churn_flag = 1 THEN monthly_charges ELSE 0 END), 2) AS monthly_loss
    FROM customers
    GROUP BY contract, internet_service
)
SELECT 
    contract,
    internet_service,
    monthly_loss,
    SUM(monthly_loss) OVER (ORDER BY monthly_loss DESC) AS cumulative_mrr_at_risk,
    ROUND(SUM(monthly_loss) OVER (ORDER BY monthly_loss DESC) * 100.0 / (SELECT SUM(monthly_charges) FROM customers WHERE churn = 'Yes'), 2) AS cumulative_pct_of_total_risk
FROM segment_rev
ORDER BY monthly_loss DESC;
```

**Output:**

| contract | internet_service | monthly_loss | cumulative_mrr_at_risk | cumulative_pct_of_total_risk |
| --- | --- | --- | --- | --- |
| Month-to-month | Fiber optic | 100482.0 | 100482.0 | 72.22 |
| Month-to-month | DSL | 18367.25 | 118849.25 | 85.42 |
| One year | Fiber optic | 10571.95 | 129421.2 | 93.02 |
| One year | DSL | 3356.25 | 132777.45 | 95.43 |
| Two year | Fiber optic | 3246.1 | 136023.55000000002 | 97.77 |
| Month-to-month | No | 1997.85 | 138021.40000000002 | 99.2 |
| Two year | DSL | 805.7 | 138827.10000000003 | 99.78 |
| One year | No | 190.25 | 139017.35000000003 | 99.92 |
| Two year | No | 113.5 | 139130.85000000003 | 100.0 |


## File: `05_advanced_analysis.sql`

### ====================================================================
```sql
-- ====================================================================
-- Script: 05_advanced_analysis.sql
-- Project: Customer Churn & Retention Analytics
-- Description: Advanced SQL demonstrating CTEs, Window Functions (RANK, DENSE_RANK, ROW_NUMBER), and Analytical Partitions
-- ====================================================================

-- 1. Ranking Customer Sub-Segments by Churn Rate (RANK vs DENSE_RANK)
-- Identifies the most vulnerable cohorts across Contract and Internet Service
WITH segment_metrics AS (
    SELECT 
        contract,
        internet_service,
        payment_category,
        COUNT(customer_id) AS total_customers,
        SUM(churn_flag) AS churned_customers,
        ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct,
        ROUND(SUM(CASE WHEN churn_flag = 1 THEN monthly_charges ELSE 0 END), 2) AS monthly_revenue_at_risk
    FROM customers
    GROUP BY contract, internet_service, payment_category
    HAVING COUNT(customer_id) >= 50 -- Filter for statistically significant segments
)
SELECT 
    contract,
    internet_service,
    payment_category,
    total_customers,
    churned_customers,
    churn_rate_pct,
    monthly_revenue_at_risk,
    RANK() OVER (ORDER BY churn_rate_pct DESC) AS churn_rate_rank,
    DENSE_RANK() OVER (ORDER BY monthly_revenue_at_risk DESC) AS rev_risk_dense_rank
FROM segment_metrics
ORDER BY rev_risk_dense_rank ASC;
```

**Output:**

| contract | internet_service | payment_category | total_customers | churned_customers | churn_rate_pct | monthly_revenue_at_risk | churn_rate_rank | rev_risk_dense_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Month-to-month | Fiber optic | Manual | 1508 | 891 | 59.08 | 76688.75 | 1 | 1 |
| Month-to-month | Fiber optic | Automatic | 620 | 271 | 43.71 | 23793.25 | 2 | 2 |
| Month-to-month | DSL | Manual | 841 | 305 | 36.27 | 14068.55 | 3 | 3 |
| One year | Fiber optic | Manual | 232 | 58 | 25.0 | 5835.25 | 4 | 4 |
| One year | Fiber optic | Automatic | 307 | 46 | 14.98 | 4736.7 | 7 | 5 |
| Month-to-month | DSL | Automatic | 382 | 89 | 23.3 | 4298.7 | 5 | 6 |
| Two year | Fiber optic | Automatic | 316 | 21 | 6.65 | 2235.35 | 12 | 7 |
| One year | DSL | Automatic | 317 | 28 | 8.83 | 1829.75 | 11 | 8 |
| Month-to-month | No | Manual | 394 | 80 | 20.3 | 1602.7 | 6 | 9 |
| One year | DSL | Manual | 253 | 25 | 9.88 | 1526.5 | 9 | 10 |
| Two year | Fiber optic | Manual | 113 | 10 | 8.85 | 1010.75 | 10 | 11 |
| Two year | DSL | Automatic | 461 | 8 | 1.74 | 574.6 | 16 | 12 |
| Month-to-month | No | Automatic | 130 | 19 | 14.62 | 395.15 | 8 | 13 |
| Two year | DSL | Manual | 167 | 4 | 2.4 | 231.1 | 14 | 14 |
| One year | No | Automatic | 165 | 5 | 3.03 | 105.35 | 13 | 15 |
| One year | No | Manual | 199 | 4 | 2.01 | 84.9 | 15 | 16 |
| Two year | No | Automatic | 368 | 3 | 0.82 | 69.65 | 17 | 17 |
| Two year | No | Manual | 270 | 2 | 0.74 | 43.85 | 18 | 18 |


### 2. Within-Contract Customer Spend Ranking using ROW_NUMBER() and PARTITION BY
```sql
-- 2. Within-Contract Customer Spend Ranking using ROW_NUMBER() and PARTITION BY
-- Ranks the top highest paying churned customers within each contract commitment
WITH ranked_churned_accounts AS (
    SELECT 
        customer_id,
        contract,
        tenure,
        monthly_charges,
        total_charges,
        internet_service,
        tech_support,
        ROW_NUMBER() OVER (
            PARTITION BY contract 
            ORDER BY monthly_charges DESC, tenure DESC
        ) AS rank_in_contract
    FROM customers
    WHERE churn = 'Yes'
)
SELECT 
    contract,
    rank_in_contract,
    customer_id,
    tenure,
    monthly_charges,
    total_charges,
    internet_service,
    tech_support
FROM ranked_churned_accounts
WHERE rank_in_contract <= 5
ORDER BY contract, rank_in_contract;
```

**Output:**

| contract | rank_in_contract | customer_id | tenure | monthly_charges | total_charges | internet_service | tech_support |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Month-to-month | 1 | 2302-ANTDP | 48 | 117.45 | 5438.9 | Fiber optic | Yes |
| Month-to-month | 2 | 4361-BKAXE | 41 | 114.5 | 4527.45 | Fiber optic | Yes |
| Month-to-month | 3 | 9158-VCTQB | 41 | 113.6 | 4594.95 | Fiber optic | Yes |
| Month-to-month | 4 | 7279-BUYWN | 41 | 113.2 | 4689.5 | Fiber optic | No |
| Month-to-month | 5 | 1583-IHQZE | 12 | 112.95 | 1384.75 | Fiber optic | Yes |
| One year | 1 | 8199-ZLLSA | 67 | 118.35 | 7804.15 | Fiber optic | Yes |
| One year | 2 | 2889-FPWRM | 72 | 117.8 | 8684.8 | Fiber optic | Yes |
| One year | 3 | 1444-VVSGW | 70 | 115.65 | 7968.85 | Fiber optic | Yes |
| One year | 4 | 0201-OAMXR | 70 | 115.55 | 8127.6 | Fiber optic | Yes |
| One year | 5 | 6664-FPDAC | 56 | 111.95 | 6418.9 | Fiber optic | Yes |
| Two year | 1 | 9053-JZFKV | 67 | 116.2 | 7752.3 | Fiber optic | Yes |
| Two year | 2 | 1555-DJEQW | 70 | 114.2 | 7723.9 | Fiber optic | Yes |
| Two year | 3 | 5271-YNWVR | 68 | 113.15 | 7856.0 | Fiber optic | Yes |
| Two year | 4 | 5236-PERKL | 57 | 112.95 | 6465.0 | Fiber optic | No |
| Two year | 5 | 3090-HAWSU | 61 | 111.6 | 6876.05 | Fiber optic | Yes |


### 3. Dynamic Customer Risk Profiling & Window Percentile Comparison
```sql
-- 3. Dynamic Customer Risk Profiling & Window Percentile Comparison
-- Compares individual customer spend against the average spend of their respective tenure cohort
WITH cohort_benchmarks AS (
    SELECT 
        customer_id,
        tenure_group,
        contract,
        monthly_charges,
        churn_flag,
        AVG(monthly_charges) OVER (PARTITION BY tenure_group) AS cohort_avg_monthly_charges,
        monthly_charges - AVG(monthly_charges) OVER (PARTITION BY tenure_group) AS variance_from_cohort_avg
    FROM customers
)
SELECT 
    tenure_group,
    ROUND(cohort_avg_monthly_charges, 2) AS cohort_avg_spend,
    COUNT(customer_id) AS total_customers,
    SUM(CASE WHEN variance_from_cohort_avg > 0 THEN 1 ELSE 0 END) AS above_avg_spenders,
    ROUND(AVG(CASE WHEN variance_from_cohort_avg > 0 THEN churn_flag ELSE NULL END) * 100.0, 2) AS above_avg_churn_rate_pct,
    ROUND(AVG(CASE WHEN variance_from_cohort_avg <= 0 THEN churn_flag ELSE NULL END) * 100.0, 2) AS below_avg_churn_rate_pct
FROM cohort_benchmarks
GROUP BY tenure_group, cohort_avg_monthly_charges
ORDER BY tenure_group;
```

**Output:**

| tenure_group | cohort_avg_spend | total_customers | above_avg_spenders | above_avg_churn_rate_pct | below_avg_churn_rate_pct |
| --- | --- | --- | --- | --- | --- |
| 0-12 Months | 56.1 | 2186 | 1091 | 62.79 | 32.15 |
| 13-24 Months | 61.36 | 1024 | 549 | 42.08 | 13.26 |
| 25-48 Months | 65.93 | 1594 | 888 | 30.86 | 7.22 |
| 49+ Months | 73.95 | 2239 | 1328 | 13.55 | 3.62 |


### 4. Multi-Condition Window Priority Scoring for Active Customers
```sql
-- 4. Multi-Condition Window Priority Scoring for Active Customers
-- Identifies the Top 15 highest-value active accounts most urgently requiring retention intervention
WITH active_at_risk_pool AS (
    SELECT 
        customer_id,
        contract,
        tenure,
        monthly_charges,
        internet_service,
        tech_support,
        payment_method,
        -- Calculate heuristic risk weighting
        (CASE WHEN contract = 'Month-to-month' THEN 3 ELSE 0 END) +
        (CASE WHEN internet_service = 'Fiber optic' AND tech_support = 'No' THEN 3 ELSE 0 END) +
        (CASE WHEN payment_method = 'Electronic check' THEN 2 ELSE 0 END) +
        (CASE WHEN tenure <= 12 THEN 2 ELSE 0 END) AS calculated_risk_points
    FROM customers
    WHERE churn = 'No' AND customer_value_segment = 'High Value'
)
SELECT 
    ROW_NUMBER() OVER (ORDER BY calculated_risk_points DESC, monthly_charges DESC) AS priority_rank,
    customer_id,
    contract,
    tenure AS tenure_months,
    monthly_charges,
    internet_service,
    tech_support,
    payment_method,
    calculated_risk_points
FROM active_at_risk_pool
ORDER BY priority_rank
LIMIT 15;
```

**Output:**

| priority_rank | customer_id | contract | tenure_months | monthly_charges | internet_service | tech_support | payment_method | calculated_risk_points |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 6734-GMPVK | Month-to-month | 5 | 105.3 | Fiber optic | No | Electronic check | 10 |
| 2 | 7145-FEJWU | Month-to-month | 12 | 105.3 | Fiber optic | No | Electronic check | 10 |
| 3 | 7379-FNIUJ | Month-to-month | 2 | 100.2 | Fiber optic | No | Electronic check | 10 |
| 4 | 6645-MXQJT | Month-to-month | 2 | 97.1 | Fiber optic | No | Electronic check | 10 |
| 5 | 4566-NECEV | Month-to-month | 5 | 96.55 | Fiber optic | No | Electronic check | 10 |
| 6 | 4060-LDNLU | Month-to-month | 7 | 96.2 | Fiber optic | No | Electronic check | 10 |
| 7 | 2984-AFWNC | Month-to-month | 3 | 95.4 | Fiber optic | No | Electronic check | 10 |
| 8 | 1960-UYCNN | Month-to-month | 10 | 95.25 | Fiber optic | No | Electronic check | 10 |
| 9 | 7398-SKNQZ | Month-to-month | 3 | 94.9 | Fiber optic | No | Electronic check | 10 |
| 10 | 5150-ITWWB | Month-to-month | 3 | 94.85 | Fiber optic | No | Electronic check | 10 |
| 11 | 5168-MSWXT | Month-to-month | 8 | 94.75 | Fiber optic | No | Electronic check | 10 |
| 12 | 6350-XFYGW | Month-to-month | 4 | 94.75 | Fiber optic | No | Electronic check | 10 |
| 13 | 3338-CVVEH | Month-to-month | 12 | 94.55 | Fiber optic | No | Electronic check | 10 |
| 14 | 8161-QYMTT | Month-to-month | 7 | 94.1 | Fiber optic | No | Electronic check | 10 |
| 15 | 8087-LGYHQ | Month-to-month | 9 | 94.05 | Fiber optic | No | Electronic check | 10 |


## File: `06_business_questions.sql`

### ====================================================================
```sql
-- ====================================================================
-- Script: 06_business_questions.sql
-- Project: Customer Churn & Retention Analytics
-- Description: Direct, production-grade SQL solutions to PRD Questions Q1 to Q10
-- ====================================================================

-- --------------------------------------------------------------------
-- Q1 — Overall Churn Rate
-- Formula: Churned Customers / Total Customers
-- --------------------------------------------------------------------
SELECT 
    COUNT(customer_id) AS total_customers,
    SUM(churn_flag) AS churned_customers,
    COUNT(customer_id) - SUM(churn_flag) AS active_retained_customers,
    ROUND(SUM(churn_flag) * 100.0 / COUNT(customer_id), 2) AS churn_rate_pct
FROM customers;
```

**Output:**

| total_customers | churned_customers | active_retained_customers | churn_rate_pct |
| --- | --- | --- | --- |
| 7043.0 | 1869.0 | 5174.0 | 26.54 |


### 
```sql
-- --------------------------------------------------------------------
-- Q2 — Churn by Contract Type
-- Find: Contract Type, Total Customers, Churned Customers, Churn Rate
-- --------------------------------------------------------------------
SELECT 
    contract AS contract_type,
    COUNT(customer_id) AS total_customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct
FROM customers
GROUP BY contract
ORDER BY churn_rate_pct DESC;
```

**Output:**

| contract_type | total_customers | churned_customers | churn_rate_pct |
| --- | --- | --- | --- |
| Month-to-month | 3875 | 1655 | 42.71 |
| One year | 1473 | 166 | 11.27 |
| Two year | 1695 | 48 | 2.83 |


### 
```sql
-- --------------------------------------------------------------------
-- Q3 — Churn by Tenure Cohort
-- Identify the tenure groups with the highest churn
-- --------------------------------------------------------------------
SELECT 
    tenure_group,
    COUNT(customer_id) AS total_customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct
FROM customers
GROUP BY tenure_group
ORDER BY churn_rate_pct DESC;
```

**Output:**

| tenure_group | total_customers | churned_customers | churn_rate_pct |
| --- | --- | --- | --- |
| 0-12 Months | 2186 | 1037 | 47.44 |
| 13-24 Months | 1024 | 294 | 28.71 |
| 25-48 Months | 1594 | 325 | 20.39 |
| 49+ Months | 2239 | 213 | 9.51 |


### 
```sql
-- --------------------------------------------------------------------
-- Q4 — Revenue at Risk
-- Calculate monthly revenue and annualized run-rate lost from churned customers
-- --------------------------------------------------------------------
SELECT 
    ROUND(SUM(monthly_charges), 2) AS total_monthly_revenue_all_customers,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN monthly_charges ELSE 0 END), 2) AS monthly_revenue_at_risk,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN monthly_charges ELSE 0 END) * 12, 2) AS annualized_revenue_at_risk,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN monthly_charges ELSE 0 END) * 100.0 / SUM(monthly_charges), 2) AS pct_of_mrr_at_risk
FROM customers;
```

**Output:**

| total_monthly_revenue_all_customers | monthly_revenue_at_risk | annualized_revenue_at_risk | pct_of_mrr_at_risk |
| --- | --- | --- | --- |
| 456116.6 | 139130.85 | 1669570.2 | 30.5 |


### 
```sql
-- --------------------------------------------------------------------
-- Q5 — High-Value Churn Accounts
-- Identify customers with high monthly charges (>$80), high tenure/lifetime, who churned
-- --------------------------------------------------------------------
SELECT 
    customer_id,
    tenure AS tenure_months,
    contract,
    payment_method,
    internet_service,
    monthly_charges,
    total_charges
FROM customers
WHERE churn = 'Yes' 
  AND customer_value_segment = 'High Value'
  AND tenure >= 24
ORDER BY monthly_charges DESC, total_charges DESC
LIMIT 15;
```

**Output:**

| customer_id | tenure_months | contract | payment_method | internet_service | monthly_charges | total_charges |
| --- | --- | --- | --- | --- | --- | --- |
| 8199-ZLLSA | 67 | One year | Bank transfer (automatic) | Fiber optic | 118.35 | 7804.15 |
| 2889-FPWRM | 72 | One year | Bank transfer (automatic) | Fiber optic | 117.8 | 8684.8 |
| 2302-ANTDP | 48 | Month-to-month | Electronic check | Fiber optic | 117.45 | 5438.9 |
| 9053-JZFKV | 67 | Two year | Credit card (automatic) | Fiber optic | 116.2 | 7752.3 |
| 1444-VVSGW | 70 | One year | Credit card (automatic) | Fiber optic | 115.65 | 7968.85 |
| 0201-OAMXR | 70 | One year | Credit card (automatic) | Fiber optic | 115.55 | 8127.6 |
| 4361-BKAXE | 41 | Month-to-month | Bank transfer (automatic) | Fiber optic | 114.5 | 4527.45 |
| 1555-DJEQW | 70 | Two year | Bank transfer (automatic) | Fiber optic | 114.2 | 7723.9 |
| 9158-VCTQB | 41 | Month-to-month | Bank transfer (automatic) | Fiber optic | 113.6 | 4594.95 |
| 7279-BUYWN | 41 | Month-to-month | Electronic check | Fiber optic | 113.2 | 4689.5 |
| 5271-YNWVR | 68 | Two year | Electronic check | Fiber optic | 113.15 | 7856.0 |
| 5236-PERKL | 57 | Two year | Bank transfer (automatic) | Fiber optic | 112.95 | 6465.0 |
| 6664-FPDAC | 56 | One year | Electronic check | Fiber optic | 111.95 | 6418.9 |
| 2403-BCASL | 41 | One year | Electronic check | Fiber optic | 111.95 | 4534.9 |
| 3090-HAWSU | 61 | Two year | Credit card (automatic) | Fiber optic | 111.6 | 6876.05 |


### 
```sql
-- --------------------------------------------------------------------
-- Q6 — Service-Based Churn Comparison
-- Compare churn across core Internet, Security, and Support offerings
-- --------------------------------------------------------------------
SELECT 
    'Internet: ' || internet_service AS service_offering,
    COUNT(customer_id) AS total_subscribers,
    SUM(churn_flag) AS churned_subscribers,
    ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct
FROM customers
GROUP BY internet_service

UNION ALL

SELECT 
    'Tech Support: ' || tech_support AS service_offering,
    COUNT(customer_id) AS total_subscribers,
    SUM(churn_flag) AS churned_subscribers,
    ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct
FROM customers
GROUP BY tech_support

UNION ALL

SELECT 
    'Online Security: ' || online_security AS service_offering,
    COUNT(customer_id) AS total_subscribers,
    SUM(churn_flag) AS churned_subscribers,
    ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct
FROM customers
GROUP BY online_security
ORDER BY churn_rate_pct DESC;
```

**Output:**

| service_offering | total_subscribers | churned_subscribers | churn_rate_pct |
| --- | --- | --- | --- |
| Internet: Fiber optic | 3096 | 1297 | 41.89 |
| Online Security: No | 3498 | 1461 | 41.77 |
| Tech Support: No | 3473 | 1446 | 41.64 |
| Internet: DSL | 2421 | 459 | 18.96 |
| Tech Support: Yes | 2044 | 310 | 15.17 |
| Online Security: Yes | 2019 | 295 | 14.61 |
| Internet: No | 1526 | 113 | 7.4 |
| Tech Support: No internet service | 1526 | 113 | 7.4 |
| Online Security: No internet service | 1526 | 113 | 7.4 |


### 
```sql
-- --------------------------------------------------------------------
-- Q7 — Customer Value Segmentation
-- Segments: Low Value (<$35), Medium Value ($35-$70), High Value (>$70)
-- --------------------------------------------------------------------
SELECT 
    customer_value_segment,
    COUNT(customer_id) AS customer_count,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM customers), 2) AS customer_pct,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_spend,
    ROUND(SUM(monthly_charges), 2) AS total_segment_mrr,
    SUM(churn_flag) AS churned_count,
    ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct
FROM customers
GROUP BY customer_value_segment
ORDER BY avg_monthly_spend DESC;
```

**Output:**

| customer_value_segment | customer_count | customer_pct | avg_monthly_spend | total_segment_mrr | churned_count | churn_rate_pct |
| --- | --- | --- | --- | --- | --- | --- |
| High Value | 3583 | 50.87 | 90.23 | 323302.3 | 1267 | 35.36 |
| Medium Value | 1729 | 24.55 | 54.79 | 94737.15 | 414 | 23.94 |
| Low Value | 1731 | 24.58 | 22.0 | 38077.15 | 188 | 10.86 |


### 
```sql
-- --------------------------------------------------------------------
-- Q8 — Top At-Risk Segments using Window Functions / Ranking
-- Identify customer cohorts with the highest churn rate (filtered for min volume 50)
-- --------------------------------------------------------------------
WITH cohort_stats AS (
    SELECT 
        contract,
        tenure_group,
        internet_service,
        COUNT(customer_id) AS cohort_size,
        SUM(churn_flag) AS churned_count,
        ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct,
        ROUND(SUM(CASE WHEN churn_flag = 1 THEN monthly_charges ELSE 0 END), 2) AS lost_mrr
    FROM customers
    GROUP BY contract, tenure_group, internet_service
    HAVING COUNT(customer_id) >= 50
)
SELECT 
    RANK() OVER (ORDER BY churn_rate_pct DESC) AS risk_rank,
    contract,
    tenure_group,
    internet_service,
    cohort_size,
    churned_count,
    churn_rate_pct,
    lost_mrr
FROM cohort_stats
ORDER BY risk_rank
LIMIT 10;
```

**Output:**

| risk_rank | contract | tenure_group | internet_service | cohort_size | churned_count | churn_rate_pct | lost_mrr |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Month-to-month | 0-12 Months | Fiber optic | 916 | 643 | 70.2 | 53178.3 |
| 2 | Month-to-month | 13-24 Months | Fiber optic | 425 | 215 | 50.59 | 19046.9 |
| 3 | Month-to-month | 25-48 Months | Fiber optic | 521 | 226 | 43.38 | 20762.05 |
| 4 | Month-to-month | 0-12 Months | DSL | 690 | 293 | 42.46 | 13351.9 |
| 5 | Month-to-month | 49+ Months | Fiber optic | 266 | 78 | 29.32 | 7494.75 |
| 6 | Month-to-month | 13-24 Months | DSL | 232 | 55 | 23.71 | 2765.4 |
| 7 | Month-to-month | 0-12 Months | No | 388 | 88 | 22.68 | 1771.25 |
| 8 | One year | 25-48 Months | Fiber optic | 154 | 31 | 20.13 | 3039.1 |
| 9 | One year | 49+ Months | Fiber optic | 355 | 67 | 18.87 | 6926.2 |
| 10 | Month-to-month | 25-48 Months | DSL | 227 | 36 | 15.86 | 1755.75 |


### 
```sql
-- --------------------------------------------------------------------
-- Q9 — Payment Method Analysis
-- Compare churn rate and volume across all payment methods
-- --------------------------------------------------------------------
SELECT 
    payment_method,
    payment_category,
    COUNT(customer_id) AS total_customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN churn_flag = 1 THEN monthly_charges ELSE 0 END), 2) AS monthly_revenue_lost
FROM customers
GROUP BY payment_method, payment_category
ORDER BY churn_rate_pct DESC;
```

**Output:**

| payment_method | payment_category | total_customers | churned_customers | churn_rate_pct | monthly_revenue_lost |
| --- | --- | --- | --- | --- | --- |
| Electronic check | Manual | 2365 | 1071 | 45.29 | 84288.75 |
| Mailed check | Manual | 1612 | 308 | 19.11 | 16803.6 |
| Bank transfer (automatic) | Automatic | 1544 | 258 | 16.71 | 20091.9 |
| Credit card (automatic) | Automatic | 1522 | 232 | 15.24 | 17946.6 |


### 
```sql
-- --------------------------------------------------------------------
-- Q10 — Strategic Retention Opportunity
-- Identify customer groups with: High Customer Value + High Churn Risk
-- These are the highest-priority business targets for retention outreach
-- --------------------------------------------------------------------
SELECT 
    strategic_segment,
    COUNT(customer_id) AS total_customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(AVG(churn_flag) * 100.0, 2) AS churn_rate_pct,
    ROUND(SUM(monthly_charges), 2) AS current_mrr,
    ROUND(SUM(CASE WHEN churn_flag = 1 THEN monthly_charges ELSE 0 END), 2) AS monthly_revenue_at_risk,
    ROUND(SUM(CASE WHEN churn_flag = 1 THEN monthly_charges ELSE 0 END) * 12, 2) AS annual_revenue_at_risk
FROM customers
GROUP BY strategic_segment
ORDER BY annual_revenue_at_risk DESC;
```

**Output:**

| strategic_segment | total_customers | churned_customers | churn_rate_pct | current_mrr | monthly_revenue_at_risk | annual_revenue_at_risk |
| --- | --- | --- | --- | --- | --- | --- |
| High Value + High Risk (Retention Priority) | 1912 | 1071 | 56.01 | 167096.4 | 93343.5 | 1120122.0 |
| High Value + Low/Med Risk (Loyal Champions) | 1671 | 196 | 11.73 | 156205.9 | 19147.5 | 229770.0 |
| Low/Med Value + Low/Med Risk (Stable Core) | 3040 | 386 | 12.7 | 112002.5 | 15750.35 | 189004.2 |
| Low/Med Value + High Risk (At-Risk Core) | 420 | 216 | 51.43 | 20811.8 | 10889.5 | 130674.0 |

