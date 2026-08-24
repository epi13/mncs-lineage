#!/usr/bin/env python3
"""Evidence-invalidation probe for the synthetic lineage.

Demonstrates, end to end, that Lineage evidence is identity-bound:

1. take the frozen synthetic-lineage-g0 candidate manifest;
2. export its dependency-bound evidence manifest;
3. derive a successor source whose succession policy changed (a rollback
   gate now holds instead of rejecting);
4. show that every evidence record bound to the changed decision functions
   is invalidated — the old evidence cannot silently certify the successor;
5. show that the successor evaluated against the parent's corpus no longer
   satisfies the old expectations, so re-evaluation is required.

Exit code 0 means invalidation was detected correctly.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

from build_lineage_artifacts import (  # noqa: E402
    Mncs,
    REPO_ROOT as ROOT,
    bind_contract_evidence,
    compile_source,
    language_root,
    relative_to_language_root,
)

BASELINE_MANIFEST = (
    ROOT / "artifacts" / "lineage" / "synthetic-lineage-g0" / "synthetic-lineage-g0.manifest.json"
)
VARIANT_SOURCE = ROOT / "language" / "variants" / "g0-rollback-holds-on-missing-artifact.mncs"
CORPUS = ROOT / "examples" / "execution" / "synthetic-lineage-g0-corpus.json"


def build_variant_manifest(cli: Mncs, out_dir: Path) -> Path:
    canonical = compile_source(cli, VARIANT_SOURCE, out_dir / "compiled")
    program = canonical["json"]
    if isinstance(program, str):
        program = json.loads(program)
    program, _ = bind_contract_evidence(program)
    path = out_dir / "variant.manifest.json"
    path.write_text(json.dumps(program, indent=1, sort_keys=True) + "\n")
    return path


def main() -> int:
    cli = Mncs()
    if not BASELINE_MANIFEST.exists():
        raise SystemExit("baseline artifacts missing; run tools/build_lineage_artifacts.py first")

    workdir = ROOT / "artifacts" / "lineage" / "invalidation-probe"
    workdir.mkdir(parents=True, exist_ok=True)

    # 2. Export the baseline evidence manifest (dependency-fingerprint bound).
    evidence = cli.run(
        ["evidence-manifest", relative_to_language_root(BASELINE_MANIFEST)],
        cwd=language_root(),
    )
    evidence_path = workdir / "parent-evidence-manifest.json"
    evidence_path.write_text(json.dumps(evidence, indent=1, sort_keys=True) + "\n")

    # 3-4. Assess the parent evidence against the changed successor artifact.
    variant_manifest = build_variant_manifest(cli, workdir)
    assessment = cli.run(
        [
            "evidence-check",
            relative_to_language_root(evidence_path),
            relative_to_language_root(variant_manifest),
        ],
        cwd=language_root(),
    )
    assessment_path = workdir / "evidence-assessment.json"
    assessment_path.write_text(json.dumps(assessment, indent=1, sort_keys=True) + "\n")

    reports = assessment if isinstance(assessment, list) else assessment.get("reports", [])
    stale = [r for r in reports if r.get("freshness") != "current"]
    print(f"evidence records assessed: {len(reports)}")
    print(f"records invalidated by the policy change: {len(stale)}")
    for record in stale[:6]:
        reasons = record.get("invalidated_by") or []
        print(f"  - {record.get('subject', '?')}: {reasons[:2]}")
    if not stale:
        print("FAILURE: no evidence was invalidated; staleness detection is broken")
        return 1

    # 5. The parent's corpus no longer satisfies the changed contract: the
    # rollback-missing case expected REJECT and the successor now holds, so
    # promotion evidence must be re-established under the successor identity.
    proc = subprocess.run(
        cli.argv(
            [
                "experiment",
                "run",
                relative_to_language_root(variant_manifest),
                "--backend",
                "mncs-research-bytecode",
                "--corpus",
                relative_to_language_root(CORPUS),
                "--output-dir",
                relative_to_language_root(workdir / "experiment-parent-corpus"),
            ]
        ),
        cwd=language_root(),
        capture_output=True,
        text=True,
    )
    # A FAIL exit is the expected honest outcome here; anything else is a probe error.
    if proc.returncode not in (0, 1):
        raise SystemExit(f"experiment run failed unexpectedly:\n{proc.stderr}")
    try:
        experiment = json.loads(proc.stdout)
    except json.JSONDecodeError as error:
        raise SystemExit(f"non-JSON experiment output: {error}\n{proc.stdout[:400]}")
    failed_expectations = [
        case["case_id"]
        for case in experiment["cases"]
        if case.get("expectation_met") is False
    ]
    print(f"successor vs parent corpus status: {experiment['status']}")
    print(f"cases whose inherited expectation no longer holds: {failed_expectations}")
    if not failed_expectations:
        print("WARNING: changed policy satisfied the unchanged corpus; probe scenario is stale")
        return 1

    summary = {
        "schema_version": "mncs-lineage/evidence-invalidation-probe/0.1",
        "invalidated_records": len(stale),
        "assessed_records": len(reports),
        "reevaluation_required": True,
        "inherited_expectations_failing": failed_expectations,
    }
    (workdir / "probe-summary.json").write_text(
        json.dumps(summary, indent=1, sort_keys=True) + "\n"
    )
    print("evidence invalidation confirmed; re-evaluation required")
    return 0


if __name__ == "__main__":
    sys.exit(main())
