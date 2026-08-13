import json
from typing import Dict, List
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from src.config import LLM_MODEL, LLM_API_KEY, LLM_BASE_URL, LLM_TEMPERATURE, STRATEGIC_DIRECTIONS, INDUSTRY_TRENDS


class IntelligenceAgent:
    """Agent ②: 情报 Agent — 整合国家战略、行业趋势、高校数据"""

    SYSTEM_PROMPT = """你是一位国家战略与产业趋势分析师。请根据学生的兴趣方向和能力标签，从知识库中检索并整合相关信息。

你需要整合：
1. **国家战略方向**：与该生特质相关的国家重大科技方向（如胶球/南天门/核聚变/量子 等）
2. **行业趋势**：相关行业的增长数据、人才缺口、薪资水平
3. **高校专业匹配**：相关专业的学科评估排名、推荐院校

输出 JSON：
{
  "matched_directions": [
    {
      "name": "方向名称",
      "national_significance": "国家战略意义的一句话说人话版",
      "major_path": ["本科专业", "硕士方向", "博士方向"],
      "institutions": ["推荐院校"],
      "industry_data": {"growth": "增长率", "salary": "薪资区间", "gap": "人才缺口"},
      "fit_reason": "为什么这个方向适合这个学生"
    }
  ],
  "knowledge_card": "一个 200 字的精华摘要，把这个方向讲给高中生能听懂的话"
}
"""

    def __init__(self):
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            api_key=LLM_API_KEY,
            base_url=LLM_BASE_URL or None,
            temperature=LLM_TEMPERATURE,
        )
        self.strategic_directions = STRATEGIC_DIRECTIONS
        self.industry_trends = INDUSTRY_TRENDS

    def gather(self, profile: Dict) -> Dict:
        capability_tags = profile.get("capability_tags", [])
        riasec_top = profile.get("top_riasec", [])
        recommended_categories = profile.get("recommended_major_categories", [])

        user_message = f"""学生画像：
- 能力标签：{capability_tags}
- Holland 兴趣类型：{riasec_top}
- 推荐学科门类：{recommended_categories}

已知的国家战略方向：
{json.dumps(self.strategic_directions, ensure_ascii=False, indent=2)}

已知的行业趋势数据：
{json.dumps(self.industry_trends, ensure_ascii=False, indent=2)}

请从上述知识库中筛选 3-5 个最匹配的方向，并输出 JSON。"""

        response = self.llm.invoke([
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(content=user_message),
        ])

        result = self._parse_json(response.content)
        result["knowledge_sources"] = {
            "strategic_count": len(self.strategic_directions),
            "industry_count": len(self.industry_trends),
        }
        return result

    def _parse_json(self, text: str) -> Dict:
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())
