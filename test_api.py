import json, urllib.request, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

API = "http://localhost:8800/api/analyze"

cases = [
    {
        "label": "文科-历史兴趣",
        "payload": {
            "subjects": ["历史", "语文", "政治"],
            "interests": "喜欢阅读文学作品和历史书籍，写日记和散文，关注社会新闻和公共议题，平时在社团组织活动",
            "self_description": "善于表达和沟通，对人和社会的运作方式很感兴趣，共情能力强，不太喜欢数学和抽象推理"
        }
    },
    {
        "label": "理科-物理狂热",
        "payload": {
            "subjects": ["数学", "物理", "信息技术"],
            "interests": "从小喜欢拆电器研究电路，看《三体》对太空和宇宙着迷，写代码做物理模拟，参加数学竞赛",
            "self_description": "逻辑思维强，喜欢一个人钻研问题，对数字和公式敏感，享受解决复杂谜题的过程，社交偏被动"
        }
    },
    {
        "label": "均衡-生物+艺术",
        "payload": {
            "subjects": ["生物", "化学", "美术"],
            "interests": "喜欢在自然里观察动植物并画下来，对基因和生物进化很好奇，也在学数字绘画和3D建模",
            "self_description": "左右脑都用的类型，既能专注实验数据，也能沉浸在创作里。希望找到科学与艺术交叉的方向"
        }
    },
    {
        "label": "社科-领导型",
        "payload": {
            "subjects": ["政治", "英语", "历史"],
            "interests": "参加模联和辩论赛，关注国际关系和经济发展，喜欢看商业案例分析，在做校园创业项目",
            "self_description": "目标导向，喜欢带领团队完成挑战，对商业和法律都有兴趣，不擅长也不喜欢数理推导"
        }
    },
]

def test(case):
    data = json.dumps(case["payload"]).encode()
    req = urllib.request.Request(API, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            result = json.loads(resp.read())
            scores = result.get("riasec_scores", {})
            riasec_str = ", ".join([f"{k}={v:.1f}" for k, v in sorted(scores.items(), key=lambda x: -x[1])])
            top3 = sorted(scores, key=scores.get, reverse=True)[:3]
            careers = result.get("careers", [])
            career_str = ", ".join([f"{c['name']}({c.get('match','?')}%)" for c in careers[:3]])
            strategies = result.get("strategies", [])
            strat_str = ", ".join([f"{s['name']}({s.get('score','?')})" for s in strategies[:3]])
            print(f"\n{'='*60}")
            print(f"  {case['label']}")
            print(f"  RIASEC → {riasec_str}")
            print(f"  Top3  → {top3}")
            print(f"  ✅ 战略 → {strat_str}")
            print(f"  ✅ 职业 → {career_str}")
            print(f"  🧠 画像 → {result.get('persona_summary','')[:80]}")
            return True
    except Exception as e:
        print(f"\n  ❌ {case['label']} 失败: {e}")
        return False

if __name__ == "__main__":
    print("🧪 星图·择途 API 自动测试\n")
    ok = 0
    for c in cases:
        if test(c):
            ok += 1
    print(f"\n{'='*60}")
    print(f"  {ok}/{len(cases)} 轮通过")
