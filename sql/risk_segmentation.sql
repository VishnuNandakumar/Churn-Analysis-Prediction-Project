-- ============================================================
-- risk_segmentation.sql
-- Tags customers as High / Medium / Low churn risk
-- using rule-based signals from the EDA findings
-- ============================================================


-- ── Rule-based risk scoring ───────────────────────────────────
-- Each flag contributes to a risk score (0–5).
-- Final segment: High (4–5), Medium (2–3), Low (0–1)

WITH risk_flags AS (
    SELECT
        customerID,
        tenure,
        MonthlyCharges,
        Contract,
        PaymentMethod,
        OnlineSecurity,
        TechSupport,
        Churn,

        -- Flag 1: Month-to-month contract (highest churn rate ~42%)
        CASE WHEN Contract = 'Month-to-month'         THEN 1 ELSE 0 END AS flag_contract,

        -- Flag 2: Electronic check payment (2.3× higher churn)
        CASE WHEN PaymentMethod = 'Electronic check'  THEN 1 ELSE 0 END AS flag_payment,

        -- Flag 3: Early-stage customer (first 12 months = critical window)
        CASE WHEN tenure <= 12                         THEN 1 ELSE 0 END AS flag_tenure,

        -- Flag 4: No online security
        CASE WHEN OnlineSecurity = 'No'               THEN 1 ELSE 0 END AS flag_no_security,

        -- Flag 5: No tech support
        CASE WHEN TechSupport = 'No'                  THEN 1 ELSE 0 END AS flag_no_support

    FROM telco_churn
),
risk_scored AS (
    SELECT
        *,
        (flag_contract + flag_payment + flag_tenure + flag_no_security + flag_no_support)
            AS risk_score
    FROM risk_flags
)
SELECT
    customerID,
    tenure,
    MonthlyCharges,
    Contract,
    PaymentMethod,
    risk_score,
    CASE
        WHEN risk_score >= 4 THEN 'High'
        WHEN risk_score >= 2 THEN 'Medium'
        ELSE                      'Low'
    END AS risk_segment,
    Churn AS actual_churn
FROM risk_scored
ORDER BY risk_score DESC, MonthlyCharges DESC;


-- ── Segment summary for Power BI import ──────────────────────
SELECT
    CASE
        WHEN risk_score >= 4 THEN 'High'
        WHEN risk_score >= 2 THEN 'Medium'
        ELSE                      'Low'
    END                                                        AS risk_segment,
    COUNT(*)                                                   AS customers,
    ROUND(AVG(MonthlyCharges), 2)                              AS avg_monthly_charge,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)            AS actual_churned,
    ROUND(
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2
    )                                                          AS churn_rate_pct
FROM (
    SELECT *,
        (CASE WHEN Contract = 'Month-to-month' THEN 1 ELSE 0 END
       + CASE WHEN PaymentMethod = 'Electronic check' THEN 1 ELSE 0 END
       + CASE WHEN tenure <= 12 THEN 1 ELSE 0 END
       + CASE WHEN OnlineSecurity = 'No' THEN 1 ELSE 0 END
       + CASE WHEN TechSupport = 'No' THEN 1 ELSE 0 END
        ) AS risk_score
    FROM telco_churn
) scored
GROUP BY risk_segment
ORDER BY churn_rate_pct DESC;
