
## gemma2_9b_T0  (gemma2:9b, T=0.0, 3 repeats)

| Condition | Accuracy per run (mean ± SD) [min–max] | 95% CI (scenario bootstrap) | Identical veto decision across runs | Mean latency, s (mean of scenario means; SD across runs) |
|---|---|---|---|---|
| baseline | 28.6 ± 0.0 [29–29] | 7–50% | 100% | 9.0 (0.08) |
| legal_only | 85.7 ± 0.0 [86–86] | 64–100% | 100% | 9.3 (0.04) |
| noveto | 28.6 ± 0.0 [29–29] | 7–50% | 100% | 23.3 (0.14) |
| full | 85.7 ± 0.0 [86–86] | 64–100% | 100% | 22.7 (0.23) |

| Paired comparison (accuracy) | Mean diff, pp [95% CI] | b / c per run | Exact McNemar p per run |
|---|---|---|---|
| full vs noveto | +57.1 [+14.3, +92.9] | 10/2, 10/2, 10/2 | 0.0386, 0.0386, 0.0386 |
| full vs baseline | +57.1 [+14.3, +92.9] | 10/2, 10/2, 10/2 | 0.0386, 0.0386, 0.0386 |
| full vs legal_only | +0.0 [+0.0, +0.0] | 0/0, 0/0, 0/0 | 1, 1, 1 |
| legal_only vs noveto | +57.1 [+14.3, +92.9] | 10/2, 10/2, 10/2 | 0.0386, 0.0386, 0.0386 |

| Latency comparison (scenario means over runs) | Median diff, s | Wilcoxon p |
|---|---|---|
| full − noveto | -0.93 (mean -0.68) | 0.0295 |
| baseline − noveto | -14.51 (mean -14.30) | 0.000122 |

JSON parse failures (failed/total calls): j2 0/126, j3 0/126, jag 0/126, j4 0/84

Veto provenance (full, all runs): score rule: 36

| τ | Accuracy % | FP per run | FN per run |
|---|---|---|---|
| 0.50 | 71 | 0.0 | 4.0 |
| 0.55 | 71 | 0.0 | 4.0 |
| 0.60 | 71 | 0.0 | 4.0 |
| 0.65 | 86 | 2.0 | 0.0 |
| 0.70 | 86 | 2.0 | 0.0 |
| 0.75 | 86 | 2.0 | 0.0 |
| 0.80 | 86 | 2.0 | 0.0 |
| 0.85 | 86 | 2.0 | 0.0 |
| 0.90 | 86 | 2.0 | 0.0 |
| 0.95 | 71 | 4.0 | 0.0 |
| 1.00 | 71 | 4.0 | 0.0 |

## llama31_8b_T07  (llama3.1:8b, T=0.7, 5 repeats)

| Condition | Accuracy per run (mean ± SD) [min–max] | 95% CI (scenario bootstrap) | Identical veto decision across runs | Mean latency, s (mean of scenario means; SD across runs) |
|---|---|---|---|---|
| legal_only | 91.4 ± 3.2 [86–93] | 76–100% | 93% | 5.3 (0.35) |
| full | 85.7 ± 0.0 [86–86] | 64–100% | 100% | 17.4 (0.20) |

| Paired comparison (accuracy) | Mean diff, pp [95% CI] | b / c per run | Exact McNemar p per run |
|---|---|---|---|
| full vs legal_only | -5.7 [-17.1, +0.0] | 0/1, 0/1, 0/1, 0/0, 0/1 | 1, 1, 1, 1, 1 |

| Latency comparison (scenario means over runs) | Median diff, s | Wilcoxon p |
|---|---|---|

JSON parse failures (failed/total calls): jag 0/140, j2 5/70, j4 0/70, j3 6/70

Veto provenance (full, all runs): score rule: 60

| τ | Accuracy % | FP per run | FN per run |
|---|---|---|---|
| 0.50 | 79 | 0.0 | 3.0 |
| 0.55 | 81 | 0.2 | 2.4 |
| 0.60 | 81 | 0.2 | 2.4 |
| 0.65 | 90 | 0.6 | 0.8 |
| 0.70 | 90 | 0.6 | 0.8 |
| 0.75 | 94 | 0.8 | 0.0 |
| 0.80 | 94 | 0.8 | 0.0 |
| 0.85 | 86 | 2.0 | 0.0 |
| 0.90 | 86 | 2.0 | 0.0 |
| 0.95 | 86 | 2.0 | 0.0 |
| 1.00 | 86 | 2.0 | 0.0 |

## llama31_8b_T0_neutralJAG  (llama3.1:8b, T=0.0, 3 repeats)

| Condition | Accuracy per run (mean ± SD) [min–max] | 95% CI (scenario bootstrap) | Identical veto decision across runs | Mean latency, s (mean of scenario means; SD across runs) |
|---|---|---|---|---|
| full | 78.6 ± 0.0 [79–79] | 57–100% | 100% | 16.1 (0.04) |
| legal_only | 100.0 ± 0.0 [100–100] | 100–100% | 100% | 4.6 (0.04) |

