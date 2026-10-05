"""
RiskGuard Copilot - Database Schema & Data Seeder
Populates SQLite database with high-fidelity banking transactions, customer profiles,
credit facilities, liquidity positions, and audit records.
"""

import sqlite3
import os
import json
import hashlib
from datetime import datetime, timedelta

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DB_DIR, "riskguard.db")


def get_db_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Drop existing tables to allow clean schema refresh
    cur.execute("DROP TABLE IF EXISTS audit_trail")
    cur.execute("DROP TABLE IF EXISTS risk_findings")
    cur.execute("DROP TABLE IF EXISTS liquidity_positions")
    cur.execute("DROP TABLE IF EXISTS credit_facilities")
    cur.execute("DROP TABLE IF EXISTS transactions")
    cur.execute("DROP TABLE IF EXISTS accounts")
    cur.execute("DROP TABLE IF EXISTS customers")

    # 1. Customers Table
    cur.execute("""
    CREATE TABLE customers (
        customer_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        customer_type TEXT NOT NULL,
        risk_rating TEXT NOT NULL,
        kyc_status TEXT NOT NULL,
        declared_monthly_turnover REAL NOT NULL,
        pan_tax_id TEXT,
        city TEXT,
        country TEXT DEFAULT 'India',
        created_at TEXT NOT NULL
    )
    """)

    # 2. Accounts Table
    cur.execute("""
    CREATE TABLE accounts (
        account_id TEXT PRIMARY KEY,
        customer_id TEXT NOT NULL,
        account_type TEXT NOT NULL,
        currency TEXT DEFAULT 'INR',
        current_balance REAL NOT NULL,
        status TEXT NOT NULL,
        opened_date TEXT NOT NULL,
        last_activity_date TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
    """)

    # 3. Transactions Table
    cur.execute("""
    CREATE TABLE transactions (
        txn_id TEXT PRIMARY KEY,
        account_id TEXT NOT NULL,
        customer_id TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        amount REAL NOT NULL,
        txn_type TEXT NOT NULL, -- 'CREDIT' or 'DEBIT'
        channel TEXT NOT NULL,  -- 'IMPS', 'RTGS', 'NEFT', 'CASH', 'WIRE', 'UPI'
        counterparty_name TEXT,
        counterparty_account TEXT,
        counterparty_bank TEXT,
        narration TEXT,
        is_flagged INTEGER DEFAULT 0,
        flag_reason TEXT,
        FOREIGN KEY (account_id) REFERENCES accounts(account_id),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
    """)

    # 4. Credit Facilities Table
    cur.execute("""
    CREATE TABLE credit_facilities (
        facility_id TEXT PRIMARY KEY,
        customer_id TEXT NOT NULL,
        facility_type TEXT NOT NULL,
        sanctioned_amount REAL NOT NULL,
        outstanding_amount REAL NOT NULL,
        dpd INTEGER NOT NULL, -- Days Past Due
        asset_classification TEXT NOT NULL, -- 'Standard', 'SMA-0', 'SMA-1', 'SMA-2', 'NPA'
        dscr REAL NOT NULL, -- Debt Service Coverage Ratio
        debt_to_ebitda REAL NOT NULL,
        current_ratio REAL NOT NULL,
        covenant_status TEXT NOT NULL, -- 'COMPLIANT' or 'BREACHED'
        interest_rate REAL NOT NULL,
        last_financial_review TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
    """)

    # 5. Liquidity Positions (Treasury / Basel III)
    cur.execute("""
    CREATE TABLE liquidity_positions (
        report_date TEXT PRIMARY KEY,
        hqla_level_1 REAL NOT NULL,
        hqla_level_2a REAL NOT NULL,
        hqla_level_2b REAL NOT NULL,
        total_hqla REAL NOT NULL,
        expected_30d_cash_outflows REAL NOT NULL,
        expected_30d_cash_inflows REAL NOT NULL,
        net_cash_outflows REAL NOT NULL,
        lcr_percentage REAL NOT NULL,
        nsfr_percentage REAL NOT NULL,
        supervisory_status TEXT NOT NULL, -- 'NORMAL', 'WARNING_ALERT', 'CRITICAL_BREACH'
        notes TEXT
    )
    """)

    # 6. Risk Findings (Governed Findings)
    cur.execute("""
    CREATE TABLE risk_findings (
        finding_id TEXT PRIMARY KEY,
        domain TEXT NOT NULL, -- 'AML', 'CREDIT', 'LIQUIDITY'
        entity_id TEXT NOT NULL,
        risk_level TEXT NOT NULL, -- 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
        pattern_detected TEXT NOT NULL,
        confidence_score REAL NOT NULL,
        signal_summary TEXT NOT NULL,
        evidence_json TEXT NOT NULL,
        policy_citation TEXT NOT NULL,
        regulatory_basis TEXT NOT NULL,
        recommended_action TEXT NOT NULL,
        status TEXT DEFAULT 'OPEN', -- 'OPEN', 'ESCALATED', 'STR_FILED', 'RESOLVED'
        created_at TEXT NOT NULL
    )
    """)

    # 7. Immutable Audit Trail
    cur.execute("""
    CREATE TABLE audit_trail (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        user_action TEXT NOT NULL,
        query_text TEXT,
        target_entity TEXT,
        result_summary TEXT,
        prev_hash TEXT,
        current_hash TEXT NOT NULL
    )
    """)

    conn.commit()
    seed_data(conn)
    conn.close()
    print(f"Database initialized successfully at: {DB_PATH}")


