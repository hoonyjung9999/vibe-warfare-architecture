# Vibe Warfare Architecture (VWA) – evaluation code and data

Code, scenarios, prompts, raw outputs, and analysis scripts for the manuscript

> Seunghoon Jung. *Vibe Warfare Architecture: A Natural Language-Driven Multi-Agent Framework for Virtual Staff Operations in Military Command and Control.* Manuscript under review (Journal of Defense Modeling and Simulation).

**Status:** research prototype for a simulation study. It is not a validated system and must not be used to support real operational or targeting decisions.

## What is and is not implemented

The prototype implements four LLM agents (J2 intelligence, J3 operations/COA, J4 logistics, JAG legal review) and the Inter-Agent Checks and Balances (IACB) layer: two conflict-detection threshold rules, one veto rule (JAG flag, or any of the three IHL scores below 0.85, or an unparseable JAG output), and a structured audit record. The other agents of the architecture, the parsing of a commander's Vibe into a structured intent, and a final recommendation text are **not** implemented. The audit log is not tamper-evident.

## What the evaluation measures

"Agreement" is the share of the 14 scenarios in which the veto outcome matches the label **assigned by the author** when writing the scenario (`scenarios/*.json`, field `expected_veto`). It is not an independent measure of legal correctness or of the safety of a course of action, and no independent expert labelling was done. The scenarios are synthetic and contain no classified or real operational material.

## Reported results (all models local via Ollama, temperature 0, 95 % bootstrap intervals over scenarios)

| Model (repeats) | Baseline | VWA-NoVeto | VWA-Full | JAG-only |
|---|---|---|---|---|
| Llama 3.1 8B (5) | 29 % | 29 % | 86 % | 93 % |
| Qwen 2.5 7B (3) | 29 % | 29 % | 79 % | 86 % |
| Gemma 2 9B (3) | 29 % | 29 % | 86 % | 86 % |
| Mistral 7B (3) | 29 % | 29 % | 86 % | 86 % |

Baseline and NoVeto cannot veto by construction, so their 29 % (4 of 14 scenarios labelled "no veto") is fixed by the label distribution. A single legal-agent call on the raw scenario (JAG-only) agrees with the labels at least as often as the full ensemble, so these data support the structural veto rule but do not show a benefit of the staff agents. Full tables, intervals, paired tests, latency, threshold sweep, and the label-sensitivity analysis are in `results/v2/analysis_all_final.md`, `analysis_summary.json`, and `label_sensitivity.json`. Latency is 15–23 s per scenario for the four-call configurations and follows the number of sequential LLM calls.

## Layout

```
agents/        J2, J3, J4, JAG agents and the IACB module (the code used for all reported results)
orchestrator.py  pipelines of the original run
prompts/       agent_prompts.yaml (original) and agent_prompts_neutral.yaml (neutral JAG prompt check)
scenarios/     S1–S14 (Vibe text, structured context, author-assigned label)
experiments/   run_experiments.py (original run); run_experiments_v2.py (extended runs);
               analyze_v2.py; label_sensitivity.py; concurrency_check.py;
               generate_figures.py; run_all_v2.sh, run_remaining_v2.sh (drivers; zsh)
results/original/  original single run and the October 2026 reproduction run
results/v2/    raw JSON outputs of every run (prompts, agent outputs, veto decisions, timings), logs, analyses
figures/       vector figures used in the manuscript
```

## Reproducing

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
ollama pull llama3.1:8b && ollama pull qwen2.5:7b && ollama pull gemma2:9b && ollama pull mistral:7b
zsh experiments/run_all_v2.sh          # extended runs (several hours on an Apple M2 Pro)
zsh experiments/run_remaining_v2.sh    # Mistral re-run and neutral-prompt check
python experiments/analyze_v2.py results/v2
python experiments/label_sensitivity.py
python experiments/generate_figures.py
```

Environment of the reported runs: macOS on Apple M2 Pro (32 GB), Python 3.14.7, Ollama 0.32.1, default Ollama builds of the four models (run metadata, including `ollama list`, is stored in each result file). Results may differ on other hardware or software versions; at temperature 0 the veto decisions were identical across repeats on this machine, but determinism is not guaranteed elsewhere.

## Known issues

* `agents/iacb.py`, phase 3 (confidence scoring) raises an exception when an agent returns a null numeric field. Phase 3 runs only when no veto is raised and does not influence the veto decision. The extended harness (`run_experiments_v2.py`, `safe_iacb`) catches the error, falls back to the JAG veto flag, and records it; the reported results are not affected. The module is left unchanged so that the released code is the code that produced the results.
* JSON parse failures of some agents (7–14 % of calls for Llama and Qwen J2/J3) are recorded in the analysis; an unparseable JAG output is treated as a veto (fail-safe).

## License and citation

License: MIT (see `LICENSE`). Copyright (c) 2026 Seunghoon Jung. The scenarios and results in this repository are released under the same license.
This is a research prototype; see the notice at the top of this file about operational use.
Citation: *to be added after acceptance.*
