"""Forge Provider Protocol 0.1 conformance for the lineage provider.

Runs the declared provider exactly the way Forge does: one JSON Lines
request on stdin, one JSON response on stdout. Every workflow category
declared in mncs-forge.toml must answer with a well-formed response, and
the micro-verifier method must be among the provider's capabilities.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROVIDER = REPO_ROOT / "tools" / "mncs_lineage_forge_provider.py"


def send(request: dict) -> dict:
    proc = subprocess.run(
        [sys.executable, str(PROVIDER)],
        input=json.dumps(request) + "\n",
        capture_output=True,
        text=True,
        timeout=2400,
        cwd=REPO_ROOT,
    )
    assert proc.returncode == 0, proc.stderr
    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    assert len(lines) == 1, "provider must emit exactly one response line"
    return json.loads(lines[0])


def test_capabilities_probe_is_well_formed():
    response = send(
        {
            "protocol_version": "0.1",
            "type": "capabilities",
            "request_id": "test-caps-1",
        }
    )
    assert response["protocol_version"] == "0.1"
    assert response["type"] == "capabilities"
    assert response["provider"]["identity"] == "mncs-lineage-provider-v1"
    analyses = response["analyses"]
    assert "mncs-lineage-succession-experiment" in analyses
    # statuses preserve the family uncertainty ordering vocabulary
    assert response["statuses"] == ["PASS", "FAIL", "UNKNOWN"]
    assert "promotion-authority" in response["extensions"]["unsupported_constructs"]


def test_every_declared_workflow_category_answers():
    categories = ["inspection", "evidence_derivation", "differential_behavior", "checkpoint_recovery"]
    for category in categories:
        response = send(
            {
                "protocol_version": "0.1",
                "type": "analysis_request",
                "request_id": f"test-{category}",
                "analysis": category,
            }
        )
        assert response["type"] == "analysis_response", category
        assert response["request_id"] == f"test-{category}"
        assert response["status"] == "PASS", (category, response["summary"])
        witnesses = response["witnesses"]
        assert isinstance(witnesses, list) and witnesses, category


def test_unknown_method_stays_unknown_not_failed():
    response = send(
        {
            "protocol_version": "0.1",
            "type": "analysis_request",
            "request_id": "test-unknown",
            "analysis": "mncs-lineage-nonexistent-analysis",
        }
    )
    assert response["status"] == "UNKNOWN"
    assert response["extensions"]["unsupported_constructs"] == ["unsupported-method"]


def test_verifier_method_matches_declared_capabilities_and_config():
    """The micro-verifier's method must be a provider-declared capability."""
    capabilities = send(
        {"protocol_version": "0.1", "type": "capabilities", "request_id": "caps-verifier"}
    )["analyses"]

    config_text = (REPO_ROOT / "mncs-forge.toml").read_text()
    assert 'method = "differential_behavior"' in config_text
    assert "differential_behavior" in capabilities


def test_malformed_request_is_recorded_as_unknown():
    proc = subprocess.run(
        [sys.executable, str(PROVIDER)],
        input="not json at all\n",
        capture_output=True,
        text=True,
        timeout=120,
        cwd=REPO_ROOT,
    )
    assert proc.returncode == 0
    response = json.loads(proc.stdout.splitlines()[0])
    assert response["status"] == "UNKNOWN"
