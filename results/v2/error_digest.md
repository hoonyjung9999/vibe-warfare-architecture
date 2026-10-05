## gemma2_9b_T0 3 repeats
 baseline: all-no-veto; FN on ['S1', 'S10', 'S12', 'S14', 'S2', 'S4', 'S5', 'S6', 'S8', 'S9']
 legal_only: FP {'S11': 3, 'S13': 3} FN {}  (counts over 3 repeats)
 noveto: all-no-veto; FN on ['S1', 'S10', 'S12', 'S14', 'S2', 'S4', 'S5', 'S6', 'S8', 'S9']
 full: FP {'S11': 3, 'S13': 3} FN {}  (counts over 3 repeats)
## llama31_8b_T07 5 repeats
 legal_only: FP {'S11': 5, 'S13': 1} FN {}  (counts over 5 repeats)
 full: FP {'S11': 5, 'S13': 5} FN {}  (counts over 5 repeats)
## llama31_8b_T0_neutralJAG 3 repeats
 full: FP {'S11': 3, 'S13': 3} FN {'S8': 3}  (counts over 3 repeats)
 legal_only: FP {} FN {}  (counts over 3 repeats)
## llama31_8b_T0 5 repeats
 full: FP {'S11': 5, 'S13': 5} FN {}  (counts over 5 repeats)
 legal_only: FP {'S11': 5} FN {}  (counts over 5 repeats)
 full_seq: FP {'S11': 5, 'S13': 5} FN {}  (counts over 5 repeats)
 noveto: all-no-veto; FN on ['S1', 'S10', 'S12', 'S14', 'S2', 'S4', 'S5', 'S6', 'S8', 'S9']
 baseline: all-no-veto; FN on ['S1', 'S10', 'S12', 'S14', 'S2', 'S4', 'S5', 'S6', 'S8', 'S9']
## mistral_7b_T0 3 repeats
 full: FP {'S11': 3, 'S13': 3} FN {}  (counts over 3 repeats)
 noveto: all-no-veto; FN on ['S1', 'S10', 'S12', 'S14', 'S2', 'S4', 'S5', 'S6', 'S8', 'S9']
 legal_only: FP {'S7': 3, 'S11': 3} FN {}  (counts over 3 repeats)
 baseline: all-no-veto; FN on ['S1', 'S10', 'S12', 'S14', 'S2', 'S4', 'S5', 'S6', 'S8', 'S9']
## qwen25_7b_T0 3 repeats
 full: FP {'S13': 3} FN {'S10': 3, 'S14': 3}  (counts over 3 repeats)
 noveto: all-no-veto; FN on ['S1', 'S10', 'S12', 'S14', 'S2', 'S4', 'S5', 'S6', 'S8', 'S9']
 baseline: all-no-veto; FN on ['S1', 'S10', 'S12', 'S14', 'S2', 'S4', 'S5', 'S6', 'S8', 'S9']
 legal_only: FP {'S13': 3} FN {'S10': 3}  (counts over 3 repeats)
