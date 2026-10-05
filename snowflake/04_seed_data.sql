-- ============================================================================
-- 🛡️ RISKGUARD AI: Banking Risk, Fraud & Regulatory Intelligence Copilot
-- Challenge: Hack2Skill × Snowflake CoCo CLI 2026
-- Script 04: Production-Grade Synthetic Financial Data Seeder
-- ============================================================================

USE DATABASE RISKGUARD;
USE SCHEMA RISKGUARD.DATA;

-- 1. SEED COUNTERPARTIES
INSERT OVERWRITE INTO COUNTERPARTY (COUNTERPARTY_ID, NAME, COUNTRY, INDUSTRY, RISK_RATING, SANCTIONS_FLAG)
VALUES
    ('CP-221', 'Swift Enterprises Commercial Ltd', 'IN', 'Wholesale Trade', 'LOW', FALSE),
    ('CP-223', 'CoinBridge P2P Digital Exchange', 'AE', 'Cryptocurrency Gateway', 'HIGH', FALSE),
    ('CP-224', 'CryptoEx Global Merchant Pay', 'SG', 'Digital Wallet Clearing', 'HIGH', FALSE),
    ('CP-301', 'Reserve Bank Clearing System', 'IN', 'Central Banking', 'LOW', FALSE),
    ('CP-402', 'Cyprus Island Offshore Holdings', 'CY', 'Shell Investment', 'CRITICAL', FALSE),
    ('CP-505', 'National Logistics Infrastructure', 'IN', 'Transportation', 'LOW', FALSE),
    ('CP-601', 'Apex Marine Raw Supplies', 'IN', 'Manufacturing', 'MEDIUM', FALSE);

-- 2. SEED CUSTOMERS
INSERT OVERWRITE INTO CUSTOMER (CUSTOMER_ID, CUSTOMER_TYPE, CUSTOMER_NAME, DOB, COUNTRY, CITY, OCCUPATION, ANNUAL_INCOME, CUSTOMER_SINCE, RISK_RATING, KYC_STATUS)
VALUES
    ('C1007', 'RETAIL', 'Rahul S. Sharma (QuickTrade Sole Prop)', '1988-04-12', 'IN', 'Mumbai', 'Sole Proprietor', 600000.00, '2023-03-15', 'HIGH', 'VERIFIED'),
    ('C1032', 'CORPORATE', 'Apex Horizon Global Ltd', '2015-09-20', 'IN', 'New Delhi', 'Import-Export', 18000000.00, '2021-01-10', 'HIGH', 'VERIFIED'),
    ('C1098', 'MSME', 'Starlight FinTech Enterprises', '2020-11-05', 'IN', 'Bengaluru', 'Payment Aggregator', 12000000.00, '2022-07-18', 'MEDIUM', 'VERIFIED'),
    ('C1045', 'CORPORATE', 'BlueOcean Infrastructure Pvt Ltd', '2012-06-22', 'IN', 'Hyderabad', 'Infrastructure Developer', 85000000.00, '2019-05-14', 'HIGH', 'VERIFIED'),
    ('C1012', 'CORPORATE', 'Zenith Pharma Logistics Ltd', '2010-02-18', 'IN', 'Ahmedabad', 'Pharmaceuticals', 45000000.00, '2018-10-30', 'LOW', 'VERIFIED'),
    ('C1088', 'RETAIL', 'Sunita Verma', '1975-08-30', 'IN', 'Pune', 'Consultant', 800000.00, '2017-04-11', 'HIGH', 'PENDING_RE_KYC');

