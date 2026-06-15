DROP VIEW IF EXISTS vw_powerbi_customer_churn;

CREATE VIEW vw_powerbi_customer_churn AS
SELECT
    customer_id,
    gender,
    senior_citizen,
    partner,
    dependents,
    tenure,
    tenure_bucket,
    phone_service,
    multiple_lines,
    internet_service,
    online_security,
    online_backup,
    device_protection,
    tech_support,
    streaming_tv,
    streaming_movies,
    contract,
    paperless_billing,
    payment_method,
    monthly_charges,
    total_charges,
    churn_label,
    churn_flag,
    monthly_charge_bucket,
    risk_segment,
    revenue_at_risk
FROM telco_churn;
