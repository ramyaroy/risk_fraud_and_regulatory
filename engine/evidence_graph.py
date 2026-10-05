"""
RiskGuard Copilot - Evidence Graph & Provenance Engine
Constructs the full end-to-end provenance graph:
Signal -> Transaction Evidence -> Customer Profile -> Detected Pattern -> Policy/Regulation -> Finding -> Audit Report
Generates interactive Plotly graph visualizations and hierarchical provenance trees.
"""

import json
import hashlib
from typing import Optional


class EvidenceGraphBuilder:
    """
    Builds structured graph models and interactive visualizations for risk provenance.
    """

    @staticmethod
    def build_aml_graph(finding_id: str, customer_id: str, customer_name: str, 
                        pattern_name: str, txns: list[dict], 
                        policy_sections: list[dict], confidence: float = 0.94) -> dict:
        """
        Builds the Evidence Graph for AML / Fraud investigations.
        """
        nodes = []
        edges = []

        # 1. Finding Root Node
        nodes.append({
            "id": finding_id,
            "label": f"Finding #{finding_id}",
            "type": "Finding",
            "color": "#ef4444",  # Red
            "size": 30,
            "details": f"Confidence: {int(confidence*100)}% | Status: OPEN"
        })

        # 2. Risk Signal Node
        signal_id = f"SIG-{finding_id}"
        nodes.append({
            "id": signal_id,
            "label": f"Signal: {pattern_name}",
            "type": "Signal",
            "color": "#f97316",  # Orange
            "size": 24,
            "details": f"{len(txns)} transactions flagged | Velocity Anomaly"
        })
        edges.append({"source": finding_id, "target": signal_id, "relation": "TRIGGERED_BY"})

        # 3. Customer Profile Node
        cust_node_id = customer_id
        nodes.append({
            "id": cust_node_id,
            "label": f"Customer: {customer_name} ({customer_id})",
            "type": "Customer",
            "color": "#3b82f6",  # Blue
            "size": 22,
            "details": f"Entity: {customer_name}"
        })
        edges.append({"source": signal_id, "target": cust_node_id, "relation": "OBSERVED_ON"})

        # 4. Pattern Node
        pattern_node_id = f"PAT-{finding_id}"
        nodes.append({
            "id": pattern_node_id,
            "label": f"Pattern: {pattern_name}",
            "type": "Pattern",
            "color": "#8b5cf6",  # Purple
            "size": 20,
            "details": "Rapid Inbound-to-Outbound Pass-Through (< 45 min)"
        })
        edges.append({"source": signal_id, "target": pattern_node_id, "relation": "MATCHES_PATTERN"})

        # 5. Transaction Evidence Nodes (up to 4 prominent txns)
        for i, t in enumerate(txns[:4]):
            t_id = t.get("txn_id", f"TXN-{i}")
            amt = t.get("amount", 0.0)
            time_str = t.get("time") or t.get("timestamp", "")
            cp = t.get("counterparty") or t.get("counterparty_name", "Third Party")
            
            nodes.append({
                "id": t_id,
                "label": f"{t_id}: ₹{amt/100000:.2f}L",
                "type": "Transaction",
                "color": "#eab308",  # Yellow / Amber
                "size": 18,
                "details": f"{time_str} | {cp}"
            })
            edges.append({"source": signal_id, "target": t_id, "relation": "TRANSACTION_EVIDENCE"})

        # 6. Policy & Regulatory Evidence Nodes
        for p in policy_sections[:2]:
            p_id = f"POL-{hashlib.md5(p['section_title'].encode()).hexdigest()[:6]}"
            nodes.append({
                "id": p_id,
                "label": f"Policy: {p['section_title'][:32]}...",
                "type": "Policy",
                "color": "#10b981",  # Emerald Green
                "size": 20,
                "details": p.get("authority", "PMLA / RBI Directive")
            })
            edges.append({"source": pattern_node_id, "target": p_id, "relation": "VIOLATES_RULE"})

        # 7. Regulatory Report Node
        report_node_id = f"REP-{finding_id}"
        nodes.append({
            "id": report_node_id,
            "label": f"Report: STR/SAR Filing ({finding_id})",
            "type": "Report",
            "color": "#06b6d4",  # Cyan
            "size": 24,
            "details": "Audit-ready regulatory submission package"
        })
        edges.append({"source": finding_id, "target": report_node_id, "relation": "GENERATES_FILING"})

        return {
            "finding_id": finding_id,
            "domain": "AML",
            "nodes": nodes,
            "edges": edges,
            "ascii_tree": EvidenceGraphBuilder._generate_aml_tree(finding_id, pattern_name, txns, policy_sections)
        }

    @staticmethod
    def _generate_aml_tree(finding_id: str, pattern: str, txns: list[dict], policies: list[dict]) -> str:
        lines = [
            f"Finding {finding_id}",
            "│",
            f"├── Signal",
            f"│   └── {len(txns)} unusual transactions ({pattern})",
            "│",
            "├── Transaction Evidence"
        ]
        for i, t in enumerate(txns[:3]):
            prefix = "└──" if i == len(txns[:3]) - 1 else "├──"
            t_id = t.get("txn_id", f"TXN-{i}")
            amt = t.get("amount", 0.0)
            time_str = t.get("time") or t.get("timestamp", "")
            lines.append(f"│   {prefix} {t_id} (₹{amt/100000:.2f} Lakh, {time_str})")

        lines.extend([
            "│",
            "├── Customer Evidence",
            "│   └── Historical declared profile: ₹5.00 Lakh/mo vs ₹42.80 Lakh 7-day velocity",
            "│",
            "├── Policy Evidence"
        ])
        for p in policies[:2]:
            lines.append(f"│   ├── {p['section_title']}")
        lines.extend([
            "│",
            "└── Regulatory Evidence",
            "    └── Statutory PMLA 2002 Section 12 & PMLA Rules 2005 Rule 8 / STR Mandate"
        ])
        return "\n".join(lines)

    @staticmethod
    def build_credit_graph(finding_id: str, customer_id: str, customer_name: str,
                           facility_id: str, dpd: int, dscr: float, covenant: str,
                           policy_sections: list[dict]) -> dict:
        nodes = []
        edges = []

        nodes.append({
            "id": finding_id,
            "label": f"Finding #{finding_id}",
            "type": "Finding",
            "color": "#ef4444",
            "size": 30,
            "details": f"Credit Impairment EWS | Status: OPEN"
        })

        sig_id = f"SIG-{finding_id}"
        nodes.append({
            "id": sig_id,
            "label": f"Signal: SMA-1 Deterioration ({dpd} DPD)",
            "type": "Signal",
            "color": "#f97316",
            "size": 24,
            "details": f"Overdue: {dpd} Days | DSCR: {dscr:.2f}x"
        })
        edges.append({"source": finding_id, "target": sig_id, "relation": "EVALUATED_BY"})

        nodes.append({
            "id": customer_id,
            "label": f"Borrower: {customer_name}",
            "type": "Customer",
            "color": "#3b82f6",
            "size": 22,
            "details": f"Facility ID: {facility_id}"
        })
        edges.append({"source": sig_id, "target": customer_id, "relation": "BORROWER_PROFILE"})

        dscr_id = f"METRIC-DSCR-{finding_id}"
        nodes.append({
            "id": dscr_id,
            "label": f"DSCR: {dscr:.2f}x (< 1.25x Floor)",
            "type": "Metric",
            "color": "#eab308",
            "size": 18,
            "details": "Debt Service Coverage Ratio Breached"
        })
        edges.append({"source": sig_id, "target": dscr_id, "relation": "FINANCIAL_STRESS"})

        for p in policy_sections[:2]:
            p_id = f"POL-{hashlib.md5(p['section_title'].encode()).hexdigest()[:6]}"
            nodes.append({
                "id": p_id,
                "label": f"Policy: {p['section_title'][:32]}...",
                "type": "Policy",
                "color": "#10b981",
                "size": 20,
                "details": "RBI Prudential Framework (2019)"
            })
            edges.append({"source": sig_id, "target": p_id, "relation": "STATUTORY_VIOLATION"})

        rep_id = f"REP-{finding_id}"
        nodes.append({
            "id": rep_id,
            "label": "Report: Credit Risk EWS Memo",
            "type": "Report",
            "color": "#06b6d4",
            "size": 24,
            "details": "Joint Lenders Forum Corrective Action Plan"
        })
        edges.append({"source": finding_id, "target": rep_id, "relation": "GENERATES_MEMO"})

        ascii_tree = f"""Finding {finding_id}
│
├── Signal
│   └── Borrower Incipient Stress (SMA-1, {dpd} Days Past Due)
│
├── Financial Metric Evidence
│   ├── Facility: {facility_id}
│   ├── DSCR: {dscr:.2f}x (Covenant: 1.25x)
│   └── Covenant Status: {covenant}
│
├── Borrower Evidence
│   └── {customer_name} ({customer_id})
│
├── Policy Evidence
│   └── RBI Prudential Framework Section 1.1 (Early Warning Signals)
│
└── Regulatory Evidence
    └── Banking Regulation Act 1949 §35A Mandatory CAP Formulation"""

        return {
            "finding_id": finding_id,
            "domain": "CREDIT",
            "nodes": nodes,
            "edges": edges,
            "ascii_tree": ascii_tree
        }

    @staticmethod
    def build_liquidity_graph(finding_id: str, report_date: str, lcr: float,
                             total_hqla: float, net_outflows: float,
                             policy_sections: list[dict]) -> dict:
        nodes = []
        edges = []

        nodes.append({
            "id": finding_id,
            "label": f"Finding #{finding_id}",
            "type": "Finding",
            "color": "#ef4444",
            "size": 30,
            "details": "Basel III LCR Breach | Status: ESCALATED"
        })

        sig_id = f"SIG-{finding_id}"
        nodes.append({
            "id": sig_id,
            "label": f"Signal: LCR {lcr:.2f}% (< 100% Floor)",
            "type": "Signal",
            "color": "#f97316",
            "size": 24,
            "details": f"Date: {report_date} | Statutory Breach"
        })
        edges.append({"source": finding_id, "target": sig_id, "relation": "TRIGGERED_BY"})

        hqla_id = f"HQLA-{finding_id}"
        nodes.append({
            "id": hqla_id,
            "label": f"HQLA: ₹{total_hqla:,.0f}M vs Outflow ₹{net_outflows:,.0f}M",
            "type": "Metric",
            "color": "#eab308",
            "size": 18,
            "details": "30-Day Liquidity Deficit"
        })
        edges.append({"source": sig_id, "target": hqla_id, "relation": "POSITION_EVIDENCE"})

        for p in policy_sections[:2]:
            p_id = f"POL-{hashlib.md5(p['section_title'].encode()).hexdigest()[:6]}"
            nodes.append({
                "id": p_id,
                "label": f"Policy: {p['section_title'][:32]}...",
                "type": "Policy",
                "color": "#10b981",
                "size": 20,
                "details": "Basel III (BCBS 238)"
            })
            edges.append({"source": sig_id, "target": p_id, "relation": "SUPERVISORY_MANDATE"})

        rep_id = f"REP-{finding_id}"
        nodes.append({
            "id": rep_id,
            "label": "Report: Central Bank Supervisory Notice",
            "type": "Report",
            "color": "#06b6d4",
            "size": 24,
            "details": "Mandatory Daily Central Bank Filing"
        })
        edges.append({"source": finding_id, "target": rep_id, "relation": "SUPERVISORY_FILING"})

        ascii_tree = f"""Finding {finding_id}
│
├── Signal
│   └── Statutory LCR Regulatory Breach ({lcr:.2f}% < 100.00% floor)
│
├── Position Evidence
│   ├── Total HQLA: ₹{total_hqla:,.0f}M
│   └── 30-Day Net Cash Outflows: ₹{net_outflows:,.0f}M
│
├── Regulatory Evidence
│   └── BCBS 238 Basel III Liquidity Standards Section 2.1
│
└── Mandatory Action
    └── Daily Central Bank Supervisory Notice & Contingency Drawdown"""

        return {
            "finding_id": finding_id,
            "domain": "LIQUIDITY",
            "nodes": nodes,
            "edges": edges,
            "ascii_tree": ascii_tree
        }


