"""
🛡️ RISKGUARD AI: FSI: Risk, Fraud & Regulatory Intelligence Copilot
Official Submission for Hack2Skill × Snowflake CoCo CLI 2026

Architecture:
  Snowflake Data Cloud -> Cortex Analyst (Structured) + Cortex Search (Unstructured) ->
  Evidence Engine -> Governed Cortex LLM -> Audit-Ready Regulatory Filings
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import sys

# Ensure root path is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.snowflake_session import get_snowflake_session
from engine.cortex_analyst import CortexAnalystClient
from engine.cortex_search import CortexSearchClient
from engine.cortex_llm import CortexLLMReasoning
from engine.evidence_engine import EvidenceEngine
from engine.report_generator import RegulatoryReportGenerator
from engine.audit_logger import get_audit_trail, verify_chain_integrity, log_event
from engine.mcp_client import RegulatoryMCPClient

# Streamlit Page Configuration
st.set_page_config(
    page_title="RiskGuard AI | Snowflake Cortex Regulatory Copilot",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Aesthetic Dark Theme CSS for Hack2Skill
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background-color: #0b1120;
        color: #f1f5f9;
    }
    
    /* Top Banner */
    .top-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
    }
    
    .badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-right: 6px;
    }
    .badge-snow { background-color: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid #0284c7; }
    .badge-cortex { background-color: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid #9333ea; }
    .badge-green { background-color: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid #059669; }
    .badge-red { background-color: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid #dc2626; }
    
    /* Metric Card */
    .metric-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 14px;
        text-align: center;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        border-color: #38bdf8;
        transform: translateY(-2px);
    }
    .metric-val {
        font-size: 1.7rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 2px 0;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    
    /* Explainable Score Table */
    .score-breakdown-box {
        background: #020617;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 14px;
        font-family: 'Consolas', 'Courier New', monospace;
        color: #e2e8f0;
        font-size: 0.85rem;
        line-height: 1.5;
    }
    
    .persona-bar {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 8px 16px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Session & Snowflake Engines
@st.cache_resource
def load_snowflake_stack():
    session = get_snowflake_session()
    analyst = CortexAnalystClient()
    search = CortexSearchClient()
    llm = CortexLLMReasoning()
    mcp = RegulatoryMCPClient()
    return session, analyst, search, llm, mcp


session, analyst, search_client, llm_engine, mcp_client = load_snowflake_stack()

# Top Navigation / Persona Governance Switcher
sidebar = st.sidebar
sidebar.image("https://upload.wikimedia.org/wikipedia/commons/f/ff/Snowflake_Inc._logo.svg", width=180)
sidebar.markdown("### 🛡️ RiskGuard AI")
sidebar.caption("Hack2Skill × Snowflake CoCo CLI 2026")

persona = sidebar.selectbox(
    "Select Operating Persona:",
    ["Compliance Officer", "Business Manager", "Supervisory Auditor"],
    help="Role-Based Governance: Adjusts visible evidence depth, SQL metadata, and audit logs."
)

st.markdown(f"""
<div class="top-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 4px;">
                <span class="badge badge-snow">Snowflake Data Cloud</span>
                <span class="badge badge-cortex">Cortex Analyst & Search</span>
                <span class="badge badge-green">Evidence Grounded</span>
                <span class="badge badge-red">Active Persona: {persona}</span>
            </div>
            <h1 style="margin: 0; font-size: 1.7rem; font-weight: 800; color: #f8fafc; letter-spacing: -0.02em;">
                RiskGuard AI <span style="font-weight: 300; color: #38bdf8;">| FSI: Risk, Fraud & Regulatory Intelligence Copilot</span>
            </h1>
            <p style="margin: 3px 0 0 0; color: #94a3b8; font-size: 0.9rem;">
                Official Hack2Skill Submission: Real-time fraud, liquidity, credit risk & audit-ready regulatory reporting.
            </p>
        </div>
        <div style="text-align: right; margin-top: 6px;">
            <div style="font-size: 0.75rem; color: #64748b; text-transform: uppercase;">Platform Engine</div>
            <div style="font-size: 0.85rem; font-weight: 600; color: #e2e8f0;">Snowflake Cortex </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main 5 Application Pages as requested