| Paired comparison (accuracy) | Mean diff, pp [95% CI] | b / c per run | Exact McNemar p per run |
|---|---|---|---|
| full vs legal_only | -21.4 [-42.9, +0.0] | 0/3, 0/3, 0/3 | 0.25, 0.25, 0.25 |

| Latency comparison (scenario means over runs) | Median diff, s | Wilcoxon p |
|---|---|---|

JSON parse failures (failed/total calls): j2 3/42, j4 0/42, j3 3/42, jag 0/84

Veto provenance (full, all runs): score rule: 33

| τ | Accuracy % | FP per run | FN per run |
|---|---|---|---|
| 0.50 | 29 | 0.0 | 10.0 |
| 0.55 | 29 | 0.0 | 10.0 |
| 0.60 | 29 | 0.0 | 10.0 |
| 0.65 | 43 | 0.0 | 8.0 |
| 0.70 | 43 | 0.0 | 8.0 |
| 0.75 | 79 | 0.0 | 3.0 |
| 0.80 | 79 | 0.0 | 3.0 |
| 0.85 | 79 | 2.0 | 1.0 |
| 0.90 | 79 | 2.0 | 1.0 |
| 0.95 | 86 | 2.0 | 0.0 |
| 1.00 | 86 | 2.0 | 0.0 |

## llama31_8b_T0  (llama3.1:8b, T=0.0, 5 repeats)

| Condition | Accuracy per run (mean ± SD) [min–max] | 95% CI (scenario bootstrap) | Identical veto decision across runs | Mean latency, s (mean of scenario means; SD across runs) |
|---|---|---|---|---|
| full | 85.7 ± 0.0 [86–86] | 64–100% | 100% | 18.2 (1.00) |
| legal_only | 92.9 ± 0.0 [93–93] | 79–100% | 100% | 6.1 (0.24) |
| full_seq | 85.7 ± 0.0 [86–86] | 64–100% | 100% | 18.3 (1.30) |
| noveto | 28.6 ± 0.0 [29–29] | 7–50% | 100% | 18.1 (0.70) |
| baseline | 28.6 ± 0.0 [29–29] | 7–57% | 100% | 7.3 (0.30) |

| Paired comparison (accuracy) | Mean diff, pp [95% CI] | b / c per run | Exact McNemar p per run |
|---|---|---|---|
| full vs noveto | +57.1 [+14.3, +92.9] | 10/2, 10/2, 10/2, 10/2, 10/2 | 0.0386, 0.0386, 0.0386, 0.0386, 0.0386 |
| full vs baseline | +57.1 [+14.3, +92.9] | 10/2, 10/2, 10/2, 10/2, 10/2 | 0.0386, 0.0386, 0.0386, 0.0386, 0.0386 |
| full vs legal_only | -7.1 [-21.4, +0.0] | 0/1, 0/1, 0/1, 0/1, 0/1 | 1, 1, 1, 1, 1 |
| legal_only vs noveto | +64.3 [+28.6, +92.9] | 10/1, 10/1, 10/1, 10/1, 10/1 | 0.0117, 0.0117, 0.0117, 0.0117, 0.0117 |
| full vs full_seq | +0.0 [+0.0, +0.0] | 0/0, 0/0, 0/0, 0/0, 0/0 | 1, 1, 1, 1, 1 |

| Latency comparison (scenario means over runs) | Median diff, s | Wilcoxon p |
|---|---|---|
| full − noveto | +0.18 (mean +0.16) | 0.583 |
| full_seq − noveto | +0.04 (mean +0.18) | 0.502 |
| full − full_seq | -0.10 (mean -0.02) | 0.715 |
| baseline − noveto | -9.55 (mean -10.76) | 0.000122 |

JSON parse failures (failed/total calls): j2 20/280, j4 0/210, j3 20/280, jag 0/280

Veto provenance (full, all runs): score rule: 60

| τ | Accuracy % | FP per run | FN per run |
|---|---|---|---|
| 0.50 | 83 | 0.0 | 2.4 |
| 0.55 | 90 | 0.0 | 1.4 |
| 0.60 | 90 | 0.0 | 1.4 |
| 0.65 | 90 | 0.0 | 1.4 |
| 0.70 | 90 | 0.0 | 1.4 |
| 0.75 | 93 | 1.0 | 0.0 |
| 0.80 | 93 | 1.0 | 0.0 |
| 0.85 | 86 | 2.0 | 0.0 |
| 0.90 | 86 | 2.0 | 0.0 |
| 0.95 | 86 | 2.0 | 0.0 |
| 1.00 | 86 | 2.0 | 0.0 |

## mistral_7b_T0  (mistral:7b, T=0.0, 3 repeats)

