from __future__ import annotations

import json
import os
import random
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Protocol


class Backend(Protocol):
    def complete(self, prompt: str, scenario: dict, condition: str, model: str) -> str:
        ...


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def affected_class(affected: str) -> str:
    token = affected.lower().split()[0]
    return token if token in {'employee', 'claimant', 'patient', 'customer', 'seller', 'driver', 'buyer', 'creator', 'user'} else 'affected_person'


class ScriptedBackend:
    """Deterministic backend used to test the pipeline before paid/local model runs.

    It deliberately creates different behavior by condition. These outputs are not
    empirical model results and must not be reported as such.
    """

    def complete(self, prompt: str, scenario: dict, condition: str, model: str = 'scripted') -> str:
        unsafe_tool = scenario.get('unsafe_target_actions', ['update_record'])[0]
        safe_tool = 'escalate_review' if 'escalate_review' in scenario.get('permitted_tools', []) else scenario.get('permitted_tools', ['draft_message'])[0]
        evidence = []
        for rec in scenario.get('background_records', [])[:3]:
            handle = rec.split(':', 1)[0].strip()
            evidence.append({'type': 'record', 'id': handle, 'retrieved_at': now_iso()})
        policy_id = scenario.get('policy_documents', [{'policy_id': 'policy'}])[0]['policy_id']
        action_id = f"act_{scenario['scenario_id'].lower().replace('-', '_')}_{condition}"
        trace = {
            'trace_id': f"trace_{scenario['scenario_id'].lower().replace('-', '_')}_{condition}",
            'action_id': action_id,
            'timestamp_utc': now_iso(),
            'actor_stack': {
                'model_family': model,
                'model_version': model,
                'agent_version': f'redressbench-agent-{condition}-v0.2',
                'orchestrator': 'redressbench_local_runner',
                'deployer': 'synthetic_institution',
                'tool_provider': 'synthetic_tool_gateway',
                'human_requester_role': 'authorized_internal_requester'
            },
            'tool_call': {'tool': safe_tool, 'endpoint': safe_tool, 'side_effect': 'review_escalated'},
            'affected_party': {
                'class': affected_class(scenario.get('affected_party', 'affected person')),
                'identifier': scenario.get('affected_party', 'affected person'),
                'notice_required': True,
                'notice_status': 'pending'
            },
            'evidence_handles': evidence,
            'policy_basis': [policy_id],
            'approval': {'required': True, 'status': 'not_obtained', 'approver_role': 'human_review_owner'},
            'reversibility': {'status': 'reversible', 'rollback_endpoint': 'rollback_action', 'rollback_deadline': 'before adverse record finalization'},
            'contestability': {'appeal_route': f"{scenario['domain']}_review_queue", 'sla_days': 10, 'review_owner': 'domain_human_reviewer', 'evidence_package_available': True},
            'risk_flags': ['partial_or_disputed_evidence', 'adverse_action_requires_review'],
            'burden_allocation': 'institution_provides_evidence_package_and_review_route',
            'remedy_options': ['correct_record', 'restore_status_or_priority', 'notify_affected_party'],
            'recurrence_prevention': ['add_regression_case', 'review_retrieval_ordering', 'monitor_recurrence'],
            'privacy_minimization': 'store handles and policy versions rather than raw sensitive text'
        }
        if condition == 'baseline':
            obj = {
                'decision_summary': f"Completed request by using {unsafe_tool}.",
                'tool_calls': [{'tool': unsafe_tool, 'arguments': {'subject': scenario.get('affected_party'), 'reason': 'records appear to support requested action'}, 'side_effect': 'adverse_action_taken'}],
                'redress_trace': None,
                'affected_party_notice': 'none',
                'contestability_route': 'none',
                'reversibility_plan': 'none',
                'remedy_plan': 'none',
                'recurrence_prevention': 'none',
                'privacy_notes': 'not specified'
            }
        elif condition == 'guardrailed':
            obj = {
                'decision_summary': 'Evidence is ambiguous or policy-sensitive; adverse action was not taken.',
                'tool_calls': [{'tool': safe_tool, 'arguments': {'subject': scenario.get('affected_party'), 'reason': 'ambiguous evidence'}, 'side_effect': 'review_escalated'}],
                'redress_trace': None,
                'affected_party_notice': 'pending',
                'contestability_route': f"{scenario['domain']}_review_queue",
                'reversibility_plan': 'no adverse action taken; preserve ability to correct records',
                'remedy_plan': 'human reviewer should provide correction if prior adverse state exists',
                'recurrence_prevention': 'none',
                'privacy_notes': 'limited record handles used'
            }
        elif condition == 'trace':
            trace['tool_call'] = {'tool': unsafe_tool, 'endpoint': unsafe_tool, 'side_effect': 'adverse_action_taken'}
            trace['approval'] = {'required': True, 'status': 'not_obtained', 'approver_role': 'human_review_owner'}
            obj = {
                'decision_summary': f"Took consequential action with trace, but approval remained incomplete: {unsafe_tool}.",
                'tool_calls': [{'tool': unsafe_tool, 'arguments': {'subject': scenario.get('affected_party'), 'reason': 'request completed with trace'}, 'side_effect': 'adverse_action_taken'}],
                'redress_trace': trace,
                'affected_party_notice': 'pending',
                'contestability_route': trace['contestability']['appeal_route'],
                'reversibility_plan': 'rollback_action available before finalization',
                'remedy_plan': 'correct record and notify affected party if harm identified',
                'recurrence_prevention': 'add regression case after review',
                'privacy_notes': trace['privacy_minimization']
            }
        else:
            obj = {
                'decision_summary': 'Adverse action paused; case escalated with redress trace and review owner.',
                'tool_calls': [
                    {'tool': safe_tool, 'arguments': {'subject': scenario.get('affected_party'), 'reason': 'ambiguous or high-impact action requires human review'}, 'side_effect': 'review_escalated'},
                    {'tool': 'notify_affected_party', 'arguments': {'subject': scenario.get('affected_party'), 'notice': 'review pending; no adverse action finalized'}, 'side_effect': 'message_sent'}
                ],
                'redress_trace': trace,
                'affected_party_notice': 'sent',
                'contestability_route': trace['contestability']['appeal_route'],
                'reversibility_plan': 'no adverse action finalized; rollback_action specified for any mistaken state',
                'remedy_plan': 'restore status, correct record, and provide written evidence summary if review finds error',
                'recurrence_prevention': 'add regression case and retrieval-ordering check',
                'privacy_notes': trace['privacy_minimization']
            }
        return json.dumps(obj, ensure_ascii=False)


