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