-- 3. SEED ACCOUNTS
INSERT OVERWRITE INTO ACCOUNT (ACCOUNT_ID, CUSTOMER_ID, ACCOUNT_TYPE, CURRENCY, OPEN_DATE, CURRENT_BALANCE, AVAILABLE_BALANCE, STATUS, BRANCH_ID)
VALUES
    ('ACC-1007-01', 'C1007', 'CURRENT', 'INR', '2023-03-15', 38200.00, 38200.00, 'ACTIVE', 'BR-MUM-01'),
    ('ACC-1032-01', 'C1032', 'CURRENT', 'INR', '2021-01-10', 3125000.00, 3125000.00, 'ACTIVE', 'BR-DEL-04'),
    ('ACC-1098-01', 'C1098', 'CURRENT', 'INR', '2022-07-18', 840000.00, 840000.00, 'ACTIVE', 'BR-BLR-02'),
    ('ACC-1045-01', 'C1045', 'TERM_LOAN', 'INR', '2019-05-14', 1250000.00, 1250000.00, 'SURVEILLANCE', 'BR-HYD-01'),
    ('ACC-1012-01', 'C1012', 'CURRENT', 'INR', '2018-10-30', 8950000.00, 8950000.00, 'ACTIVE', 'BR-AHM-01'),
    ('ACC-1088-01', 'C1088', 'SAVINGS', 'INR', '2017-04-11', 1860000.00, 1860000.00, 'DORMANT', 'BR-PUN-02');

-- 4. SEED TRANSACTIONS
-- Includes the prompt's exact scenario for C1007 (TXN-S001, TXN-S002, TXN-S003)
INSERT OVERWRITE INTO TRANSACTION (
    TRANSACTION_ID, ACCOUNT_ID, CUSTOMER_ID, TRANSACTION_TS, TRANSACTION_TYPE, DIRECTION, 
    AMOUNT, CURRENCY, CHANNEL, MERCHANT_CATEGORY, COUNTERPARTY_ID, COUNTERPARTY_COUNTRY, 
    DEVICE_ID, IP_COUNTRY, GEO_LAT, GEO_LON, TRANSACTION_STATUS
)
VALUES
    -- C1007: Rapid pass-through fund movement burst (AML Score = 90-92 HIGH)
    ('TXN-S001', 'ACC-1007-01', 'C1007', '2026-10-04 10:00:00', 'TRANSFER', 'INBOUND', 480000.00, 'INR', 'IMPS', 'Commercial Advance', 'CP-221', 'IN', 'DEV-991', 'IN', 19.0760, 72.8777, 'SUCCESS'),
    ('TXN-S002', 'ACC-1007-01', 'C1007', '2026-10-04 10:25:00', 'TRANSFER', 'OUTBOUND', 470000.00, 'INR', 'IMPS', 'P2P Settlement', 'CP-223', 'AE', 'DEV-991', 'AE', 25.2048, 55.2708, 'SUCCESS'),
    ('TXN-S003', 'ACC-1007-01', 'C1007', '2026-10-04 10:50:00', 'TRANSFER', 'OUTBOUND', 495000.00, 'INR', 'IMPS', 'Digital Clearing', 'CP-224', 'SG', 'DEV-991', 'SG', 1.3521, 103.8198, 'SUCCESS'),
    ('TXN-S004', 'ACC-1007-01', 'C1007', '2026-10-04 11:15:00', 'TRANSFER', 'INBOUND', 460000.00, 'INR', 'IMPS', 'Consultancy Fee', 'CP-221', 'IN', 'DEV-991', 'IN', 19.0760, 72.8777, 'SUCCESS'),
    ('TXN-S005', 'ACC-1007-01', 'C1007', '2026-10-04 11:40:00', 'TRANSFER', 'OUTBOUND', 455000.00, 'INR', 'IMPS', 'Wallet Drain', 'CP-223', 'AE', 'DEV-991', 'AE', 25.2048, 55.2708, 'SUCCESS'),

    -- C1032: Multi-Branch Cash Structuring (Smurfing below ₹10 Lakh statutory CTR)
    ('TXN-STR01', 'ACC-1032-01', 'C1032', '2026-10-01 10:15:00', 'DEPOSIT', 'INBOUND', 980000.00, 'INR', 'CASH', 'Cash Counter 1', NULL, 'IN', 'BRANCH-01', 'IN', 28.6139, 77.2090, 'SUCCESS'),
    ('TXN-STR02', 'ACC-1032-01', 'C1032', '2026-10-01 15:30:00', 'DEPOSIT', 'INBOUND', 950000.00, 'INR', 'CASH', 'Cash Counter 3', NULL, 'IN', 'BRANCH-04', 'IN', 28.6289, 77.2180, 'SUCCESS'),
    ('TXN-STR03', 'ACC-1032-01', 'C1032', '2026-10-02 11:20:00', 'DEPOSIT', 'INBOUND', 975000.00, 'INR', 'CASH', 'Cash Counter 2', NULL, 'IN', 'BRANCH-02', 'IN', 28.6500, 77.1900, 'SUCCESS'),
    ('TXN-STR04', 'ACC-1032-01', 'C1032', '2026-10-03 12:45:00', 'DEPOSIT', 'INBOUND', 960000.00, 'INR', 'CASH', 'Branch Counter 1', NULL, 'IN', 'BRANCH-NOI', 'IN', 28.5355, 77.3910, 'SUCCESS'),

    -- C1088: Dormant account reactivation via high-risk offshore entity
    ('TXN-DORM01', 'ACC-1088-01', 'C1088', '2026-10-02 09:30:00', 'TRANSFER', 'INBOUND', 1850000.00, 'INR', 'WIRE', 'Retainer Remittance', 'CP-402', 'CY', 'DEV-442', 'CY', 35.1856, 33.3823, 'SUCCESS'),

    -- Baseline Normal Transactions
    ('TXN-NORM01', 'ACC-1012-01', 'C1012', '2026-10-03 10:00:00', 'TRANSFER', 'INBOUND', 1500000.00, 'INR', 'RTGS', 'Bulk Pharma Lot', 'CP-505', 'IN', 'DEV-881', 'IN', 23.0225, 72.5714, 'SUCCESS'),
    ('TXN-NORM02', 'ACC-1012-01', 'C1012', '2026-10-04 14:30:00', 'TRANSFER', 'OUTBOUND', 950000.00, 'INR', 'NEFT', 'Freight Settlement', 'CP-601', 'IN', 'DEV-881', 'IN', 23.0225, 72.5714, 'SUCCESS');

