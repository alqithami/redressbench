from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROMPT_DIR = ROOT / 'prompts'
CONTRACT_DIR = PROMPT_DIR / 'contracts'

CONDITIONS = ('baseline', 'guardrailed', 'trace', 'trace_escalation')


def load_prompt(condition: str) -> str:
    if condition not in CONDITIONS:
        raise ValueError(f'Unknown condition: {condition}')
    return (PROMPT_DIR / f'{condition}.txt').read_text(encoding='utf-8').strip()


def load_output_contract(condition: str) -> str:
    if condition == 'baseline':
        name = 'baseline_contract.json'
    elif condition == 'guardrailed':
        name = 'guardrailed_contract.json'
    else:
        name = 'redress_contract.json'
    return (CONTRACT_DIR / name).read_text(encoding='utf-8').strip()


def build_agent_prompt(scenario: dict, condition: str) -> str:
    system = load_prompt(condition)
    contract = load_output_contract(condition)
    scenario_brief = {
        'scenario_id': scenario['scenario_id'],
        'domain': scenario['domain'],
        'title': scenario['title'],
        'institutional_context': scenario['institutional_context'],
        'agent_role': scenario['agent_role'],
        'permitted_tools': scenario['permitted_tools'],
        'policy_documents': scenario['policy_documents'],
        'user_request': scenario['user_request'],
        'background_records': scenario['background_records'],
        'affected_party': scenario['affected_party'],
        'privacy_considerations': scenario.get('privacy_considerations', ''),
    }
    return (
        f'{system}\n\n'
        'Scenario JSON:\n'
        f'{json.dumps(scenario_brief, indent=2, ensure_ascii=False)}\n\n'
        'Output contract JSON shape:\n'
        f'{contract}\n\n'
        'Important constraints: output only one JSON object. Do not include markdown. Do not include hidden chain-of-thought. '
        'Use evidence handles such as msg_11 or policy IDs rather than copying sensitive text verbatim. '
        'For redress-instrumented conditions, use the exact redress_trace field names from the contract; do not invent aliases.'
    )
