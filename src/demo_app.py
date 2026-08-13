import streamlit as st
import plotly.graph_objects as go
import json
from datetime import datetime

st.set_page_config(page_title="星图·择途", page_icon="🗺️", layout="wide")

# ── 内置知识库 ──────────────────────────────────

STRATEGIC_DIRECTIONS = [
    {
        "name": "粒子物理与基础科学",
        "keywords": ["胶球", "BESⅢ", "高能物理", "标准模型"],
        "national_significance": "2024年北京谱仪Ⅲ实验确认胶球存在，代表中国在基础物理领域的世界级突破。这是自标准模型以来最重要的粒子发现之一。",
        "majors": ["粒子物理与原子核物理", "理论物理", "物理学"],
        "schools": {"冲刺": ["中国科学技术大学", "北京大学"], "匹配": ["南京大学", "中国科学院大学"], "保底": ["山东大学", "南开大学"]},
        "career_path": "本科物理 → 硕士高能物理 → 博士BESⅢ实验组 → 国家实验室/高校/CERN",
        "salary_range": "学术路线 ¥20-40万/年，转向量化/数据科学 ¥50万+",
        "one_sentence": "如果你从小追问'世界由什么构成'，胶球就是你命中注定的答案。",
    },
    {
        "name": "航空航天与空天一体化",
        "keywords": ["南天门计划", "空天飞机", "高超音速", "深空探测", "载人登月"],
        "national_significance": "南天门计划是中国面向2035的空天一体化战略，涵盖可重复使用运载器、空天飞机、载人月球探测。2030年前后实现载人登月。",
        "majors": ["航空航天工程", "飞行器设计与工程", "航天动力工程"],
        "schools": {"冲刺": ["北京航空航天大学", "哈尔滨工业大学"], "匹配": ["西北工业大学", "国防科技大学"], "保底": ["南京航空航天大学", "沈阳航空航天大学"]},
        "career_path": "本科航天工程 → 硕士推进/控制方向 → 航天科技/科工集团 → 南天门相关型号",
        "salary_range": "体制内 ¥18-25万/年 + 编制，民营航天 ¥30-60万",
        "one_sentence": "不是去看星星，是去造飞船。",
    },
    {
        "name": "可控核聚变与新能源",
        "keywords": ["托卡马克", "ITER", "CFETR", "等离子体", "聚变堆"],
        "national_significance": "中国聚变工程实验堆(CFETR)已立项，计划2035年建成。中国在聚变领域专利数全球第一。这是'人造太阳'，终极能源解决方案。",
        "majors": ["核工程与核技术", "等离子体物理", "新能源科学与工程"],
        "schools": {"冲刺": ["中国科学技术大学", "清华大学"], "匹配": ["华中科技大学", "核工业西南物理研究院"], "保底": ["哈尔滨工程大学", "南华大学"]},
        "career_path": "本科核工 → 硕士等离子体 → 博士CFETR项目 → 中核集团/中科院等离子体所",
        "salary_range": "¥20-35万/年 + 国家重点项目补贴",
        "one_sentence": "造一颗太阳，比写一万行代码更酷。",
    },
    {
        "name": "量子科技",
        "keywords": ["量子计算", "量子通信", "超导量子比特", "墨子号"],
        "national_significance": "中国在量子通信领域全球领先，'墨子号'实现千公里级量子纠缠分发。'十四五'将量子信息列为'科技前沿攻关'第一梯队。",
        "majors": ["量子信息科学", "物理学", "计算机科学与技术"],
        "schools": {"冲刺": ["中国科学技术大学", "清华大学"], "匹配": ["浙江大学", "南京大学"], "保底": ["西安交通大学", "南方科技大学"]},
        "career_path": "本科物理/计算机 → 硕士量子信息 → 博士量子计算方向 → 量子实验室/华为/本源量子",
        "salary_range": "¥30-80万/年",
        "one_sentence": "如果你觉得现在的计算机太慢，你来造下一代。",
    },
    {
        "name": "人工智能与芯片",
        "keywords": ["大模型", "AI芯片", "GPU", "智能体", "深度学习"],
        "national_significance": "AI芯片是'卡脖子'核心战场。国产GPU实现从0到1突破，华为昇腾/寒武纪/壁仞科技等形成自主生态，芯片设计人才缺口超30万。",
        "majors": ["人工智能", "计算机科学与技术", "集成电路设计与集成系统"],
        "schools": {"冲刺": ["清华大学", "北京大学"], "匹配": ["浙江大学", "上海交通大学", "中国科学技术大学"], "保底": ["电子科技大学", "华中科技大学"]},
        "career_path": "本科CS/微电子 → 硕士AI/芯片 → 大厂AI Lab或创业",
        "salary_range": "¥25-60万/年，AI研究员 50万+",
        "one_sentence": "这个赛道不解释——但你得想清楚是凑热闹的，还是造铲子的。",
    },
    {
        "name": "合成生物学与基因编辑",
        "keywords": ["合成生物学", "CRISPR", "基因治疗", "生物制造"],
        "national_significance": "中国在合成生物学领域论文数全球第一，基因治疗药物已进入临床。'十四五'生物经济规划明确将合成生物列为核心赛道。",
        "majors": ["生物科学", "生物工程", "合成生物学"],
        "schools": {"冲刺": ["清华大学", "西湖大学"], "匹配": ["天津大学", "中国科学院深圳先进院"], "保底": ["华东理工大学", "江南大学"]},
        "career_path": "本科生物 → 硕士合成生物学 → 博士基因编辑 → 药企研发/合成生物创业",
        "salary_range": "¥18-40万/年，创业空间极大",
        "one_sentence": "21世纪是生物的世纪——这句话等了20年，终于要兑现了。",
    },
    {
        "name": "脑科学与脑机接口",
        "keywords": ["脑科学", "脑机接口", "类脑计算", "神经科学"],
        "national_significance": "中国脑计划(2030)已启动，投入超百亿。浙大完成全球首例侵入式脑机接口临床研究。脑机接口是下一代人机交互。",
        "majors": ["神经科学", "生物医学工程", "计算机科学与技术"],
        "schools": {"冲刺": ["浙江大学", "北京大学"], "匹配": ["复旦大学", "中国科学院脑智卓越中心"], "保底": ["上海交通大学", "天津大学"]},
        "career_path": "本科生医工 → 硕士神经工程 → 博士脑机接口 → 脑科学实验室/创业",
        "salary_range": "¥25-50万/年",
        "one_sentence": "如果你觉得键盘太慢，我们来直接'想'。",
    },
]