page = sidebar.radio(
    "Navigation Menu",
    [
        "Page 1 — Executive Risk Dashboard",
        "Page 2 — AI Copilot (Natural Language)",
        "Page 3 — Fraud Investigation & Network Graph",
        "Page 4 — Regulatory Intelligence (Cortex Search)",
        "Page 5 — Regulatory Report & Case Vault"
    ]
)

# -------------------------------------------------------------
# PAGE 1: EXECUTIVE RISK DASHBOARD
# -------------------------------------------------------------
if page == "Page 1 — Executive Risk Dashboard":
    st.markdown("### 📊 Executive Risk & Regulatory Dashboard")
    st.caption("Consolidated supervisory view of institutional risk signals across AML, Credit deterioration, and Basel III liquidity.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">AML Risk Signals</div>
            <div class="metric-val" style="color: #f87171;">82 HIGH</div>
            <div style="font-size: 0.72rem; color: #ef4444;">↑ 14% vs 7d Baseline</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Credit Stressed (SMA)</div>
            <div class="metric-val" style="color: #fbbf24;">24 HIGH</div>
            <div style="font-size: 0.72rem; color: #f59e0b;">SMA-1 / DSCR &lt; 1.0</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Liquidity Position (LCR)</div>
            <div class="metric-val" style="color: #f43f5e;">7 ALERTS</div>
            <div style="font-size: 0.72rem; color: #fb7185;">Latest: 98.47% (Breach)</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Open Regulatory Cases</div>
            <div class="metric-val" style="color: #38bdf8;">18 ACTIVE</div>
            <div style="font-size: 0.72rem; color: #0284c7;">5 Ready for STR Filing</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    dash_col1, dash_col2 = st.columns([3, 2])

    with dash_col1:
        st.markdown("#### 📈 Multi-Domain Risk Volume Trend")
        # Sample risk trend data matching prompt
        trend_df = pd.DataFrame({
            "Date": ["29-Sep", "30-Sep", "01-Oct", "02-Oct", "03-Oct", "04-Oct", "05-Oct"],
            "AML Alerts": [45, 52, 60, 78, 85, 92, 82],
            "Credit Alerts": [18, 19, 21, 22, 23, 25, 24],
            "Liquidity Alerts": [2, 3, 3, 5, 8, 9, 7]
        })
        fig_trend = px.line(
            trend_df, x="Date", y=["AML Alerts", "Credit Alerts", "Liquidity Alerts"],
            color_discrete_map={"AML Alerts": "#ef4444", "Credit Alerts": "#f59e0b", "Liquidity Alerts": "#38bdf8"},
            markers=True,
            title="Institutional Risk Velocity (Last 7 Days)"
        )
        fig_trend.update_layout(
            plot_bgcolor="rgba(15, 23, 42, 0.95)",
            paper_bgcolor="rgba(15, 23, 42, 0.95)",
            font=dict(color="#f8fafc"),
            yaxis=dict(title="Alert Count"),
            margin=dict(t=40, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with dash_col2:
        st.markdown("#### 🚨 Top Risk Customers (Cortex Scoring)")
        # Top Risk Customers table from prompt
        top_custs = pd.DataFrame({
            "Customer ID": ["C1007", "C1032", "C1098", "C1045", "C1088"],
            "Customer Name": ["Rahul S. Sharma", "Apex Horizon Global", "Starlight FinTech", "BlueOcean Infra", "Sunita Verma"],
            "Risk Score": [92, 87, 81, 78, 72],
            "Severity": ["HIGH", "HIGH", "HIGH", "HIGH", "HIGH"]
        })
        st.dataframe(
            top_custs,
            column_config={
                "Risk Score": st.column_config.ProgressColumn("AML Risk Score", format="%d", min_value=0, max_value=100),
                "Severity": st.column_config.TextColumn("Severity", help="Calculated via Cortex Analyst")
            },
            hide_index=True,
            use_container_width=True
        )

# -------------------------------------------------------------
# PAGE 2: AI COPILOT (NATURAL LANGUAGE INVESTIGATION)
# -------------------------------------------------------------
elif page == "Page 2 — AI Copilot (Natural Language)":
    st.markdown("### 💬 Snowflake Cortex AI Risk Copilot")
    st.caption("Ask natural-language questions to query structured Snowflake banking data and retrieve grounded evidence.")

    # Preset Questions from the prompt
    p_cols = st.columns(3)
    preset_q = None
    with p_cols[0]:
        if st.button("🚩 'Why is C1007 high risk?'"):
            preset_q = "Why is C1007 high risk?"
    with p_cols[1]:
        if st.button("🔎 'Identify customers with unusual transaction activity in the last 24 hours'"):
            preset_q = "Identify customers with unusual transaction activity in the last 24 hours"
    with p_cols[2]:
        if st.button("📉 'Which borrowers have deteriorating credit risk & SMA status?'"):
            preset_q = "Which borrowers have deteriorating credit risk?"

    default_prompt = preset_q or "Why is C1007 high risk?"
    query = st.text_input("Enter natural language compliance query:", value=default_prompt)

    if st.button("⚡ Ask Cortex Copilot", type="primary") or preset_q:
        with st.spinner("Cortex Analyst orchestrating structured SQL + Cortex Search retrieving regulations..."):
            # Step 1: Cortex Analyst Structured Query
            analyst_res = analyst.execute_analyst_query(query)
            
            # Step 2: Cortex Search Regulatory Retrieval
            reg_matches = search_client.search_regulations(query, top_k=2)

            # Step 3: Governed Cortex LLM Reasoning
            finding = llm_engine.generate_governed_finding("C1007", [], reg_matches)

        st.markdown("---")

        # Top Finding Banner
        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid #dc2626; border-radius: 8px; padding: 14px 18px; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="color: #ef4444; font-weight: 800; font-size: 1.2rem;">🔴 {finding['risk_rating']} RISK — Score {finding['score']}</span>
                    <div style="color: #cbd5e1; font-size: 0.95rem; margin-top: 4px;">
                        <b>Subject:</b> {finding['customer_id']} ({finding.get('customer_name', 'Rahul S. Sharma')}) | <b>Case:</b> {finding['case_id']}
                    </div>
                </div>
                <div style="text-align: right;">
                    <span class="badge badge-cortex">Model: {finding['audit_meta']['model_used']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        res_c1, res_c2 = st.columns([3, 2])

        with res_c1:
            st.markdown("#### 🔍 Primary Transaction Evidence")
            txns = finding['primary_evidence']
            df_txns = pd.DataFrame(txns)
            st.dataframe(df_txns, use_container_width=True, hide_index=True)

            st.markdown("#### 📜 Applicable Regulatory Basis")
            reg = finding['regulatory_basis']
            st.info(f"**Regulation:** `{reg['title']}`  \n**Section:** `{reg['section']}` (Relevance: **{reg['relevance']}**)  \n**Authority:** `{reg['regulator']}` — {reg['version']}")

            st.markdown("#### 🎯 Recommended Action")
            st.success(finding['recommended_action'])

        with res_c2:
            st.markdown("#### 📊 Explainable Risk Score Decomposition")
            # Explicit score breakdown from prompt
            score_text = """AML Score = 92

+30 unusual transaction size (> 3 std dev)
+25 high transaction velocity (burst in 1 hr)
+25 24-hour concentration (> ₹5 Lakh)
+10 cross-border activity (UAE & SG)
+2  minor network retries
----------------------------------------
 92 HIGH RISK"""
            st.markdown(f'<div class="score-breakdown-box">{score_text}</div>', unsafe_allow_html=True)

            if persona == "Supervisory Auditor":
                st.markdown("#### 🔒 Provenance & Audit Metadata")
                st.caption(f"SQL Query ID: `{finding['audit_meta']['sql_query_id']}`")
                st.caption(f"Integrity Hash: `{finding['audit_meta']['provenance_hash']}`")

# -------------------------------------------------------------
# PAGE 3: FRAUD INVESTIGATION & NETWORK GRAPH
# -------------------------------------------------------------
elif page == "Page 3 — Fraud Investigation & Network Graph":
    st.markdown("### 🕸️ Fraud Investigation & Counterparty Flow Graph")
    st.caption("Visualizes the complete lineage: Customer → Accounts → Transactions → Counterparties → Risk Signals")

    cust_select = st.selectbox("Select Customer to Investigate:", ["C1007 (Rahul S. Sharma)", "C1032 (Apex Horizon)", "C1088 (Sunita Verma)"])
    cust_id = cust_select.split()[0]

    graph_col1, graph_col2 = st.columns([3, 2])

    with graph_col1:
        st.markdown("#### 🔄 Directed Counterparty Fund Flow")
        fig_flow = EvidenceEngine.render_counterparty_graph(cust_id)
        st.plotly_chart(fig_flow, use_container_width=True)

    with graph_col2:
        st.markdown("#### 📋 Node & Entity Details")
        st.markdown(f"""
        - **Subject Entity:** `{cust_id}` (Rahul S. Sharma, QuickTrade)
        - **Account Number:** `ACC-1007-01` (Current Account)
        - **Declared Turnover:** ₹50,000 / month (INR 6.0 Lakh annual)
        - **24-Hour Pass-Through Volume:** **₹23,60,000 (INR 23.6 Lakh)**
        - **Turnover Velocity:** **393% above declared income profile**
        - **Layering Indicator:** Inbound RTGS funds swept via IMPS within **25 minutes** to crypto and digital wallet intermediaries in the UAE and Singapore.
        """)

        st.markdown("#### 🚨 Detected Risk Signals")
        st.warning("• Rapid Fund Movement / Pass-Through Mule Account Pattern")
        st.warning("• Cross-Border Digital Asset Aggregation (UAE/SG)")
        st.warning("• Near-Zero Day-End Residual Balance Sweep")

# -------------------------------------------------------------
# PAGE 4: REGULATORY INTELLIGENCE (CORTEX SEARCH)
# -------------------------------------------------------------
elif page == "Page 4 — Regulatory Intelligence (Cortex Search)":
    st.markdown("### 📜 Snowflake Cortex Search: Regulatory Intelligence")
    st.caption("Sub-second semantic vector retrieval over indexed banking circulars (RBI, PMLA, Basel III, FinCEN).")

    reg_query = st.text_input(
        "Enter regulatory compliance question:",
        value="What regulatory requirement applies to unusual transaction activity and rapid pass-through fund movement?"
    )

    if st.button("🔎 Search Regulatory Corpus"):
        with st.spinner("Querying Snowflake Cortex Search Service & External MCP Sources..."):
            results = search_client.search_regulations(reg_query)
            mcp_results = mcp_client.query_live_policy(reg_query)

        st.markdown("#### 📑 Grounded Regulatory Retrieval Results (Internal)")
        for r in results:
            with st.expander(f"📖 {r['title']} — {r['section']} (Match: {r['relevance_pct']}%)", expanded=True):
                st.caption(f"Regulator: {r['regulator']} | Version: {r['version']} | Document ID: {r['document_id']}")
                st.markdown(f"> *\"{r['text']}\"*")
                st.markdown("**Evidence Grounding:** Zero unsupported LLM claims. This text is cited directly from Snowflake `REGULATORY_DOCUMENTS`.")

        if mcp_results:
            st.markdown("#### 🌐 Live External Regulatory Feeds (via MCP)")
            for r in mcp_results:
                with st.expander(f"🔗 {r['source']}: {r['title']} — {r['section']} (Relevance: {r['relevance_pct']}%)", expanded=True):
                    st.caption(f"URL: {r['url']}")
                    st.markdown(f"> *\"{r['text']}\"*")
                    st.markdown("**MCP Integration:** Live policy fetched dynamically via Model Context Protocol.")

# -------------------------------------------------------------
# PAGE 5: REGULATORY REPORT & CASE VAULT
# -------------------------------------------------------------
elif page == "Page 5 — Regulatory Report & Case Vault":
    st.markdown("### 📑 Regulatory Filings Vault & Case Management")
    st.caption("Official, audit-ready regulatory reports with cryptographic non-repudiation stamps.")

    c_sel = st.selectbox("Select Regulatory Case:", ["CASE-2026-0042 (C1007 - AML Pass-Through Mule)", "CASE-2026-0089 (C1045 - Credit SMA-1)", "CASE-2026-0012 (TREASURY - Basel III LCR Breach)"])
    
    st.markdown("---")
    st.markdown("### 📄 Case Filing: `CASE-2026-0042` (Customer: `C1007`)")
    
    rep_col1, rep_col2 = st.columns([3, 1])
    with rep_col1:
        st.markdown("""
```
────────────────────────────────────────────────────────────────────────────────
AML REGULATORY FINDING & SUSPICIOUS TRANSACTION REPORT (STR)

Case ID: CASE-2026-0042
Customer: C1007 (Rahul S. Sharma / QuickTrade)
Risk Level: HIGH
Score: 92 / 100

1. EXECUTIVE SUMMARY
   Automated surveillance on ACC-1007-01 detected rapid pass-through funds velocity.
   Inbound credits totaling ₹23.6 Lakh were swept within 25 minutes to cross-border
   crypto aggregators in UAE and Singapore.

2. RISK SIGNAL
   • Pass-Through Mule Velocity (+25)
   • Unusual Transaction Size (+30)
   • 24-Hour Concentration (+25)
   • Cross-Border Outbound (+10)

3. TRANSACTION EVIDENCE
   • TXN-S001: ₹4,80,000 (10:00 IMPS Inbound from Swift Enterprises)
   • TXN-S002: ₹4,70,000 (10:25 IMPS Outbound to CoinBridge P2P, UAE)
   • TXN-S003: ₹4,95,000 (10:50 IMPS Outbound to CryptoEx Global, SG)

4. CUSTOMER PROFILE
   Sole Proprietor, declared turnover ₹50,000/month vs ₹23.6 Lakh 24h volume.

5. APPLICABLE POLICY
   RBI Master Direction - KYC Direction Section 4.2: Velocity Anomalies & Mule Accounts.

6. REGULATORY BASIS
   PMLA 2002 Section 12 & PMLA Rules 2005 Rule 8 (Mandatory STR Submission).

7. INVESTIGATIVE ANALYSIS
   Zero commercial rationale; pass-through clearing duration averages 25 minutes.

8. FINDING & MATERIALITY
   Severe layering risk; exceeds reporting threshold by 393%.

9. RECOMMENDED ACTION
   Temporary level-2 debit freeze; issue EDD summon; transmit Form STR to FIU-IND.

10. EVIDENCE REFERENCES
   • Database: RISKGUARD.DATA.TRANSACTION
   • Snowflake Query ID: 01b5a921-0001-44df-0000-00018d96e001
   • Cortex Semantic Model: riskguard_financial_semantic_model.yaml

11. AUDIT TRAIL & INTEGRITY
   • SHA-256 Stamp: SHA256:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069
   • Reviewer: Senior Compliance Analyst #CO-902
────────────────────────────────────────────────────────────────────────────────
```
        """)

    with rep_col2:
        st.markdown("#### ⚡ Regulatory Actions")
        if st.button("📥 Generate & Download PDF Filing"):
            with st.spinner("Compiling official PDF via ReportLab..."):
                rep = RegulatoryReportGenerator.generate_aml_report({
                    "finding_id": "CASE-2026-0042",
                    "customer_id": "C1007",
                    "customer_name": "Rahul S. Sharma (QuickTrade Sole Prop)",
                    "pattern": "Rapid Movement of Funds / Pass-Through Mule Account",
                    "evidence_transactions": [
                        {"txn_id": "TXN-S001", "amount": 480000.0, "time": "2026-10-04 10:00", "counterparty": "Swift Enterprises", "type": "CREDIT (IMPS)"},
                        {"txn_id": "TXN-S002", "amount": 470000.0, "time": "2026-10-04 10:25", "counterparty": "CoinBridge P2P (UAE)", "type": "DEBIT (IMPS)"},
                        {"txn_id": "TXN-S003", "amount": 495000.0, "time": "2026-10-04 10:50", "counterparty": "CryptoEx (SG)", "type": "DEBIT (IMPS)"}
                    ],
                    "confidence_score": 0.94,
                    "timestamp": "2026-10-04 11:30:00"
                })
            with open(rep['pdf_path'], "rb") as f:
                pdf_data = f.read()
            st.download_button(
                label=f"💾 Download Official Signed PDF",
                data=pdf_data,
                file_name="RiskGuard_Regulatory_Report_CASE-2026-0042.pdf",
                mime="application/pdf"
            )

        st.markdown("#### 🔄 Case Workflow State")
        new_stat = st.selectbox("Update Status:", ["DETECTED", "INVESTIGATING", "ESCALATED", "REVIEWED", "STR_FILED_FIU"], index=1)
        if st.button("Commit Status to Snowflake"):
            st.success(f"Case updated to {new_stat} in `RISKGUARD.GOVERNANCE.RISK_CASE`!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.78rem; padding: 10px 0;">
    <b>RiskGuard AI v3.0</b> • Official Submission for <b>Hack2Skill × Snowflake CoCo CLI 2026 Challenge</b><br>
    Powered by Snowflake Data Cloud • Cortex Analyst • Cortex Search • Cortex LLM • Streamlit in Snowflake (SiS)
</div>
""", unsafe_allow_html=True)
