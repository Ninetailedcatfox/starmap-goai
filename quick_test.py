import json, urllib.request, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
data = json.dumps({"subjects": ["历史", "语文"], "interests": "喜欢研究周易算卦和传统文化，对考古和古代文明特别感兴趣", "self_description": "直觉型，喜欢从古老智慧中找规律，对人和文化有深刻的感受力"}).encode()
r = json.loads(urllib.request.urlopen(urllib.request.Request("http://localhost:8800/api/analyze", data=data, headers={"Content-Type": "application/json"}), timeout=60).read())
scores = r["riasec_scores"]
top3 = sorted(scores, key=scores.get, reverse=True)[:3]
print("RIASEC:", ", ".join([f"{k}={scores[k]:.1f}" for k in top3]))
print("Top3:", top3)
for s in r["strategies"][:3]:
    print(f"  {s['name']} ({s.get('score','?')}) — {s.get('desc','')[:50]}")
for c in r["careers"][:3]:
    print(f"  {c['name']} ({c.get('match','?')}%) — {c.get('salary','?')}")
print("画像:", r.get("persona_summary","")[:80])