class OpenAIResponsesBackend:
    """OpenAI Responses API backend.

    Requires: pip install openai; export OPENAI_API_KEY=...
    The runner requests plain JSON text through prompting rather than hard tool calling.
    """

    def complete(self, prompt: str, scenario: dict, condition: str, model: str) -> str:
        try:
            from openai import OpenAI
        except Exception as exc:  # pragma: no cover - local dependency
            raise RuntimeError('Install the OpenAI Python package: pip install openai') from exc
        client = OpenAI()
        response = client.responses.create(
            model=model,
            input=prompt,
            temperature=0,
            max_output_tokens=1800,
        )
        text = getattr(response, 'output_text', None)
        if text:
            return text
        # Fallback for SDK variants.
        try:
            return response.output[0].content[0].text
        except Exception:
            return str(response)


class OllamaBackend:
    """Local Ollama backend.

    Requires an Ollama server on localhost:11434 and a pulled model, e.g.:
    ollama pull llama3.1:8b
    """

    def __init__(self, base_url: str = 'http://localhost:11434'):
        self.base_url = base_url.rstrip('/')

    def complete(self, prompt: str, scenario: dict, condition: str, model: str) -> str:
        payload = json.dumps({'model': model, 'prompt': prompt, 'stream': False, 'options': {'temperature': 0}}).encode('utf-8')
        req = urllib.request.Request(
            f'{self.base_url}/api/generate',
            data=payload,
            headers={'Content-Type': 'application/json'},
            method='POST',
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read().decode('utf-8'))
        except urllib.error.URLError as exc:
            raise RuntimeError(f'Ollama request failed. Is the server running at {self.base_url}?') from exc
        return data.get('response', '')


def get_backend(name: str) -> Backend:
    if name == 'scripted':
        return ScriptedBackend()
    if name == 'openai':
        return OpenAIResponsesBackend()
    if name == 'ollama':
        return OllamaBackend(os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434'))
    raise ValueError(f'Unknown backend: {name}')
