"""
RiskGuard AI - Evidence Engine & Counterparty Graph Visualizer
Constructs grounded evidence trees and interactive Plotly counterparty fraud graphs:
CP-221 -> C1007 -> CP-223 / CP-224
"""

import plotly.graph_objects as go
import pandas as pd


class EvidenceEngine:
    """
    Manages grounded evidence cards and renders fraud investigation network graphs.
    """

    @staticmethod
    def render_counterparty_graph(customer_id: str = "C1007"):
        """
        Renders the interactive directed transaction flow graph:
        Inbound remitter -> Subject Customer -> Outbound digital aggregators
        """
        fig = go.Figure()

        # Coordinates for nodes
        # Center = C1007 (0, 0)
        # Top = CP-221 (0, 1.2)
        # Bottom-Left = CP-223 (-1.2, -1.0)
        # Bottom-Right = CP-224 (1.2, -1.0)

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
        # Edge 1: CP-221 -> C1007
        fig.add_annotation(
            x=0, y=0.15, ax=0, ay=1.05,
            xref="x", yref="y", axref="x", ayref="y",
            text="<b>₹4.80L</b> (10:00 IMPS)",
            showarrow=True, arrowhead=3, arrowsize=1.5, arrowwidth=2.5,
            arrowcolor="#38bdf8", font=dict(color="#38bdf8", size=11)
        )

        # Edge 2: C1007 -> CP-223
        fig.add_annotation(
            x=-1.05, y=-0.88, ax=-0.15, ay=-0.12,
            xref="x", yref="y", axref="x", ayref="y",
            text="<b>₹4.70L</b> (10:25 IMPS [25m])",
            showarrow=True, arrowhead=3, arrowsize=1.5, arrowwidth=2.5,
            arrowcolor="#f87171", font=dict(color="#f87171", size=11)
        )

        # Edge 3: C1007 -> CP-224
        fig.add_annotation(
            x=1.05, y=-0.88, ax=0.15, ay=-0.12,
            xref="x", yref="y", axref="x", ayref="y",
            text="<b>₹4.95L</b> (10:50 IMPS [25m])",
            showarrow=True, arrowhead=3, arrowsize=1.5, arrowwidth=2.5,
            arrowcolor="#f87171", font=dict(color="#f87171", size=11)
        )

        # Draw nodes
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
