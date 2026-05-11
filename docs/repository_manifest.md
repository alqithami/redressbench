# Repository Manifest

## Core benchmark files

- `data/scenarios_v0_2.jsonl`: 40 seed scenarios.
- `data/scenarios_v0_4_stress.jsonl`: 24 stress scenarios.
- `data/scenarios_v0_4_combined.jsonl`: 64 combined scenarios.
- `schemas/scenario.schema.json`: scenario schema.
- `schemas/redress_trace.schema.json`: redress trace schema.

## Prompt and contract files

- `prompts/baseline.txt`
- `prompts/guardrailed.txt`
- `prompts/trace.txt`
- `prompts/trace_escalation.txt`
- `prompts/contracts/baseline_contract.json`
- `prompts/contracts/guardrailed_contract.json`
- `prompts/contracts/redress_contract.json`

## Code

- `src/redressbench/run_experiment.py`: run scenarios under model/condition combinations.
- `src/redressbench/backends.py`: scripted, OpenAI, and Ollama backends.
- `src/redressbench/prompts.py`: prompt assembly.
- `src/redressbench/scoring.py`: diagnostic scoring.
- `src/redressbench/audit_runs.py`: aggregate diagnostics.
- `src/redressbench/build_blinded_casefiles.py`: blinded case-file generation.
- `src/redressbench/validate_annotations.py`: annotation CSV validation.
- `src/redressbench/annotation_agreement.py`: agreement and disagreement reports.

## Human annotation

- `rubrics/redressability_rubric.md`: scoring rubric.
- `docs/annotator_quickstart.md`: short annotator instructions.
- `docs/annotation_protocol.md`: detailed protocol.
- `docs/irb_ethics_note.md`: ethics/IRB guidance.

## Generated files

Generated files are normally gitignored:

- `outputs/*.jsonl`
- `analysis/**`
- `casefiles/**`
- `results/raw/**`
- `results/final_annotations/**`

The final artifact may selectively include generated files needed to reproduce the paper tables.