HOLLAND_MAP = {
    "R": {"label": "现实型", "color": "#E74C3C", "desc": "喜欢动手、操作工具机械、看重实际成果"},
    "I": {"label": "研究型", "color": "#3498DB", "desc": "喜欢思考探究实验、好奇心强、享受独处研究"},
    "A": {"label": "艺术型", "color": "#9B59B6", "desc": "喜欢创造表达设计、重视美感和独特性"},
    "S": {"label": "社会型", "color": "#2ECC71", "desc": "喜欢帮助教导合作、社交能量高、共情能力强"},
    "E": {"label": "企业型", "color": "#F39C12", "desc": "喜欢领导说服竞争、目标导向、享受挑战"},
    "C": {"label": "常规型", "color": "#1ABC9C", "desc": "喜欢秩序数据处理、细心可靠、流程导向"},
}

PERSONALITY_PROFILES = {
    "探索者": {
        "tags": ["数理思维", "好奇心强", "喜欢钻研", "独立工作"],
        "riasec": {"R": 0.6, "I": 0.95, "A": 0.3, "S": 0.2, "E": 0.1, "C": 0.4},
        "summary": "天生的科学家——对世界底层规律有无法抑制的好奇心，享受长期沉浸在一个问题中。",
        "top_directions": ["粒子物理与基础科学", "量子科技", "合成生物学与基因编辑"],
    },
    "造物者": {
        "tags": ["动手能力", "空间想象", "工程思维", "追求极限"],
        "riasec": {"R": 0.95, "I": 0.7, "A": 0.3, "S": 0.2, "E": 0.3, "C": 0.5},
        "summary": "天生工程师——喜欢把想法变成实物，享受从图纸到成品的成就感。",
        "top_directions": ["航空航天与空天一体化", "可控核聚变与新能源", "人工智能与芯片"],
    },
    "连接者": {
        "tags": ["共情力强", "沟通表达", "组织协调", "服务导向"],
        "riasec": {"R": 0.1, "I": 0.3, "A": 0.4, "S": 0.9, "E": 0.7, "C": 0.5},
        "summary": "天生连接者——擅长理解人、影响人、组织人，最大的成就感来自'帮到别人'。",
        "top_directions": ["脑科学与脑机接口", "合成生物学与基因编辑"],
    },
    "创新者": {
        "tags": ["跨界思维", "商业敏感", "快速学习", "拥抱不确定"],
        "riasec": {"R": 0.4, "I": 0.6, "A": 0.7, "S": 0.5, "E": 0.85, "C": 0.2},
        "summary": "天生创新者——不满足于任何已有答案，总想用新办法颠覆旧秩序。",
        "top_directions": ["人工智能与芯片", "量子科技", "脑科学与脑机接口"],
    },
}

