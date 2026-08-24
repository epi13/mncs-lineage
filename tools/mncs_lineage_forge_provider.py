#!/usr/bin/env python3
"""Bounded MNCS Lineage Provider Protocol 0.1 adapter for Forge.

Analyses (each is a deterministic re-run of a lineage verification the
repository also exposes through pytest):

- ``mncs-lineage-source-validation``      validate every succession module;
- ``mncs-lineage-succession-experiment``  rebuild frozen artifacts and require
                                          PASS on both reference backends;
- ``mncs-lineage-evidence-invalidation``  confirm stale evidence cannot be
                                          reused after a policy change;
- ``mncs-lineage-determinism``            reproduce freeze records exactly.

This provider is development evidence only. It runs ordinary local processes,
is not a sandbox, and holds no promotion authority.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

PROVIDER = {
    "id": "mncs-lineage-provider",
    "name": "mncs-lineage-provider",
    "identity": "mncs-lineage-provider-v1",
    "version": "0.1",
}
METHODS = [
    "mncs-lineage-source-validation",
    "mncs-lineage-succession-experiment",
    "mncs-lineage-evidence-invalidation",
    "mncs-lineage-determinism",
    # Workflow-category aliases declared in mncs-forge.toml; Forge routes
    # workflows and verifier methods through these.
    "inspection",
    "evidence_derivation",
    "differential_behavior",
    "checkpoint_recovery",
]
OUTPUT_LIMIT = 65_536
TIMEOUT_SECONDS = 900


def response(
    request: dict[str, Any],
    status: str,
    summary: str,
    *,
    witnesses: list[object] | None = None,
    limitations: list[str] | None = None,
    unsupported: list[str] | None = None,
) -> dict[str, object]:
    return {
        "protocol_version": "0.1",
        "type": "analysis_response",
        "request_id": request.get("request_id", "unknown"),
        "provider": PROVIDER,
        "status": status,
        "summary": summary,
        "witnesses": witnesses or [],
        "limitations": limitations or [],
        "extensions": {
            "unsupported_constructs": unsupported or [],
            "unsupported": unsupported or [],
            "mncs_forge": {
                "assumptions": [
                    "lineage fixtures and corpora in this checkout are the declared bounded subset"
                ],
                "dependency_envelope": {
                    "paths": [
                        "language/lineage-core.mncs",
                        "language/synthetic-lineage-g0.mncs",
                        "examples/execution/synthetic-lineage-g0-corpus.json",
                    ],
                    "identities": {},
                    "complete": False,
                },
            },
        },
    }


def run_script(name: str) -> tuple[bool, str]:
    try:
        completed = subprocess.run(
            [sys.executable, str(REPO_ROOT / "tools" / name)],
            cwd=REPO_ROOT,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return False, str(error)
    return completed.returncode == 0, completed.stdout[-OUTPUT_LIMIT:]


def source_validation(request: dict[str, Any]) -> dict[str, object]:
    ok, output = run_script("build_lineage_artifacts.py")
    witnesses = [{"script": "build_lineage_artifacts.py", "passed": ok, "output_tail": output[-2000:]}]
    if not ok:
        return response(request, "FAIL", "a lineage succession module failed validation", witnesses=witnesses)
    return response(request, "PASS", "all succession modules validate", witnesses=witnesses)


def succession_experiment(request: dict[str, Any]) -> dict[str, object]:
    ok, output = run_script("build_lineage_artifacts.py")
    witnesses = [{"script": "build_lineage_artifacts.py", "passed": ok, "output_tail": output[-4000:]}]
    if not ok:
        return response(request, "FAIL", "synthetic succession experiment did not reach PASS", witnesses=witnesses)
    record_path = REPO_ROOT / "artifacts/lineage/synthetic-lineage-g0/candidate-freeze-record.json"
    record = json.loads(record_path.read_text())
    statuses = {e["backend"]: e["status"] for e in record["experiments"]}
    if set(statuses.values()) != {"PASS"}:
        return response(request, "FAIL", f"experiment statuses were not all PASS: {statuses}", witnesses=witnesses)
    return response(
        request,
        "PASS",
        "frozen candidate reached PASS on both reference backends",
        witnesses=[*witnesses, {"backends": list(statuses), "record": str(record_path.relative_to(REPO_ROOT))}],
    )


def evidence_invalidation(request: dict[str, Any]) -> dict[str, object]:
    # The probe intentionally derives an unpromotable successor artifact; its
    # own exit code reports detection success, so process failure is meaningful.
    ok, output = run_script("invalidate_evidence_probe.py")
    witnesses = [{"script": "invalidate_evidence_probe.py", "passed": ok, "output_tail": output[-2000:]}]
    summary_path = REPO_ROOT / "artifacts/lineage/invalidation-probe/probe-summary.json"
    if not summary_path.exists():
        return response(request, "UNKNOWN", "invalidation probe produced no summary", witnesses=witnesses)
    summary = json.loads(summary_path.read_text())
    if not ok or summary["invalidated_records"] == 0:
        return response(request, "FAIL", "stale evidence was not detected", witnesses=witnesses)
    return response(request, "PASS", "stale evidence detected; re-evaluation required", witnesses=witnesses)


def determinism(request: dict[str, Any]) -> dict[str, object]:
    try:
        completed = subprocess.run(
            [sys.executable, str(REPO_ROOT / "tools" / "build_lineage_artifacts.py"), "--check"],
            cwd=REPO_ROOT,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return response(request, "UNKNOWN", f"determinism probe could not run: {error}")
    output = completed.stdout[-OUTPUT_LIMIT:]
    witnesses = [{"exit_code": completed.returncode, "output_tail": output[-2000:]}]
    if "determinism probe: records reproduce exactly" in output:
        return response(request, "PASS", "freeze records reproduce byte-for-byte", witnesses=witnesses)
    return response(request, "FAIL", "determinism probe failed", witnesses=witnesses)


HANDLERS = {
    "mncs-lineage-source-validation": source_validation,
    "inspection": source_validation,
    "mncs-lineage-succession-experiment": succession_experiment,
    "evidence_derivation": succession_experiment,
    "mncs-lineage-evidence-invalidation": evidence_invalidation,
    "differential_behavior": evidence_invalidation,
    "mncs-lineage-determinism": determinism,
    "checkpoint_recovery": determinism,
}


def dispatch(request: dict[str, Any]) -> dict[str, object]:
    if request.get("type") == "capabilities":
        return {
            "protocol_version": "0.1",
            "type": "capabilities",
            "request_id": request.get("request_id", "unknown"),
            "provider": PROVIDER,
            "analyses": METHODS,
            "statuses": ["PASS", "FAIL", "UNKNOWN"],
            "cancellation": False,
            "health_checks": False,
            "extensions": {
                "supported_constructs": [
                    "lineage-succession-modules",
                    "deterministic-corpora",
                    "candidate-freeze-records",
                    "evidence-invalidation-probe",
                    "generation-graph-reconstruction",
                ],
                "unsupported_constructs": [
                    "neural-training",
                    "sandboxed-execution",
                    "promotion-authority",
                ],
                "limitations": ["normal local process; not a sandbox; development evidence only"],
            },
        }
    handler = HANDLERS.get(request.get("analysis"))
    if handler is None:
        return response(request, "UNKNOWN", "requested provider method is unsupported", unsupported=["unsupported-method"])
    return handler(request)


def main() -> int:
    try:
        request = json.loads(sys.stdin.readline())
        result = dispatch(request)
    except (json.JSONDecodeError, TypeError) as error:
        result = response({"request_id": "malformed"}, "UNKNOWN", "provider request was malformed", limitations=[str(error)], unsupported=["malformed-request"])
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
