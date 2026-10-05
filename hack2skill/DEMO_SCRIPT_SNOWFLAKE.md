# 🎬 RiskGuard AI: The 3-Minute Snowflake Winning Demo Script

> **Hack2Skill × Snowflake CoCo CLI 2026**  
> **Core Journey:** $\text{Signal} \longrightarrow \text{Evidence} \longrightarrow \text{Regulation} \longrightarrow \text{Finding} \longrightarrow \text{Report}$

---

## ⏱️ Step-by-Step Live Presentation Guide

### [0:00 - 0:30] Step 1: The Executive Signal
- **Action:** Open `http://localhost:8501`. Show **Page 1 — Executive Risk Dashboard**.
- **Talking Point:**  
  *"Judges, this is RiskGuard AI running natively on Snowflake Data Cloud. In our executive dashboard, we see 82 high-risk AML signals, 24 stressed credit facilities, and our Basel III Liquidity Coverage Ratio in critical alert at 98.47%. Notice our top risk customers ranked via Snowflake analytical window features: C1007 is at the top with a risk score of 92."*

---

### [0:30 - 1:15] Step 2 & 3: Cortex Analyst & Transparent Score Decomposition
- **Action:** Switch to **Page 2 — AI Copilot**. Click preset:  
  `'Why is C1007 high risk?'` or `'Identify customers with unusual transaction activity in the last 24 hours'`. Click **⚡ Ask Cortex Copilot**.
- **Talking Point:**  
  *"I ask a natural-language question. Instead of calling a black-box LLM, Snowflake Cortex Analyst queries our structured semantic model.  
  Look at the result: **🔴 HIGH RISK — Score 92**.  
  And here is why RiskGuard wins on explainability: look at this score breakdown:*
  ```
  AML Score = 92
  +30 unusual transaction size (> 3 std dev)
  +25 high transaction velocity (burst in 1 hr)
  +25 24-hour concentration (> ₹5 Lakh)
  +10 cross-border activity (UAE & SG)
  +2  failed status
  ----------------------------------------
   92 HIGH RISK
  ```
  *The judge doesn't have to guess why AI flagged this customer. Every point is backed by mathematics."*

---

### [1:15 - 1:55] Step 4 & 5: Cortex Search Grounded Evidence
- **Action:** Point out the **Primary Transaction Evidence table** and the **Applicable Regulatory Basis**.
- **Talking Point:**  
  *"Look at the transaction evidence: TXN-S001 of ₹4.8 Lakh arrives via IMPS at 10:00. Just 25 minutes later, TXN-S002 of ₹4.7 Lakh is swept out to CoinBridge P2P in UAE. Another 25 minutes later, TXN-S003 of ₹4.95 Lakh is swept out to CryptoEx in Singapore.  
  Then, Snowflake **Cortex Search** retrieves the exact regulatory mandate: **RBI Master Direction Section 4.2: Velocity Anomalies & Pass-Through Mule Accounts** with 94% relevance. Zero hallucination; zero unsupported claims."*

---

### [1:55 - 2:25] Step 6: Fraud Investigation & Counterparty Network Graph
- **Action:** Switch to **Page 3 — Fraud Investigation & Network Graph**.
- **Talking Point:**  
  *"Now we switch to our Fraud Investigation page. RiskGuard renders the directed counterparty fund flow graph in real time:  
  **CP-221 (Swift Enterprises)** funnels ₹4.8 Lakh into **C1007**, which immediately splits and funnels outbound to **CP-223 in UAE** and **CP-224 in Singapore**.  
  A compliance investigator understands the entire mule layering topology in two seconds."*

---

### [2:25 - 3:00] Step 7 & 8: Regulatory Report & Non-Repudiation
- **Action:** Switch to **Page 5 — Regulatory Report & Case Vault**. Click **📥 Generate & Download PDF Filing**.
- **Talking Point:**  
  *"Finally, the compliance officer needs to file with the regulator. With one click, RiskGuard compiles an official 11-section Suspicious Transaction Report (STR) compliant with FIU-IND and FinCEN specifications. It includes executive summary, transaction tables, statutory analysis, and a SHA-256 cryptographic audit stamp.  
  From question to signal to evidence to regulation to report — in under 3 minutes. That is RiskGuard AI on Snowflake. Thank you!"*
