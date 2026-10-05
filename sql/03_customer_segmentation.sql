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
