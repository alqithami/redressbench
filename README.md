# Agent RedressBench v0.3

This package is a revised experiment scaffold for the AIES 2026 redressability paper.

## What changed from v0.2

- Condition-specific output contracts:
  - `baseline` no longer receives redress fields.
  - `guardrailed` receives safety-basis fields but no redress trace.
  - `trace` and `trace_escalation` receive the full redress-trace contract.
- Redress prompts now require exact schema keys rather than free-form trace aliases.
- The diagnostic scorer normalizes common aliases but should still be treated as a debugging proxy, not a publication-grade labeler.
- The diagnostic scorer distinguishes an over-inclusive `unsafe_action_proxy` from an actual adverse-side-effect flag.
- Added `audit_runs.py` for run diagnostics.
- Added `build_blinded_casefiles.py` for randomized, condition-blinded human annotation.
- Ollama backend now requests JSON output, uses a larger default timeout, and permits `OLLAMA_TIMEOUT_SECONDS` and `OLLAMA_NUM_PREDICT` overrides.

## Recommended run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -r requirements.txt

export OPENAI_API_KEY="..."
export MODEL="gpt-4.1"

PYTHONPATH=src python -m redressbench.run_experiment \
  --provider openai \
  --model "$MODEL" \
  --conditions baseline guardrailed trace trace_escalation \
  --output "outputs/${MODEL}_v03_full_runs.jsonl"

PYTHONPATH=src python -m redressbench.audit_runs \
  --runs "outputs/${MODEL}_v03_full_runs.jsonl" \
  --out-dir "analysis/${MODEL}_v03"

PYTHONPATH=src python -m redressbench.build_blinded_casefiles \
  --runs "outputs/${MODEL}_v03_full_runs.jsonl" \
  --case-dir "casefiles/${MODEL}_v03_blinded" \
  --annotation-csv "casefiles/${MODEL}_v03_blinded_annotations.csv" \
  --mapping-csv "casefiles/${MODEL}_v03_blinded_mapping_private.csv"
```

## Ollama pilot

```bash
ollama pull llama3.1:8b
export OLLAMA_TIMEOUT_SECONDS=900
export OLLAMA_NUM_PREDICT=2200

PYTHONPATH=src python -m redressbench.run_experiment \
  --provider ollama \
  --model llama3.1:8b \
  --limit 8 \
  --conditions baseline guardrailed trace trace_escalation \
  --output outputs/ollama_llama31_8b_v03_pilot_runs.jsonl
```

If the 8B model still times out or produces invalid JSON, do not use it as a main result. Use it as a robustness failure note, or switch to a stronger local model.

## Human annotation

Use the blinded annotation template rather than the unblinded case files. Keep the private mapping file separate from annotators. Minimum viable annotation:

- 160 GPT-4.1 case files, condition-blinded.
- At least two independent annotators per case.
- Third adjudicator for safety disagreements or redress dimension disagreements above one ordinal point.
- Report inter-annotator agreement before resolving disagreements.

The deterministic score is a triage proxy only. Paper claims should use human annotations.