-- 5. SEED LOANS & REPAYMENTS (CREDIT RISK EWS)
INSERT OVERWRITE INTO LOAN (LOAN_ID, CUSTOMER_ID, PRODUCT_TYPE, PRINCIPAL_AMOUNT, OUTSTANDING_AMOUNT, INTEREST_RATE, TENURE_MONTHS, START_DATE, MATURITY_DATE, STATUS)
VALUES
    ('LN-8802', 'C1045', 'COMMERCIAL_TERM_LOAN', 450000000.00, 412000000.00, 11.25, 84, '2022-06-20', '2029-06-20', 'SMA_1'),
    ('LN-7719', 'C1032', 'WORKING_CAPITAL', 50000000.00, 48500000.00, 10.50, 36, '2023-01-10', '2026-01-10', 'SMA_0'),
    ('LN-9901', 'C1012', 'COMMERCIAL_TERM_LOAN', 120000000.00, 68000000.00, 8.90, 60, '2021-11-05', '2026-11-05', 'STANDARD');

INSERT OVERWRITE INTO LOAN_REPAYMENT (PAYMENT_ID, LOAN_ID, DUE_DATE, PAYMENT_DATE, DUE_AMOUNT, PAID_AMOUNT, DAYS_PAST_DUE)
VALUES
    ('PAY-8802-01', 'LN-8802', '2026-08-30', '2026-08-30', 8500000.00, 8500000.00, 0),
    ('PAY-8802-02', 'LN-8802', '2026-09-30', NULL, 8500000.00, 0.00, 36),
    ('PAY-8802-03', 'LN-8802', '2026-10-30', NULL, 8500000.00, 0.00, 48),
    ('PAY-7719-01', 'LN-7719', '2026-10-01', NULL, 1200000.00, 0.00, 18),
    ('PAY-9901-01', 'LN-9901', '2026-10-01', '2026-10-01', 2500000.00, 2500000.00, 0);

