"""
RiskGuard AI - Evidence Engine & Counterparty Graph Visualizer
Constructs grounded evidence trees and interactive Plotly counterparty fraud graphs:
CP-221 -> C1007 -> CP-223 / CP-224
"""

import plotly.graph_objects as go
import pandas as pd
import math
from engine.snowflake_session import get_snowflake_session


class EvidenceEngine:
    """
    Manages grounded evidence cards and renders fraud investigation network graphs.
    Supports both calibrated demo graph for C1007 and dynamic graphs for all entities.
    """

    @staticmethod
    def render_counterparty_graph(customer_id: str = "C1007"):
        """
        Renders the interactive directed transaction flow graph:
        Inbound remitter -> Subject Customer -> Outbound digital aggregators
        """
        session = get_snowflake_session()

        # If C1007, use the precisely calibrated demo graph
        if customer_id == "C1007":
            fig = go.Figure()
            node_x = [0, 0, -1.2, 1.2]
            node_y = [1.2, 0, -1.0, -1.0]
            node_labels = [
                "<b>CP-221</b><br>Swift Enterprises<br>(Inbound Remitter)",
                f"<b>{customer_id}</b><br>Rahul S. Sharma<br>(Subject Account)",
                "<b>CP-223</b><br>CoinBridge P2P<br>(UAE - Crypto Gateway)",
                "<b>CP-224</b><br>CryptoEx Global<br>(SG - Digital Wallet)"
            ]
            node_colors = ["#3b82f6", "#ef4444", "#f59e0b", "#f59e0b"]
            node_sizes = [35, 48, 38, 38]

            # Directed Edges
            fig.add_annotation(
                x=0, y=0.15, ax=0, ay=1.05,
                xref="x", yref="y", axref="x", ayref="y",
                text="<b>₹4.80L</b> (10:00 IMPS)",
                showarrow=True, arrowhead=3, arrowsize=1.5, arrowwidth=2.5,
                arrowcolor="#38bdf8", font=dict(color="#38bdf8", size=11)
            )

            fig.add_annotation(
                x=-1.05, y=-0.88, ax=-0.15, ay=-0.12,
                xref="x", yref="y", axref="x", ayref="y",
                text="<b>₹4.70L</b> (10:25 IMPS [25m])",
                showarrow=True, arrowhead=3, arrowsize=1.5, arrowwidth=2.5,
                arrowcolor="#f87171", font=dict(color="#f87171", size=11)
            )

            fig.add_annotation(
                x=1.05, y=-0.88, ax=0.15, ay=-0.12,
                xref="x", yref="y", axref="x", ayref="y",
                text="<b>₹4.95L</b> (10:50 IMPS [25m])",
                showarrow=True, arrowhead=3, arrowsize=1.5, arrowwidth=2.5,
                arrowcolor="#f87171", font=dict(color="#f87171", size=11)
            )

            fig.add_trace(go.Scatter(
                x=node_x, y=node_y,
                mode='markers+text',
                marker=dict(
                    color=node_colors,
                    size=node_sizes,
                    line=dict(color="#0f172a", width=2.5)
                ),
                text=node_labels,
                textposition="top center",
                textfont=dict(color="#f8fafc", size=11, family="Inter, sans-serif"),
                hoverinfo='none'
            ))

            fig.update_layout(
                title=dict(
                    text=f"<b>Fraud Flow Investigation Graph: {customer_id} Pass-Through Layering</b>",
                    font=dict(size=15, color="#f8fafc")
                ),
                showlegend=False,
                plot_bgcolor="rgba(15, 23, 42, 0.95)",
                paper_bgcolor="rgba(15, 23, 42, 0.95)",
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.8, 1.8]),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.5, 1.7]),
                height=460,
                margin=dict(l=20, r=20, t=50, b=20)
            )
            return fig

        # Dynamic graph generation for ANY customer in Snowflake
        try:
            df_cust = session.sql(f"SELECT CUSTOMER_NAME, RISK_RATING FROM CUSTOMER WHERE CUSTOMER_ID = '{customer_id}'").to_pandas()
            cust_name = df_cust['CUSTOMER_NAME'].iloc[0] if not df_cust.empty else "Customer Entity"
            cust_risk = df_cust['RISK_RATING'].iloc[0] if not df_cust.empty else "HIGH"

            df_txns = session.sql(f"""
            SELECT t.TRANSACTION_ID, t.DIRECTION, t.AMOUNT, t.CHANNEL, t.TRANSACTION_TS,
                   t.COUNTERPARTY_ID, t.COUNTERPARTY_COUNTRY,
                   COALESCE(c.NAME, t.COUNTERPARTY_ID, 'Counterparty') as CP_NAME,
                   COALESCE(c.RISK_RATING, 'MEDIUM') as CP_RISK
            FROM TRANSACTIONS t
            LEFT JOIN COUNTERPARTY c ON t.COUNTERPARTY_ID = c.COUNTERPARTY_ID
            WHERE t.CUSTOMER_ID = '{customer_id}'
            ORDER BY t.TRANSACTION_TS ASC
            LIMIT 10
            """).to_pandas()
        except Exception:
            df_txns = pd.DataFrame()
            cust_name = "Subject Account"
            cust_risk = "HIGH"

        fig = go.Figure()

        if df_txns.empty:
            # Standalone entity
            fig.add_trace(go.Scatter(
                x=[0], y=[0],
                mode='markers+text',
                marker=dict(color="#ef4444" if cust_risk == "HIGH" else "#38bdf8", size=50),
                text=[f"<b>{customer_id}</b><br>{cust_name}<br>(No active transactions)"],
                textposition="top center",
                textfont=dict(color="#f8fafc", size=12)
            ))
            fig.update_layout(
                title=dict(text=f"<b>Counterparty Network Graph: {customer_id}</b>", font=dict(color="#f8fafc")),
                plot_bgcolor="rgba(15, 23, 42, 0.95)",
                paper_bgcolor="rgba(15, 23, 42, 0.95)",
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                height=440
            )
            return fig

        # Center Subject Node
        center_color = "#ef4444" if cust_risk == "HIGH" else ("#10b981" if cust_risk == "LOW" else "#f59e0b")
        node_x = [0]
        node_y = [0]
        node_labels = [f"<b>{customer_id}</b><br>{cust_name[:20]}<br>(Subject)"]
        node_colors = [center_color]
        node_sizes = [48]

        inbound_txns = df_txns[df_txns['DIRECTION'].str.upper() == 'INBOUND']
        outbound_txns = df_txns[df_txns['DIRECTION'].str.upper() == 'OUTBOUND']

        # Position Inbounds along top arc
        in_count = len(inbound_txns)
        for idx, (_, row) in enumerate(inbound_txns.iterrows()):
            angle = math.pi * 0.75 - (idx * (math.pi * 0.5) / max(in_count, 1))
            x = math.cos(angle) * 1.2
            y = math.sin(angle) * 1.1 + 0.3
            node_x.append(x)
            node_y.append(y)
            cp_label = f"<b>{row['COUNTERPARTY_ID'] or 'Inbound'}</b><br>{str(row['CP_NAME'])[:18]}<br>({row.get('COUNTERPARTY_COUNTRY', 'IN')})"
            node_labels.append(cp_label)
            node_colors.append("#38bdf8")
            node_sizes.append(36)

            amt_str = f"₹{row['AMOUNT']/100000:.2f}L" if row['AMOUNT'] >= 100000 else f"₹{row['AMOUNT']:,.0f}"
            fig.add_annotation(
                x=0, y=0.15, ax=x, ay=y - 0.15,
                xref="x", yref="y", axref="x", ayref="y",
                text=f"<b>{amt_str}</b> ({row['CHANNEL']})",
                showarrow=True, arrowhead=3, arrowsize=1.3, arrowwidth=2,
                arrowcolor="#38bdf8", font=dict(color="#38bdf8", size=10)
            )

        # Position Outbounds along bottom arc
        out_count = len(outbound_txns)
        for idx, (_, row) in enumerate(outbound_txns.iterrows()):
            angle = -math.pi * 0.25 - (idx * (math.pi * 0.5) / max(out_count, 1))
            x = math.cos(angle) * 1.25
            y = math.sin(angle) * 1.05
            node_x.append(x)
            node_y.append(y)
            cp_label = f"<b>{row['COUNTERPARTY_ID'] or 'Outbound'}</b><br>{str(row['CP_NAME'])[:18]}<br>({row.get('COUNTERPARTY_COUNTRY', 'IN')})"
            node_labels.append(cp_label)
            node_colors.append("#f87171" if row.get('COUNTERPARTY_COUNTRY') != 'IN' else "#f59e0b")
            node_sizes.append(36)

            amt_str = f"₹{row['AMOUNT']/100000:.2f}L" if row['AMOUNT'] >= 100000 else f"₹{row['AMOUNT']:,.0f}"
            fig.add_annotation(
                x=x, y=y + 0.15, ax=0, ay=-0.15,
                xref="x", yref="y", axref="x", ayref="y",
                text=f"<b>{amt_str}</b> ({row['CHANNEL']})",
                showarrow=True, arrowhead=3, arrowsize=1.3, arrowwidth=2,
                arrowcolor="#f87171", font=dict(color="#f87171", size=10)
            )

        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            marker=dict(color=node_colors, size=node_sizes, line=dict(color="#0f172a", width=2)),
            text=node_labels,
            textposition="top center",
            textfont=dict(color="#f8fafc", size=10, family="Inter, sans-serif"),
            hoverinfo='none'
        ))

        fig.update_layout(
            title=dict(
                text=f"<b>Directed Counterparty Fund Flow: {customer_id} ({cust_name})</b>",
                font=dict(size=14, color="#f8fafc")
            ),
            showlegend=False,
            plot_bgcolor="rgba(15, 23, 42, 0.95)",
            paper_bgcolor="rgba(15, 23, 42, 0.95)",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-2.0, 2.0]),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.8, 1.8]),
            height=460,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        return fig
