# 星图·择途 (StarMap)

## GOAI 世界人工智能开源大赛 — Boundless Agents · AI+教育

基于多智能体的高考志愿与未来职业导航系统。不做第 1001 个 AI 志愿填报工具，做第一个帮孩子"看见未来"的择路智能体。

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

- **前端**: 原生 HTML + Chart.js（深色星空主题，纯静态）
- **后端**: Python HTTP Server（ThreadingHTTPServer）
- **模型层**: OpenAI 兼容 API（默认 gpt-5.5，可换 DeepSeek / Qwen / Claude）
- **匹配逻辑**: LLM 先打 RIASEC 六维分数，再据此生成方向/职业/时间轴

### 快速开始

```bash
pip install -r requirements.txt
# 复制 .env.example 为 .env 并填入 API Key
python src/server.py
# 浏览器打开 http://localhost:8800
```

### 目录结构

```
├── 初赛/              # 提交材料
│   ├── 项目简介.md
│   └── 方案PPT大纲.md
├── src/
│   ├── server.py      # 后端主入口（HTTP Server + LLM）
│   ├── index.html     # 前端页面（星空主题 + Chart.js）
│   ├── config.py      # 配置
│   ├── demo_app.py    # 早期 Streamlit 原型
│   └── agents/        # 早期四 Agent 原型
├── docs/              # 技术文档
├── .env.example       # 环境变量模板
└── requirements.txt
```

### 竞赛信息

- 赛事：GOAI 世界人工智能开源大赛
- 赛道：无界应用 (Boundless Agents)
- 方向：AI+教育
- 初赛截止：2026-08-16
- 官网：https://goaihz.com
- 开源地址：https://github.com/Ninetailedcatfox/starmap-goai
