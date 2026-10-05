# 🛡️ RiskGuard AI: Hack2Skill × Snowflake CoCo CLI 2026 Submission Guide

> **Official Challenge Track:** Banking Risk, Fraud & Regulatory Intelligence Copilot  
> **Target Architecture:** Snowflake Data Cloud + Cortex Analyst + Cortex Search + Cortex LLM + Streamlit in Snowflake (SiS)

---

## 🏛️ Snowflake System Architecture

```
                                  USER / REGULATOR
                                         │
                                         ▼
                            ┌───────────────────────────┐
                            │    Streamlit in Snowflake │
                            │     Natural Language UI   │
                            └─────────────┬─────────────┘
                                          │
                                          ▼
                            ┌───────────────────────────┐
                            │     RISK ORCHESTRATOR     │
                            │   AML  │  CREDIT  │  LCR  │
                            └─────────────┬─────────────┘
                                          │
                   ┌──────────────────────┴──────────────────────┐
                   ▼                                             ▼
        ┌─────────────────────┐                       ┌─────────────────────┐
        │   CORTEX ANALYST    │                       │    CORTEX SEARCH    │
        │ Structured Banking  │                       │ Unstructured Policy │
        │    Data (SQL)       │                       │ & Regulation Corpus │
        └──────────┬──────────┘                       └──────────┬──────────┘
                   │                                             │
                   └──────────────────────┬──────────────────────┘
                                          ▼
                                ┌───────────────────┐
                                │  EVIDENCE ENGINE  │
                                │ Signal → Evidence │
                                │ → Rule → Finding  │
                                └─────────┬─────────┘
                                          ▼
                                ┌───────────────────┐
                                │    CORTEX LLM     │
                                │ Explain + Reason  │
                                │                   │
                                └─────────┬─────────┘
                                          ▼
                                ┌───────────────────┐
                                │  REGULATORY CASE  │
                                │  / AUDIT REPORT   │
                                └───────────────────┘
```

---

## 📂 Snowflake Project Assets

| Script / Artifact | Description |
| :--- | :--- |
| [`snowflake/01_setup_database_schema.sql`](file:///c:/python/banking_finance_issue/snowflake/01_setup_database_schema.sql) | DDL for core database, schemas (`DATA`, `ANALYTICS`, `GOVERNANCE`), and normalized financial tables: `CUSTOMER`, `ACCOUNT`, `TRANSACTION`, `COUNTERPARTY`, `LOAN`, `LOAN_REPAYMENT`, `LIQUIDITY_POSITION`, `REGULATORY_DOCUMENTS`, `RISK_EVIDENCE`, `RISK_CASE`. |
| [`snowflake/02_analytical_features.sql`](file:///c:/python/banking_finance_issue/snowflake/02_analytical_features.sql) | Window functions computing rolling velocity (`TXN_COUNT_1H`), 24h concentration (`TXN_AMOUNT_24H`), customer baseline deviations, and the **transparent additive AML Risk Score (+30, +25, +25, +10, +5)**. |
| [`snowflake/03_cortex_search_and_services.sql`](file:///c:/python/banking_finance_issue/snowflake/03_cortex_search_and_services.sql) | DDL for `RISKGUARD_REGULATORY_SEARCH` Cortex Search Service, semantic model stage, and governed `GENERATE_GOVERNED_RISK_EXPLANATION` Cortex LLM stored function. |
| [`snowflake/04_seed_data.sql`](file:///c:/python/banking_finance_issue/snowflake/04_seed_data.sql) | Realistic synthetic records including `C1007` (Rahul Sharma), counterparties (`CP-221`, `CP-223`, `CP-224`), pass-through transactions (`TXN-S001`, `TXN-S002`, `TXN-S003`), loans, liquidity time series, and indexed circulars. |
| [`snowflake/riskguard_semantic_model.yaml`](file:///c:/python/banking_finance_issue/snowflake/riskguard_semantic_model.yaml) | Official Cortex Analyst semantic model specification defining tables, dimensions, measures, formulas, and financial synonyms. |
| [`app.py`](file:///c:/python/banking_finance_issue/app.py) | Upgraded 5-page Streamlit / SiS application with Persona Switcher (`Business Manager`, `Compliance Officer`, `Auditor`). |

---

## 🚀 How to Deploy in Snowflake

### Step 1: Execute SQL Setup in Snowflake Worksheets
Log in to your Snowflake account and run the SQL scripts in numerical sequence:
```sql
-- 1. Database & Schemas
!source snowflake/01_setup_database_schema.sql;

-- 2. Analytical Feature Engineering & Transparent Scoring
!source snowflake/02_analytical_features.sql;

-- 3. Cortex Search Service & Cortex LLM Functions
!source snowflake/03_cortex_search_and_services.sql;

-- 4. Synthetic Banking Data & Regulatory Corpus
!source snowflake/04_seed_data.sql;
```

### Step 2: Upload Semantic Model for Cortex Analyst
```sql
USE DATABASE RISKGUARD;
USE SCHEMA RISKGUARD.ANALYTICS;

PUT file://snowflake/riskguard_semantic_model.yaml @SEMANTIC_MODELS_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
```

### Step 3: Run as Streamlit in Snowflake (SiS)
1. In Snowflake Web UI, navigate to **Streamlit** $\to$ **+ Streamlit App**.
2. Set Database: `RISKGUARD`, Schema: `ANALYTICS`, Warehouse: `RISKGUARD_WH`.
3. Paste the contents of [`app.py`](file:///c:/python/banking_finance_issue/app.py).
4. Click **Run**. The application automatically picks up `from snowflake.snowpark.context import get_active_session`.

### Or Run Locally / Offline:
```bash
streamlit run app.py
```
*(The embedded Snowflake emulator engine runs locally with zero external dependencies and 100% fidelity!)*
