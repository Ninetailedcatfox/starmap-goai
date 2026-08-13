import json
from typing import Dict, List
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from src.config import LLM_MODEL, LLM_API_KEY, LLM_BASE_URL, LLM_TEMPERATURE, RIASEC_TYPES


class ProfileAgent:
    """Agent ①: 洞察 Agent — 构建学生能力-兴趣画像"""

    SYSTEM_PROMPT = """你是一位经验丰富的生涯规划师。根据学生提供的信息，生成一份结构化的能力-兴趣画像。

你需要完成以下分析：

1. **Holland 职业兴趣推断**（不让学生做完整量表，而是从对话中推断）：
   - 现实型(R)：喜欢动手操作、工具、机械
   - 研究型(I)：喜欢思考、探究、实验、读论文
   - 艺术型(A)：喜欢创造、表达、设计、写作
   - 社会型(S)：喜欢帮助、教导、合作、沟通
   - 企业型(E)：喜欢领导、说服、组织、竞争
   - 常规型(C)：喜欢秩序、数据处理、流程、规范

2. **核心能力标签**（3-5 个关键词）

3. **一句话人格摘要**（如"数理突出、喜欢动手探索的工程师型"）

请以 JSON 格式输出：
{
  "riasec_scores": {"R": 0.8, "I": 0.9, "A": 0.2, "S": 0.3, "E": 0.1, "C": 0.5},
  "top_riasec": ["I", "R"],
  "capability_tags": ["数理思维", "动手能力", "逻辑推理"],
  "persona_summary": "数理突出、喜欢动手探索的工程师型",
  "learning_style": "实验驱动型",
  "recommended_major_categories": ["工科", "理科"],
  "avoid_major_categories": ["纯文科", "管理类"]
}
"""

    def __init__(self):
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            api_key=LLM_API_KEY,
            base_url=LLM_BASE_URL or None,
            temperature=LLM_TEMPERATURE,
        )

    def analyze(self, student_input: Dict) -> Dict:
        subjects = student_input.get("subjects", {})
        interests = student_input.get("interests", "")
        self_description = student_input.get("self_description", "")
        scores = student_input.get("scores", {})

        user_message = f"""请分析这位学生的画像：

选科/擅长科目：{json.dumps(subjects, ensure_ascii=False)}
平时成绩：{json.dumps(scores, ensure_ascii=False)}
兴趣爱好：{interests}
自我描述：{self_description}

请输出 JSON 格式的画像结果。"""

        response = self.llm.invoke([
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(content=user_message),
        ])

        result = self._parse_json(response.content)
        result["raw_input"] = student_input
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
