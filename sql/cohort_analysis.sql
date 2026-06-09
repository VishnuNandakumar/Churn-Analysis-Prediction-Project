-- ============================================================
-- cohort_analysis.sql
-- Monthly cohort churn rates by tenure bucket
-- ============================================================


-- ── Monthly churn rate by cohort (signup tenure bucket) ──────
-- This query simulates cohort analysis using tenure as a proxy
-- for signup month (common approach when join_date is unavailable)

WITH cohort_base AS (
    SELECT
        customerID,
        tenure,
        MonthlyCharges,
        Churn,
        CASE
            WHEN tenure BETWEEN  1 AND  3 THEN 'Month 1–3'
            WHEN tenure BETWEEN  4 AND  6 THEN 'Month 4–6'
            WHEN tenure BETWEEN  7 AND 12 THEN 'Month 7–12'
            WHEN tenure BETWEEN 13 AND 24 THEN 'Month 13–24'
            WHEN tenure BETWEEN 25 AND 48 THEN 'Month 25–48'
            ELSE                               'Month 48+'
        END AS cohort_bucket
    FROM telco_churn
),
cohort_summary AS (
    SELECT
        cohort_bucket,
        COUNT(*)                                                   AS cohort_size,
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)            AS churned_count,
        ROUND(
            100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2
        )                                                          AS churn_rate_pct,
        ROUND(AVG(MonthlyCharges), 2)                              AS avg_monthly_charge
    FROM cohort_base
    GROUP BY cohort_bucket
)
SELECT
    cohort_bucket,
    cohort_size,
    churned_count,
    churn_rate_pct,
    avg_monthly_charge,
    -- Cumulative churned share
    ROUND(
        100.0 * SUM(churned_count) OVER (ORDER BY MIN(tenure) ROWS UNBOUNDED PRECEDING)
        / SUM(cohort_size) OVER (), 2
    ) AS cumulative_churn_pct
FROM cohort_summary
JOIN cohort_base USING (cohort_bucket)
GROUP BY cohort_bucket, cohort_size, churned_count, churn_rate_pct, avg_monthly_charge
ORDER BY MIN(cohort_base.tenure);


-- ── Contract upgrade funnel ───────────────────────────────────
-- How many month-to-month customers reach 12+ months (upgrade candidates)?
SELECT
    Contract,
    SUM(CASE WHEN tenure < 12  THEN 1 ELSE 0 END)   AS lt_12_months,
    SUM(CASE WHEN tenure >= 12 THEN 1 ELSE 0 END)   AS gte_12_months,
    SUM(CASE WHEN Churn = 'Yes' AND tenure < 12 THEN 1 ELSE 0 END)  AS churned_lt_12,
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes' AND tenure < 12 THEN 1 ELSE 0 END)
        / NULLIF(SUM(CASE WHEN tenure < 12 THEN 1 ELSE 0 END), 0), 2
    )                                                AS early_churn_rate_pct
FROM telco_churn
GROUP BY Contract
ORDER BY early_churn_rate_pct DESC;
