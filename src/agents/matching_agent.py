import json
from typing import Dict, List
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from src.config import LLM_MODEL, LLM_API_KEY, LLM_BASE_URL, LLM_TEMPERATURE


class MatchingAgent:
    """Agent ③: 匹配 Agent — 交叉比对输出推荐方向"""

    SYSTEM_PROMPT = """你是一位高考志愿规划与职业发展顾问。请根据学生画像 + 情报数据，做交叉匹配分析。

匹配权重：
- 能力匹配度 40%
- 兴趣契合度 30%
- 国家战略相关性 20%
- 发展容错率 10%（该路径是否有多条退路/变道可能）

输出 JSON：
{
  "recommendations": [
    {
      "rank": 1,
      "direction_name": "方向名称",
      "fit_score": 0.92,
      "ability_match": "为什么能力匹配",
      "interest_match": "为什么兴趣匹配",
      "national_relevance": "国家战略关联度说明",
      "academic_path": "本科→硕士→博士 推荐路径",
      "institutions_tiered": {
        "冲刺": ["院校"],
        "匹配": ["院校"],
        "保底": ["院校"]
      },
      "future_outlook": "5-10年职业前景",
      "one_sentence": "一句话推荐理由"
    }
  ],
  "avoid": [
    {
      "direction": "方向",
      "reason": "为什么不建议"
    }
  ],
  "hidden_gems": [
    {
      "direction": "小众方向",
      "reason": "为什么是隐藏宝藏"
    }
  ]
}
"""

    def __init__(self):
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            api_key=LLM_API_KEY,
            base_url=LLM_BASE_URL or None,
            temperature=LLM_TEMPERATURE,
        )

    def match(self, profile: Dict, intelligence: Dict) -> Dict:
        user_message = f"""请进行交叉匹配分析：

【学生画像】
{json.dumps(profile, ensure_ascii=False, indent=2)}

【情报数据】
{json.dumps(intelligence.get("matched_directions", []), ensure_ascii=False, indent=2)}

请输出匹配结果 JSON。确保推荐有层次："冲刺/匹配/保底"院校，以及"避坑"和"隐藏宝藏"。"""

        response = self.llm.invoke([
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(content=user_message),
        ])

        result = self._parse_json(response.content)
        result["matching_metadata"] = {
            "profile_input_keys": list(profile.keys()),
            "intelligence_directions_count": len(intelligence.get("matched_directions", [])),
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
