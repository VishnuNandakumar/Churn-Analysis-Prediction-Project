-- ============================================================
-- churn_eda.sql
-- Exploratory behavioral signal analysis on Telco Churn data
-- Run against: SQLite / PostgreSQL / any SQL engine
-- ============================================================


-- ── 1. Overall churn rate ────────────────────────────────────
SELECT
    COUNT(*)                                          AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)   AS churned,
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2
    )                                                 AS churn_rate_pct
FROM telco_churn;


-- ── 2. Churn rate by contract type ───────────────────────────
SELECT
    Contract,
    COUNT(*)                                                  AS customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)           AS churned,
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2
    )                                                         AS churn_rate_pct
FROM telco_churn
GROUP BY Contract
ORDER BY churn_rate_pct DESC;


-- ── 3. Churn rate by tenure group ────────────────────────────
SELECT
    CASE
        WHEN tenure <= 12  THEN '0–12 months'
        WHEN tenure <= 24  THEN '13–24 months'
        WHEN tenure <= 48  THEN '25–48 months'
        ELSE                    '48+ months'
    END                                                       AS tenure_group,
    COUNT(*)                                                  AS customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)           AS churned,
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2
    )                                                         AS churn_rate_pct
FROM telco_churn
GROUP BY tenure_group
ORDER BY MIN(tenure);


-- ── 4. Churn rate by payment method ──────────────────────────
SELECT
    PaymentMethod,
    COUNT(*)                                                  AS customers,
    ROUND(AVG(MonthlyCharges), 2)                             AS avg_monthly_charge,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)           AS churned,
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2
    )                                                         AS churn_rate_pct
FROM telco_churn
GROUP BY PaymentMethod
ORDER BY churn_rate_pct DESC;


-- ── 5. High-risk customer profile ────────────────────────────
-- Month-to-month, electronic check, no online security
SELECT
    customerID,
    tenure,
    MonthlyCharges,
    Contract,
    PaymentMethod,
    OnlineSecurity,
    TechSupport,
    Churn
FROM telco_churn
WHERE
    Contract      = 'Month-to-month'
    AND PaymentMethod  = 'Electronic check'
    AND OnlineSecurity = 'No'
    AND TechSupport    = 'No'
ORDER BY MonthlyCharges DESC;


-- ── 6. Avg monthly charges — churned vs retained ─────────────
SELECT
    Churn,
    ROUND(AVG(MonthlyCharges), 2)   AS avg_monthly_charge,
    ROUND(AVG(TotalCharges),   2)   AS avg_total_charge,
    ROUND(AVG(tenure),         1)   AS avg_tenure_months
FROM telco_churn
GROUP BY Churn;


-- ── 7. Service add-ons impact on churn ───────────────────────
SELECT
    OnlineSecurity,
    TechSupport,
    COUNT(*)                                                  AS customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)           AS churned,
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2
    )                                                         AS churn_rate_pct
FROM telco_churn
GROUP BY OnlineSecurity, TechSupport
ORDER BY churn_rate_pct DESC;
