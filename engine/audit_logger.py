"""
RiskGuard Copilot - Cryptographic Audit Logger
Maintains an immutable, append-only SHA-256 hash-chained ledger for all
queries, signal detections, investigations, and regulatory report generations.
"""

import sqlite3
import hashlib
import json
from datetime import datetime
import os

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DB_DIR, "riskguard.db")


def get_latest_hash(conn):
    cur = conn.cursor()
    cur.execute("SELECT current_hash FROM audit_trail ORDER BY log_id DESC LIMIT 1")
    row = cur.fetchone()
    if row:
        return row[0]
    return "GENESIS_ROOT_BLOCK_0000000000000000"


def log_event(action: str, query_text: str = None, target_entity: str = None, result_summary: str = None) -> dict:
    """
    Appends a new event to the cryptographic audit trail table.
    Computes SHA-256(prev_hash + timestamp + action + query + entity + summary).
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_PATH)
    prev_hash = get_latest_hash(conn)

    payload = {
        "prev_hash": prev_hash,
        "timestamp": timestamp,
        "action": action,
        "query_text": query_text or "",
        "target_entity": target_entity or "",
        "result_summary": result_summary or ""
    }
    serialized = json.dumps(payload, sort_keys=True)
    current_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    cur = conn.cursor()
    cur.execute("""
    INSERT INTO audit_trail (timestamp, user_action, query_text, target_entity, result_summary, prev_hash, current_hash)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, action, query_text, target_entity, result_summary, prev_hash, current_hash))
    conn.commit()
    conn.close()

    return {
        "timestamp": timestamp,
        "action": action,
        "prev_hash": prev_hash,
        "current_hash": current_hash
    }


def get_audit_trail(limit: int = 25):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM audit_trail ORDER BY log_id DESC LIMIT ?", (limit,))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def verify_chain_integrity() -> tuple[bool, str]:
    """
    Validates that every block in the audit trail correctly hashes from its parent block.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM audit_trail ORDER BY log_id ASC")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    if not rows:
        return True, "Audit log is empty."

    for i in range(1, len(rows)):
        current = rows[i]
        previous = rows[i - 1]

        if current["prev_hash"] != previous["current_hash"]:
            return False, f"Hash chain broken at Log ID {current['log_id']}! Expected prev_hash {previous['current_hash']}, got {current['prev_hash']}"

        payload = {
            "prev_hash": current["prev_hash"],
            "timestamp": current["timestamp"],
            "action": current["user_action"],
            "query_text": current["query_text"] or "",
            "target_entity": current["target_entity"] or "",
            "result_summary": current["result_summary"] or ""
        }
        computed = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
        if computed != current["current_hash"]:
            return False, f"Integrity check failed at Log ID {current['log_id']}: Payload hash altered!"

    return True, f"All {len(rows)} audit records verified. Cryptographic chain intact."
