from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_scripted_two_scenario_run(tmp_path: Path):
    output = tmp_path / 'runs.jsonl'
    cmd = [
        sys.executable,
        '-m',
        'redressbench.run_experiment',
        '--provider',
        'scripted',
        '--model',
        'scripted',
        '--limit',
        '2',
        '--output',
        str(output),
    ]
    subprocess.run(cmd, cwd=ROOT, check=True, env={**os.environ, 'PYTHONPATH': 'src'})
    rows = [json.loads(line) for line in output.read_text(encoding='utf-8').splitlines() if line.strip()]
    assert len(rows) == 8
    assert all(row['score']['parse_ok'] for row in rows)


def test_audit_help():
    cmd = [sys.executable, '-m', 'redressbench.audit_runs', '--help']
    completed = subprocess.run(cmd, cwd=ROOT, env={**os.environ, 'PYTHONPATH': 'src'}, capture_output=True, text=True)
    assert completed.returncode == 0
    assert 'Audit' in completed.stdout or 'audit' in completed.stdout