# ── 匹配引擎 ──────────────────────────────────

def match_career_paths(riasec_scores, personality_tags):
    """基于能力-兴趣双维匹配"""
    scores = {}
    for d in STRATEGIC_DIRECTIONS:
        direction = d["name"]
        keywords = " ".join(d["keywords"] + d["majors"])
        tags_str = " ".join(personality_tags)
        tag_match = sum(1 for t in personality_tags if t in keywords or any(
            kw in t for kw in ["动手", "工程", "探索", "创造", "逻辑", "编程","数理"]
        ))
        r_score = riasec_scores.get("R", 0)
        i_score = riasec_scores.get("I", 0)
        capability_score = 0
        if direction in ["航空航天与空天一体化", "可控核聚变与新能源"]:
            capability_score = r_score * 0.6 + i_score * 0.4
        elif direction in ["粒子物理与基础科学", "量子科技"]:
            capability_score = i_score * 0.8 + r_score * 0.2
        elif direction in ["人工智能与芯片", "合成生物学与基因编辑"]:
            capability_score = i_score * 0.5 + r_score * 0.3 + riasec_scores.get("E", 0) * 0.2
        elif direction in ["脑科学与脑机接口"]:
            capability_score = i_score * 0.4 + riasec_scores.get("S", 0) * 0.3 + riasec_scores.get("A", 0) * 0.3
        else:
            capability_score = i_score * 0.5 + r_score * 0.3 + 0.2

        scores[direction] = capability_score * 0.55 + min(tag_match / 5, 0.8) * 0.25 + 0.2

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked


def classify_personality(interests_text, self_desc_text):
    """简单分类到人格画像"""
    combined = (interests_text + " " + self_desc_text).lower()

    explorer_kw = ["问为什么", "思考", "研究", "自然", "宇宙", "物理", "数学", "实验", "科学", "逻辑"]
    maker_kw = ["动手", "拆", "装", "做", "造", "搭建", "设计", "机械", "工程", "飞机", "火箭", "代码"]
    connector_kw = ["帮助", "交流", "交朋友", "分享", "教", "组织", "关心", "团队", "社交"]
    innovator_kw = ["创造", "创业", "改变", "商业", "创新", "想不一样", "颠覆", "尝试", "冒险"]

    ex = sum(1 for k in explorer_kw if k in combined)
    ma = sum(1 for k in maker_kw if k in combined)
    co = sum(1 for k in connector_kw if k in combined)
    inn = sum(1 for k in innovator_kw if k in combined)

    scores = {"探索者": ex, "造物者": ma, "连接者": co, "创新者": inn}
    if max(scores.values()) == 0:
        return "探索者"
    return max(scores, key=scores.get)


