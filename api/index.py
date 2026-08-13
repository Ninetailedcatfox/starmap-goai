import json
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from openai import OpenAI

app = FastAPI()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
)
MODEL = os.getenv("MODEL", "gpt-5.5")

SYSTEM_PROMPT = """你是星图·择途。分析高中生画像，返回JSON。

## RIASEC 评分规则 (0-10)
R(现实型)=动手操作/工具机械 I(研究型)=思考探究/科研实验 A(艺术型)=创造表达/设计
S(社会型)=帮助沟通/协作 E(企业型)=领导说服/组织 C(常规型)=数据处理/规范
- 纯文科(历史/语文/政治): A/S/E > 6, I/R < 4
- 理科(数理/化/信息): I/R/C > 6, A/S < 4

## 匹配规则（关键）
1. 先评分RIASEC，再根据分数匹配方向——不是反过来
2. A/S主导的学生：推荐人文社科类前沿（文化遗产数字化、AI伦理与法律、认知科学教育、科技考古、数字治理、创意产业经济…）
3. I/R主导的学生：推荐理工类前沿（粒子物理/胶球、航天/南天门、聚变/CFETR、量子/墨子号、AI芯片、合成生物/CRISPR、脑机接口…）
4. 方向从你的知识中自由生成，不限个数。每个方向必须：真实、前沿、有国家战略背景
5. 每个方向配一句话说明"为什么是国家战略级前沿"和一个院校梯度(冲刺/匹配/保底)

## 输出格式（严格JSON，无其他文本）
{
  "riasec_scores": {"R":3,"I":5,"A":8,"S":7,"E":6,"C":4},
  "persona_summary": "100字有温度的人格描述",
  "capability_tags": ["标签1","标签2","标签3"],
  "strategies": [
    {"name":"方向名","score":85,"desc":"40字解释+国家战略意义","schools":[{"tier":"冲刺","list":["校1","校2"]},{"tier":"匹配","list":["校3","校4"]},{"tier":"保底","list":["校5"]}]}
  ],
  "careers": [
    {"name":"专业/职业名","match":82,"desc":"40字描述","salary":"薪资区间","growth":"行业趋势","schools":["校1","校2","校3"]}
  ],
  "timeline_stages": [
    {"period":"高中2025-2027","title":"高中","desc":"50字","icon":"📚","tags":["备1","备2"]},
    {"period":"本科2027-2031","title":"本科","desc":"50字","icon":"🎓","tags":["专1","专2"]},
    {"period":"深造/初入职场","title":"深造","desc":"50字","icon":"💼","tags":["方1","方2"]},
    {"period":"成熟期","title":"十年后","desc":"50字","icon":"🌟","tags":["远1","远2"]}
  ]
}

strategies 3-5个、careers 3-5个。scores/match是0-100的整数。A/S型学生top方向不能出现粒子物理/航天/聚变。"""


@app.post("/api/analyze")
async def analyze(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    subjects = data.get("subjects", [])
    interests = data.get("interests", "")
    self_desc = data.get("self_description", "")
    user_msg = (
        f"选科:{', '.join(subjects) if subjects else '无'}\n"
        f"兴趣:{interests or '无'}\n"
        f"自述:{self_desc or '无'}\n输出JSON。"
    )

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.3,
            timeout=60,
        )
        content = resp.choices[0].message.content
        if "```" in content:
            parts = content.split("```")
            content = parts[1] if len(parts) > 1 else parts[0]
            if content.startswith("json"):
                content = content[4:]
        result = json.loads(content.strip())
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)