# Business Recommendation Report

## Problem statement

The business is losing recurring telecom revenue due to customer churn. The objective is to identify high-risk customers early and translate model output into targeted retention actions.

## Likely churn drivers

- Month-to-month contracts
- Low-tenure customers
- Higher monthly charges
- Electronic check payment method
- Weak service bundling, especially security and support add-ons

## Recommended actions

1. Convert month-to-month customers into annual plans with targeted discounts.
2. Launch first-90-day retention journeys for new customers with onboarding and service education.
3. Bundle high-value add-ons such as online security and tech support for risky segments.

## Revenue impact framing

Estimate monthly revenue at risk as:

`predicted_churn_probability * MonthlyCharges`

This can be aggregated by segment, account manager, geography, or offer group in Power BI.

## 30 / 60 / 90 day roadmap

### 30 days

- Validate data quality and deploy dashboard
- Align churn KPIs with business stakeholders
- Launch pilot outreach for high-risk month-to-month customers

### 60 days

- A/B test retention offers
- Monitor churn lift by segment
- Improve feature set with support tickets or usage data if available

### 90 days

- Productionize scoring pipeline
- Integrate model output into CRM workflows
- Track retained revenue against baseline

## Risks and limitations

- Dataset is static and lacks time-series customer behavior
- No direct campaign response or support usage features
- Class imbalance can impact recall/precision trade-offs
- Interpretability should be balanced with predictive performance
