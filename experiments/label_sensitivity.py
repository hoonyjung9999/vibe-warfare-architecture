"""Computes (a) agreement on the 10 unambiguous scenarios only; (b) range of paired differences over all 16 alternative labelings of the 4 borderline scenarios (S11-S14).
Unit: scenario-level veto outcome (majority over repeats; at T=0 outcomes are identical across repeats). Output: label_sensitivity.json"""
import json, glob, itertools, random, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/../results/v2")
TAGS = ["llama31_8b_T0", "qwen25_7b_T0", "gemma2_9b_T0", "mistral_7b_T0"]
IDS = [f"S{i}" for i in range(1, 15)]
LAB = {s: True for s in IDS}; 
for s in ["S3", "S7", "S11", "S13"]: LAB[s] = False
def outcomes(tag):
    acc = {}
    for f in sorted(glob.glob(tag + "_r[0-9].json")):
        d = json.load(open(f)); recs = d if isinstance(d, list) else d.get("results", d)
        if isinstance(recs, dict): recs = list(recs.values())
        for r in recs:
            for c, v in r["conditions"].items(): acc.setdefault((c, r["scenario_id"]), []).append(bool(v["veto_triggered"]))
    return {k: (sum(v) * 2 > len(v)) for k, v in acc.items()}
def ci(vals, B=10000, seed=1):
    rnd = random.Random(seed); n = len(vals); m = sorted(sum(vals[rnd.randrange(n)] for _ in range(n)) / n * 100 for _ in range(B)); return round(m[int(.025 * B)], 1), round(m[int(.975 * B) - 1], 1)
OUT = {}
for tag in TAGS:
    o = outcomes(tag); res = {"unamb": {}, "paired_range": {}}
    un = IDS[:10]
    for c in ["baseline", "noveto", "full", "legal_only"]:
        ok = [int(o[(c, s)] == LAB[s]) for s in un]; res["unamb"][c] = {"agree": sum(ok), "n": 10, "pct": sum(ok) * 10, "ci": ci(ok)}
    d_fn = [int(o[("full", s)] == LAB[s]) - int(o[("noveto", s)] == LAB[s]) for s in un]; res["unamb"]["full-noveto_pp"] = round(sum(d_fn) * 10, 1); res["unamb"]["full-noveto_ci"] = ci(d_fn)
    d_fj = [int(o[("full", s)] == LAB[s]) - int(o[("legal_only", s)] == LAB[s]) for s in un]; res["unamb"]["full-legal_pp"] = round(sum(d_fj) * 10, 1)
    fn, fj, accF = [], [], []
    for bl in itertools.product([True, False], repeat=4):
        L = dict(LAB); L.update(dict(zip(["S11", "S12", "S13", "S14"], bl)))
        a = lambda c: sum(o[(c, s)] == L[s] for s in IDS) / 14 * 100
        fn.append(a("full") - a("noveto")); fj.append(a("full") - a("legal_only")); accF.append(a("full"))
    res["paired_range"] = {"full-noveto_pp": [round(min(fn), 1), round(max(fn), 1)], "full-legal_pp": [round(min(fj), 1), round(max(fj), 1)], "full_agree_pct": [round(min(accF), 1), round(max(accF), 1)]}
    OUT[tag] = res; print(tag, json.dumps(res))
json.dump(OUT, open("label_sensitivity.json", "w"), indent=1)
