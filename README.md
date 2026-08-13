# 星图·择途 (StarMap)

## GOAI 世界人工智能开源大赛 — Boundless Agents · AI+教育

基于多智能体的高考志愿与未来职业导航系统。不做第 1001 个 AI 家教，做第一个帮孩子"看见未来"的择路智能体。

### 核心能力

```
学生画像(成绩+性格+兴趣) ──┐
国家战略方向(胶球/南天门/核聚变...) ──┼──→ 多Agent协同引擎 ──→ 个性化择路报告
行业真实数据(招聘趋势/薪资/缺口) ──┘
```

### 四 Agent 架构

| Agent | 职责 | 输入 | 输出 |
|---|---|---|---|
| ① 洞察 Agent | "你是谁" | 成绩/选科/性格测评/兴趣描述 | 能力-兴趣雷达图 |
| ② 情报 Agent | "世界怎样" | 国家战略/行业趋势/高校数据 | 结构化的方向-专业知识图谱 |
| ③ 匹配 Agent | "路在何方" | 学生画像 + 情报数据 | Top N 推荐方向 + 避坑 + 隐藏选项 |
| ④ 可视化 Agent | "看见未来" | 匹配结果 | 交互式人生航线图 |

### 技术栈

- **前端**: Streamlit
- **Agent 编排**: LangGraph (State Graph)
- **模型层**: 模型无关 (支持 OpenAI / Claude / DeepSeek / Qwen)
- **知识库**: ChromaDB
- **可观测**: LangSmith tracing

### 快速开始

```bash
pip install -r requirements.txt
streamlit run src/app.py
```

### 目录结构

```
├── 初赛/              # 提交材料
│   ├── 项目简介.md
│   └── 方案PPT大纲.md
├── src/
│   ├── app.py         # Streamlit 主入口
│   ├── config.py      # 配置
│   └── agents/        # 四个 Agent 实现
├── data/
│   └── knowledge/     # 知识库 JSON
├── docs/              # 技术文档
└── requirements.txt
```

### 竞赛信息

- 赛事：GOAI 世界人工智能开源大赛
- 赛道：无界应用 (Boundless Agents)
- 方向：AI+教育
- 初赛截止：2026-08-16
- 官网：https://goaihz.com
