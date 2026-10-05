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
