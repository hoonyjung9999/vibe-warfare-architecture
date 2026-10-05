#!/bin/zsh
cd "$(dirname "$0")/.." || exit 1
L=results/v2/logs
echo "[driver2] start $(date)" >> $L/driver2.log
python experiments/run_experiments_v2.py --model mistral:7b --repeats 3 --temperature 0 --conditions baseline noveto full legal_only --tag mistral_7b_T0 > $L/mistral_7b_T0.log 2>&1
echo "[driver2] mistral done $(date)" >> $L/driver2.log
VWA_PROMPTS_FILE=prompts/agent_prompts_neutral.yaml python experiments/run_experiments_v2.py --model llama3.1:8b --repeats 3 --temperature 0 --conditions full legal_only --tag llama31_8b_T0_neutralJAG > $L/llama31_8b_T0_neutralJAG.log 2>&1
echo "[driver2] neutral done $(date)" >> $L/driver2.log
echo "[driver2] ALL DONE $(date)" >> $L/driver2.log
