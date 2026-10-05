# 🛡️ Hack2Skill Project Submission Dossier
# Project: RiskGuard Copilot
### **Tagline:** An Evidence-First AI Copilot that turns financial risk signals into explainable, audit-ready regulatory findings.

---

## 1. Executive Summary & Problem Statement

### The Problem in Numbers & Operations
Banking and Non-Banking Financial Company (NBFC) risk teams operate under immense regulatory scrutiny across three critical pillars:
1. **Real-Time Financial Crime & AML:** Tracking rapid fund velocity, mule accounts, smurfing/structuring, and dormant account takeovers under the Prevention of Money Laundering Act (PMLA §12) and FATF standards.
2. **Credit Risk & Stressed Asset Resolution:** Early identification of Special Mention Accounts (SMA-0, SMA-1, SMA-2) and financial covenant deterioration (DSCR, Debt/EBITDA) under the Reserve Bank of India (RBI) Prudential Framework.
3. **Treasury Liquidity Risk & Basel III:** Daily monitoring of High Quality Liquid Assets (HQLA) and 30-Day Stressed Net Cash Outflows to ensure Liquidity Coverage Ratio (LCR $\ge$ 100%) and Net Stable Funding Ratio (NSFR $\ge$ 100%).

### Why Existing Solutions Fail
- **Siloed Databases:** Core transaction ledgers (SQL databases) are isolated from legal policies and regulatory circulars (unstructured text).
- **Labor-Intensive Investigations:** Investigating a single AML or credit alert takes an analyst 3 to 5 business days across multiple spreadsheet exports and manual policy cross-checks.
- **The LLM Hallucination Trap:** Generic conversational LLMs invent statutory citations, confuse circular dates, and lack verifiable provenance. In banking, an unverified LLM answer is an immediate audit penalty.

---

## 2. The Solution & Core Innovation

**RiskGuard Copilot** is designed from first principles as an **evidence-first, governed agentic system**. Rather than answering questions in isolation, RiskGuard enforces an unbroken, deterministic chain:

$$\mathbf{Signal} \longrightarrow \mathbf{Evidence} \longrightarrow \mathbf{Detected\ Pattern} \longrightarrow \mathbf{Policy / Regulation} \longrightarrow \mathbf{Finding} \longrightarrow \mathbf{Audit\ Report}$$

### The Three Core Innovations
1. **Dual-Path Hybrid RAG:** Avoids the fatal mistake of putting tabular transactions into vector embeddings. Instead, it routes structured entity/metric queries through **Parameterized SQL** and routes regulatory circulars through **BM25 + Dense TF-IDF semantic retrieval**, fusing both at the reasoning layer.
2. **Interactive Evidence Graph:** Every statement produced is linked to concrete nodes: Transaction IDs, Account numbers, Customer profiles, Anomaly scores, and exact Regulatory Sections (e.g. RBI Master Direction §4.2, PMLA §12).
3. **Cryptographic Provenance Ledger:** Every query, detection, and filing is committed to an append-only SHA-256 blockchain-style ledger, guaranteeing non-repudiation for regulatory examiners.

---

## 3. End-to-End System Architecture

```
                ┌──────────────────────────────────────────────┐
                │          Business / Compliance User          │
                │          Natural-language question           │
                └──────────────────────┬───────────────────────┘
                                       ↓
                ┌──────────────────────────────────────────────┐
                │     Query Understanding & Intent Detection   │
                └──────────────────────┬───────────────────────┘
                                       ↓
        ┌──────────────────────────────────────────────────────────────┐
        │             Dual-Path Hybrid Retrieval Layer                 │
        │                                                              │
        │   Structured Path (SQL):           Unstructured Path (RAG):  │
        │   • Transactions (Amounts, Times)  • RBI Master Directions   │
        │   • Accounts & Declared Turnover   • PMLA 2002 §12 Rules     │
        │   • Credit Facilities & DPD        • Basel III BCBS 238      │
        │   • Treasury Daily LCR Ratios      • FinCEN & FATF Red Flags │
        │               ↓                                ↓             │
        │        Parameterized SQL             BM25 + Dense TF-IDF     │
        └──────────────────────┬─────────────────────────┬─────────────┘
                               └───────────┬─────────────┘
                                           ↓
        ┌──────────────────────────────────────────────────────────────┐
        │               Risk & Fraud Detection Engine                  │
        │                                                              │
        │   • Isolation Forest (ML Unsupervised Outlier Scorer)        │
        │   • AML Velocity Rule: Inbound-Outbound Pass-Through Mules   │
        │   • Structuring Rule: Multi-Branch Cash Smurfing (< ₹10L)    │
        │   • Credit EWS Rule: SMA Classification & DSCR Deterioration │
        │   • Liquidity Rule: Basel III 30-Day LCR Stress Monitoring   │
        └──────────────────────────────┬───────────────────────────────┘
                                       ↓
        ┌──────────────────────────────────────────────────────────────┐
        │               Interactive Evidence Graph Engine              │
        │   Signal → Evidence → Entity → Pattern → Rule → Report       │
        └──────────────────────────────┬───────────────────────────────┘
                                       ↓
        ┌──────────────────────────────────────────────────────────────┐
        │              Governed LLM Reasoning & Guardrails             │
        │   • Anti-Hallucination: If No Evidence → Explicit Refusal    │
        │   • Attribution Mandate: Explicit Txn IDs & Section Titles   │
        │   • Verifiable Confidence Scoring (0.0 to 1.0)               │
        └──────────────────────────────┬───────────────────────────────┘
                                       ↓
        ┌──────────────────────────────────────────────────────────────┐
        │          Regulatory Reporting & Cryptographic Ledger         │
        │   • Form STR / SAR Regulatory Filing (FIU-IND / FinCEN)      │
        │   • Credit Risk Early Warning Memorandum (RBI Prudential)    │
        │   • Basel III LCR Supervisory Notice (BCBS 238)              │
        │   • High-Resolution Signed PDF with SHA-256 Non-Repudiation  │
        │   • Cryptographic Append-Only Blockchain-Style Audit Ledger  │
        └──────────────────────────────────────────────────────────────┘
```

