"""MNCS Lineage — language integration and deterministic succession tests.

These tests exercise the synthetic lineage through the real MNCS Language
toolchain (reference compiler, validator, obligation engine, experiment
suite, and evidence machinery). They require either a built `mncs` binary
via MNCS_BIN or a checkout of mncs-language next to this repository.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import build_lineage_artifacts as builder  # noqa: E402

CORE_SOURCE = REPO_ROOT / "language" / "lineage-core.mncs"
G0_SOURCE = REPO_ROOT / "language" / "synthetic-lineage-g0.mncs"
NEGATIVE_SELF_CERT = REPO_ROOT / "language" / "negative" / "g0-proposer-self-certification.mncs"
VARIANT_SOURCE = (
    REPO_ROOT / "language" / "variants" / "g0-rollback-holds-on-missing-artifact.mncs"
)
CORPUS = REPO_ROOT / "examples" / "execution" / "synthetic-lineage-g0-corpus.json"


def run_mncs(args: list[str], expect_success: bool = True) -> dict:
    argv = builder.Mncs().argv(args)
    proc = subprocess.run(argv, cwd=builder.language_root(), capture_output=True, text=True)
    if expect_success and proc.returncode != 0:
        raise AssertionError(f"{args} failed ({proc.returncode}):\n{proc.stderr}")
    try:
        return json.loads(proc.stdout) if proc.stdout.strip() else {}
    except json.JSONDecodeError as error:
        raise AssertionError(f"{args} emitted non-JSON output: {error}\n{proc.stdout[:400]}")


# ---------------------------------------------------------------------------
# Source-level semantics
# ---------------------------------------------------------------------------


def test_lineage_sources_validate_through_reference_front_end():
    for source in (CORE_SOURCE, G0_SOURCE):
        report = run_mncs(["validate", builder.relative_to_language_root(source)])
        assert report["valid"] is True, report["errors"]
        assert report["errors"] == []


def test_module_names_follow_family_namespace_conventions():
    text = G0_SOURCE.read_text()
    assert "module lineage.synthetic.g0.v1;" in text
    # `mncs` is a keyword; module roots cannot start with it (recorded finding).
    assert "module mncs." not in text


def test_verdict_vocabulary_is_first_class_and_exhaustive():
    program_text = CORE_SOURCE.read_text()
    for keyword in ("PASS", "FAIL", "UNKNOWN"):
        assert f"    {keyword}," in program_text or f"{keyword} =>" in program_text
    for reason in (
        "STALE_EVIDENCE",
        "MISSING_VERIFIER",
        "BUDGET_EXHAUSTED",
        "UNSUPPORTED_TARGET",
        "CONTAMINATED_PARTITION",
        "DEPENDENCY_CHANGED",
        "INSUFFICIENT_EVIDENCE",
    ):
        assert reason in program_text


def test_proposal_authority_cannot_self_certify():
    """The self-certification module must be rejected at validation time."""
    proc = subprocess.run(
        builder.Mncs().argv(
            ["validate", builder.relative_to_language_root(NEGATIVE_SELF_CERT)]
        ),
        cwd=builder.language_root(),
        capture_output=True,
        text=True,
    )
    assert proc.returncode != 0, "self-certification module must not validate"
    diagnostics = json.loads(proc.stdout)
    codes = [item["code"] for item in diagnostics]
    assert "MNE134" in codes, codes


# ---------------------------------------------------------------------------
# Deterministic synthetic succession experiment
# ---------------------------------------------------------------------------


def test_corpus_covers_topology_authority_and_invalidation():
    corpus = json.loads(CORPUS.read_text())
    by_id = {case["id"]: case for case in corpus["cases"]}
    # branching topology: C1 rejected, C2 held, C3 promoted
    assert "topology-canonical-g0" in by_id
    assert "self-certification-admits-nobody" in by_id
    # evidence invalidation on identity change
    assert "changed-dependency-invalidates-pass" in by_id
    assert "stale-reason-is-dependency-changed" in by_id
    # protected-property gate beats target improvement
    assert "c1-target-improves-but-protected-regresses" in by_id


def test_frozen_candidate_passes_on_both_backends():
    summary = builder.build_target(builder.Mncs(), builder.TARGETS[0], REPO_ROOT / "artifacts" / "lineage")
    record = summary["record"]
    assert record["schema_version"] == "mncs-lineage/candidate-freeze-record/0.1"
    assert len(record["experiments"]) == 2
    backends = {e["backend"]: e["status"] for e in record["experiments"]}
    assert backends == {
        "mncs-research-bytecode": "PASS",
        "mncs-portable-wasm-mvp": "PASS",
    }
    assert record["evidence_binding"]["remaining_unresolved_obligations"] == []
    assert len(record["evidence_binding"]["discharged_contracts"]) >= 10


def test_freeze_record_binds_candidate_identity_inputs():
    workdir = REPO_ROOT / "artifacts" / "lineage"
    record_path = workdir / "synthetic-lineage-g0" / "candidate-freeze-record.json"
    if not record_path.exists():
        builder.build_target(builder.Mncs(), builder.TARGETS[0], workdir)
    record = json.loads(record_path.read_text())
    frozen = record["frozen_candidate"]
    # every identity-bearing dependency is bound by content hash
    assert frozen["source_sha256"] == builder.file_sha256(G0_SOURCE)
    assert frozen["corpus_sha256"] == builder.file_sha256(CORPUS)
    manifest_sha = frozen["manifest_sha256"]
    manifest_path = workdir / "synthetic-lineage-g0" / "synthetic-lineage-g0.manifest.json"
    assert manifest_sha == builder.file_sha256(manifest_path)


def test_generation_graph_reconstructs_g0_g1_g2():
    workdir = REPO_ROOT / "artifacts" / "lineage"
    graph_path = workdir / "synthetic-lineage-g0" / "generation-graph.json"
    if not graph_path.exists():
        builder.build_target(builder.Mncs(), builder.TARGETS[0], workdir)
    graph = json.loads(graph_path.read_text())
    builder.check_generation_graph(graph)
    ids = [g["generation_id"] for g in graph["generations"]]
    assert len(ids) == 3
    # cumulative provenance: G2 -> G1 -> G0
    g2 = next(g for g in graph["generations"] if g["depth"] == 2)
    assert g2["inherited_from"]["role"] == "promoted-candidate"
    assert g2["rollback_target"] in ids
    # branching history retained: one rejected, one unknown sibling under G0
    assert graph["rejected_candidates"][0]["reason"] == "protected_regression"
    assert graph["unknown_candidates"][0]["unknown_reason"] == "DEPENDENCY_CHANGED"


def test_replay_is_deterministic():
    """Rerunning the whole round reproduces identical freeze records."""
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "build_lineage_artifacts.py"), "--check"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "determinism probe: records reproduce exactly" in proc.stdout


def test_cross_backend_behavior_agrees():
    comparison_path = (
        REPO_ROOT
        / "artifacts"
        / "lineage"
        / "synthetic-lineage-g0"
        / "cross-backend-comparison.json"
    )
    if not comparison_path.exists():
        builder.build_target(builder.Mncs(), builder.TARGETS[0], REPO_ROOT / "artifacts" / "lineage")
    comparison = json.loads(comparison_path.read_text())
    assert comparison["same_semantics"] is True
    assert comparison["same_hir"] is True
    assert comparison["bounded_behavior_agrees"] is True


# ---------------------------------------------------------------------------
# Evidence invalidation
# ---------------------------------------------------------------------------


def test_changed_policy_invalidates_parent_evidence():
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "invalidate_evidence_probe.py")],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    summary = json.loads(
        (REPO_ROOT / "artifacts" / "lineage" / "invalidation-probe" / "probe-summary.json").read_text()
    )
    assert summary["invalidated_records"] > 0
    assert summary["reevaluation_required"] is True
    # the inherited corpus expectation that no longer holds under the new policy
    assert "rollback-artifact-missing-blocks-promotion" in summary["inherited_expectations_failing"]
