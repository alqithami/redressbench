#!/usr/bin/env bash
set -euo pipefail

MODEL="${MODEL:-llama3.1:8b}"
export OLLAMA_TIMEOUT_SECONDS="${OLLAMA_TIMEOUT_SECONDS:-900}"
export OLLAMA_NUM_PREDICT="${OLLAMA_NUM_PREDICT:-2200}"

mkdir -p outputs analysis casefiles

PYTHONPATH=src python -m redressbench.run_experiment \
  --provider ollama \
  --model "$MODEL" \
  --conditions baseline guardrailed trace trace_escalation \
  --output outputs/ollama_llama31_8b_v03_full_runs.jsonl

PYTHONPATH=src python -m redressbench.audit_runs \
  --runs outputs/ollama_llama31_8b_v03_full_runs.jsonl \
  --out-dir analysis/ollama_llama31_8b_v03_full

PYTHONPATH=src python -m redressbench.build_blinded_casefiles \
  --runs outputs/ollama_llama31_8b_v03_full_runs.jsonl \
  --scenarios data/scenarios_v0_2.jsonl \
  --case-dir casefiles/ollama_llama31_8b_v03_blinded \
  --annotation-csv casefiles/ollama_llama31_8b_v03_annotation_template.csv \
  --mapping-csv casefiles/ollama_llama31_8b_v03_private_mapping.csv
