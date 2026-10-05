import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.anomaly_detector import RiskDetectorEngine
from engine.audit_logger import log_event, verify_chain_integrity

print("--- Testing Anomaly Detector ---")
eng = RiskDetectorEngine()
results = eng.run_all_detectors()
print(f"Total signals: {results['total_signals_detected']}")
print(f"Rapid fund AML signals: {len(results['aml_rapid_fund_signals'])}")
print(f"Structuring AML signals: {len(results['aml_structuring_signals'])}")
print(f"Credit signals: {len(results['credit_risk_signals'])}")
print(f"Liquidity signals: {len(results['liquidity_risk_signals'])}")

print("--- Testing Audit Integrity ---")
log_event("TEST_ACTION", "test query", "CUST-10482", "Test logged successfully")
valid, msg = verify_chain_integrity()
print(f"Audit chain valid: {valid} - {msg}")
