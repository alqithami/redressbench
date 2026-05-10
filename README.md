# Agent RedressBench v0.2

This package is the experiment scaffold for the AIES 2026 draft **Who Can Undo the Agent? Redressability as a First-Class Safety Property for Tool-Using AI Agents**.

It contains a synthetic seed benchmark, prompts, redress-trace schema, scoring proxy, and local run scripts. The included scripted backend is only a pipeline sanity check. It is **not empirical evidence**.

## What is included

- `data/scenarios_v0_2.jsonl`: 40 synthetic institutional scenarios.
- `data/scenarios_v0_2.csv`: compact spreadsheet-style scenario summary.
- `schemas/scenario.schema.json`: scenario schema.
- `schemas/redress_trace.schema.json`: action-level redress-trace schema.
- `rubrics/redressability_rubric.md`: human annotation rubric.
- `prompts/`: four experimental condition prompts and reviewer prompt.
- `src/redressbench/run_experiment.py`: local experiment runner.
- `src/redressbench/scoring.py`: deterministic heuristic scorer for pilot calibration.
- `src/redressbench/build_casefiles.py`: creates markdown case files and annotation CSV.
- `src/redressbench/summarize_results.py`: creates summary tables by condition.

## Benchmark domains

| Domain | Scenarios | Examples of adverse action |
|---|---:|---|
| Workplace administration | 10 | HR warning, eligibility revocation, compliance flag |
| Public-service administration | 10 | benefit delay, case closure, fraud flag, waitlist change |
| Healthcare administration | 10 | appointment cancellation, waitlist downgrade, privacy leakage, coverage denial |
| Customer support/platform governance | 10 | refund denial, account freeze, listing removal, driver suspension |

All examples are synthetic composites and should be reviewed by domain experts before any public release.

## Experimental conditions

1. `baseline`: ordinary tool-using agent.
2. `guardrailed`: baseline plus safety policy instructions.
3. `trace`: baseline plus required redress traces for consequential actions.
4. `trace_escalation`: trace agent plus escalation, notice, and rollback requirements.

## Local setup

```bash
cd agent_redressbench_v0_2
python -m venv .venv
source .venv/bin/activate
pip install -e .
# Optional only if running the OpenAI backend:
pip install openai
```

## Run the scripted demo

The scripted demo checks that files, scoring, summaries, and case-file generation work.

```bash
./scripts/run_scripted_demo.sh
```

Expected outputs:

- `outputs/scripted_demo_runs.jsonl`
- `analysis/scripted_demo_summary.csv`
- `casefiles/scripted_demo/*.md`
- `casefiles/scripted_demo_annotation_template.csv`

Do not report scripted-demo numbers as empirical model findings.

## Run a small OpenAI pilot

Set an API key and model name, then run a small pilot. The runner uses the OpenAI Responses API through the `openai` Python package.

```bash
export OPENAI_API_KEY="..."
export MODEL="gpt-4.1"     # replace with the exact model you want to test
export LIMIT=8              # start small to inspect outputs
./scripts/run_openai_pilot.sh
```

The pilot runs all four conditions on the first `LIMIT` scenarios. Increase `LIMIT=40` for a full seed run.

## Run a local Ollama pilot

```bash
ollama pull llama3.1:8b
PYTHONPATH=src python -m redressbench.run_experiment \
  --provider ollama \
  --model llama3.1:8b \
  --limit 8 \
  --output outputs/ollama_llama31_8b_pilot_runs.jsonl
PYTHONPATH=src python -m redressbench.summarize_results \
  --runs outputs/ollama_llama31_8b_pilot_runs.jsonl \
  --out-csv analysis/ollama_llama31_8b_pilot_summary.csv
```

## Full run recommended for paper development

For each model to compare, run all 40 scenarios across all four conditions:

```bash
PYTHONPATH=src python -m redressbench.run_experiment \
  --provider openai \
  --model "$MODEL" \
  --conditions baseline guardrailed trace trace_escalation \
  --output "outputs/${MODEL}_full_runs.jsonl"
PYTHONPATH=src python -m redressbench.summarize_results \
  --runs "outputs/${MODEL}_full_runs.jsonl" \
  --out-csv "analysis/${MODEL}_summary.csv"
PYTHONPATH=src python -m redressbench.build_casefiles \
  --runs "outputs/${MODEL}_full_runs.jsonl" \
  --case-dir "casefiles/${MODEL}_full" \
  --annotation-csv "casefiles/${MODEL}_annotation_template.csv"
```

## What to send back for analysis

After a local pilot or full run, share these files:

1. The run JSONL file in `outputs/`.
2. The summary CSV in `analysis/`.
3. The generated annotation CSV in `casefiles/` after human reviewers fill it in.
4. Notes about the model version, date run, temperature, and any failed or retried calls.

## Human annotation plan

Minimum viable version:

- 3 reviewers.
- 40 scenarios x 4 conditions = 160 case files for one model.
- Each case receives at least 2 independent annotations.
- Resolve disagreements by discussion or a third reviewer.
- Report inter-rater agreement and dimension-level means.

Best-paper version:

- Add 3-5 domain experts or stakeholder reviewers.
- Compare at least two models or agent frameworks.
- Include qualitative coding of failure modes: missing notice, no appeal path, no rollback, burden shifting, privacy leakage, and unclear value-chain owner.

## Important caveat

The current scoring script is a calibration proxy. The paper should rely on human annotation and statistical analysis, not only the heuristic scores.
