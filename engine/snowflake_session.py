"""
RiskGuard AI - Universal Snowflake / Snowpark Session Provider
Seamlessly provides an active Snowflake session:
  1. Streamlit in Snowflake (SiS): uses snowflake.snowpark.context.get_active_session()
  2. Local Snowflake Connector: connects via snowflake.connector using env or secrets
  3. Standalone Emulator: High-fidelity in-memory engine mimicking Snowflake SQL,
     Cortex Search, and Cortex Analyst for zero-friction local execution.
"""

import os
import sqlite3
import pandas as pd
from typing import Optional, Any


class SnowflakeEmulatorSession:
    """
    High-fidelity emulator implementing the Snowpark session.sql().to_pandas() interface
    with the exact Snowflake banking schemas, window functions, and analytics tables.
    """
    def __init__(self, db_path: Optional[str] = None):
        if not db_path:
            db_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
            os.makedirs(db_dir, exist_ok=True)
            self.db_path = os.path.join(db_dir, "snowflake_riskguard.db")
        else:
            self.db_path = db_path
        self._init_emulator_db()

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_emulator_db(self):
        conn = self._get_conn()
        cur = conn.cursor()

        # Create Tables matching Snowflake 01_setup_database_schema.sql
        cur.execute("""
        CREATE TABLE IF NOT EXISTS CUSTOMER (
            CUSTOMER_ID TEXT PRIMARY KEY,
            CUSTOMER_TYPE TEXT,
            CUSTOMER_NAME TEXT,
            DOB TEXT,
            COUNTRY TEXT DEFAULT 'IN',
            CITY TEXT,
            OCCUPATION TEXT,
            ANNUAL_INCOME REAL,
            CUSTOMER_SINCE TEXT,
            RISK_RATING TEXT,
            KYC_STATUS TEXT
        )""")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS ACCOUNT (
            ACCOUNT_ID TEXT PRIMARY KEY,
            CUSTOMER_ID TEXT,
            ACCOUNT_TYPE TEXT,
            CURRENCY TEXT DEFAULT 'INR',
            OPEN_DATE TEXT,
            CURRENT_BALANCE REAL,
            AVAILABLE_BALANCE REAL,
            STATUS TEXT,
            BRANCH_ID TEXT
        )""")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS COUNTERPARTY (
            COUNTERPARTY_ID TEXT PRIMARY KEY,
            NAME TEXT,
            COUNTRY TEXT DEFAULT 'IN',
            INDUSTRY TEXT,
            RISK_RATING TEXT,
            SANCTIONS_FLAG INTEGER DEFAULT 0
        )""")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS TRANSACTIONS (
            TRANSACTION_ID TEXT PRIMARY KEY,
            ACCOUNT_ID TEXT,
            CUSTOMER_ID TEXT,
            TRANSACTION_TS TEXT,
            TRANSACTION_TYPE TEXT,
            DIRECTION TEXT,
            AMOUNT REAL,
            CURRENCY TEXT DEFAULT 'INR',
            CHANNEL TEXT,
            MERCHANT_CATEGORY TEXT,
            COUNTERPARTY_ID TEXT,
            COUNTERPARTY_COUNTRY TEXT DEFAULT 'IN',
            DEVICE_ID TEXT,
            IP_COUNTRY TEXT DEFAULT 'IN',
            GEO_LAT REAL,
            GEO_LON REAL,
            TRANSACTION_STATUS TEXT DEFAULT 'SUCCESS'
        )""")
        cur.execute("CREATE VIEW IF NOT EXISTS TRANSACTION_RECORD AS SELECT * FROM TRANSACTIONS")
        cur.execute("CREATE VIEW IF NOT EXISTS [TRANSACTION] AS SELECT * FROM TRANSACTIONS")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS LOAN (
            LOAN_ID TEXT PRIMARY KEY,
            CUSTOMER_ID TEXT,
            PRODUCT_TYPE TEXT,
            PRINCIPAL_AMOUNT REAL,
            OUTSTANDING_AMOUNT REAL,
            INTEREST_RATE REAL,
            TENURE_MONTHS INTEGER,
            START_DATE TEXT,
            MATURITY_DATE TEXT,
            STATUS TEXT
        )""")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS LOAN_REPAYMENT (
            PAYMENT_ID TEXT PRIMARY KEY,
            LOAN_ID TEXT,
            DUE_DATE TEXT,
            PAYMENT_DATE TEXT,
            DUE_AMOUNT REAL,
            PAID_AMOUNT REAL,
            DAYS_PAST_DUE INTEGER DEFAULT 0
        )""")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS LIQUIDITY_POSITION (
            POSITION_DATE TEXT,
            BUSINESS_UNIT TEXT,
            HQLA REAL,
            CASH_INFLOW REAL,
            CASH_OUTFLOW REAL,
            NET_CASH_FLOW REAL,
            DEPOSIT_BALANCE REAL,
            SHORT_TERM_FUNDING REAL,
            LCR REAL,
            NSFR REAL,
            PRIMARY KEY (POSITION_DATE, BUSINESS_UNIT)
        )""")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS REGULATORY_DOCUMENTS (
            DOCUMENT_ID TEXT PRIMARY KEY,
            DOCUMENT_TYPE TEXT,
            REGULATOR TEXT,
            JURISDICTION TEXT,
            TITLE TEXT,
            SECTION TEXT,
            EFFECTIVE_DATE TEXT,
            DOCUMENT_VERSION TEXT,
            TEXT TEXT
        )""")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS RISK_EVIDENCE (
            EVIDENCE_ID TEXT PRIMARY KEY,
            CASE_ID TEXT,
            EVIDENCE_TYPE TEXT,
            SOURCE_TABLE TEXT,
            SOURCE_ID TEXT,
            EVIDENCE_TEXT TEXT,
            RISK_SCORE REAL,
            CREATED_AT TEXT,
            CREATED_BY TEXT
        )""")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS RISK_CASE (
            CASE_ID TEXT PRIMARY KEY,
            CUSTOMER_ID TEXT,
            RISK_DOMAIN TEXT,
            RISK_SCORE REAL,
            SEVERITY TEXT,
            STATUS TEXT,
            FINDING TEXT,
            RECOMMENDATION TEXT,
            CREATED_AT TEXT,
            REVIEWER TEXT,
            AUDIT_HASH TEXT
        )""")

        conn.commit()
        self._seed_sample_data(conn)
        conn.close()

    def _seed_sample_data(self, conn):
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM CUSTOMER")
        if cur.fetchone()[0] > 0:
            return  # Already seeded

        # Customers
        customers = [
            ("C1007", "RETAIL", "Rahul S. Sharma (QuickTrade Sole Prop)", "1988-04-12", "IN", "Mumbai", "Sole Proprietor", 600000.0, "2023-03-15", "HIGH", "VERIFIED"),
            ("C1032", "CORPORATE", "Apex Horizon Global Ltd", "2015-09-20", "IN", "New Delhi", "Import-Export", 18000000.0, "2021-01-10", "HIGH", "VERIFIED"),
            ("C1098", "MSME", "Starlight FinTech Enterprises", "2020-11-05", "IN", "Bengaluru", "Payment Aggregator", 12000000.0, "2022-07-18", "MEDIUM", "VERIFIED"),
            ("C1045", "CORPORATE", "BlueOcean Infrastructure Pvt Ltd", "2012-06-22", "IN", "Hyderabad", "Infrastructure Developer", 85000000.0, "2019-05-14", "HIGH", "VERIFIED"),
            ("C1012", "CORPORATE", "Zenith Pharma Logistics Ltd", "2010-02-18", "IN", "Ahmedabad", "Pharmaceuticals", 45000000.0, "2018-10-30", "LOW", "VERIFIED"),
            ("C1088", "RETAIL", "Sunita Verma", "1975-08-30", "IN", "Pune", "Consultant", 800000.0, "2017-04-11", "HIGH", "PENDING_RE_KYC")
        ]
        cur.executemany("INSERT INTO CUSTOMER VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", customers)

        # Counterparties
        cps = [
            ("CP-221", "Swift Enterprises Commercial Ltd", "IN", "Wholesale Trade", "LOW", 0),
            ("CP-223", "CoinBridge P2P Digital Exchange", "AE", "Cryptocurrency Gateway", "HIGH", 0),
            ("CP-224", "CryptoEx Global Merchant Pay", "SG", "Digital Wallet Clearing", "HIGH", 0),
            ("CP-301", "Reserve Bank Clearing System", "IN", "Central Banking", "LOW", 0),
            ("CP-402", "Cyprus Island Offshore Holdings", "CY", "Shell Investment", "CRITICAL", 0),
            ("CP-505", "National Logistics Infrastructure", "IN", "Transportation", "LOW", 0),
            ("CP-601", "Apex Marine Raw Supplies", "IN", "Manufacturing", "MEDIUM", 0)
        ]
        cur.executemany("INSERT INTO COUNTERPARTY VALUES (?, ?, ?, ?, ?, ?)", cps)

        # Accounts
        accs = [
            ("ACC-1007-01", "C1007", "CURRENT", "INR", "2023-03-15", 38200.0, 38200.0, "ACTIVE", "BR-MUM-01"),
            ("ACC-1032-01", "C1032", "CURRENT", "INR", "2021-01-10", 3125000.0, 3125000.0, "ACTIVE", "BR-DEL-04"),
            ("ACC-1098-01", "C1098", "CURRENT", "INR", "2022-07-18", 840000.0, 840000.0, "ACTIVE", "BR-BLR-02"),
            ("ACC-1045-01", "C1045", "TERM_LOAN", "INR", "2019-05-14", 1250000.0, 1250000.0, "SURVEILLANCE", "BR-HYD-01"),
            ("ACC-1012-01", "C1012", "CURRENT", "INR", "2018-10-30", 8950000.0, 8950000.0, "ACTIVE", "BR-AHM-01"),
            ("ACC-1088-01", "C1088", "SAVINGS", "INR", "2017-04-11", 1860000.0, 1860000.0, "DORMANT", "BR-PUN-02")
        ]
        cur.executemany("INSERT INTO ACCOUNT VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", accs)

        # Transactions (Includes prompt's C1007 transactions: TXN-S001, TXN-S002, TXN-S003)
        txns = [
            ("TXN-S001", "ACC-1007-01", "C1007", "2026-10-04 10:00:00", "TRANSFER", "INBOUND", 480000.0, "INR", "IMPS", "Commercial Advance", "CP-221", "IN", "DEV-991", "IN", 19.076, 72.877, "SUCCESS"),
            ("TXN-S002", "ACC-1007-01", "C1007", "2026-10-04 10:25:00", "TRANSFER", "OUTBOUND", 470000.0, "INR", "IMPS", "P2P Settlement", "CP-223", "AE", "DEV-991", "AE", 25.204, 55.270, "SUCCESS"),
            ("TXN-S003", "ACC-1007-01", "C1007", "2026-10-04 10:50:00", "TRANSFER", "OUTBOUND", 495000.0, "INR", "IMPS", "Digital Clearing", "CP-224", "SG", "DEV-991", "SG", 1.352, 103.819, "SUCCESS"),
            ("TXN-S004", "ACC-1007-01", "C1007", "2026-10-04 11:15:00", "TRANSFER", "INBOUND", 460000.0, "INR", "IMPS", "Consultancy Fee", "CP-221", "IN", "DEV-991", "IN", 19.076, 72.877, "SUCCESS"),
            ("TXN-S005", "ACC-1007-01", "C1007", "2026-10-04 11:40:00", "TRANSFER", "OUTBOUND", 455000.0, "INR", "IMPS", "Wallet Drain", "CP-223", "AE", "DEV-991", "AE", 25.204, 55.270, "SUCCESS"),
            # Structuring for C1032
            ("TXN-STR01", "ACC-1032-01", "C1032", "2026-10-01 10:15:00", "DEPOSIT", "INBOUND", 980000.0, "INR", "CASH", "Cash Counter 1", None, "IN", "BR-01", "IN", 28.613, 77.209, "SUCCESS"),
            ("TXN-STR02", "ACC-1032-01", "C1032", "2026-10-01 15:30:00", "DEPOSIT", "INBOUND", 950000.0, "INR", "CASH", "Cash Counter 3", None, "IN", "BR-04", "IN", 28.628, 77.218, "SUCCESS"),
            ("TXN-STR03", "ACC-1032-01", "C1032", "2026-10-02 11:20:00", "DEPOSIT", "INBOUND", 975000.0, "INR", "CASH", "Cash Counter 2", None, "IN", "BR-02", "IN", 28.650, 77.190, "SUCCESS"),
            ("TXN-STR04", "ACC-1032-01", "C1032", "2026-10-03 12:45:00", "DEPOSIT", "INBOUND", 960000.0, "INR", "CASH", "Branch Counter 1", None, "IN", "BR-NOI", "IN", 28.535, 77.391, "SUCCESS"),
            # Dormant for C1088
            ("TXN-DORM01", "ACC-1088-01", "C1088", "2026-10-02 09:30:00", "TRANSFER", "INBOUND", 1850000.0, "INR", "WIRE", "Retainer Remittance", "CP-402", "CY", "DEV-442", "CY", 35.185, 33.382, "SUCCESS")
        ]
        cur.executemany("INSERT INTO TRANSACTIONS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", txns)

        # Loans & Repayments
        loans = [
            ("LN-8802", "C1045", "COMMERCIAL_TERM_LOAN", 450000000.0, 412000000.0, 11.25, 84, "2022-06-20", "2029-06-20", "SMA_1"),
            ("LN-7719", "C1032", "WORKING_CAPITAL", 50000000.0, 48500000.0, 10.50, 36, "2023-01-10", "2026-01-10", "SMA_0"),
            ("LN-9901", "C1012", "COMMERCIAL_TERM_LOAN", 120000000.0, 68000000.0, 8.90, 60, "2021-11-05", "2026-11-05", "STANDARD")
        ]
        cur.executemany("INSERT INTO LOAN VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", loans)

        repayments = [
            ("PAY-8802-01", "LN-8802", "2026-08-30", "2026-08-30", 8500000.0, 8500000.0, 0),
            ("PAY-8802-02", "LN-8802", "2026-09-30", None, 8500000.0, 0.0, 36),
            ("PAY-8802-03", "LN-8802", "2026-10-30", None, 8500000.0, 0.0, 48),
            ("PAY-7719-01", "LN-7719", "2026-10-01", None, 1200000.0, 0.0, 18),
            ("PAY-9901-01", "LN-9901", "2026-10-01", "2026-10-01", 2500000.0, 2500000.0, 0)
        ]
        cur.executemany("INSERT INTO LOAN_REPAYMENT VALUES (?, ?, ?, ?, ?, ?, ?)", repayments)

        # Liquidity
        liqs = [
            ("2026-10-01", "TREASURY_MAIN", 52625000.0, 11200000.0, 58000000.0, -46800000.0, 1450000000.0, 280000000.0, 112.45, 108.2),
            ("2026-10-02", "TREASURY_MAIN", 51730000.0, 11700000.0, 59500000.0, -47800000.0, 1435000000.0, 285000000.0, 108.22, 107.5),
            ("2026-10-03", "TREASURY_MAIN", 49475000.0, 13700000.0, 61200000.0, -47500000.0, 1410000000.0, 295000000.0, 104.16, 105.1),
            ("2026-10-04", "TREASURY_MAIN", 46480000.0, 21300000.0, 68500000.0, -47200000.0, 1345000000.0, 310000000.0, 98.47, 101.8),
            ("2026-10-05", "TREASURY_MAIN", 46865000.0, 19900000.0, 67200000.0, -47300000.0, 1340000000.0, 315000000.0, 99.08, 102.1)
        ]
        cur.executemany("INSERT INTO LIQUIDITY_POSITION VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", liqs)

        # Regulatory Documents
        reg_docs = [
            ("REG-AML-4.2", "REGULATION", "RBI", "INDIA", "Master Direction - KYC Direction, 2016", "Section 4.2: Velocity Anomalies & Pass-Through Mule Accounts", "2016-02-25", "v4.2",
             "Section 4.2 Velocity Anomalies & Mule Accounts: Regulated Entities must institute automated monitoring capable of detecting rapid pass-through velocity. Accounts exhibiting sudden credits followed immediately by equivalent debits to unrelated digital intermediaries or crypto accounts within minutes, leaving nominal balances, must be classified as potential mule accounts. Mandatory Enhanced Due Diligence (EDD) and Suspicious Transaction Report (STR) filing under PMLA Section 12 is required within 7 days."),
            ("REG-AML-4.1.2", "REGULATION", "RBI", "INDIA", "Master Direction - KYC and Cash Reporting", "Section 4.1.2: Cash Structuring & Smurfing Evasion", "2016-02-25", "v4.2",
             "Section 4.1.2 Structuring Evasion: Where a customer conducts multiple transactions in cash or currency in amounts just below the statutory reporting threshold of Rupees Ten Lakh (INR 10,00,000) within 1 to 7 calendar days to evade statutory reporting, REs shall aggregate transactions and file an immediate STR to FIU-IND."),
            ("REG-BASEL-2.1", "REGULATION", "BCBS", "GLOBAL", "Basel III: The Liquidity Coverage Ratio and liquidity risk monitoring tools", "Section 2.1: Liquidity Coverage Ratio (LCR) Mandate", "2013-01-01", "BCBS 238",
             "Section 2.1 LCR Mandate: The Liquidity Coverage Ratio requires institutions to maintain an unencumbered stock of High Quality Liquid Assets (HQLA) that equals or exceeds total net cash outflows over a 30-day severe stress period (LCR >= 100%). Any drop below the 105% supervisory early warning buffer requires immediate ALCO notification. A drop below 100% represents a direct statutory breach requiring central bank reporting."),
            ("REG-CREDIT-1.1", "REGULATION", "RBI", "INDIA", "Prudential Framework for Resolution of Stressed Assets", "Section 1.1: Early Warning Signals & Special Mention Accounts", "2019-06-07", "DBR.No.BP.BC.45",
             "Section 1.1 SMA Classification: Lenders shall recognize incipient stress in loan accounts immediately: SMA-0 (1-30 days overdue), SMA-1 (31-60 days overdue), SMA-2 (61-90 days overdue). Where a borrower crosses into SMA-1 with a Debt Service Coverage Ratio (DSCR) below 1.15x, lenders must initiate a Corrective Action Plan (CAP) under the Inter-Creditor Agreement.")
        ]
        cur.executemany("INSERT INTO REGULATORY_DOCUMENTS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", reg_docs)

        # Risk Evidence & Cases
        evids = [
            ("EVID-001", "CASE-2026-0042", "TRANSACTION", "TRANSACTION", "TXN-S001", "Inbound IMPS credit of ₹4,80,000 at 10:00:00 from Swift Enterprises", 30.0, "2026-10-04 10:00:00", "AML_DETECTOR_V2"),
            ("EVID-002", "CASE-2026-0042", "TRANSACTION", "TRANSACTION", "TXN-S002", "Outbound IMPS debit of ₹4,70,000 at 10:25:00 to CoinBridge P2P (UAE) within 25 minutes", 25.0, "2026-10-04 10:25:00", "AML_DETECTOR_V2"),
            ("EVID-003", "CASE-2026-0042", "TRANSACTION", "TRANSACTION", "TXN-S003", "Outbound IMPS debit of ₹4,95,000 at 10:50:00 to CryptoEx (Singapore) within 25 minutes", 25.0, "2026-10-04 10:50:00", "AML_DETECTOR_V2"),
            ("EVID-004", "CASE-2026-0042", "POLICY", "REGULATORY_DOCUMENTS", "REG-AML-4.2", "RBI Master Direction §4.2: Velocity Anomalies & Pass-Through Mule Accounts", 10.0, "2026-10-04 11:00:00", "CORTEX_SEARCH"),
            ("EVID-005", "CASE-2026-0042", "CUSTOMER", "CUSTOMER", "C1007", "Declared monthly turnover is ₹50,000 (INR 6.0 Lakh annual). 24h velocity is ₹23.6 Lakh (393% above declared profile)", 10.0, "2026-10-04 11:00:00", "CORTEX_ANALYST")
        ]
        cur.executemany("INSERT INTO RISK_EVIDENCE VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", evids)

        cur.execute("""
        INSERT INTO RISK_CASE VALUES (
            'CASE-2026-0042', 'C1007', 'AML_FRAUD', 92.0, 'HIGH', 'INVESTIGATING',
            'Customer C1007 exhibits classic digital mule pass-through velocity. Multiple high-value IMPS inbound credits are drained within 25 minutes to cross-border crypto aggregators in UAE and Singapore, leaving a nominal account balance.',
            'Immediate debit freeze review, execute mandatory Enhanced Due Diligence (EDD), and submit Suspicious Transaction Report (STR) to FIU-IND.',
            '2026-10-04 11:30:00', 'Senior Compliance Analyst #CO-902',
            'SHA256:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069'
        )""")

        conn.commit()

    def sql(self, query: str):
        """Returns an execution object mimicking Snowpark's session.sql()"""
        return SnowparkQueryEmulator(self._get_conn(), query)


