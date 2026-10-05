import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.snowflake_session import get_snowflake_session
from engine.cortex_analyst import CortexAnalystClient
from engine.cortex_search import CortexSearchClient
from engine.cortex_llm import CortexLLMReasoning
from engine.evidence_engine import EvidenceEngine
from engine.report_generator import RegulatoryReportGenerator

print("--- 1. Testing Snowflake Session ---")
session = get_snowflake_session()
df = session.sql("SELECT COUNT(*) as count FROM CUSTOMER").to_pandas()
print(f"Customer records: {df['count'].iloc[0]}")

print("--- 2. Testing Cortex Analyst ---")
analyst = CortexAnalystClient()
res = analyst.execute_analyst_query("Why is C1007 high risk?")
print(f"Generated SQL: {res['generated_sql'][:60]}...")
print(f"Rows retrieved: {len(res['data'])}")

print("--- 3. Testing Cortex Search ---")
search = CortexSearchClient()
reg_matches = search.search_regulations("unusual velocity mule account")
print(f"Regulatory matches: {len(reg_matches)} (Top: {reg_matches[0]['section']} - {reg_matches[0]['relevance_pct']}%)")

print("--- 4. Testing Cortex LLM Governed Reasoning ---")
llm = CortexLLMReasoning()
finding = llm.generate_governed_finding("C1007", [], reg_matches)
print(f"Case ID: {finding['case_id']} | Risk Score: {finding['score']} | Rating: {finding['risk_rating']}")

print("--- 5. Testing Evidence Engine Graph ---")
fig = EvidenceEngine.render_counterparty_graph("C1007")
print(f"Graph annotations: {len(fig.layout.annotations)}")

print("--- 6. Testing Report Generation ---")
rep = RegulatoryReportGenerator.generate_aml_report({
    "finding_id": finding["case_id"],
    "customer_id": "C1007",
    "customer_name": "Rahul S. Sharma",
    "pattern": "Pass-Through Mule Velocity",
    "evidence_transactions": finding["primary_evidence"],
    "confidence_score": 0.94
})
print(f"PDF compiled at: {rep['pdf_path']}")
print(f"SHA-256 Hash: {rep['sha256_hash']}")

print("\n[OK] ALL SNOWFLAKE TEST CHECKS PASSED SUCCESSFULLY!")
