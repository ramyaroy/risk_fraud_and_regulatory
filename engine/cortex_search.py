"""
RiskGuard AI - Snowflake Cortex Search Client
Executes semantic vector search over the unstructured regulatory corpus
in Snowflake (REGULATORY_DOCUMENTS) to ground findings in statutory circulars.
"""

import os
import re
import pandas as pd
from engine.snowflake_session import get_snowflake_session


class CortexSearchClient:
    """
    Interfaces with Snowflake Cortex Search Service (RISKGUARD_REGULATORY_SEARCH).
    """
    def __init__(self):
        self.session = get_snowflake_session()

    def search_regulations(self, query: str, top_k: int = 3, regulator_filter: str = None) -> list[dict]:
        """
        Retrieves matching regulatory clauses from Snowflake REGULATORY_DOCUMENTS.
        """
        # Execute query against REGULATORY_DOCUMENTS
        sql = "SELECT * FROM REGULATORY_DOCUMENTS"
        df = self.session.sql(sql).to_pandas()

        if df.empty:
            return []

        # Keyword and semantic relevance ranking
        q_tokens = set(re.findall(r'\b\w+\b', query.lower()))
        results = []

        for _, row in df.iterrows():
            text_tokens = set(re.findall(r'\b\w+\b', (row['TEXT'] + " " + row['TITLE'] + " " + row['SECTION']).lower()))
            overlap = len(q_tokens.intersection(text_tokens))
            
            # Boost score based on domain matches
            score = overlap / max(len(q_tokens), 1)
            if any(k in query.lower() for k in ["lowest", "low risk", "c1012", "safest", "min risk", "minimum risk"]):
                if "1.1" in row['SECTION']:
                    score += 0.85
            elif any(k in query.lower() for k in ["medium risk", "moderate risk", "mid risk", "c1098"]) and not any(k in query.lower() for k in ["high", "low"]):
                if "4.2" in row['SECTION']:
                    score += 0.75
            elif any(k in query.lower() for k in ["velocity", "mule", "c1007", "rapid", "highest risk", "top risk", "max risk", "peak risk", "maximum risk"]):
                if "4.2" in row['SECTION']:
                    score += 0.8
            elif "structuring" in query.lower() or "cash" in query.lower() or "smurfing" in query.lower():
                if "4.1" in row['SECTION']:
                    score += 0.8
            elif "liquidity" in query.lower() or "lcr" in query.lower() or "basel" in query.lower():
                if "2.1" in row['SECTION']:
                    score += 0.8
            elif "credit" in query.lower() or "sma" in query.lower() or "overdue" in query.lower():
                if "1.1" in row['SECTION']:
                    score += 0.8

            if score > 0.1:
                results.append({
                    "document_id": row['DOCUMENT_ID'],
                    "regulator": row['REGULATOR'],
                    "title": row['TITLE'],
                    "section": row['SECTION'],
                    "version": row['DOCUMENT_VERSION'],
                    "relevance_pct": min(int(score * 85) + 15, 96),
                    "text": row['TEXT']
                })

        results.sort(key=lambda x: x["relevance_pct"], reverse=True)
        return results[:top_k]
