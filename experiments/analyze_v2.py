#!/usr/bin/env python
"""
VWA extended evaluation - analysis
Reads results/v2/<tag>_r<k>.json (written by run_experiments_v2.py) and reports, per model/tag and condition:
  * accuracy = agreement of the veto outcome with the author-assigned label (per run: mean, SD, min, max)
  * 95% bootstrap CI over scenarios of the run-averaged per-scenario correctness (10,000 resamples, seed 1)
  * paired comparisons between conditions: mean difference with bootstrap CI, discordant counts and exact McNemar p per run
  * run-to-run consistency of the veto decision
  * latency: mean of scenario means (SD across runs), paired Wilcoxon signed-rank tests between conditions
  * score-only threshold sweep (JAG scores from the `full` condition; the LLM's own boolean flag is ignored)
  * veto provenance (score rule / LLM flag only / parse failure) and JSON parse-failure rates
Usage:  python analyze_v2.py [results/v2]   ->  prints Markdown tables, writes <dir>/analysis_summary.json
"""
import glob
import json
import os
import re
import sys
from collections import defaultdict
from math import comb

import numpy as np

try:
    from scipy.stats import wilcoxon
except Exception:
    wilcoxon = None

D = sys.argv[1] if len(sys.argv) > 1 else "results/v2"
rng = np.random.default_rng(1)
B = 10000


def load():
    runs = defaultdict(dict)
    for fn in sorted(glob.glob(f"{D}/*_r*.json")):
        m = re.match(r"(.+)_r(\d+)\.json$", os.path.basename(fn))
        if not m:
            continue
        with open(fn) as f:
            runs[m.group(1)][int(m.group(2))] = json.load(f)
    return runs


def mcnemar_exact(b, c):
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = 2 * sum(comb(n, i) for i in range(0, k + 1)) / 2 ** n
    return min(1.0, p)