def create_plotly_network_figure(graph_data: dict):
    """
    Renders an interactive, visually stunning Plotly network graph for the evidence chain.
    """
    import plotly.graph_objects as go
    import networkx as nx

    G = nx.DiGraph()
    nodes = graph_data["nodes"]
    edges = graph_data["edges"]

    for n in nodes:
        G.add_node(n["id"], **n)

    for e in edges:
        G.add_edge(e["source"], e["target"], relation=e["relation"])

    # Compute hierarchical spring layout
    pos = nx.spring_layout(G, k=1.2, seed=42)

    # Edge traces
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.8, color="#475569"),
        hoverinfo='none',
        mode='lines'
    )

    # Node traces
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    node_size = []
    node_hover = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        d = G.nodes[node]
        node_text.append(d.get("label", node))
        node_color.append(d.get("color", "#38bdf8"))
        node_size.append(d.get("size", 20))
        node_hover.append(f"<b>{d.get('type')}: {d.get('label')}</b><br>{d.get('details', '')}")

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        hovertext=node_hover,
        text=node_text,
        textposition="top center",
        textfont=dict(size=11, color="#f8fafc", family="Inter, sans-serif"),
        marker=dict(
            showscale=False,
            color=node_color,
            size=node_size,
            line=dict(width=2, color="#0f172a")
        )
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=dict(
                text=f"<b>Evidence Graph: Provenance Chain for {graph_data.get('finding_id')}</b>",
                font=dict(size=16, color="#f8fafc")
            ),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=20, r=20, t=50),
            plot_bgcolor="rgba(15, 23, 42, 0.9)",
            paper_bgcolor="rgba(15, 23, 42, 0.9)",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=420
        )
    )
    return fig
