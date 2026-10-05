"""
VWA figure generator.

Fig. 3: agreement of the veto outcome with the labels per condition for four local LLMs (95% scenario-bootstrap intervals), with the temperature and neutral-JAG-prompt checks.
Fig. 4: mean latency against the number of LLM calls per condition.
Fig. 5: post-hoc threshold sweep of the JAG score rule.
Reads results/v2/analysis_summary.json. Run from the repository root:   python experiments/generate_figures.py
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SRC = "results/v2/analysis_summary.json"
OUT = "figures"
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["STIXGeneral", "DejaVu Serif"], "mathtext.fontset": "stix",
    "font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42, "ps.fonttype": 42,
})
COL = {"baseline": "#C0392B", "noveto": "#E67E22", "full": "#1A5276", "legal_only": "#1E8449", "full_seq": "#5DADE2"}
LAB = {"baseline": "Baseline", "noveto": "VWA-NoVeto", "full": "VWA-Full", "legal_only": "JAG-only", "full_seq": "VWA-Full (sequential)"}
MODELS = [("llama31_8b_T0", "Llama 3.1 8B"), ("qwen25_7b_T0", "Qwen 2.5 7B"), ("gemma2_9b_T0", "Gemma 2 9B"), ("mistral_7b_T0", "Mistral 7B")]
CALLS = {"baseline": 2, "noveto": 4, "full": 4, "full_seq": 4, "legal_only": 1}

D = json.load(open(SRC))


def save(fig, name):
    fig.savefig(f"{OUT}/{name}.pdf", bbox_inches="tight")
    fig.savefig(f"{OUT}/{name}.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("saved", name)


def fig3():
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.4, 3.1), gridspec_kw={"width_ratios": [1.7, 1]})
    conds = ["baseline", "noveto", "full", "legal_only"]
    w = 0.2
    for i, c in enumerate(conds):
        for j, (tag, _) in enumerate(MODELS):
            v = D[tag]["conditions"][c]
            x = j + (i - 1.5) * w
            a.bar(x, v["acc_mean"], w * 0.92, color=COL[c], label=LAB[c] if j == 0 else None)
            a.errorbar(x, v["acc_mean"], yerr=[[v["acc_mean"] - v["ci"][0]], [v["ci"][1] - v["acc_mean"]]], color="#222", lw=0.8, capsize=1.5)
            a.text(x, 103, f"{v['acc_mean']:.0f}", ha="center", va="bottom", fontsize=6.5)
    a.set_xticks(range(len(MODELS))); a.set_xticklabels([m for _, m in MODELS])
    a.set_ylim(0, 112); a.set_yticks([0, 25, 50, 75, 100]); a.set_ylabel("Agreement of veto outcome\nwith labels (%)")
    a.legend(frameon=False, fontsize=7, ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.22))
    a.set_title("(a) Four local LLMs, T=0", fontsize=8.5, y=-0.28)

    groups = [("llama31_8b_T0", "T=0\noriginal"), ("llama31_8b_T07", "T=0.7\noriginal"), ("llama31_8b_T0_neutralJAG", "T=0\nneutral JAG")]
    w2 = 0.3
    for i, c in enumerate(["full", "legal_only"]):
        for j, (tag, _) in enumerate(groups):
            v = D[tag]["conditions"][c]
            x = j + (i - 0.5) * w2
            b.bar(x, v["acc_mean"], w2 * 0.92, color=COL[c], label=LAB[c] if j == 0 else None)
            b.errorbar(x, v["acc_mean"], yerr=[[v["acc_mean"] - v["ci"][0]], [v["ci"][1] - v["acc_mean"]]], color="#222", lw=0.8, capsize=1.5)
            b.text(x, 103, f"{v['acc_mean']:.0f}", ha="center", va="bottom", fontsize=6.5)
    b.set_xticks(range(len(groups))); b.set_xticklabels([g for _, g in groups], fontsize=7.5)
    b.set_ylim(0, 112); b.set_yticks([0, 25, 50, 75, 100])
    b.legend(frameon=False, fontsize=7, ncol=2, loc="upper center", bbox_to_anchor=(0.5, 1.22))
    b.set_title("(b) Llama 3.1 8B robustness checks", fontsize=8.5, y=-0.28)
    fig.tight_layout()
    save(fig, "figure3_evaluation")


def fig4():
    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    marks = {"llama31_8b_T0": "o", "qwen25_7b_T0": "s", "gemma2_9b_T0": "^", "mistral_7b_T0": "D"}
    for tag, name in MODELS:
        for c, v in D[tag]["conditions"].items():
            ax.errorbar(CALLS[c], v["lat_mean"], yerr=v["lat_sd"], fmt=marks[tag], color=COL[c], mfc=COL[c] if c != "full_seq" else "white",
                        ms=5, lw=0.8, capsize=1.5, alpha=0.9)
    xs = np.array([CALLS[c] for tag, _ in MODELS for c in D[tag]["conditions"]], float)
    ys = np.array([v["lat_mean"] for tag, _ in MODELS for v in D[tag]["conditions"].values()])
    k = float((xs * ys).sum() / (xs * xs).sum())
    xx = np.linspace(0, 4.4, 20)
    ax.plot(xx, k * xx, color="#888", lw=0.8, ls="--")
    ax.text(2.35, 2.2, f"dashed: ≈{k:.1f} s per call on average\n(least squares through the origin)", ha="left", fontsize=7, color="#555")
    ax.set_xticks([1, 2, 4]); ax.set_xticklabels(["1\nJAG-only", "2\nBaseline", "4\nNoVeto / Full"])
    ax.set_xlim(0.5, 4.6); ax.set_ylim(0, 27)
    ax.set_xlabel("LLM calls per scenario"); ax.set_ylabel("Mean latency per scenario (s)")
    handles = [plt.Line2D([], [], marker=m, color="#555", ls="", ms=5, label=n) for (t, n), m in zip(MODELS, marks.values())]
    ax.legend(handles=handles, frameon=False, fontsize=7, loc="upper left")
    fig.tight_layout()
    save(fig, "figure4_latency_calls")


def fig5():
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    sty = {"llama31_8b_T0": ("Llama 3.1 8B, T=0", "-", "#1A5276"), "llama31_8b_T07": ("Llama 3.1 8B, T=0.7", "--", "#1A5276"),
           "qwen25_7b_T0": ("Qwen 2.5 7B", "-", "#E67E22"), "gemma2_9b_T0": ("Gemma 2 9B", "-", "#1E8449"), "mistral_7b_T0": ("Mistral 7B", "-", "#8E44AD")}
    for tag, (lab, ls, col) in sty.items():
        ts = sorted(D[tag]["threshold_sweep"], key=float)
        ax.plot([float(t) for t in ts], [D[tag]["threshold_sweep"][t]["acc"] for t in ts], ls=ls, color=col, lw=1.3, marker="o", ms=2.5, label=lab)
    ax.axvline(0.85, color="#999", lw=0.8, ls=":")
    ax.text(0.857, 101, "pre-set τ = 0.85", fontsize=7, color="#555", va="top")
    ax.set_xlabel("Score threshold τ (veto if any IHL score < τ)"); ax.set_ylabel("Agreement with labels (%)")
    ax.set_ylim(40, 105); ax.legend(frameon=False, fontsize=7, loc="lower right", bbox_to_anchor=(1.0, 0.0), borderaxespad=0.2)
    fig.tight_layout()
    save(fig, "figure5_threshold")


if __name__ == "__main__":
    fig3(); fig4(); fig5()
