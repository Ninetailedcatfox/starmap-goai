import json, urllib.request, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
cases = [
    ("历史算卦", {"subjects":["历史","语文"],"interests":"研究周易算卦和民俗传统，对考古和古代文明着迷","self_description":"直觉型，喜欢从传统中找规律"}),
    ("物理编程", {"subjects":["数学","物理","信息技术"],"interests":"写代码做物理模拟，看三体对太空着迷，拆电器研究电路","self_description":"逻辑推理强，享受解决复杂问题"}),
]
for label, payload in cases:
    r = json.loads(urllib.request.urlopen(urllib.request.Request("http://localhost:8800/api/analyze", data=json.dumps(payload).encode(), headers={"Content-Type":"application/json"}), timeout=60).read())
    s = ', '.join([f"{c['name'][:4]}({c['match']}%)" for c in r["careers"][:3]])
    riasec = ', '.join([f"{k}={v:.0f}" for k,v in sorted(r["riasec_scores"].items(), key=lambda x:-x[1])[:3]])
    print(f"{label}: {s}\n  RIASEC: {riasec}\n")
