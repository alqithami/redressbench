# Reproducibility Guide

This guide describes how to reproduce the diagnostic results and prepare annotation artifacts.

## Environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -r requirements.txt
```

Optional dependencies:

```bash
pip install openai      # for OpenAI Responses API backend
```

For Ollama, install and run Ollama separately and pull the local model.

## Smoke test

```bash
bash scripts/run_smoke_test.sh
```

This verifies JSON generation, parsing, diagnostic scoring, summaries, and blinded case-file generation.

## GPT-4.1 stress run

```bash
export OPENAI_API_KEY="..."
export MODEL="gpt-4.1"

PYTHONPATH=src python -m redressbench.run_experiment \
  --scenarios data/scenarios_v0_4_stress.jsonl \
  --provider openai \
  --model "$MODEL" \
  --conditions baseline guardrailed trace trace_escalation \
  --output outputs/gpt-4.1_v04_stress_runs.jsonl

PYTHONPATH=src python -m redressbench.audit_runs \
  --runs outputs/gpt-4.1_v04_stress_runs.jsonl \
  --out-dir analysis/gpt-4.1_v04_stress
```

## Llama 3.1 8B seed run

```bash
ollama pull llama3.1:8b
export OLLAMA_TIMEOUT_SECONDS=900
export OLLAMA_NUM_PREDICT=2200

PYTHONPATH=src python -m redressbench.run_experiment \
  --provider ollama \
  --model llama3.1:8b \
  --conditions baseline guardrailed trace trace_escalation \
  --output outputs/ollama_llama31_8b_v03_full_runs.jsonl

PYTHONPATH=src python -m redressbench.audit_runs \
  --runs outputs/ollama_llama31_8b_v03_full_runs.jsonl \
  --out-dir analysis/ollama_llama31_8b_v03_full
```

## Blinded case files

```bash
PYTHONPATH=src python -m redressbench.build_blinded_casefiles \
  --runs outputs/gpt-4.1_v04_stress_runs.jsonl \
  --scenarios data/scenarios_v0_4_stress.jsonl \
  --case-dir casefiles/gpt41_v04_stress_blinded \
  --annotation-csv casefiles/gpt41_v04_stress_annotation_template.csv \
  --mapping-csv casefiles/gpt41_v04_stress_private_mapping.csv
```

## Annotation validation

```bash
PYTHONPATH=src python -m redressbench.validate_annotations \
  --annotations annotation_A1.csv \
  --case-dir casefiles/gpt41_v04_stress_blinded
```

## Agreement report

```bash
PYTHONPATH=src python -m redressbench.annotation_agreement \
  --a1 annotation_A1.csv \
  --a2 annotation_A2.csv \
  --out-dir analysis/annotation_agreement_gpt41_stress
```

## What to archive for the final paper

- raw run JSONL files;
- diagnostic summaries;
- blinded annotation templates;
- final annotation CSVs;
- adjudication notes;
- private mapping, if reviewers are allowed to inspect it;
- exact commit hash;
- model names, provider versions if available, run dates, and environment notes.