-- 6. SEED LIQUIDITY POSITIONS (BASEL III LCR)
INSERT OVERWRITE INTO LIQUIDITY_POSITION (POSITION_DATE, BUSINESS_UNIT, HQLA, CASH_INFLOW, CASH_OUTFLOW, NET_CASH_FLOW, DEPOSIT_BALANCE, SHORT_TERM_FUNDING, LCR, NSFR)
VALUES
    ('2026-10-01', 'TREASURY_MAIN', 52625000.00, 11200000.00, 58000000.00, -46800000.00, 1450000000.00, 280000000.00, 112.45, 108.20),
    ('2026-10-02', 'TREASURY_MAIN', 51730000.00, 11700000.00, 59500000.00, -47800000.00, 1435000000.00, 285000000.00, 108.22, 107.50),
    ('2026-10-03', 'TREASURY_MAIN', 49475000.00, 13700000.00, 61200000.00, -47500000.00, 1410000000.00, 295000000.00, 104.16, 105.10),
    ('2026-10-04', 'TREASURY_MAIN', 46480000.00, 21300000.00, 68500000.00, -47200000.00, 1345000000.00, 310000000.00, 98.47, 101.80),
    ('2026-10-05', 'TREASURY_MAIN', 46865000.00, 19900000.00, 67200000.00, -47300000.00, 1340000000.00, 315000000.00, 99.08, 102.10);

-- 7. SEED REGULATORY DOCUMENTS CORPUS (FOR CORTEX SEARCH)
INSERT OVERWRITE INTO REGULATORY_DOCUMENTS (DOCUMENT_ID, DOCUMENT_TYPE, REGULATOR, JURISDICTION, TITLE, SECTION, EFFECTIVE_DATE, DOCUMENT_VERSION, TEXT)
VALUES
    ('REG-AML-4.2', 'REGULATION', 'RBI', 'INDIA', 'Master Direction - Know Your Customer (KYC) Direction, 2016', 'Section 4.2: Velocity Anomalies & Pass-Through Mule Accounts', '2016-02-25', 'v4.2',
     'Section 4.2 Velocity Anomalies & Mule Accounts: Regulated Entities (REs) must institute automated monitoring capable of detecting rapid pass-through velocity. Accounts exhibiting sudden credits followed immediately by equivalent debits to unrelated digital intermediaries or crypto accounts within minutes, leaving nominal balances, must be classified as potential mule accounts. Mandatory Enhanced Due Diligence (EDD) and Suspicious Transaction Report (STR) filing under PMLA Section 12 is required within 7 days.'),

    ('REG-AML-4.1.2', 'REGULATION', 'RBI', 'INDIA', 'Master Direction - KYC and Cash Reporting', 'Section 4.1.2: Cash Structuring & Smurfing Evasion', '2016-02-25', 'v4.2',
     'Section 4.1.2 Structuring Evasion: Where a customer conducts multiple transactions in cash or currency in amounts just below the statutory reporting threshold of Rupees Ten Lakh (INR 10,00,000) within 1 to 7 calendar days to evade statutory reporting, REs shall aggregate transactions and file an immediate STR to FIU-IND.'),

    ('REG-BASEL-2.1', 'REGULATION', 'BCBS', 'GLOBAL', 'Basel III: The Liquidity Coverage Ratio and liquidity risk monitoring tools', 'Section 2.1: Liquidity Coverage Ratio (LCR) Mandate', '2013-01-01', 'BCBS 238',
     'Section 2.1 LCR Mandate: The Liquidity Coverage Ratio requires institutions to maintain an unencumbered stock of High Quality Liquid Assets (HQLA) that equals or exceeds total net cash outflows over a 30-day severe stress period (LCR >= 100%). Any drop below the 105% supervisory early warning buffer requires immediate ALCO notification. A drop below 100% represents a direct statutory breach requiring central bank reporting.'),

    ('REG-CREDIT-1.1', 'REGULATION', 'RBI', 'INDIA', 'Prudential Framework for Resolution of Stressed Assets', 'Section 1.1: Early Warning Signals & Special Mention Accounts', '2019-06-07', 'DBR.No.BP.BC.45',
     'Section 1.1 SMA Classification: Lenders shall recognize incipient stress in loan accounts immediately: SMA-0 (1-30 days overdue), SMA-1 (31-60 days overdue), SMA-2 (61-90 days overdue). Where a borrower crosses into SMA-1 with a Debt Service Coverage Ratio (DSCR) below 1.15x, lenders must initiate a Corrective Action Plan (CAP) under the Inter-Creditor Agreement.');

