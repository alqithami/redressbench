
# Agent RedressBench v0.4 Stress Extension

This extension adds a 24-scenario stress split designed to address the GPT-4.1 ceiling effect observed in the v0.3 seed run.

New data files:
- `data/scenarios_v0_4_stress.jsonl`: 24 stress scenarios, 6 per domain.
- `data/scenarios_v0_4_combined.jsonl`: original 40 seed scenarios plus the 24 stress scenarios.

Why this split exists:
- The v0.3 GPT-4.1 run had 0 adverse-side-effect harms in all conditions.
- The stress split adds stronger institutional pressure and valid consequential-action cases.
- Valid consequential-action cases test whether agents can take justified but high-impact actions while preserving notice, appeal, rollback, and remedy.

Scoring update:
- v0.4 adds `expected_consequential_tools` to distinguish wrongful adverse actions from valid consequential actions.
- `unsafe_action` should not be interpreted without human review; the automatic scorer remains diagnostic.

Run stress split with GPT-4.1:

```bash
PYTHONPATH=src python -m redressbench.run_experiment   --scenarios data/scenarios_v0_4_stress.jsonl   --provider openai   --model "$MODEL"   --conditions baseline guardrailed trace trace_escalation   --output outputs/${MODEL}_v04_stress_runs.jsonl

PYTHONPATH=src python -m redressbench.audit_runs   --runs outputs/${MODEL}_v04_stress_runs.jsonl   --out-dir analysis/${MODEL}_v04_stress
```

Run combined 64-scenario set:

```bash
PYTHONPATH=src python -m redressbench.run_experiment   --scenarios data/scenarios_v0_4_combined.jsonl   --provider openai   --model "$MODEL"   --conditions baseline guardrailed trace trace_escalation   --output outputs/${MODEL}_v04_combined_runs.jsonl
```

Recommended use:
1. First finish human annotation on the v0.3 GPT-4.1 run.
2. Run the full Ollama v0.3 seed set.
3. Then run this v0.4 stress split for GPT-4.1 and one weaker or mid-tier model.
