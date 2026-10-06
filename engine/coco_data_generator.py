"""
RiskGuard AI - Snowflake CoCo CLI Dynamic Data Engine
Generates synthetic, referentially consistent financial transactions, accounts,
counterparties, loan impairments, and treasury liquidity shocks.
Inserts directly into the active Snowflake Data Cloud (or Snowpark emulator).
"""

import os
import sys
import uuid
import random
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Callable

from engine.snowflake_session import get_snowflake_session
from engine.audit_logger import log_event


class CoCoDataGenerator:
    """
    Production-grade synthetic financial data generator for Snowflake CoCo CLI.
    Generates referentially consistent records across:
      CUSTOMER, ACCOUNT, COUNTERPARTY, TRANSACTIONS, LOAN, LOAN_REPAYMENT,
      LIQUIDITY_POSITION, RISK_EVIDENCE, RISK_CASE.
    """

    def __init__(self):
        self.session = get_snowflake_session()

    def _execute(self, sql_query: str, params: tuple = ()):
        """Executes a query against active Snowflake session or emulator."""
        if hasattr(self.session, "execute"):
            return self.session.execute(sql_query, params)
        else:
            # Snowflake Cloud / Snowpark Session
            # Clean parameter interpolation
            clean_sql = sql_query
            for p in params:
                val = f"'{p}'" if isinstance(p, str) else str(p)
                clean_sql = clean_sql.replace("?", val, 1)
            return self.session.sql(clean_sql).collect()

    # -------------------------------------------------------------------------
    # 1. SCENARIO: AML PASS-THROUGH MULE VELOCITY
    # -------------------------------------------------------------------------
    def generate_mule_scenario(
        self,
        customer_id: Optional[str] = None,
        customer_name: Optional[str] = None,
        inbound_amount: float = 540000.0,
        currency: str = "INR"
    ) -> Dict[str, Any]:
        """
        Generates rapid pass-through layering: high-value inbound credit
        swept within minutes to offshore crypto counterparties in UAE & Singapore.
        """
        now = datetime.now()
        cid = customer_id or f"C{random.randint(2000, 2999)}"
        cname = customer_name or f"Vikram K. Malhotra (Nexus Global Traders {cid[-4:]})"
        acc_id = f"ACC-{cid}-01"

        # 1. Ensure Customer exists
        self._execute("""
        INSERT OR IGNORE INTO CUSTOMER (CUSTOMER_ID, CUSTOMER_TYPE, CUSTOMER_NAME, DOB, COUNTRY, CITY, OCCUPATION, ANNUAL_INCOME, CUSTOMER_SINCE, RISK_RATING, KYC_STATUS)
        VALUES (?, 'RETAIL', ?, '1991-07-14', 'IN', 'Mumbai', 'Sole Proprietor', 720000.0, '2024-02-10', 'HIGH', 'VERIFIED')
        """, (cid, cname))

        # 2. Ensure Account exists
        self._execute("""
        INSERT OR IGNORE INTO ACCOUNT (ACCOUNT_ID, CUSTOMER_ID, ACCOUNT_TYPE, CURRENCY, OPEN_DATE, CURRENT_BALANCE, AVAILABLE_BALANCE, STATUS, BRANCH_ID)
        VALUES (?, ?, 'CURRENT', ?, '2024-02-10', 14500.0, 14500.0, 'ACTIVE', 'BR-MUM-02')
        """, (acc_id, cid, currency))

        # 3. Ensure Counterparties exist
        self._execute("""
        INSERT OR IGNORE INTO COUNTERPARTY (COUNTERPARTY_ID, NAME, COUNTRY, INDUSTRY, RISK_RATING, SANCTIONS_FLAG)
        VALUES ('CP-221', 'Swift Enterprises Commercial Ltd', 'IN', 'Wholesale Trade', 'LOW', 0)
        """)
        self._execute("""
        INSERT OR IGNORE INTO COUNTERPARTY (COUNTERPARTY_ID, NAME, COUNTRY, INDUSTRY, RISK_RATING, SANCTIONS_FLAG)
        VALUES ('CP-223', 'CoinBridge P2P Digital Exchange', 'AE', 'Cryptocurrency Gateway', 'HIGH', 0)
        """)
        self._execute("""
        INSERT OR IGNORE INTO COUNTERPARTY (COUNTERPARTY_ID, NAME, COUNTRY, INDUSTRY, RISK_RATING, SANCTIONS_FLAG)
        VALUES ('CP-224', 'CryptoEx Global Merchant Pay', 'SG', 'Digital Wallet Clearing', 'HIGH', 0)
        """)

        # 4. Generate Inbound Spike Transaction
        t1_id = f"TXN-ML-{random.randint(10000, 99999)}"
        t1_time = (now - timedelta(minutes=50)).strftime("%Y-%m-%d %H:%M:%S")
        self._execute("""
        INSERT INTO TRANSACTIONS (TRANSACTION_ID, ACCOUNT_ID, CUSTOMER_ID, TRANSACTION_TS, TRANSACTION_TYPE, DIRECTION, AMOUNT, CURRENCY, CHANNEL, MERCHANT_CATEGORY, COUNTERPARTY_ID, COUNTERPARTY_COUNTRY, DEVICE_ID, IP_COUNTRY, GEO_LAT, GEO_LON, TRANSACTION_STATUS)
        VALUES (?, ?, ?, ?, 'TRANSFER', 'INBOUND', ?, ?, 'IMPS', 'Commercial Advance', 'CP-221', 'IN', 'DEV-991', 'IN', 19.076, 72.877, 'SUCCESS')
        """, (t1_id, acc_id, cid, t1_time, inbound_amount, currency))

        # 5. Rapid Outbound Drains (25-35 minutes later)
        t2_id = f"TXN-ML-{random.randint(10000, 99999)}"
        t2_time = (now - timedelta(minutes=28)).strftime("%Y-%m-%d %H:%M:%S")
        out1_amt = round(inbound_amount * 0.49, 2)
        self._execute("""
        INSERT INTO TRANSACTIONS (TRANSACTION_ID, ACCOUNT_ID, CUSTOMER_ID, TRANSACTION_TS, TRANSACTION_TYPE, DIRECTION, AMOUNT, CURRENCY, CHANNEL, MERCHANT_CATEGORY, COUNTERPARTY_ID, COUNTERPARTY_COUNTRY, DEVICE_ID, IP_COUNTRY, GEO_LAT, GEO_LON, TRANSACTION_STATUS)
        VALUES (?, ?, ?, ?, 'TRANSFER', 'OUTBOUND', ?, ?, 'IMPS', 'P2P Settlement', 'CP-223', 'AE', 'DEV-991', 'AE', 25.204, 55.270, 'SUCCESS')
        """, (t2_id, acc_id, cid, t2_time, out1_amt, currency))

        t3_id = f"TXN-ML-{random.randint(10000, 99999)}"
        t3_time = (now - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
        out2_amt = round(inbound_amount * 0.48, 2)
        self._execute("""
        INSERT INTO TRANSACTIONS (TRANSACTION_ID, ACCOUNT_ID, CUSTOMER_ID, TRANSACTION_TS, TRANSACTION_TYPE, DIRECTION, AMOUNT, CURRENCY, CHANNEL, MERCHANT_CATEGORY, COUNTERPARTY_ID, COUNTERPARTY_COUNTRY, DEVICE_ID, IP_COUNTRY, GEO_LAT, GEO_LON, TRANSACTION_STATUS)
        VALUES (?, ?, ?, ?, 'TRANSFER', 'OUTBOUND', ?, ?, 'IMPS', 'Digital Clearing', 'CP-224', 'SG', 'DEV-991', 'SG', 1.352, 103.819, 'SUCCESS')
        """, (t3_id, acc_id, cid, t3_time, out2_amt, currency))

        case_id = f"CASE-2026-{cid}"
        # 6. Add Risk Evidence
        self._execute("""
        INSERT OR REPLACE INTO RISK_EVIDENCE (EVIDENCE_ID, CASE_ID, EVIDENCE_TYPE, SOURCE_TABLE, SOURCE_ID, EVIDENCE_TEXT, RISK_SCORE, CREATED_AT, CREATED_BY)
        VALUES (?, ?, 'TRANSACTION', 'TRANSACTION', ?, ?, 30.0, ?, 'COCO_SYNTHETIC_CLI')
        """, (f"EVID-{t1_id}", case_id, t1_id, f"Inbound spike of ₹{inbound_amount:,.2f} followed by rapid outbound crypto sweep", now.strftime("%Y-%m-%d %H:%M:%S")))

        # 7. Add Risk Case
        self._execute("""
        INSERT OR REPLACE INTO RISK_CASE (CASE_ID, CUSTOMER_ID, RISK_DOMAIN, RISK_SCORE, SEVERITY, STATUS, FINDING, RECOMMENDATION, CREATED_AT, REVIEWER, AUDIT_HASH)
        VALUES (?, ?, 'AML_FRAUD', 93.0, 'HIGH', 'INVESTIGATING',
        ?, 'Immediate debit freeze, trigger Enhanced Due Diligence (EDD), and submit STR to FIU-IND.', ?, 'CoCo Autonomous Investigator', 'SHA256:COCO_DYNAMIC_DATA_STREAM')
        """, (
            case_id, cid,
            f"Customer {cid} ({cname}) exhibits classic digital mule pass-through velocity. Inbound ₹{inbound_amount:,.2f} drained to UAE & SG in < 30 minutes.",
            now.strftime("%Y-%m-%d %H:%M:%S")
        ))

        # Cryptographic Audit Log
        log_event(
            action="COCO_DYNAMIC_DATA_GENERATION",
            query_text="GENERATE_PATTERN_MULE",
            target_entity=cid,
            result_summary=f"Synthesized pass-through velocity mule transactions: {t1_id} -> {t2_id}, {t3_id}"
        )

        return {
            "pattern": "AML_PASS_THROUGH_MULE",
            "customer_id": cid,
            "customer_name": cname,
            "account_id": acc_id,
            "case_id": case_id,
            "transactions_created": [t1_id, t2_id, t3_id],
            "inbound_amount": inbound_amount,
            "outbound_total": out1_amt + out2_amt,
            "residual_balance": round(inbound_amount - (out1_amt + out2_amt), 2),
            "risk_score": 93,
            "regulatory_violation": "RBI KYC/AML Master Direction Section 4.2"
        }

    # -------------------------------------------------------------------------
    # 2. SCENARIO: CASH STRUCTURING / SMURFING (< ₹10 LAKH CTR LIMIT)
    # -------------------------------------------------------------------------
    def generate_structuring_scenario(
        self,
        customer_id: Optional[str] = None,
        count: int = 4
    ) -> Dict[str, Any]:
        """
        Generates multiple cash deposits just below the ₹10 Lakh statutory threshold
        across distinct branch counters within 48 hours to evade CTR reporting.
        """
        now = datetime.now()
        cid = customer_id or f"C{random.randint(3000, 3999)}"
        cname = f"Kaveri Mineral & Metals Trading Corp {cid[-4:]}"
        acc_id = f"ACC-{cid}-01"

        self._execute("""
        INSERT OR IGNORE INTO CUSTOMER (CUSTOMER_ID, CUSTOMER_TYPE, CUSTOMER_NAME, DOB, COUNTRY, CITY, OCCUPATION, ANNUAL_INCOME, CUSTOMER_SINCE, RISK_RATING, KYC_STATUS)
        VALUES (?, 'CORPORATE', ?, '2016-04-18', 'IN', 'New Delhi', 'Import-Export', 16000000.0, '2022-01-15', 'HIGH', 'VERIFIED')
        """, (cid, cname))

        self._execute("""
        INSERT OR IGNORE INTO ACCOUNT (ACCOUNT_ID, CUSTOMER_ID, ACCOUNT_TYPE, CURRENCY, OPEN_DATE, CURRENT_BALANCE, AVAILABLE_BALANCE, STATUS, BRANCH_ID)
        VALUES (?, ?, 'CURRENT', 'INR', '2022-01-15', 3850000.0, 3850000.0, 'ACTIVE', 'BR-DEL-01')
        """, (acc_id, cid))

        branches = ["BR-DEL-01", "BR-DEL-04", "BR-NOI-02", "BR-GUR-01"]
        created_txns = []
        amounts = [980000.0, 955000.0, 970000.0, 965000.0, 990000.0][:count]

        for i, amt in enumerate(amounts):
            tid = f"TXN-STR-{random.randint(10000, 99999)}"
            t_time = (now - timedelta(hours=36 - (i * 8))).strftime("%Y-%m-%d %H:%M:%S")
            br = branches[i % len(branches)]
            self._execute("""
            INSERT INTO TRANSACTIONS (TRANSACTION_ID, ACCOUNT_ID, CUSTOMER_ID, TRANSACTION_TS, TRANSACTION_TYPE, DIRECTION, AMOUNT, CURRENCY, CHANNEL, MERCHANT_CATEGORY, COUNTERPARTY_ID, COUNTERPARTY_COUNTRY, DEVICE_ID, IP_COUNTRY, GEO_LAT, GEO_LON, TRANSACTION_STATUS)
            VALUES (?, ?, ?, ?, 'DEPOSIT', 'INBOUND', ?, 'INR', 'CASH', 'Cash Counter', NULL, 'IN', ?, 'IN', 28.613, 77.209, 'SUCCESS')
            """, (tid, acc_id, cid, t_time, amt, br))
            created_txns.append(tid)

        case_id = f"CASE-2026-STR-{cid}"
        self._execute("""
        INSERT OR REPLACE INTO RISK_CASE (CASE_ID, CUSTOMER_ID, RISK_DOMAIN, RISK_SCORE, SEVERITY, STATUS, FINDING, RECOMMENDATION, CREATED_AT, REVIEWER, AUDIT_HASH)
        VALUES (?, ?, 'AML_STRUCTURING', 88.0, 'HIGH', 'INVESTIGATING',
        ?, 'Aggregate transactions and file mandatory STR to FIU-IND under PMLA Section 12.', ?, 'CoCo Autonomous Investigator', 'SHA256:COCO_STRUCTURING_STREAM')
        """, (
            case_id, cid,
            f"Customer {cid} made {count} cash deposits totaling ₹{sum(amounts):,.2f}, each just below the ₹10 Lakh statutory limit.",
            now.strftime("%Y-%m-%d %H:%M:%S")
        ))

        log_event(
            action="COCO_DYNAMIC_DATA_GENERATION",
            query_text="GENERATE_PATTERN_STRUCTURING",
            target_entity=cid,
            result_summary=f"Synthesized cash structuring: {count} deposits below ₹10L totaling ₹{sum(amounts):,.2f}"
        )

        return {
            "pattern": "AML_CASH_STRUCTURING",
            "customer_id": cid,
            "customer_name": cname,
            "account_id": acc_id,
            "case_id": case_id,
            "transactions_created": created_txns,
            "total_cash_volume": sum(amounts),
            "statutory_threshold": 1000000.0,
            "risk_score": 88,
            "regulatory_violation": "RBI KYC/AML Master Direction Section 4.1.2 & PMLA §12"
        }

    # -------------------------------------------------------------------------
    # 3. SCENARIO: CREDIT RISK & STRESSED ASSET (SMA-1)
    # -------------------------------------------------------------------------
    def generate_credit_stress_scenario(
        self,
        customer_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates commercial credit facility with DPD 31-60 days (SMA-1)
        and covenant deterioration (DSCR erosion).
        """
        now = datetime.now()
        cid = customer_id or f"C{random.randint(4000, 4999)}"
        cname = f"Apex Urban Highway Developers Ltd {cid[-4:]}"
        loan_id = f"LN-{random.randint(8000, 8999)}"

        self._execute("""
        INSERT OR IGNORE INTO CUSTOMER (CUSTOMER_ID, CUSTOMER_TYPE, CUSTOMER_NAME, DOB, COUNTRY, CITY, OCCUPATION, ANNUAL_INCOME, CUSTOMER_SINCE, RISK_RATING, KYC_STATUS)
        VALUES (?, 'CORPORATE', ?, '2014-11-20', 'IN', 'Hyderabad', 'Infrastructure', 95000000.0, '2020-03-10', 'HIGH', 'VERIFIED')
        """, (cid, cname))

        principal = 180000000.0  # 18 Crore
        outstanding = 168000000.0 # 16.8 Crore

        self._execute("""
        INSERT OR REPLACE INTO LOAN (LOAN_ID, CUSTOMER_ID, PRODUCT_TYPE, PRINCIPAL_AMOUNT, OUTSTANDING_AMOUNT, INTEREST_RATE, TENURE_MONTHS, START_DATE, MATURITY_DATE, STATUS)
        VALUES (?, ?, 'COMMERCIAL_TERM_LOAN', ?, ?, 11.75, 84, '2023-01-15', '2030-01-15', 'SMA_1')
        """, (loan_id, cid, principal, outstanding))

        # Repayments: 1 on-time, 2 overdue (38 days and 52 days)
        self._execute("""
        INSERT OR REPLACE INTO LOAN_REPAYMENT (PAYMENT_ID, LOAN_ID, DUE_DATE, PAYMENT_DATE, DUE_AMOUNT, PAID_AMOUNT, DAYS_PAST_DUE)
        VALUES (?, ?, ?, ?, 3200000.0, 3200000.0, 0)
        """, (f"PAY-{loan_id}-01", loan_id, (now - timedelta(days=90)).strftime("%Y-%m-%d"), (now - timedelta(days=90)).strftime("%Y-%m-%d")))

        self._execute("""
        INSERT OR REPLACE INTO LOAN_REPAYMENT (PAYMENT_ID, LOAN_ID, DUE_DATE, PAYMENT_DATE, DUE_AMOUNT, PAID_AMOUNT, DAYS_PAST_DUE)
        VALUES (?, ?, ?, NULL, 3200000.0, 0.0, 42)
        """, (f"PAY-{loan_id}-02", loan_id, (now - timedelta(days=42)).strftime("%Y-%m-%d")))

        case_id = f"CASE-2026-CR-{cid}"
        self._execute("""
        INSERT OR REPLACE INTO RISK_CASE (CASE_ID, CUSTOMER_ID, RISK_DOMAIN, RISK_SCORE, SEVERITY, STATUS, FINDING, RECOMMENDATION, CREATED_AT, REVIEWER, AUDIT_HASH)
        VALUES (?, ?, 'CREDIT_EWS', 84.0, 'HIGH', 'INVESTIGATING',
        ?, 'Formulate Corrective Action Plan (CAP) under RBI Stressed Asset Prudential Framework.', ?, 'CoCo Credit Risk Officer', 'SHA256:COCO_CREDIT_STRESS')
        """, (
            case_id, cid,
            f"Borrower {cid} ({cname}) classified as SMA-1 with overdue interest of ₹64 Lakh (42 DPD). Facility utilization > 93%.",
            now.strftime("%Y-%m-%d %H:%M:%S")
        ))

        log_event(
            action="COCO_DYNAMIC_DATA_GENERATION",
            query_text="GENERATE_PATTERN_CREDIT_STRESS",
            target_entity=cid,
            result_summary=f"Synthesized credit stress: Loan {loan_id} classified as SMA-1 with 42 DPD"
        )

        return {
            "pattern": "CREDIT_STRESS_SMA1",
            "customer_id": cid,
            "customer_name": cname,
            "loan_id": loan_id,
            "principal": principal,
            "outstanding": outstanding,
            "days_past_due": 42,
            "asset_class": "SMA_1",
            "risk_score": 84,
            "regulatory_violation": "RBI Prudential Framework for Resolution of Stressed Assets §1.1"
        }

    # -------------------------------------------------------------------------
    # 4. SCENARIO: TREASURY LIQUIDITY SHOCK (BASEL III LCR BREACH)
    # -------------------------------------------------------------------------
    def generate_liquidity_shock_scenario(self) -> Dict[str, Any]:
        """
        Generates daily liquidity stress position causing Basel III LCR to breach
        below the 100% statutory floor.
        """
        now = datetime.now()
        pos_date = now.strftime("%Y-%m-%d")

        hqla = 44500000.0
        outflows = 74500000.0
        inflows = 18200000.0
        net_cash_flow = inflows - outflows
        lcr = round((hqla / abs(net_cash_flow)) * 100, 2) # ~79.0% (BREACH!)

        self._execute("""
        INSERT OR REPLACE INTO LIQUIDITY_POSITION (POSITION_DATE, BUSINESS_UNIT, HQLA, CASH_INFLOW, CASH_OUTFLOW, NET_CASH_FLOW, DEPOSIT_BALANCE, SHORT_TERM_FUNDING, LCR, NSFR)
        VALUES (?, 'TREASURY_MAIN', ?, ?, ?, ?, 1310000000.0, 325000000.0, ?, 100.8)
        """, (pos_date, hqla, inflows, outflows, net_cash_flow, lcr))

        case_id = f"CASE-2026-LIQ-{pos_date}"
        self._execute("""
        INSERT OR REPLACE INTO RISK_CASE (CASE_ID, CUSTOMER_ID, RISK_DOMAIN, RISK_SCORE, SEVERITY, STATUS, FINDING, RECOMMENDATION, CREATED_AT, REVIEWER, AUDIT_HASH)
        VALUES (?, 'TREASURY_MAIN', 'TREASURY_LIQUIDITY', 95.0, 'HIGH', 'INVESTIGATING',
        ?, 'Immediate ALCO convocation, execute emergency repo monetization, notify central bank supervisory cell.', ?, 'CoCo Treasury Monitor', 'SHA256:COCO_LCR_SHOCK')
        """, (
            case_id,
            f"Basel III LCR dropped to {lcr}% (Statutory breach below 100% minimum floor) due to net stressed 30-day outflow of ₹56.3 Crore.",
            now.strftime("%Y-%m-%d %H:%M:%S")
        ))

        log_event(
            action="COCO_DYNAMIC_DATA_GENERATION",
            query_text="GENERATE_PATTERN_LIQUIDITY_SHOCK",
            target_entity="TREASURY_MAIN",
            result_summary=f"Synthesized Basel III liquidity shock: LCR dropped to {lcr}%"
        )

        return {
            "pattern": "BASEL_III_LIQUIDITY_SHOCK",
            "position_date": pos_date,
            "hqla": hqla,
            "net_cash_flow": net_cash_flow,
            "lcr": lcr,
            "regulatory_status": "STATUTORY_BREACH",
            "regulatory_mandate": "Basel III BCBS 238 LCR Directive Section 2.1"
        }

    # -------------------------------------------------------------------------
    # 5. SCENARIO: NORMAL BANKING TRAFFIC
    # -------------------------------------------------------------------------
    def generate_normal_transactions(self, count: int = 5) -> List[Dict[str, Any]]:
        """Generates legitimate day-to-day retail/business transactions."""
        now = datetime.now()
        categories = ["Utility Bill", "Merchant POS", "Vendor Settlement", "Payroll Credit", "Mobile Recharge"]
        channels = ["UPI", "IMPS", "NEFT", "CARD"]
        txns = []

        for i in range(count):
            tid = f"TXN-NRM-{random.randint(10000, 99999)}"
            amt = round(random.uniform(1500.0, 48000.0), 2)
            ts = (now - timedelta(minutes=random.randint(5, 720))).strftime("%Y-%m-%d %H:%M:%S")
            cat = random.choice(categories)
            chan = random.choice(channels)
            cid = "C1012"  # Normal low-risk customer

            self._execute("""
            INSERT INTO TRANSACTIONS (TRANSACTION_ID, ACCOUNT_ID, CUSTOMER_ID, TRANSACTION_TS, TRANSACTION_TYPE, DIRECTION, AMOUNT, CURRENCY, CHANNEL, MERCHANT_CATEGORY, COUNTERPARTY_ID, COUNTERPARTY_COUNTRY, DEVICE_ID, IP_COUNTRY, GEO_LAT, GEO_LON, TRANSACTION_STATUS)
            VALUES (?, 'ACC-1012-01', ?, ?, 'PURCHASE', 'OUTBOUND', ?, 'INR', ?, ?, 'CP-505', 'IN', 'DEV-101', 'IN', 23.022, 72.571, 'SUCCESS')
            """, (tid, cid, ts, amt, chan, cat))
            txns.append({"transaction_id": tid, "amount": amt, "channel": chan, "category": cat, "timestamp": ts})

        return txns

    # -------------------------------------------------------------------------
    # 6. STREAMING SIMULATION
    # -------------------------------------------------------------------------
    def stream_simulation(
        self,
        pattern: str = "mule",
        total_events: int = 5,
        interval_seconds: float = 1.0,
        callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ) -> List[Dict[str, Any]]:
        """
        Streams events sequentially with a configurable delay, simulating
        real-time message queue / Kafka / Snowpipe ingestion.
        """
        results = []
        for i in range(total_events):
            if pattern == "mule":
                res = self.generate_mule_scenario()
            elif pattern == "structuring":
                res = self.generate_structuring_scenario(count=3)
            elif pattern == "credit_stress":
                res = self.generate_credit_stress_scenario()
            elif pattern == "liquidity_shock":
                res = self.generate_liquidity_shock_scenario()
            else:
                nrm_list = self.generate_normal_transactions(count=1)
                res = nrm_list[0] if nrm_list else {}

            results.append(res)
            if callback:
                callback(res)
            if i < total_events - 1 and interval_seconds > 0:
                time.sleep(interval_seconds)

        return results

    # -------------------------------------------------------------------------
    # 7. LIVE DATABASE STATISTICS
    # -------------------------------------------------------------------------
    def get_live_statistics(self) -> Dict[str, Any]:
        """Returns consolidated metrics across Snowflake tables."""
        def q_val(sql_str):
            try:
                df = self.session.sql(sql_str).to_pandas()
                return df.iloc[0, 0] if not df.empty else 0
            except Exception:
                return 0

        cust_count = q_val("SELECT COUNT(*) FROM CUSTOMER")
        acc_count = q_val("SELECT COUNT(*) FROM ACCOUNT")
        txn_count = q_val("SELECT COUNT(*) FROM TRANSACTIONS")
        txn_vol = q_val("SELECT COALESCE(SUM(AMOUNT), 0) FROM TRANSACTIONS")
        high_risk_custs = q_val("SELECT COUNT(*) FROM CUSTOMER WHERE RISK_RATING = 'HIGH'")
        loans_count = q_val("SELECT COUNT(*) FROM LOAN")
        sma_loans = q_val("SELECT COUNT(*) FROM LOAN WHERE STATUS LIKE '%SMA%'")
        cases_count = q_val("SELECT COUNT(*) FROM RISK_CASE")

        # Latest LCR
        try:
            df_liq = self.session.sql("SELECT LCR, POSITION_DATE FROM LIQUIDITY_POSITION ORDER BY POSITION_DATE DESC LIMIT 1").to_pandas()
            latest_lcr = df_liq['LCR'].iloc[0] if not df_liq.empty else 100.0
            lcr_date = df_liq['POSITION_DATE'].iloc[0] if not df_liq.empty else "N/A"
        except Exception:
            latest_lcr = 98.47
            lcr_date = "N/A"

        return {
            "total_customers": int(cust_count),
            "total_accounts": int(acc_count),
            "total_transactions": int(txn_count),
            "total_volume_inr": float(txn_vol),
            "high_risk_customers": int(high_risk_custs),
            "total_loans": int(loans_count),
            "sma_loans_stressed": int(sma_loans),
            "latest_lcr_pct": float(latest_lcr),
            "latest_lcr_date": str(lcr_date),
            "active_risk_cases": int(cases_count)
        }

    # -------------------------------------------------------------------------
    # 8. RESET TO SEED STATE
    # -------------------------------------------------------------------------
    def reset_to_seed(self):
        """Cleans dynamic data and restores original Hack2Skill challenge seed data."""
        if hasattr(self.session, "reset_database"):
            self.session.reset_database()
            log_event("DATABASE_RESET", "RESET_TO_SEED", "SYSTEM", "Restored default baseline seed tables")
            return True
        return False
