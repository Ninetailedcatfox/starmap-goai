import os
from dotenv import load_dotenv

load_dotenv()

LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma_db")

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "knowledge")

RIASEC_TYPES = ["现实型(R)", "研究型(I)", "艺术型(A)", "社会型(S)", "企业型(E)", "常规型(C)"]

STRATEGIC_DIRECTIONS = [
    {
        "name": "粒子物理与基础科学",
        "keywords": ["胶球", "北京谱仪", "BESⅢ", "高能物理", "标准模型"],
        "majors": ["粒子物理与原子核物理", "理论物理", "物理学"],
        "institutions": ["中国科学技术大学", "中国科学院大学", "北京大学", "南京大学"],
    },
    {
        "name": "航空航天与空天一体化",
        "keywords": ["南天门计划", "空天飞机", "高超音速", "重型运载", "深空探测"],
        "majors": ["航空航天工程", "飞行器设计与工程", "航天动力工程"],
        "institutions": ["北京航空航天大学", "哈尔滨工业大学", "西北工业大学", "国防科技大学"],
    },
    {
        "name": "可控核聚变与新能源",
        "keywords": ["托卡马克", "ITER", "聚变堆", "等离子体", "CFETR"],
        "majors": ["核工程与核技术", "等离子体物理", "新能源科学与工程"],
        "institutions": ["中国科学技术大学", "清华大学", "华中科技大学", "核工业西南物理研究院"],
    },
    {
        "name": "量子科技",
        "keywords": ["量子计算", "量子通信", "墨子号", "量子优越性", "超导量子比特"],
        "majors": ["量子信息科学", "物理学", "计算机科学与技术"],
        "institutions": ["中国科学技术大学", "清华大学", "浙江大学", "南京大学"],
    },
    {
        "name": "人工智能与芯片",
        "keywords": ["大模型", "GPU", "AI芯片", "智能体", "深度学习", "算力"],
        "majors": ["人工智能", "计算机科学与技术", "集成电路设计与集成系统"],
        "institutions": ["清华大学", "北京大学", "浙江大学", "上海交通大学", "中国科学技术大学"],
    },
    {
        "name": "合成生物学与基因编辑",
        "keywords": ["合成生物学", "CRISPR", "基因治疗", "生物制造", "人造生命"],
        "majors": ["生物科学", "生物工程", "合成生物学"],
        "institutions": ["清华大学", "西湖大学", "天津大学", "中国科学院深圳先进院"],
    },
    {
        "name": "脑科学与脑机接口",
        "keywords": ["脑科学", "脑机接口", "类脑计算", "神经科学", "Neuralink"],
        "majors": ["神经科学", "生物医学工程", "计算机科学与技术"],
        "institutions": ["浙江大学", "复旦大学", "北京大学", "中国科学院脑智卓越中心"],
    },
]

INDUSTRY_TRENDS = [
    {
        "sector": "新能源",
        "growth_3yr": "240%",
        "talent_gap": "预计 2030 年缺口 300 万",
        "avg_salary_entry": "¥18-30万/年",
        "related_majors": ["新能源科学与工程", "能源与动力工程", "材料科学与工程"],
    },
    {
        "sector": "人工智能",
        "growth_3yr": "180%",
        "talent_gap": "算法工程师缺口 500 万+",
        "avg_salary_entry": "¥25-50万/年",
        "related_majors": ["人工智能", "计算机科学与技术", "数据科学"],
    },
    {
        "sector": "半导体/芯片",
        "growth_3yr": "200%",
        "talent_gap": "芯片设计人才缺口 30 万+",
        "avg_salary_entry": "¥20-45万/年",
        "related_majors": ["集成电路设计与集成系统", "微电子科学与工程", "电子科学与技术"],
    },
    {
        "sector": "生物医药",
        "growth_3yr": "120%",
        "talent_gap": "研发人才缺口持续扩大",
        "avg_salary_entry": "¥15-35万/年",
        "related_majors": ["药学", "生物制药", "临床医学"],
    },
    {
        "sector": "航空航天",
        "growth_3yr": "150%",
        "talent_gap": "空天领域年增需求 20%",
        "avg_salary_entry": "¥18-35万/年",
        "related_majors": ["航空航天工程", "飞行器制造工程", "测控技术与仪器"],
    },
]

HOLLAND_MAJOR_MAP = {
    "现实型(R)": ["机械工程", "土木工程", "电气工程", "航空航天工程", "材料科学与工程"],
    "研究型(I)": ["物理学", "数学", "化学", "生物科学", "计算机科学", "基础医学"],
    "艺术型(A)": ["建筑学", "工业设计", "数字媒体艺术", "城市规划", "文学创作"],
    "社会型(S)": ["教育学", "心理学", "临床医学", "社会工作", "公共管理"],
    "企业型(E)": ["金融学", "工商管理", "法学", "市场营销", "国际经济与贸易"],
    "常规型(C)": ["会计学", "统计学", "信息管理与信息系统", "行政管理", "审计学"],
}
