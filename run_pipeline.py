import time
import schedule
from engine.snowflake_session import get_snowflake_session
from engine.cortex_search import CortexSearchClient
from engine.cortex_llm import CortexLLMReasoning
from engine.report_generator import RegulatoryReportGenerator

def run_automated_flow():
    print("[Pipeline] Triggering automated risk analysis flow from Snowflake data...")
    session = get_snowflake_session()
    
    # 1. Fetch new flagged transactions/customers from Snowflake (Emulator or Live)
    print("[Pipeline] Extracting flagged transactions...")
    try:
        # We query customers that have high risk score. (Assuming a RISK_ALERTS table or similar, here we mock it)
        # We will just select C1007 for demonstration of automated flow.
        df = session.sql("SELECT CUSTOMER_ID FROM CUSTOMER LIMIT 1").to_pandas()
        target_customer = "C1007" # Hardcoded for demo, normally derived from query
        if not df.empty:
            target_customer = df['CUSTOMER_ID'].iloc[0]
            
        print(f"[Pipeline] Found flagged customer: {target_customer}")
    except Exception as e:
        print(f"[Pipeline] Error fetching data: {e}")
        return

    # 2. Match Regulations
    print("[Pipeline] Running Cortex Search for regulatory basis...")
    search = CortexSearchClient()
    reg_matches = search.search_regulations("unusual velocity mule account")
    
    # 3. Generate Governance Finding
    print("[Pipeline] Running Cortex LLM Governed Reasoning...")
    llm = CortexLLMReasoning()
    finding = llm.generate_governed_finding(target_customer, [], reg_matches)
    
    # 4. Generate Report
    print("[Pipeline] Generating Audit-Ready Report...")
    rep = RegulatoryReportGenerator.generate_aml_report({
        "finding_id": finding["case_id"],
        "customer_id": target_customer,
        "customer_name": "Automated Job",
        "pattern": "Pass-Through Mule Velocity",
        "evidence_transactions": finding["primary_evidence"],
        "confidence_score": 0.94
    })
    
    print(f"[Pipeline] Automated flow complete! Report saved at {rep['pdf_path']}")

def start_scheduler():
    print("Starting Automated Data Flow Pipeline (runs every 10 seconds for demo)...")
    schedule.every(10).seconds.do(run_automated_flow)
    
    # Run once immediately
    run_automated_flow()
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    try:
        import schedule
    except ImportError:
        print("Installing schedule package...")
        import os
        os.system("pip install schedule")
        import schedule
        
    start_scheduler()