---

## 4. Technical Stack & Component Breakdown

| Layer | Technology | Engineering Rationale |
| :--- | :--- | :--- |
| **User Interface** | Streamlit + Custom Dark Glassmorphism CSS | Interactive compliance workbench, real-time filters, instant PDF download. |
| **Structured Store** | SQLite / PostgreSQL Schema | Optimized relational schema with Foreign Key integrity across 7 normalized tables. |
| **Unstructured Search** | BM25 (`rank-bm25`) + TF-IDF Vector Space | High-precision keyword matching on statutory clauses + semantic dense ranking. |
| **Machine Learning** | Scikit-Learn `IsolationForest` | Unsupervised anomaly detection on transaction velocity, amount-to-profile ratios, and time-deltas. |
| **Graph Visuals** | NetworkX + Plotly Interactive DiGraph | Dynamic spring-layout DAGs showing full provenance lineage with interactive hover cards. |
| **Report Engine** | ReportLab 5.0 (Python) | Generates official PDF filings matching FIU-IND STR format with embedded SHA-256 integrity stamp. |
| **Provenance Chain** | SHA-256 Cryptographic Hash Chain | Append-only ledger linking $H_n = \text{SHA256}(H_{n-1} + \text{Payload})$ for non-repudiation. |

---

## 5. Dataset Design & Ground Truth Scenarios

The system includes a pre-seeded, high-fidelity relational database (`data/riskguard.db`) and indexed policy repository (`data/policies/`):

1. **AML Scenario 1 (Pass-Through Mule Account):**
   - **Customer:** `CUST-10482` (Rahul S. Sharma / QuickTrade).
   - **Data:** 17 transactions across 7 days totaling ₹42.8 Lakh against a declared monthly turnover of ₹5.00 Lakh (8.56x surge). Inbound RTGS credits are drained within 18 to 45 minutes to P2P/crypto gateways.
   - **Violation:** RBI Master Direction on KYC/AML Section 4.2 & PMLA Section 12.
2. **AML Scenario 2 (Cash Structuring / Smurfing):**
   - **Customer:** `CUST-10102` (Apex Horizon Global Ltd).
   - **Data:** 6 cash deposits between ₹9,20,000 and ₹9,90,000 across 4 branch counters within 4 days.
   - **Violation:** Intentionally structured below statutory ₹10,00,000 CTR ceiling (PMLA Rule §4.1.2).
3. **Credit Risk Scenario (Stressed Borrower EWS):**
   - **Customer:** `CUST-10891` (BlueOcean Infrastructure Pvt Ltd), Loan `LN-8802` (₹41.2 Cr outstanding).
   - **Data:** 48 Days Past Due (**SMA-1**), DSCR collapsed to **0.92x** (vs 1.25x covenant), Debt/EBITDA spiked to **6.8x**.
   - **Violation:** RBI Prudential Framework for Stressed Assets (2019) Section 1.1 & 2.3.
4. **Liquidity Risk Scenario (Basel III LCR Breach):**
   - **Treasury Position:** Sudden ₹650 Cr institutional deposit run-off causes daily LCR to fall from 112.5% to **98.47%**.
   - **Violation:** BCBS 238 / RBI Master Circular Section 2.1 (Statutory breach of mandatory 100% floor).

---

## 6. Governed Agentic Guardrails

- **Zero Speculation Guarantee:** If a user queries an entity without corresponding transactions or indexed policy clauses, the agent halts and reports `"No verified evidence found"`.
- **Attribution Enforcement:** No finding can be finalized without at least one Transaction ID, Account ID, and Regulatory Section citation.
- **Audit Verification:** Auditors can click `Verify Ledger Integrity` in the UI to dynamically recalculate hashes across all blocks and prove no records have been altered.
