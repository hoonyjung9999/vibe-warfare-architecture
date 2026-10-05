#!/bin/zsh
cd "$(dirname "$0")/.." || exit 1
mkdir -p results/v2/logs
PY=python
echo "[driver] start $(date)" | tee -a results/v2/logs/driver.log

$PY experiments/run_experiments_v2.py --model llama3.1:8b --repeats 5 --temperature 0 \
    --conditions baseline noveto full full_seq legal_only --tag llama31_8b_T0 \
    >> results/v2/logs/llama31_8b_T0.log 2>&1
echo "[driver] llama T0 done $(date)" | tee -a results/v2/logs/driver.log

for m in qwen2.5:7b gemma2:9b mistral:7b; do
  ollama pull $m >> results/v2/logs/pull.log 2>&1
  echo "[driver] pulled $m $(date)" | tee -a results/v2/logs/driver.log
done

$PY experiments/run_experiments_v2.py --model llama3.1:8b --repeats 5 --temperature 0.7 \
    --conditions full legal_only --tag llama31_8b_T07 \
    >> results/v2/logs/llama31_8b_T07.log 2>&1
echo "[driver] llama T0.7 done $(date)" | tee -a results/v2/logs/driver.log

for pair in "qwen2.5:7b qwen25_7b" "gemma2:9b gemma2_9b" "mistral:7b mistral_7b"; do
  set -- ${=pair}
  $PY experiments/run_experiments_v2.py --model $1 --repeats 3 --temperature 0 \
      --conditions baseline noveto full legal_only --tag ${2}_T0 \
      >> results/v2/logs/${2}_T0.log 2>&1
  echo "[driver] $1 done $(date)" | tee -a results/v2/logs/driver.log
done
echo "[driver] ALL DONE $(date)" | tee -a results/v2/logs/driver.log