| Condition | Accuracy per run (mean ± SD) [min–max] | 95% CI (scenario bootstrap) | Identical veto decision across runs | Mean latency, s (mean of scenario means; SD across runs) |
|---|---|---|---|---|
| full | 85.7 ± 0.0 [86–86] | 64–100% | 100% | 19.3 (0.08) |
| noveto | 28.6 ± 0.0 [29–29] | 7–50% | 100% | 19.0 (0.05) |
| legal_only | 85.7 ± 0.0 [86–86] | 64–100% | 100% | 5.6 (0.02) |
| baseline | 28.6 ± 0.0 [29–29] | 7–50% | 100% | 9.5 (0.10) |

| Paired comparison (accuracy) | Mean diff, pp [95% CI] | b / c per run | Exact McNemar p per run |
|---|---|---|---|
| full vs noveto | +57.1 [+14.3, +92.9] | 10/2, 10/2, 10/2 | 0.0386, 0.0386, 0.0386 |
| full vs baseline | +57.1 [+14.3, +92.9] | 10/2, 10/2, 10/2 | 0.0386, 0.0386, 0.0386 |
| full vs legal_only | +0.0 [-21.4, +21.4] | 1/1, 1/1, 1/1 | 1, 1, 1 |
| legal_only vs noveto | +57.1 [+14.3, +92.9] | 10/2, 10/2, 10/2 | 0.0386, 0.0386, 0.0386 |

| Latency comparison (scenario means over runs) | Median diff, s | Wilcoxon p |
|---|---|---|
| full − noveto | +0.31 (mean +0.22) | 0.326 |
| baseline − noveto | -9.50 (mean -9.58) | 0.000122 |

JSON parse failures (failed/total calls): j2 0/126, j4 0/84, j3 0/126, jag 0/126

Veto provenance (full, all runs): score rule: 36

| τ | Accuracy % | FP per run | FN per run |
|---|---|---|---|
| 0.50 | 71 | 0.0 | 4.0 |
| 0.55 | 71 | 0.0 | 4.0 |
| 0.60 | 71 | 0.0 | 4.0 |
| 0.65 | 93 | 0.0 | 1.0 |
| 0.70 | 93 | 0.0 | 1.0 |
| 0.75 | 86 | 2.0 | 0.0 |
| 0.80 | 86 | 2.0 | 0.0 |
| 0.85 | 86 | 2.0 | 0.0 |
| 0.90 | 86 | 2.0 | 0.0 |
| 0.95 | 71 | 4.0 | 0.0 |
| 1.00 | 71 | 4.0 | 0.0 |

## qwen25_7b_T0  (qwen2.5:7b, T=0.0, 3 repeats)

| Condition | Accuracy per run (mean ± SD) [min–max] | 95% CI (scenario bootstrap) | Identical veto decision across runs | Mean latency, s (mean of scenario means; SD across runs) |
|---|---|---|---|---|
| full | 78.6 ± 0.0 [79–79] | 57–100% | 100% | 15.0 (0.35) |
| noveto | 28.6 ± 0.0 [29–29] | 7–50% | 100% | 15.2 (0.12) |
| baseline | 28.6 ± 0.0 [29–29] | 7–50% | 100% | 6.7 (0.07) |
| legal_only | 85.7 ± 0.0 [86–86] | 64–100% | 100% | 5.2 (0.02) |

| Paired comparison (accuracy) | Mean diff, pp [95% CI] | b / c per run | Exact McNemar p per run |
|---|---|---|---|
| full vs noveto | +50.0 [+14.3, +78.6] | 8/1, 8/1, 8/1 | 0.0391, 0.0391, 0.0391 |
| full vs baseline | +50.0 [+14.3, +78.6] | 8/1, 8/1, 8/1 | 0.0391, 0.0391, 0.0391 |
| full vs legal_only | -7.1 [-21.4, +0.0] | 0/1, 0/1, 0/1 | 1, 1, 1 |
| legal_only vs noveto | +57.1 [+21.4, +85.7] | 9/1, 9/1, 9/1 | 0.0215, 0.0215, 0.0215 |

| Latency comparison (scenario means over runs) | Median diff, s | Wilcoxon p |
|---|---|---|
| full − noveto | +0.07 (mean -0.15) | 0.761 |
| baseline − noveto | -8.42 (mean -8.51) | 0.000122 |

JSON parse failures (failed/total calls): j2 18/126, j4 0/84, j3 0/126, jag 0/126

Veto provenance (full, all runs): score rule: 24, LLM flag only: 3

| τ | Accuracy % | FP per run | FN per run |
|---|---|---|---|
| 0.50 | 50 | 0.0 | 7.0 |
| 0.55 | 50 | 0.0 | 7.0 |
| 0.60 | 50 | 0.0 | 7.0 |
| 0.65 | 79 | 0.0 | 3.0 |
| 0.70 | 79 | 0.0 | 3.0 |
| 0.75 | 86 | 0.0 | 2.0 |
| 0.80 | 86 | 0.0 | 2.0 |
| 0.85 | 86 | 0.0 | 2.0 |
| 0.90 | 79 | 1.0 | 2.0 |
| 0.95 | 86 | 2.0 | 0.0 |
| 1.00 | 86 | 2.0 | 0.0 |

written results/v2/analysis_summary.json