def seed_data(conn):
    cur = conn.cursor()

    # ------------------ SEED CUSTOMERS ------------------
    customers = [
        ("CUST-10482", "Rahul S. Sharma (QuickTrade Sole Prop)", "Retail / MSME", "High", "Verified", 500000.0, "ABFPS8821K", "Mumbai", "India", "2024-03-15"),
        ("CUST-10102", "Apex Horizon Global Ltd", "Corporate", "High", "Verified", 15000000.0, "AAACA1092M", "New Delhi", "India", "2023-01-10"),
        ("CUST-10891", "BlueOcean Infrastructure Pvt Ltd", "Corporate Borrower", "High", "Verified", 85000000.0, "AABCB9912Q", "Bengaluru", "India", "2022-06-20"),
        ("CUST-10255", "Zenith Pharma Logistics", "Corporate", "Low", "Verified", 40000000.0, "AAACZ4421L", "Hyderabad", "India", "2021-11-05"),
        ("CUST-10904", "Sunita Verma", "Retail", "High", "Pending Re-KYC", 100000.0, "BZIPV3109N", "Pune", "India", "2020-05-12"),
        ("CUST-10330", "Titanium FinTech Solutions", "NBFC Partner", "Medium", "Verified", 120000000.0, "AAACT8834E", "Mumbai", "India", "2023-08-14"),
        ("CUST-10771", "Kuber Agro Commodity Traders", "Corporate", "Medium", "Verified", 25000000.0, "AAACK5529P", "Ahmedabad", "India", "2022-09-01")
    ]
    cur.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", customers)

    # ------------------ SEED ACCOUNTS ------------------
    accounts = [
        ("ACC-4401-8291", "CUST-10482", "Current", "INR", 42150.0, "Active", "2024-03-15", "2026-10-05"),
        ("ACC-9921-1028", "CUST-10102", "Current", "INR", 3120500.0, "Active", "2023-01-10", "2026-10-04"),
        ("ACC-5520-4491", "CUST-10891", "Term Loan Escrow", "INR", 1250000.0, "Under Surveillance", "2022-06-20", "2026-10-03"),
        ("ACC-7712-3301", "CUST-10255", "Current", "INR", 8450000.0, "Active", "2021-11-05", "2026-10-05"),
        ("ACC-1109-7722", "CUST-10904", "Savings", "INR", 1875000.0, "Dormant", "2020-05-12", "2026-10-02"),
        ("ACC-8834-5511", "CUST-10330", "Current", "INR", 45000000.0, "Active", "2023-08-14", "2026-10-05"),
        ("ACC-6629-9944", "CUST-10771", "Cash Credit", "INR", 4100000.0, "Active", "2022-09-01", "2026-10-04")
    ]
    cur.executemany("INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?, ?)", accounts)

    # ------------------ SEED TRANSACTIONS ------------------
    transactions = []

    # 1. CUST-10482: 17 rapid pass-through transactions (₹42.8 Lakh total volume, 29 Sep – 05 Oct 2026)
    # Perfectly matches Prompt's Example Output:
    # TXN-98231: ₹8,40,000 (02-Oct-2026 10:42)
    # TXN-98246: ₹7,90,000 (02-Oct-2026 11:17)
    # TXN-98302: ₹8,20,000 (02-Oct-2026 13:05)
    # Plus rapid outbound transfers to digital gateways!
    cust10482_txns = [
        # 29 Sep
        ("TXN-98101", "ACC-4401-8291", "CUST-10482", "2026-09-29 09:15:00", 250000.0, "CREDIT", "IMPS", "A.K. Traders", "ACC-0912-3341", "HDFC Bank", "Invoice payment", 1, "High velocity inbound"),
        ("TXN-98105", "ACC-4401-8291", "CUST-10482", "2026-09-29 09:38:00", 245000.0, "DEBIT", "UPI", "PayFast Gateway", "UPI-GATE-9912", "ICICI Bank", "Digital wallet topup", 1, "Immediate pass-through fund sweep"),
        # 30 Sep
        ("TXN-98144", "ACC-4401-8291", "CUST-10482", "2026-09-30 14:10:00", 350000.0, "CREDIT", "NEFT", "Global Retail Hub", "ACC-4412-8812", "Axis Bank", "Advance settlement", 1, "Unusual credit burst"),
        ("TXN-98150", "ACC-4401-8291", "CUST-10482", "2026-09-30 14:32:00", 345000.0, "DEBIT", "IMPS", "CryptoEx Merchant", "ACC-7711-2299", "Yes Bank", "P2P clearing settlement", 1, "Rapid outbound transfer"),
        # 01 Oct
        ("TXN-98192", "ACC-4401-8291", "CUST-10482", "2026-10-01 11:20:00", 420000.0, "CREDIT", "RTGS", "Delta Logistics", "ACC-8812-3311", "SBI", "Freight payment", 1, "Turnover mismatch"),
        ("TXN-98198", "ACC-4401-8291", "CUST-10482", "2026-10-01 11:45:00", 415000.0, "DEBIT", "IMPS", "Zenith P2P Pool", "ACC-9921-4400", "Kotak Bank", "Merchant transfer", 1, "Pass-through liquidation"),
        # 02 Oct (Exact prompt transactions!)
        ("TXN-98231", "ACC-4401-8291", "CUST-10482", "2026-10-02 10:42:00", 840000.0, "CREDIT", "RTGS", "Swift Enterprises", "ACC-1122-3344", "Canara Bank", "Commercial remittance", 1, "Velocity anomaly / Large pass-through credit"),
        ("TXN-98239", "ACC-4401-8291", "CUST-10482", "2026-10-02 11:05:00", 830000.0, "DEBIT", "IMPS", "CoinBridge P2P Ltd", "ACC-5566-7788", "IDFC First", "Digital clearing", 1, "Immediate outbound transfer (23 mins)"),
        ("TXN-98246", "ACC-4401-8291", "CUST-10482", "2026-10-02 11:17:00", 790000.0, "CREDIT", "RTGS", "Eastern Global Ventures", "ACC-9988-1122", "Punjab National", "Service fee", 1, "Rapid succession inbound credit"),
        ("TXN-98255", "ACC-4401-8291", "CUST-10482", "2026-10-02 11:48:00", 780000.0, "DEBIT", "IMPS", "PayLink Aggregator", "ACC-2233-4455", "IndusInd Bank", "Settlement voucher", 1, "Near-zero residual balance sweep"),
        ("TXN-98302", "ACC-4401-8291", "CUST-10482", "2026-10-02 13:05:00", 820000.0, "CREDIT", "RTGS", "Nexus Imports", "ACC-3344-5566", "Union Bank", "Trade advance", 1, "High velocity multi-burst"),
        ("TXN-98315", "ACC-4401-8291", "CUST-10482", "2026-10-02 13:40:00", 815000.0, "DEBIT", "IMPS", "CryptoEx Merchant", "ACC-7711-2299", "Yes Bank", "P2P instant cash-out", 1, "Rapid outbound transfer (35 mins)"),
        # 03 Oct
        ("TXN-98380", "ACC-4401-8291", "CUST-10482", "2026-10-03 16:15:00", 610000.0, "CREDIT", "NEFT", "Vanguard Infra", "ACC-4455-6677", "Federal Bank", "Contractual advance", 1, "Exceeds declared customer profile"),
        ("TXN-98388", "ACC-4401-8291", "CUST-10482", "2026-10-03 16:50:00", 605000.0, "DEBIT", "IMPS", "PayFast Gateway", "UPI-GATE-9912", "ICICI Bank", "Outbound wallet drain", 1, "Mule account pass-through pattern"),
        # 04 Oct
        ("TXN-98440", "ACC-4401-8291", "CUST-10482", "2026-10-04 10:10:00", 520000.0, "CREDIT", "IMPS", "Apex Marine", "ACC-6677-8899", "Bank of Baroda", "Supplier deposit", 1, "High velocity"),
        ("TXN-98445", "ACC-4401-8291", "CUST-10482", "2026-10-04 10:28:00", 515000.0, "DEBIT", "UPI", "Digital Coin Nexus", "UPI-DEX-8831", "Kotak Bank", "Crypto purchase", 1, "Pass-through sweep (18 mins)"),
        # 05 Oct
        ("TXN-98510", "ACC-4401-8291", "CUST-10482", "2026-10-05 08:30:00", 480000.0, "CREDIT", "IMPS", "Metro Commercials", "ACC-7788-9900", "Axis Bank", "Clearing advance", 1, "Cumulative turnover ₹42.8 Lakh vs declared ₹5 Lakh")
    ]
    transactions.extend(cust10482_txns)

    # 2. CUST-10102: Structuring / Smurfing pattern (6 cash deposits just below ₹10 Lakh statutory CTR limit)
    cust10102_txns = [
        ("TXN-88101", "ACC-9921-1028", "CUST-10102", "2026-10-01 10:15:00", 980000.0, "CREDIT", "CASH", "Self / Agent", "BRANCH-DEL-01", "Self Branch", "Cash deposit counter 1", 1, "Structuring below ₹10 Lakh CTR limit"),
        ("TXN-88122", "ACC-9921-1028", "CUST-10102", "2026-10-01 15:30:00", 950000.0, "CREDIT", "CASH", "Self / Agent", "BRANCH-DEL-04", "Branch Connaught", "Cash deposit counter 3", 1, "Structuring below ₹10 Lakh CTR limit"),
        ("TXN-88204", "ACC-9921-1028", "CUST-10102", "2026-10-02 11:20:00", 975000.0, "CREDIT", "CASH", "Self / Agent", "BRANCH-DEL-02", "Branch Karol Bagh", "Cash deposit counter 2", 1, "Structuring below ₹10 Lakh CTR limit"),
        ("TXN-88289", "ACC-9921-1028", "CUST-10102", "2026-10-03 12:45:00", 960000.0, "CREDIT", "CASH", "Self / Agent", "BRANCH-NOI-01", "Branch Noida Sec 18", "Cash deposit counter 1", 1, "Multi-branch smurfing"),
        ("TXN-88340", "ACC-9921-1028", "CUST-10102", "2026-10-04 14:00:00", 990000.0, "CREDIT", "CASH", "Self / Agent", "BRANCH-GUR-01", "Branch Gurgaon Cyber", "Cash deposit counter 2", 1, "Structuring below ₹10 Lakh CTR limit"),
        ("TXN-88410", "ACC-9921-1028", "CUST-10102", "2026-10-04 16:30:00", 920000.0, "CREDIT", "CASH", "Self / Agent", "BRANCH-DEL-01", "Branch Main", "Cash deposit counter 4", 1, "Aggregate Cash ₹57.75 Lakh in 4 days")
    ]
    transactions.extend(cust10102_txns)

    # 3. CUST-10904: Dormant account reactivation + high-value offshore wire
    cust10904_txns = [
        ("TXN-77101", "ACC-1109-7722", "CUST-10904", "2026-10-02 09:30:00", 1850000.0, "CREDIT", "WIRE", "Cyprus Island Holdings", "ACC-CY-99120", "Bank of Cyprus", "Consultancy retainer", 1, "Dormant account sudden reactivation (> ₹18.5L) from tax haven")
    ]
    transactions.extend(cust10904_txns)

    # 4. Normal baseline transactions for other customers
    normal_txns = [
        ("TXN-66101", "ACC-7712-3301", "CUST-10255", "2026-10-01 10:00:00", 1500000.0, "CREDIT", "RTGS", "Sun Healthcare", "ACC-9988-7766", "HDFC Bank", "Raw material invoice", 0, None),
        ("TXN-66102", "ACC-7712-3301", "CUST-10255", "2026-10-03 14:20:00", 850000.0, "DEBIT", "NEFT", "National Logistics", "ACC-5544-3322", "SBI", "Freight payment", 0, None),
        ("TXN-55101", "ACC-8834-5511", "CUST-10330", "2026-10-02 12:00:00", 12500000.0, "CREDIT", "RTGS", "Reserve Bank Clearing", "ACC-RB-0012", "RBI", "Repo liquidity rollover", 0, None),
        ("TXN-44101", "ACC-6629-9944", "CUST-10771", "2026-10-04 11:30:00", 2200000.0, "CREDIT", "RTGS", "Maha Agri Mandi", "ACC-3322-1100", "Bank of Maharashtra", "Cotton supply lot 4", 0, None)
    ]
    transactions.extend(normal_txns)

    cur.executemany("INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", transactions)

    # ------------------ SEED CREDIT FACILITIES ------------------
    credit_facilities = [
        ("LN-8802", "CUST-10891", "Project Term Loan (Infra)", 450000000.0, 412000000.0, 48, "SMA-1", 0.92, 6.8, 0.82, "BREACHED", 11.25, "2026-09-25"),
        ("LN-7719", "CUST-10102", "Working Capital Overdraft", 50000000.0, 48500000.0, 18, "SMA-0", 1.12, 4.8, 1.05, "COMPLIANT", 10.50, "2026-09-20"),
        ("LN-9901", "CUST-10255", "Corporate Term Loan", 120000000.0, 68000000.0, 0, "Standard", 1.85, 2.3, 1.75, "COMPLIANT", 8.90, "2026-08-30"),
        ("LN-6644", "CUST-10771", "Agri Cash Credit", 30000000.0, 27500000.0, 32, "SMA-1", 1.08, 5.1, 1.10, "BREACHED", 10.75, "2026-09-15"),
        ("LN-5521", "CUST-10330", "NBFC Co-Lending Line", 500000000.0, 310000000.0, 0, "Standard", 1.62, 3.1, 1.45, "COMPLIANT", 9.20, "2026-09-28")
    ]
    cur.executemany("INSERT INTO credit_facilities VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", credit_facilities)

    # ------------------ SEED LIQUIDITY POSITIONS (Basel III / LCR) ------------------
    # Showing stress progression from 112.5% down into supervisory breach 98.4%
    liquidity_data = [
        ("2026-10-01", 45000.0, 8000.0, 2500.0, 52625.0, 58000.0, 11200.0, 46800.0, 112.45, 108.2, "NORMAL", "Stable liquidity surplus; retail inflows steady"),
        ("2026-10-02", 44200.0, 7800.0, 2500.0, 51730.0, 59500.0, 11700.0, 47800.0, 108.22, 107.5, "NORMAL", "Routine corporate tax outflows absorbed"),
        ("2026-10-03", 42100.0, 7500.0, 2400.0, 49475.0, 61200.0, 13700.0, 47500.0, 104.16, 105.1, "WARNING_ALERT", "LCR dipped below 105% early warning supervisory buffer; non-operational wholesale run-off detected"),
        ("2026-10-04", 39800.0, 6800.0, 2200.0, 46480.0, 68500.0, 21300.0, 47200.0, 98.47, 101.8, "CRITICAL_BREACH", "Statutory breach: LCR fell to 98.47% (< 100% statutory mandate) due to unexpected ₹6,500M institutional corporate outflow"),
        ("2026-10-05", 40100.0, 6900.0, 2200.0, 46865.0, 67200.0, 19900.0, 47300.0, 99.08, 102.1, "CRITICAL_BREACH", "Critical breach persists (99.08%). Mandatory Central Bank notification and ALCO contingency drawdown required")
    ]
    cur.executemany("INSERT INTO liquidity_positions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", liquidity_data)

    # ------------------ SEED RISK FINDINGS ------------------
    # Exact finding from user prompt: Risk Finding #AML-2026-0142
    cust10482_evidence = {
        "customer_id": "CUST-10482",
        "customer_name": "Rahul S. Sharma (QuickTrade Sole Prop)",
        "period": "29 Sep – 5 Oct 2026",
        "total_value_inr": 4280000.0,
        "total_transactions": 17,
        "declared_monthly_profile": 500000.0,
        "velocity_ratio": "8.56x declared turnover",
        "sample_evidence_txns": [
            {"txn_id": "TXN-98231", "amount": 840000.0, "time": "2026-10-02 10:42", "counterparty": "Swift Enterprises", "type": "CREDIT (RTGS)"},
            {"txn_id": "TXN-98239", "amount": 830000.0, "time": "2026-10-02 11:05", "counterparty": "CoinBridge P2P Ltd", "type": "DEBIT (IMPS pass-through 23 min)"},
            {"txn_id": "TXN-98246", "amount": 790000.0, "time": "2026-10-02 11:17", "counterparty": "Eastern Global Ventures", "type": "CREDIT (RTGS)"},
            {"txn_id": "TXN-98255", "amount": 780000.0, "time": "2026-10-02 11:48", "counterparty": "PayLink Aggregator", "type": "DEBIT (IMPS pass-through 31 min)"},
            {"txn_id": "TXN-98302", "amount": 820000.0, "time": "2026-10-02 13:05", "counterparty": "Nexus Imports", "type": "CREDIT (RTGS)"},
            {"txn_id": "TXN-98315", "amount": 815000.0, "time": "2026-10-02 13:40", "counterparty": "CryptoEx Merchant", "type": "DEBIT (IMPS pass-through 35 min)"}
        ]
    }

    cur.execute("""
    INSERT INTO risk_findings VALUES (
        'AML-2026-0142',
        'AML',
        'CUST-10482',
        'High',
        'Rapid movement of funds / Mule pass-through velocity',
        0.94,
        '17 transactions show a repeated pattern of funds entering the account and being transferred out shortly afterward. Transaction behaviour is inconsistent with historical activity.',
        ?,
        'RBI Master Direction on KYC/AML Section 4.2 & PMLA Section 12',
        'PMLA Rules 2005 Rule 8 / Section 4.2.1 Pass-Through Mule Accounts',
        'Initiate enhanced due diligence (EDD), temporary debit freeze review, and submit Suspicious Transaction Report (STR) to FIU-IND.',
        'OPEN',
        '2026-10-05 14:30:00'
    )
    """, (json.dumps(cust10482_evidence),))

    # Finding 2: Credit Risk Deterioration for BlueOcean Infrastructure
    credit_evidence = {
        "customer_id": "CUST-10891",
        "customer_name": "BlueOcean Infrastructure Pvt Ltd",
        "facility_id": "LN-8802",
        "sanctioned_amount": 450000000.0,
        "outstanding_amount": 412000000.0,
        "dpd": 48,
        "asset_class": "SMA-1",
        "dscr": 0.92,
        "dscr_threshold": 1.25,
        "debt_to_ebitda": 6.8,
        "debt_to_ebitda_limit": 4.0,
        "current_ratio": 0.82
    }
    cur.execute("""
    INSERT INTO risk_findings VALUES (
        'CRD-2026-0089',
        'CREDIT',
        'CUST-10891',
        'High',
        'Impaired Debt Service Coverage (DSCR < 1.0) & SMA-1 Overdue (48 DPD)',
        0.96,
        'Borrower principal/interest overdue by 48 days (SMA-1). Operational cash flow insufficient to service debt (DSCR 0.92x vs 1.25x covenant). Debt-to-EBITDA spiked to 6.8x.',
        ?,
        'RBI Prudential Framework for Stressed Assets (DBR.No.BP.BC.45/21.04.048/2018-19) Section 1.1 & Section 2.3',
        'Banking Regulation Act 1949 Section 35A / Mandatory CAP under SMA-1',
        'Formulate mandatory Corrective Action Plan (CAP), establish Joint Lenders Forum (JLF), and ring-fence escrow cash flows.',
        'OPEN',
        '2026-10-04 16:45:00'
    )
    """, (json.dumps(credit_evidence),))

    # Finding 3: Liquidity Regulatory Breach
    liquidity_evidence = {
        "report_date": "2026-10-04",
        "current_lcr": 98.47,
        "statutory_min_lcr": 100.0,
        "supervisory_buffer": 105.0,
        "deficit_amount_cr": 720.0,
        "primary_cause": "Unscheduled withdrawal of ₹6,500M institutional non-operational deposits",
        "hqla_available": 46480.0,
        "net_outflows_30d": 47200.0
    }
    cur.execute("""
    INSERT INTO risk_findings VALUES (
        'LIQ-2026-0012',
        'LIQUIDITY',
        'TREASURY-LCR',
        'Critical',
        'Statutory LCR Regulatory Breach (< 100%)',
        0.99,
        'Liquidity Coverage Ratio (LCR) fell to 98.47%, breaching the mandatory 100% Basel III statutory floor.',
        ?,
        'BCBS 238 Basel III Liquidity Framework & RBI Master Circular RBI/2019-20/99 Section 2.1',
        'RBI Basel III Liquidity Standards Section 2.1.5 Mandatory Supervisory Action',
        'Immediate notification to RBI Supervisory Department, convene emergency ALCO, activate Contingency Funding Plan (CFP) Level 2.',
        'ESCALATED',
        '2026-10-04 18:00:00'
    )
    """, (json.dumps(liquidity_evidence),))

    # ------------------ INITIALIZE AUDIT TRAIL ------------------
    genesis_entry = {
        "timestamp": "2026-10-01 00:00:00",
        "action": "SYSTEM_GENESIS",
        "query": "Init RiskGuard Ledger",
        "entity": "CORE_SYSTEM",
        "summary": "RiskGuard Evidence & Provenance Ledger initialized with SHA-256 cryptographic chain"
    }
    genesis_str = json.dumps(genesis_entry, sort_keys=True)
    genesis_hash = hashlib.sha256(genesis_str.encode()).hexdigest()

    cur.execute("""
    INSERT INTO audit_trail (timestamp, user_action, query_text, target_entity, result_summary, prev_hash, current_hash)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (genesis_entry["timestamp"], genesis_entry["action"], genesis_entry["query"], genesis_entry["entity"], genesis_entry["summary"], "GENESIS_ROOT_BLOCK_0000000000000000", genesis_hash))

    conn.commit()


if __name__ == "__main__":
    init_database()
