# 🛡️ RiskGuard AI: FSI: Risk, Fraud & Regulatory Intelligence Copilot

> **Official Submission for the Hack2Skill × Snowflake CoCo CLI 2026 Challenge**  
> **Tagline:** An Evidence-First AI Copilot on Snowflake Data Cloud that turns financial risk signals into explainable, audit-ready regulatory findings.

[![Snowflake](https://img.shields.io/badge/Platform-Snowflake%20Data%20Cloud-blue.svg)](https://www.snowflake.com/)
[![Cortex Analyst](https://img.shields.io/badge/Cortex-Analyst%20(Structured%20SQL)-purple.svg)]()
[![Cortex Search](https://img.shields.io/badge/Cortex-Search%20(Regulatory%20RAG)-emerald.svg)]()
[![Cortex LLM](https://img.shields.io/badge/Cortex-COMPLETE%20(Claude--3.5--Sonnet)-orange.svg)]()
[![Streamlit in Snowflake](https://img.shields.io/badge/UI-Streamlit%20in%20Snowflake%20(SiS)-red.svg)]()

---

## 🚀 What CoCo CLI Makes Possible

1. Generate synthetic, referentially consistent transaction + account datasets - no production data needed
2. Build semantic views over transaction and policy text for governed natural language queries
3. Create Cortex Agent skills for fraud signal detection, AML pattern matching, and Basel metric computation
4. Orchestrate the full flow: signal -> evidence -> audit-ready regulatory report via CLI
5. Scaffold a compliance officer Streamlit dashboard with cited, explainable outputs
6. Connect to external regulatory sources via MCP for live policy lookups

---

## 📌 Executive Summary & Architecture

Banking and NBFC compliance teams spend days investigating alerts across **financial crime (AML), credit deterioration, and treasury liquidity (Basel III)**. Generic AI chatbots fail because they hallucinate regulatory sections and cannot compute exact mathematical aggregations.

**RiskGuard AI** is built natively on the **Snowflake Data Cloud + Cortex AI ecosystem**:
- **Structured Banking Data:** Queried via **Snowflake Cortex Analyst** using our official semantic model ([`riskguard_semantic_model.yaml`](file:///c:/python/banking_finance_issue/snowflake/riskguard_semantic_model.yaml)).
- **Unstructured Regulatory Corpus:** Indexed via **Snowflake Cortex Search** over central bank directives (RBI, Basel III, PMLA, FinCEN).
- **Governed Reasoning:** Powered by **Snowflake Cortex LLM** (`SNOWFLAKE.CORTEX.COMPLETE` with `claude-3-5-sonnet`) with strict, non-negotiable anti-hallucination guardrails.
- **Enterprise UI:** **Streamlit in Snowflake (SiS)** with role-based governance for Business Managers, Compliance Officers, and Auditors.

```
                         USER / REGULATOR
                                │
                                ▼
                    ┌──────────────────────┐
                    │   Streamlit / SiS    │
                    │ Natural Language UI  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    RISK ORCHESTRATOR │
                    │                      │
                    │ AML │ CREDIT │ LCR   │
                    └───────┬──────┬───────┘
                            │      │
                   ┌────────┘      └─────────┐
                   ▼                         ▼
           ┌──────────────┐          ┌──────────────┐
           │Cortex Analyst│          │ Cortex Search│
           │ Structured   │          │ Policies /   │
           │ Banking Data │          │ Regulations  │
           └──────┬───────┘          └──────┬───────┘
                  │                         │
                  └──────────┬──────────────┘
                             ▼
                    ┌──────────────────┐
                    │ Evidence Engine  │
                    │                  │
                    │ Signal → Evidence│
                    │ → Rule → Finding │
                    └────────┬─────────┘
                             ▼
                    ┌──────────────────┐
                    │ Cortex LLM       │
                    │ Explain + Reason │
                    └────────┬─────────┘
                             ▼
                    ┌──────────────────┐
                    │ Regulatory Case  │
                    │ / Audit Report   │
                    └──────────────────┘
```

---

## 📁 Repository Structure

```
c:\python\banking_finance_issue\
  ├── snowflake/                                <-- ❄️ Official Snowflake SQL & Cortex Assets
  │   ├── 01_setup_database_schema.sql         (DDL for CUSTOMER, ACCOUNT, TRANSACTION, LOAN, LIQUIDITY, EVIDENCE)
  │   ├── 02_analytical_features.sql           (Window functions & explainable additive AML risk scoring)
  │   ├── 03_cortex_search_and_services.sql    (Cortex Search Service DDL & Cortex LLM stored function)
  │   ├── 04_seed_data.sql                     (Production-grade synthetic banking records & regulatory corpus)
  │   └── riskguard_semantic_model.yaml        (Official Cortex Analyst Semantic Model specification)
  ├── hack2skill/                              <-- 🏆 Hack2Skill Submission Dossier & Playbooks
  │   ├── SNOWFLAKE_SUBMISSION_GUIDE.md        (Step-by-step Snowflake deployment & architecture guide)
  │   ├── DEMO_SCRIPT_SNOWFLAKE.md             (3-minute winning demo script using Customer C1007)
  │   ├── PPT_SNOWFLAKE_PITCH.md               (10-slide presentation deck customized for Snowflake CoCo CLI)
  │   ├── PROJECT_SUBMISSION_DOSSIER.md        (Master project documentation and problem statement)
  │   └── JUDGING_CRITERIA_MAPPING.md          (Line-by-line alignment with Hack2Skill rubrics)
  ├── engine/                                  <-- 🧠 Python Intelligence Engine
  │   ├── snowflake_session.py                 (Universal Snowpark session provider: SiS, Cloud, or Local Emulator)
  │   ├── cortex_analyst.py                    (Cortex Analyst NL-to-SQL client using semantic model)
  │   ├── cortex_search.py                     (Cortex Search client over REGULATORY_DOCUMENTS)
  │   ├── cortex_llm.py                        (Cortex COMPLETE governed reasoning with zero-hallucination guardrails)
  │   ├── evidence_engine.py                   (Grounded score decomposition & Plotly counterparty flow graph)
  │   ├── report_generator.py                  (Official 11-section STR/SAR & EWS PDF generator via ReportLab)
  │   └── audit_logger.py                      (Immutable SHA-256 cryptographic audit trail)
  ├── app.py                                   <-- 🚀 5-Page Streamlit / SiS Interactive Application
  └── run_copilot.py                           <-- ⚡ One-click launcher and sanity verifier
```

---

## 🚀 Quick Start: Running RiskGuard AI

### Option A: Run Locally / Offline (Zero-Friction Emulator)
The application runs out of the box with its built-in Snowflake Snowpark & Cortex emulator:
```bash
python run_copilot.py
```
Or directly:
```bash
streamlit run app.py
```
Open your browser at **`http://localhost:8501`**.

### Option B: Deploy to Snowflake Data Cloud / Streamlit in Snowflake (SiS)
1. Open a Snowflake SQL Worksheet and run scripts in order:
   - `01_setup_database_schema.sql`
   - `02_analytical_features.sql`
   - `03_cortex_search_and_services.sql`
   - `04_seed_data.sql`
2. Upload the semantic model to the stage:
   ```sql
   PUT file://snowflake/riskguard_semantic_model.yaml @RISKGUARD.ANALYTICS.SEMANTIC_MODELS_STAGE AUTO_COMPRESS=FALSE;
   ```
3. Create a **Streamlit in Snowflake (SiS)** app in `RISKGUARD.ANALYTICS` and paste [`app.py`](file:///c:/python/banking_finance_issue/app.py).

---

## 🎯 The Core Demo Journey (Demonstrated in 3 Minutes)

1. **Ask Cortex Copilot:** *"Why is C1007 high risk?"*
2. **Explainable Score Breakdown:**
   ```
   AML Score = 92
   +30 unusual transaction size (> 3 std dev)
   +25 high transaction velocity (burst in 1 hr)
   +25 24-hour concentration (> ₹5 Lakh)
   +10 cross-border activity (UAE & SG)
   +2  minor network retries
   ----------------------------------------
    92 HIGH RISK
   ```
3. **Transaction Evidence:** TXN-S001 (₹4.8L inbound) swept via IMPS to CoinBridge P2P (UAE) and CryptoEx (SG) in under **25 minutes**.
4. **Cortex Search Regulatory Match:** Direct citation of **RBI KYC/AML Master Direction Section 4.2: Velocity Anomalies & Mule Accounts** (94% relevance).
5. **Interactive Fraud Flow Graph:** Directed network showing `CP-221 -> C1007 -> CP-223 / CP-224`.
6. **Regulatory Filing:** One-click generation and download of signed 11-section STR PDF with an embedded SHA-256 cryptographic audit stamp.

---

*RiskGuard AI — Engineered for the Hack2Skill × Snowflake CoCo CLI 2026 Challenge.*