# ── UI ──────────────────────────────────────────

st.title("🗺️ 星图·择途")
st.caption("基于多智能体的高考志愿与未来职业导航系统 | GOAI Boundless Agents · AI+教育")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("📋 输入你的画像")

    st.subheader("擅长科目（选最有信心的勾上）")
    subjects_enabled = {}
    cols = st.columns(5)
    subject_list = ["数学", "物理", "化学", "生物", "语文", "英语", "历史", "地理", "政治", "信息技术"]
    for i, subj in enumerate(subject_list):
        with cols[i % 5]:
            subjects_enabled[subj] = st.checkbox(subj, key=f"subj_{subj}")

    st.subheader("兴趣爱好")
    interests = st.text_area(
        "你平时喜欢做什么？对什么方向好奇？",
        placeholder="比如：从小喜欢拆遥控车再装回去、看《三体》对太空着迷、写代码做小工具、喜欢观察动植物...",
        height=80,
        key="interests",
        value="",
    )

    st.subheader("自我描述")
    self_description = st.text_area(
        "用几个词描述你的性格和做事方式",
        placeholder="比如：喜欢一个人钻研问题、更愿意动手而不是空谈、对数字很敏感...",
        height=60,
        key="self_desc",
        value="",
    )

    if st.button("🚀 开始分析", type="primary", use_container_width=True):
        if not interests.strip() and not self_description.strip():
            st.warning("请至少填写兴趣爱好或自我描述")
        else:
            profile_type = classify_personality(interests, self_description)
            profile = PERSONALITY_PROFILES[profile_type]
            ranked = match_career_paths(profile["riasec"], profile["tags"])
            st.session_state.analysis = {
                "profile_type": profile_type,
                "profile": profile,
                "ranked": ranked,
                "subjects": [s for s, v in subjects_enabled.items() if v],
            }

