-- Overall churn rate
SELECT
    COUNT(*) AS customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(100.0 * AVG(churn_flag), 2) AS churn_rate_pct
FROM telco_churn;

-- Churn by contract type
SELECT
    contract,
    COUNT(*) AS customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(100.0 * AVG(churn_flag), 2) AS churn_rate_pct,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges
FROM telco_churn
GROUP BY contract
ORDER BY churn_rate_pct DESC;

-- Revenue at risk by payment method
SELECT
    payment_method,
    ROUND(SUM(revenue_at_risk), 2) AS revenue_at_risk,
    ROUND(100.0 * AVG(churn_flag), 2) AS churn_rate_pct
FROM telco_churn
GROUP BY payment_method
ORDER BY revenue_at_risk DESC;

-- Risk segmentation summary
SELECT
    risk_segment,
    COUNT(*) AS customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(100.0 * AVG(churn_flag), 2) AS churn_rate_pct,
    ROUND(SUM(monthly_charges), 2) AS total_monthly_revenue
FROM telco_churn
GROUP BY risk_segment
ORDER BY CASE risk_segment
    WHEN 'High' THEN 1
    WHEN 'Medium' THEN 2
    ELSE 3
END;
