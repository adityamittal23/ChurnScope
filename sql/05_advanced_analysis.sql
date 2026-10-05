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
