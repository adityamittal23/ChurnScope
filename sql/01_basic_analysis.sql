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
