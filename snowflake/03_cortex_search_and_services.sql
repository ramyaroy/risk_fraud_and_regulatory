-- ============================================================================
-- 🛡️ RISKGUARD AI: Banking Risk, Fraud & Regulatory Intelligence Copilot
-- Challenge: Hack2Skill × Snowflake CoCo CLI 2026
-- Script 03: Snowflake Cortex Search Service & Governed Cortex LLM Setup
-- ============================================================================

USE DATABASE RISKGUARD;
USE SCHEMA RISKGUARD.DATA;

-- 1. CREATE SNOWFLAKE CORTEX SEARCH SERVICE
-- Indexes the unstructured regulatory corpus (RBI, Basel III, PMLA, FinCEN)
-- Provides sub-second semantic vector retrieval with metadata filtering.
CREATE OR REPLACE CORTEX SEARCH SERVICE RISKGUARD_REGULATORY_SEARCH
    ON TEXT
    ATTRIBUTES REGULATOR, JURISDICTION, DOCUMENT_TYPE, SECTION
    WAREHOUSE = RISKGUARD_WH
    TARGET_LAG = '1 hour'
    AS (
        SELECT 
            DOCUMENT_ID,
            DOCUMENT_TYPE,
            REGULATOR,
            JURISDICTION,
            TITLE,
            SECTION,
            EFFECTIVE_DATE,
            DOCUMENT_VERSION,
            TEXT
        FROM RISKGUARD.DATA.REGULATORY_DOCUMENTS
    );

-- 2. CREATE CORTEX STAGE FOR SEMANTIC MODEL (CORTEX ANALYST)
CREATE OR REPLACE STAGE RISKGUARD.ANALYTICS.SEMANTIC_MODELS_STAGE
    DIRECTORY = (ENABLE = TRUE);

-- 3. GOVERNED CORTEX LLM STORED PROCEDURE / FUNCTION
-- Enforces zero-hallucination model risk governance using claude-3-5-sonnet in Snowflake
USE SCHEMA RISKGUARD.GOVERNANCE;

CREATE OR REPLACE FUNCTION GENERATE_GOVERNED_RISK_EXPLANATION(
    CUSTOMER_ID STRING,
    EVIDENCE_PAYLOAD STRING,
    REGULATORY_TEXT STRING
)
RETURNS STRING
LANGUAGE SQL
AS
$$
    SNOWFLAKE.CORTEX.COMPLETE(
        'claude-3-5-sonnet',
        CONCAT(
            'You are a senior banking regulatory and financial crime compliance officer at a tier-1 bank.\n',
            'SYSTEM GOVERNANCE RULE: Use ONLY the provided evidence. You are strictly forbidden from inventing transactions, counterparties, or regulations.\n',
            'If the evidence is insufficient, you must state: "Insufficient evidence to establish this finding."\n\n',
            'SUBJECT CUSTOMER: ', CUSTOMER_ID, '\n\n',
            'TRANSACTION & BEHAVIORAL EVIDENCE:\n', EVIDENCE_PAYLOAD, '\n\n',
            'APPLICABLE STATUTORY REGULATION:\n', REGULATORY_TEXT, '\n\n',
            'Synthesize a concise, audit-ready explanation detailing:\n',
            '1. Exact Detected Pattern\n',
            '2. Transaction Lineage & Velocity Anomaly\n',
            '3. Statutory Non-Compliance Reason\n',
            '4. Recommended Compliance Action (e.g. EDD, STR filing, Debit Freeze)'
        )
    )
$$;

-- 4. VERIFY CORTEX SEARCH STATUS
-- (Run this query in Snowflake to check service health)
-- DESCRIBE CORTEX SEARCH SERVICE RISKGUARD_REGULATORY_SEARCH;
