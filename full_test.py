import json, urllib.request, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
data = json.dumps({"subjects": ["历史", "语文"], "interests": "喜欢考古和民俗研究，对古代文明特别着迷", "self_description": "直觉型，擅长从古老文本和传统中找规律，对文化符号敏感"}).encode()
r = json.loads(urllib.request.urlopen(urllib.request.Request("http://localhost:8800/api/analyze", data=data, headers={"Content-Type": "application/json"}), timeout=60).read())
scores = r["riasec_scores"]
print("RIASEC:", {k:round(v,1) for k,v in sorted(scores.items(), key=lambda x:-x[1])})
print()
for s in r["strategies"]:
    print(f"  {s['name']}: {s['score']}%")
print()
for c in r["careers"]:
    print(f"  {c['name']}: {c['match']}%")
