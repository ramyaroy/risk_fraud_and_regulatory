"""
RiskGuard Copilot - Launch Script
Validates environment, verifies database and knowledge base, and launches the Streamlit application.
"""

import os
import sys
import subprocess

def main():
    print("=" * 60)
    print("🛡️  RiskGuard Copilot: Evidence-First Risk & Regulatory AI")
    print("=" * 60)

    # 1. Verify Database
    from engine.db_schema import init_database, DB_PATH
    if not os.path.exists(DB_PATH):
        print("Initializing RiskGuard Database...")
        init_database()
    else:
        print(f"✓ Database verified at: {DB_PATH}")

    # 2. Verify Policy Knowledge Base
    policies_dir = os.path.join(os.path.dirname(__file__), "data", "policies")
    policy_files = [f for f in os.listdir(policies_dir) if f.endswith(".md")]
    print(f"✓ Regulatory Policies indexed: {len(policy_files)} documents ({', '.join(policy_files)})")

    # 3. Verify Cryptographic Ledger
    from engine.audit_logger import verify_chain_integrity
    valid, msg = verify_chain_integrity()
    print(f"✓ Cryptographic Audit Trail: {msg}")

    # 4. Launch Streamlit
    print("\nLaunching Streamlit Web Application on http://localhost:8501 ...")
    cmd = [sys.executable, "-m", "streamlit", "run", "app.py", "--server.headless=true"]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()
