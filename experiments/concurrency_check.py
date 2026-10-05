"""Checks whether overlapping two Ollama requests (J2 and J4 prompts) reduce wall-clock time vs sequential?
Llama 3.1 8B, T=0, scenario S5, 8 interleaved trials; warm-up excluded. Output: results/v2/concurrency_check.json"""
import json, time, threading, yaml, ollama, statistics as st
P = yaml.safe_load(open("prompts/agent_prompts.yaml")); sc = json.load(open("scenarios/s5_pattern_of_life.json")); c = sc["context"]
u2 = f"\nSituation: {sc['vibe']}\nLocation: {c['location']}\nThreat: {c['threat']}\nCivilian Presence: {c['civilian_presence']}\nTime Pressure: {c['time_pressure']}\nAvailable Assets: {', '.join(c['available_assets'])}\n\nProvide your intelligence assessment.\n"
u4 = f"\nOperation: {sc['vibe']}\nLocation: {c['location']}\nAvailable Assets: {', '.join(c['available_assets'])}\nTime Pressure: {c['time_pressure']}\n\nAssess logistical support for this operation.\n"
def call(sys_, u, out, k):
    t = time.time(); ollama.chat(model="llama3.1:8b", messages=[{"role": "system", "content": sys_}, {"role": "user", "content": u}], options={"temperature": 0}); out[k] = time.time() - t
def seq():
    o = {}; t = time.time(); call(P["j2_agent"], u2, o, "j2"); call(P["j4_agent"], u4, o, "j4"); return time.time() - t, o
def con():
    o = {}; t = time.time(); th = [threading.Thread(target=call, args=(P["j2_agent"], u2, o, "j2")), threading.Thread(target=call, args=(P["j4_agent"], u4, o, "j4"))]
    [x.start() for x in th]; [x.join() for x in th]; return time.time() - t, o
seq()
R = {"seq": [], "con": []}
for i in range(8):
    order = ["seq", "con"] if i % 2 == 0 else ["con", "seq"]
    for m in order:
        t, o = (seq if m == "seq" else con)(); R[m].append({"total": round(t, 2), "j2": round(o["j2"], 2), "j4": round(o["j4"], 2)}); print(i, m, R[m][-1], flush=True)
S = {m: {"mean_total": round(st.mean(r["total"] for r in R[m]), 2), "mean_j2": round(st.mean(r["j2"] for r in R[m]), 2), "mean_j4": round(st.mean(r["j4"] for r in R[m]), 2)} for m in R}
json.dump({"runs": R, "summary": S}, open("results/v2/concurrency_check.json", "w"), indent=1); print("SUMMARY", S)