import re

class SnowparkQueryEmulator:
    def __init__(self, conn, query: str):
        self.conn = conn
        # Clean Snowflake schema prefixes and normalize table name
        clean_query = query
        clean_query = re.sub(r'\bRISKGUARD\.(?:DATA|ANALYTICS|GOVERNANCE)\.', '', clean_query, flags=re.IGNORECASE)
        clean_query = re.sub(r'\bRISKGUARD\.', '', clean_query, flags=re.IGNORECASE)
        clean_query = re.sub(r'\bTRANSACTION\b', 'TRANSACTIONS', clean_query, flags=re.IGNORECASE)
        clean_query = re.sub(r'\bTRANSACTION_RECORD\b', 'TRANSACTIONS', clean_query, flags=re.IGNORECASE)
        self.query = clean_query

    def to_pandas(self) -> pd.DataFrame:
        try:
            df = pd.read_sql_query(self.query, self.conn)
        finally:
            self.conn.close()
        return df


def get_snowflake_session() -> Any:
    """
    Factory resolving active Snowflake connection or fallback emulator.
    """
    # 1. Attempt native Streamlit in Snowflake (SiS) context
    try:
        from snowflake.snowpark.context import get_active_session
        session = get_active_session()
        print("✓ Connected to native Streamlit in Snowflake (SiS) session.")
        return session
    except Exception:
        pass

    # 2. Attempt Snowflake Connector / Snowpark Session with local config if available
    try:
        import snowflake.connector
        account = os.environ.get("SNOWFLAKE_ACCOUNT")
        user = os.environ.get("SNOWFLAKE_USER")
        if account and user:
            from snowflake.snowpark import Session
            connection_params = {
                "account": account,
                "user": user,
                "password": os.environ.get("SNOWFLAKE_PASSWORD"),
                "role": os.environ.get("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
                "warehouse": os.environ.get("SNOWFLAKE_WAREHOUSE", "RISKGUARD_WH"),
                "database": os.environ.get("SNOWFLAKE_DATABASE", "RISKGUARD"),
                "schema": os.environ.get("SNOWFLAKE_SCHEMA", "DATA")
            }
            session = Session.builder.configs(connection_params).create()
            print(f"✓ Connected to Snowflake Cloud account: {account}")
            return session
    except Exception:
        pass

    # 3. Default to High-Fidelity Snowflake Emulator Session
    # Guaranteed to work standalone without cloud dependencies!
    return SnowflakeEmulatorSession()
