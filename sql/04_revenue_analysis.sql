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
