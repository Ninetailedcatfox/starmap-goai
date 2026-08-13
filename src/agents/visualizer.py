import json
from typing import Dict, List
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


class Visualizer:
    """Agent ④: 可视化 Agent — 生成交互式图表"""

    @staticmethod
    def riasec_radar(scores: Dict[str, float]) -> go.Figure:
        categories = list(scores.keys())
        values = list(scores.values())
        values.append(values[0])
        categories.append(categories[0])

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Holland 兴趣画像',
            line=dict(color='#636EFA', width=2),
            fillcolor='rgba(99, 110, 250, 0.3)',
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            title="Holland 职业兴趣六边形",
            showlegend=False,
            height=400,
        )
        return fig

    @staticmethod
    def recommendation_bar(recommendations: List[Dict]) -> go.Figure:
        names = [r["direction_name"] for r in recommendations]
        scores = [r.get("fit_score", 0) * 100 for r in recommendations]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=scores,
            y=names,
            orientation='h',
            marker=dict(
                color=scores,
                colorscale='Blues',
                showscale=False,
            ),
            text=[f"{s:.0f}%" for s in scores],
            textposition='outside',
        ))
        fig.update_layout(
            title="推荐方向匹配度",
            xaxis=dict(title="匹配度 (%)", range=[0, 100]),
            yaxis=dict(autorange="reversed"),
            height=300,
            margin=dict(l=150, r=30, t=50, b=30),
        )
        return fig

    @staticmethod
    def timeline_chart(recommendations: List[Dict]) -> go.Figure:
        stages = ["本科", "硕士", "博士/工作", "职业发展"]
        fig = go.Figure()

        for i, rec in enumerate(recommendations[:3]):
            y_positions = [i] * len(stages)
            fig.add_trace(go.Scatter(
                x=stages,
                y=y_positions,
                mode='lines+markers+text',
                name=rec["direction_name"],
                text=[rec["direction_name"]] * len(stages),
                textposition="top center",
                line=dict(width=3),
                marker=dict(size=12),
            ))

        fig.update_layout(
            title="人生航线图",
            xaxis=dict(title="时间阶段"),
            yaxis=dict(showticklabels=False, title=""),
            height=350,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
        )
        return fig

    @staticmethod
    def generate_full_dashboard(profile: Dict, intelligence: Dict, matching: Dict) -> Dict[str, go.Figure]:
        """生成完整仪表盘的所有图表"""

        riasec_scores = profile.get("riasec_scores", {})
        recommendations = matching.get("recommendations", [])

        figs = {}

        if riasec_scores:
            figs["riasec_radar"] = Visualizer.riasec_radar(riasec_scores)

        if recommendations:
            figs["recommendation_bar"] = Visualizer.recommendation_bar(recommendations)
            figs["timeline"] = Visualizer.timeline_chart(recommendations)

        return figs