def boot_ci(x, y=None):
    """x (and y) : arrays (scenarios,) of run-averaged correctness. returns mean, lo, hi of mean(x) or mean(x-y)."""
    v = np.asarray(x if y is None else np.asarray(x) - np.asarray(y), dtype=float)
    idx = rng.integers(0, len(v), size=(B, len(v)))
    m = v[idx].mean(axis=1)
    return float(v.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def conds_of(run):
    return list(run["results"][0]["conditions"].keys())


def main():
    runs = load()
    out = {}
    for tag, reps in runs.items():
        ks = sorted(reps)
        first = reps[ks[0]]
        conds = conds_of(first)
        meta = first["metadata"]
        scen = [r["scenario_id"] for r in first["results"]]
        exp = np.array([r["expected_veto"] for r in first["results"]])
        n = len(scen)
        T = {"model": meta["model"], "temperature": meta["temperature"], "repeats": len(ks), "conditions": {}}
        veto = {c: np.array([[reps[k]["results"][i]["conditions"][c]["veto_triggered"] for i in range(n)] for k in ks]) for c in conds}
        corr = {c: (veto[c] == exp[None, :]) for c in conds}
        lat = {c: np.array([[reps[k]["results"][i]["conditions"][c]["total_elapsed_seconds"] for i in range(n)] for k in ks]) for c in conds}
        print(f"\n## {tag}  ({meta['model']}, T={meta['temperature']}, {len(ks)} repeats)")
        print("\n| Condition | Accuracy per run (mean ± SD) [min–max] | 95% CI (scenario bootstrap) | Identical veto decision across runs | Mean latency, s (mean of scenario means; SD across runs) |")
        print("|---|---|---|---|---|")
        for c in conds:
            acc_runs = corr[c].mean(axis=1) * 100
            m, lo, hi = boot_ci(corr[c].mean(axis=0))
            same = float((veto[c].min(axis=0) == veto[c].max(axis=0)).mean()) * 100
            lrun = lat[c].mean(axis=1)
            T["conditions"][c] = dict(acc_runs=acc_runs.tolist(), acc_mean=float(acc_runs.mean()), acc_sd=float(acc_runs.std(ddof=1)) if len(ks) > 1 else 0.0,
                                      ci=[lo * 100, hi * 100], consistency_pct=same, lat_mean=float(lrun.mean()),
                                      lat_sd=float(lrun.std(ddof=1)) if len(ks) > 1 else 0.0, lat_min=float(lat[c].min()), lat_max=float(lat[c].max()))
            sd = acc_runs.std(ddof=1) if len(ks) > 1 else 0.0
            print(f"| {c} | {acc_runs.mean():.1f} ± {sd:.1f} [{acc_runs.min():.0f}–{acc_runs.max():.0f}] | {lo*100:.0f}–{hi*100:.0f}% | {same:.0f}% | {lrun.mean():.1f} ({(lrun.std(ddof=1) if len(ks)>1 else 0):.2f}) |")

        pairs = [("full", "noveto"), ("full", "baseline"), ("full", "legal_only"), ("legal_only", "noveto"), ("full", "full_seq")]
        print("\n| Paired comparison (accuracy) | Mean diff, pp [95% CI] | b / c per run | Exact McNemar p per run |")
        print("|---|---|---|---|")
        T["paired"] = {}
        for a, b_ in pairs:
            if a in conds and b_ in conds:
                d, lo, hi = boot_ci(corr[a].mean(axis=0), corr[b_].mean(axis=0))
                bc, ps = [], []
                for r in range(len(ks)):
                    b = int((corr[a][r] & ~corr[b_][r]).sum()); c_ = int((~corr[a][r] & corr[b_][r]).sum())
                    bc.append(f"{b}/{c_}"); ps.append(mcnemar_exact(b, c_))
                T["paired"][f"{a}-{b_}"] = dict(diff_pp=d * 100, ci=[lo * 100, hi * 100], bc=bc, p=ps)
                print(f"| {a} vs {b_} | {d*100:+.1f} [{lo*100:+.1f}, {hi*100:+.1f}] | {', '.join(bc)} | {', '.join(f'{p:.3g}' for p in ps)} |")

        lp = [("full", "noveto"), ("full_seq", "noveto"), ("full", "full_seq"), ("baseline", "noveto")]
        print("\n| Latency comparison (scenario means over runs) | Median diff, s | Wilcoxon p |")
        print("|---|---|---|")
        T["latency_pairs"] = {}
        for a, b_ in lp:
            if a in conds and b_ in conds:
                x = lat[a].mean(axis=0); y = lat[b_].mean(axis=0)
                p = float(wilcoxon(x, y).pvalue) if wilcoxon is not None and np.any(x != y) else float("nan")
                T["latency_pairs"][f"{a}-{b_}"] = dict(median_diff=float(np.median(x - y)), mean_diff=float((x - y).mean()), p=p)
                print(f"| {a} − {b_} | {np.median(x-y):+.2f} (mean {np.mean(x-y):+.2f}) | {p:.3g} |")

        T["lat_by_scenario"] = {c: lat[c].mean(axis=0).tolist() for c in conds}
        T["scenario_ids"] = scen
        pf = defaultdict(lambda: [0, 0])
        for k in ks:
            for r in reps[k]["results"]:
                for c in conds:
                    for ag, o in r["conditions"][c]["agents"].items():
                        pf[ag][1] += 1
                        if "raw_response" in o:
                            pf[ag][0] += 1
        T["parse_failures"] = {ag: v for ag, v in pf.items()}
        print("\nJSON parse failures (failed/total calls): " + ", ".join(f"{ag} {v[0]}/{v[1]}" for ag, v in pf.items()))

        if "full" in conds:
            prov = defaultdict(int)
            sweep = defaultdict(lambda: [0, 0, 0])
            taus = [round(t, 2) for t in np.arange(0.50, 1.001, 0.05)]
            for k in ks:
                for r in reps[k]["results"]:
                    j = r["conditions"]["full"]["agents"]["jag"]
                    e = r["expected_veto"]
                    if "raw_response" in j:
                        prov["parse failure"] += 1
                        sc = None
                    else:
                        sc = [j.get("distinction_score", 0), j.get("proportionality_score", 0), j.get("necessity_score", 0)]
                        try:
                            by_score = any(s < 0.85 for s in sc)
                        except TypeError:
                            by_score = True
                        if by_score:
                            prov["score rule"] += 1
                        elif j.get("veto_triggered"):
                            prov["LLM flag only"] += 1
                    for t in taus:
                        v = True if sc is None else any((s < t) for s in sc if isinstance(s, (int, float)))
                        sweep[t][0] += int(v == e); sweep[t][1] += int(v and not e); sweep[t][2] += int((not v) and e)
            tot = len(ks) * n
            T["veto_provenance"] = dict(prov)
            T["threshold_sweep"] = {str(t): dict(acc=sweep[t][0] / tot * 100, fp=sweep[t][1] / len(ks), fn=sweep[t][2] / len(ks)) for t in taus}
            print("\nVeto provenance (full, all runs): " + ", ".join(f"{k}: {v}" for k, v in prov.items()))
            print("\n| τ | Accuracy % | FP per run | FN per run |\n|---|---|---|---|")
            for t in taus:
                print(f"| {t:.2f} | {sweep[t][0]/tot*100:.0f} | {sweep[t][1]/len(ks):.1f} | {sweep[t][2]/len(ks):.1f} |")
        out[tag] = T
    with open(f"{D}/analysis_summary.json", "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwritten {D}/analysis_summary.json")


if __name__ == "__main__":
    main()