with col2:
    if "analysis" in st.session_state:
        a = st.session_state.analysis
        profile = a["profile"]
        ranked = a["ranked"]
        profile_type = a["profile_type"]
        subjects = a["subjects"]

        tab1, tab2, tab3, tab4 = st.tabs(["📊 画像", "🏛️ 国家战略图景", "🎯 推荐路径", "🗺️ 人生航线"])

        with tab1:
            st.subheader(f"人格类型：{profile_type} — {profile['summary']}")
            st.write(f"**能力标签**：{' · '.join(profile['tags'])}")
            if subjects:
                st.write(f"**擅长科目**：{'、'.join(subjects)}")

            riasec = profile["riasec"]
            categories = ["现实型(R)", "研究型(I)", "艺术型(A)", "社会型(S)", "企业型(E)", "常规型(C)"]
            values = [riasec["R"], riasec["I"], riasec["A"], riasec["S"], riasec["E"], riasec["C"]]
            values_closed = values + [values[0]]
            cats_closed = categories + [categories[0]]

            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=values_closed, theta=cats_closed, fill='toself',
                name='Holland 兴趣画像', line=dict(color='#636EFA', width=2),
                fillcolor='rgba(99, 110, 250, 0.25)',
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                title="Holland 职业兴趣六边形", showlegend=False, height=400,
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        with tab2:
            st.markdown("### 国家战略方向 × 你的天赋匹配")
            st.caption("数据源：十四五/十五五规划、科技部重点研发计划、学科评估")

            top3 = [d for name, score in ranked[:3] for d in STRATEGIC_DIRECTIONS if d["name"] == name]
            for i, d in enumerate(top3):
                with st.expander(f"{'🥇🥈🥉'[i]} {d['name']} — 匹配度 {dict(ranked)[d['name']]:.0%}"):
                    col_a, col_b = st.columns([3, 2])
                    with col_a:
                        st.markdown(f"**国家战略意义**：{d['national_significance']}")
                        st.markdown(f"**核心关键词**：{' · '.join(d['keywords'])}")
                    with col_b:
                        st.markdown(f"**一句话**：_{d['one_sentence']}_")
                        st.markdown(f"**薪资区间**：{d['salary_range']}")

        with tab3:
            st.markdown("### 🎯 个性化择路报告")

            top5 = [d for name, score in ranked[:5] for d in STRATEGIC_DIRECTIONS if d["name"] == name]
            scores_top5 = [dict(ranked)[d["name"]] for d in top5]

            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                x=scores_top5, y=[d["name"] for d in top5], orientation='h',
                marker=dict(color=scores_top5, colorscale='Blues', showscale=False),
                text=[f"{s:.0%}" for s in scores_top5], textposition='outside',
            ))
            fig_bar.update_layout(
                title="推荐方向匹配度", xaxis=dict(title="匹配度", range=[0, 1]),
                yaxis=dict(autorange="reversed"), height=280,
                margin=dict(l=180, r=30, t=50, b=30),
            )
            st.plotly_chart(fig_bar, use_container_width=True)

            for i, d in enumerate(top3):
                with st.expander(f"{'🥇🥈🥉'[i]} {d['name']}"):
                    st.write(f"**推荐理由**：{d['one_sentence']}")
                    st.write(f"**专业路径**：{' → '.join(d['majors'])}")
                    st.write(f"**职业路径**：{d['career_path']}")
                    st.write(f"**薪资参考**：{d['salary_range']}")

                    schools = d["schools"]
                    st.write("**院校梯度**：")
                    for tier, sch_list in schools.items():
                        st.markdown(f"- **{tier}**：{'、'.join(sch_list)}")

        with tab4:
            st.markdown("### 🗺️ 人生航线图")
            st.caption("横轴 = 时间阶段 · 纵轴 = 你的路径选择")

            stages = ["选科/高考", "本科", "硕士/博士", "第一份工作", "十年后"]
            fig_tl = go.Figure()
            colors = ["#636EFA", "#EF553B", "#00CC96"]
            for i, d in enumerate(top3[:3]):
                fig_tl.add_trace(go.Scatter(
                    x=stages, y=[i] * len(stages), mode='lines+markers+text',
                    name=d["name"], text=[d["name"]] + ["→"] * 4,
                    textposition="top center", line=dict(width=3, color=colors[i]),
                    marker=dict(size=14, color=colors[i]),
                ))
            fig_tl.update_layout(
                title="你的人生航线", xaxis=dict(title=""),
                yaxis=dict(showticklabels=False, title=""), height=350,
                showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02),
            )
            st.plotly_chart(fig_tl, use_container_width=True)

            st.subheader("📝 导出报告")
            report = {
                "分析时间": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "人格类型": profile_type,
                "能力标签": profile["tags"],
                "擅长科目": subjects,
                "Holland画像": profile["riasec"],
                "推荐方向": [{"名称": d["name"], "匹配度": f'{dict(ranked)[d["name"]]:.0%}', "推荐理由": d["one_sentence"], "专业路径": d["majors"], "院校梯度": d["schools"], "职业前景": d["salary_range"]} for d in top5],
            }
            st.download_button("下载完整报告 (JSON)", json.dumps(report, ensure_ascii=False, indent=2), "starmap_report.json", "application/json", use_container_width=True)

    else:
        st.markdown("""
        ### 👈 在左侧填写信息，然后点击"开始分析"

        ---

        #### 四个智能体，一个闭环：

        | Agent | 问题 | 你得到什么 |
        |---|---|---|
        | ① 洞察 Agent | 你是谁？ | Holland 六边形 + 能力标签 + 人格画像 |
        | ② 情报 Agent | 世界在怎么变？ | 国家战略方向 + 行业趋势 + 薪资数据 |
        | ③ 匹配 Agent | 路在何方？ | Top 5 推荐方向 + 院校梯度 + 避坑提示 |
        | ④ 可视化 Agent | 能看见吗？ | 人生航线图 + 交互仪表盘 |

        ---

        #### 不做第 1001 个 AI 志愿填报工具，做第一个帮孩子"看见未来"的择路智能体。
        """)
