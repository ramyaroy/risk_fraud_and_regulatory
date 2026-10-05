# 🎤 RiskGuard Copilot: Hack2Skill Pitch & Demo Playbook

---

## Part 1: The 2-Minute Winning Elevator Pitch

> **Tip for Delivery:** Speak with conviction, confidence, and pace. Emphasize the phrase *"Evidence-First"* rather than *"AI Chatbot"*.

### [0:00 - 0:30] The Hook & The Critical Problem
"Respected judges, every single day, compliance officers at banks and NBFCs drown in thousands of false positives and manual investigations across money laundering, credit distress, and liquidity emergencies. 
Today, when an alert fires, a compliance officer spends **three to five business days** exporting spreadsheets, manually calculating ratios, searching through 200-page RBI and Basel III PDFs, and drafting regulatory filings. 

The industry’s first instinct was to plug in generic AI chatbots. But in banking, a generic chatbot is dangerous: it hallucinates section numbers, invents rules, and has zero provenance. In banking, an unverified AI answer is a multi-million-dollar regulatory fine."

### [0:30 - 1:10] The Solution & Innovation
"That is why we built **RiskGuard Copilot: an evidence-first AI copilot that turns financial risk signals into explainable, audit-ready regulatory findings.**

RiskGuard doesn't just answer questions. It enforces a strict, unbroken mathematical lineage:
$$\mathbf{Signal} \longrightarrow \mathbf{Evidence} \longrightarrow \mathbf{Detected\ Pattern} \longrightarrow \mathbf{Policy / Regulation} \longrightarrow \mathbf{Finding} \longrightarrow \mathbf{Audit\ Report}$$

Technically, we solved this with **Dual-Path Hybrid RAG**. We do NOT put transactional data into vector embeddings where math fails. Instead, structured transactions and credit metrics are queried through **parameterized SQL**, while regulatory circulars are retrieved through **BM25 and dense TF-IDF vectors**. We then fuse both into our **Interactive Evidence Graph**."

### [1:10 - 1:50] The Demo Proof & Real-World Impact
"In our live working prototype:
A compliance user asks in plain English: *'Show me high-risk transactions from the last 7 days and explain why they indicate AML risk.'*
Within seconds, RiskGuard:
1. Queries the transaction ledger using Isolation Forest anomaly detection.
2. Uncovers a pass-through mule account moving ₹42.8 Lakh across 17 transactions in 7 days — draining funds in under 30 minutes.
3. Retrieves **RBI Master Direction Section 4.2** and **PMLA Section 12**.
4. Generates an interactive **Evidence Graph** linking every rupee to the exact statutory clause.
5. And with one click, compiles an official, signed **Suspicious Transaction Report (STR)** as a downloadable PDF stamped with an immutable **SHA-256 cryptographic hash**."

### [1:50 - 2:00] The Closing Punchline
"RiskGuard reduces investigation and filing time from **days to seconds**, while guaranteeing 100% audit explainability. We aren't building a chatbot; we are building the autonomous, governed future of financial compliance. Thank you!"

---

## Part 2: The 3-Minute Live Screen Demo Script

