import streamlit as st
import json
from typing import Dict
from src.agents.profile_agent import ProfileAgent
from src.agents.intelligence_agent import IntelligenceAgent
from src.agents.matching_agent import MatchingAgent
from src.agents.visualizer import Visualizer

st.set_page_config(
    page_title="星图·择途",
    page_icon="🗺️",
    layout="wide",
)

st.title("🗺️ 星图·择途")
st.caption("基于多智能体的高考志愿与未来职业导航系统 | GOAI Boundless Agents · AI+教育")

if "profile" not in st.session_state:
    st.session_state.profile = None
if "intelligence" not in st.session_state:
    st.session_state.intelligence = None
if "matching" not in st.session_state:
    st.session_state.matching = None

col1, col2 = st.columns([1, 2])

with col1:
    st.header("📋 你的画像")

    subjects = {}
    st.subheader("选科 / 擅长科目")
    subject_names = ["语文", "数学", "英语", "物理", "化学", "生物", "历史", "地理", "政治", "信息技术"]
    for subj in subject_names:
        val = st.slider(subj, 0, 150, 100, 5, key=f"score_{subj}")
        if val > 0:
            subjects[subj] = val

    st.subheader("兴趣爱好")
    interests = st.text_area(
        "你平时喜欢做什么？有没有特别感兴趣的方向？",
        placeholder="比如：喜欢拆东西再装回去、看科幻小说、写代码、画漫画...",
        height=80,
        key="interests",
    )

    st.subheader("自我描述")
    self_description = st.text_area(
        "用几个词或一句话描述你的性格",
        placeholder="比如：喜欢一个人钻研、团队中更愿意做执行者、对数字很敏感...",
        height=60,
        key="self_description",
    )

    if st.button("🚀 开始分析", type="primary", use_container_width=True):
        if not interests and not self_description:
            st.warning("请至少填写兴趣爱好或自我描述")
        else:
            with st.spinner("洞察 Agent 正在分析你的画像..."):
                profile_agent = ProfileAgent()
                student_input = {
                    "subjects": subjects,
                    "interests": interests,
                    "self_description": self_description,
                    "scores": {k: v for k, v in subjects.items()},
                }
                st.session_state.profile = profile_agent.analyze(student_input)

            with st.spinner("情报 Agent 正在整合国家战略与行业趋势..."):
                intelligence_agent = IntelligenceAgent()
                st.session_state.intelligence = intelligence_agent.gather(st.session_state.profile)

            with st.spinner("匹配 Agent 正在计算最佳路径..."):
                matching_agent = MatchingAgent()
                st.session_state.matching = matching_agent.match(
                    st.session_state.profile,
                    st.session_state.intelligence,
                )

            st.success("分析完成！查看右侧结果")
            st.rerun()

with col2:
    if st.session_state.profile:
        profile = st.session_state.profile
        intelligence = st.session_state.intelligence
        matching = st.session_state.matching or {}

        tab1, tab2, tab3, tab4 = st.tabs(["📊 画像", "🏛️ 情报", "🎯 推荐", "🗺️ 航线"])

        with tab1:
            st.subheader(f"人格摘要：{profile.get('persona_summary', '')}")
            st.write(f"**学习风格**：{profile.get('learning_style', '')}")
            st.write(f"**推荐学科门类**：{'、'.join(profile.get('recommended_major_categories', []))}")

            col_a, col_b = st.columns(2)
            with col_a:
                st.write("**能力标签**：")
                for tag in profile.get("capability_tags", []):
                    st.markdown(f"- {tag}")
            with col_b:
                st.write("**兴趣类型**（Holland）：")
                scores = profile.get("riasec_scores", {})
                for t, s in sorted(scores.items(), key=lambda x: x[1], reverse=True):
                    label = {"R": "现实型", "I": "研究型", "A": "艺术型", "S": "社会型", "E": "企业型", "C": "常规型"}
                    st.markdown(f"- {label.get(t, t)}({t}): {s:.0%}")

            if profile.get("riasec_scores"):
                fig = Visualizer.riasec_radar(profile["riasec_scores"])
                st.plotly_chart(fig, use_container_width=True)

        with tab2:
            matched = intelligence.get("matched_directions", []) if intelligence else []
            if intelligence and intelligence.get("knowledge_card"):
                st.info(intelligence["knowledge_card"])

            for d in matched:
                with st.expander(f"🔬 {d.get('name', '')}"):
                    st.write(f"**国家战略意义**：{d.get('national_significance', '')}")
                    st.write(f"**专业路径**：{' → '.join(d.get('major_path', []))}")
                    st.write(f"**推荐院校**：{'、'.join(d.get('institutions', []))}")
                    st.write(f"**匹配理由**：{d.get('fit_reason', '')}")

        with tab3:
            recs = matching.get("recommendations", [])
            if recs:
                fig_bar = Visualizer.recommendation_bar(recs)
                st.plotly_chart(fig_bar, use_container_width=True)

            for r in recs:
                with st.expander(f"{'🥇🥈🥉'[min(r['rank']-1, 2)]} {r.get('direction_name', '')} — 匹配度 {r.get('fit_score', 0):.0%}"):
                    st.write(f"**推荐理由**：{r.get('one_sentence', '')}")
                    st.write(f"**能力匹配**：{r.get('ability_match', '')}")
                    st.write(f"**兴趣匹配**：{r.get('interest_match', '')}")
                    st.write(f"**国家战略关联**：{r.get('national_relevance', '')}")

                    tiers = r.get("institutions_tiered", {})
                    if tiers:
                        st.write("**院校梯度**：")
                        for tier_name, schools in tiers.items():
                            st.markdown(f"- **{tier_name}**：{'、'.join(schools)}")

                    st.write(f"**学术路径**：{r.get('academic_path', '')}")
                    st.write(f"**职业前景**：{r.get('future_outlook', '')}")

            st.divider()

            avoids = matching.get("avoid", [])
            if avoids:
                st.subheader("⚠️ 避坑提示")
                for a in avoids:
                    st.markdown(f"- **{a.get('direction', '')}**：{a.get('reason', '')}")

            gems = matching.get("hidden_gems", [])
            if gems:
                st.subheader("💎 隐藏宝藏")
                for g in gems:
                    st.markdown(f"- **{g.get('direction', '')}**：{g.get('reason', '')}")

        with tab4:
            recs = matching.get("recommendations", [])
            if recs:
                fig = Visualizer.timeline_chart(recs)
                st.plotly_chart(fig, use_container_width=True)

            st.subheader("📝 完整报告")
            full_report = {
                "profile": profile,
                "intelligence": intelligence,
                "matching": matching,
            }
            st.download_button(
                "下载完整报告 (JSON)",
                json.dumps(full_report, ensure_ascii=False, indent=2),
                "starmap_report.json",
                "application/json",
                use_container_width=True,
            )

    else:
        st.header("👈 先在左侧填写你的信息，点击"开始分析"")
        st.markdown("""
        ### 四个智能体各司其职：
        1. **洞察 Agent**：读懂你是谁
        2. **情报 Agent**：告诉世界在怎样变化
        3. **匹配 Agent**：找到属于你的路
        4. **可视化 Agent**：让你看见未来

        ---
        #### 与传统志愿填报工具的差异：
        - 不只是看分数，更看**你这个人的特质**
        - 不只是查学校，更看**国家战略方向**
        - 不只是选专业，更看**长周期职业路径**
        - 不只是列数据，更是**可探索的交互体验**
        """)