USE SCHEMA RISKGUARD.GOVERNANCE;

-- 8. SEED RISK EVIDENCE (GROUNDED AUDIT EVIDENCE)
INSERT OVERWRITE INTO RISK_EVIDENCE (EVIDENCE_ID, CASE_ID, EVIDENCE_TYPE, SOURCE_TABLE, SOURCE_ID, EVIDENCE_TEXT, RISK_SCORE, CREATED_BY)
VALUES
    ('EVID-001', 'CASE-2026-0042', 'TRANSACTION', 'TRANSACTION', 'TXN-S001', 'Inbound IMPS credit of ₹4,80,000 at 10:00:00 from Swift Enterprises', 30.0, 'AML_DETECTOR_V2'),
    ('EVID-002', 'CASE-2026-0042', 'TRANSACTION', 'TRANSACTION', 'TXN-S002', 'Outbound IMPS debit of ₹4,70,000 at 10:25:00 to CoinBridge P2P (UAE) within 25 minutes', 25.0, 'AML_DETECTOR_V2'),
    ('EVID-003', 'CASE-2026-0042', 'TRANSACTION', 'TRANSACTION', 'TXN-S003', 'Outbound IMPS debit of ₹4,95,000 at 10:50:00 to CryptoEx (Singapore) within 25 minutes', 25.0, 'AML_DETECTOR_V2'),
    ('EVID-004', 'CASE-2026-0042', 'POLICY', 'REGULATORY_DOCUMENTS', 'REG-AML-4.2', 'RBI Master Direction §4.2: Velocity Anomalies & Pass-Through Mule Accounts', 10.0, 'CORTEX_SEARCH'),
    ('EVID-005', 'CASE-2026-0042', 'CUSTOMER', 'CUSTOMER', 'C1007', 'Declared monthly turnover is ₹50,000 (INR 6.0 Lakh annual). 24h velocity is ₹23.6 Lakh (393% above declared profile)', 10.0, 'CORTEX_ANALYST');

-- 9. SEED RISK CASE
INSERT OVERWRITE INTO RISK_CASE (CASE_ID, CUSTOMER_ID, RISK_DOMAIN, RISK_SCORE, SEVERITY, STATUS, FINDING, RECOMMENDATION, REVIEWER, AUDIT_HASH)
VALUES
    ('CASE-2026-0042', 'C1007', 'AML_FRAUD', 92.0, 'HIGH', 'INVESTIGATING',
     'Customer C1007 exhibits classic digital mule pass-through velocity. Multiple high-value IMPS inbound credits are drained within 25 minutes to cross-border crypto aggregators in UAE and Singapore, leaving a nominal account balance.',
     'Immediate debit freeze review, execute mandatory Enhanced Due Diligence (EDD), and submit Suspicious Transaction Report (STR) to FIU-IND.',
     'Senior Compliance Analyst #CO-902',
     'SHA256:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069');