| Timestamp | Screen Action | What You Say to the Judges |
| :--- | :--- | :--- |
| **0:00 - 0:30** | Open `http://localhost:8501`. Point out the Top Header Banner & Live KPI Cards. | *"Here is the live RiskGuard Copilot dashboard. Notice our real-time KPI bar: 8 active risk signals detected across AML, Credit, and Liquidity, and our SHA-256 cryptographic audit ledger is verified green."* |
| **0:30 - 1:15** | Go to **Tab 1: Ask RiskGuard**. Click preset: `Show me high-risk transactions from the last 7 days and explain why they may indicate AML risk`. Click **🚀 Analyze with RiskGuard**. | *"Let's test the exact core problem. I ask in plain English for high-risk transactions indicating AML risk. Watch the live 5-stage pipeline: Signal $\to$ Evidence $\to$ Policy $\to$ Finding $\to$ Report. RiskGuard immediately flags Customer CUST-10482, Rahul Sharma."* |
| **1:15 - 1:45** | Scroll down to the **Why Flagged** section, **Primary Evidence Table**, and **Policy Citations**. | *"Look at the explainability here: It shows 17 transactions totaling ₹42.8 Lakh against a declared monthly profile of ₹5 Lakh — an 8.56x turnover surge. It highlights TXN-98231, TXN-98239, showing RTGS deposits swept out to crypto gateways in under 23 minutes. Under Policy Evidence, it cites RBI KYC/AML Master Direction Section 4.2.1."* |
| **1:45 - 2:15** | Scroll to the right column: **Interactive Evidence Graph** & **Provenance Hierarchy Tree**. | *"This is our killer differentiator: The Evidence Graph. Judges can see the exact DAG linking Finding $\to$ Signal $\to$ Transactions $\to$ Customer Profile $\to$ Regulatory Clause. Every single statement has a traceable provenance root."* |
| **2:15 - 2:40** | Click **"⚡ Generate Official Report & PDF Certificate"**. Click **"📥 Download Official PDF"**. | *"Now comes the regulatory output. A compliance officer clicks Generate Report. RiskGuard compiles an official 11-section Suspicious Transaction Report (STR) compliant with FIU-IND, complete with evidence tables, statutory analysis, and an embedded SHA-256 integrity hash."* |
| **2:40 - 3:00** | Click **Tab 6: Cryptographic Audit Ledger**. Show the SHA-256 hash chain and verification button. | *"Finally, every query and action is written to an immutable SHA-256 blockchain-style ledger. When auditors examine the bank, they can verify non-repudiation in one click. That is complete, governed, end-to-end execution."* |

---

## Part 3: Defensive Judge Q&A Playbook

### Q1: "Why not just put all transaction data into a Vector Database with Chroma or Pinecone?"
**Your Answer:**
> *"That is the number one architectural mistake teams make in GenAI finance. Vector databases perform semantic similarity on text; they cannot perform precise arithmetic, temporal window aggregations, or strict balance thresholds. If you ask a vector DB 'Find accounts where sum(amount) > ₹10 Lakh', it approximates instead of computing. 
> RiskGuard uses a **Dual-Path Hybrid Architecture**: Parameterized SQL for deterministic math and ledger queries, and BM25 + Vector RAG for statutory legal texts. We get the best of both worlds with zero math hallucinations."*

### Q2: "How do you guarantee the LLM won't hallucinate a non-existent regulation or section number?"
**Your Answer:**
> *"We enforce a strict **Anti-Hallucination Guardrail Protocol**:
> 1. The LLM is strictly context-bounded; it is only permitted to cite policy chunks returned by our BM25/TF-IDF retriever.
> 2. If no matching statutory clause or transaction record is retrieved with high confidence, the system triggers an explicit refusal: 'No verified policy evidence found'.
> 3. Every citation is programmatically validated against our indexed master directory before the finding is finalized."*

### Q3: "How does this scale to millions of banking transactions per day?"
**Your Answer:**
> *"RiskGuard is decoupled into three tiers:
> 1. High-throughput stream processing or SQL database indexing (PostgreSQL / Snowflake / BigQuery) handles real-time transaction ingestion.
> 2. Our Scikit-Learn Isolation Forest and rule detectors run as asynchronous microservices, flagging candidate anomalies.
> 3. The GenAI Reasoning and Evidence Graph generation only execute on the high-risk candidate subset (< 1% of total volume), making LLM inference cost-effective and sub-second fast."*

### Q4: "Can this handle other risk domains beyond AML?"
**Your Answer:**
> *"Yes! Notice Tabs 3 and 4 in our live app: We have already built and demonstrated **Credit Risk Early Warning** (tracking SMA-0, SMA-1, SMA-2, and DSCR covenant erosion under RBI Prudential guidelines) and **Treasury Liquidity Risk** (daily Basel III LCR and HQLA stress monitoring). The architecture is completely modular."*
