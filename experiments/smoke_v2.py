import sys, json, os
sys.argv=["x"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_experiments_v2 as m
llm=m.LLM("llama3.1:8b",0.0)
sc=json.load(open("scenarios/s5_pattern_of_life.json"))
for c in ["baseline","noveto","full","full_seq","legal_only"]:
    r=m.PIPES[c](llm,sc)
    print(c, r["veto"], r["total_elapsed_seconds"], len(r["conflicts"]), {k:v.get("elapsed_seconds") for k,v in r["agents"].items()}, flush=True)
print("DONE")
