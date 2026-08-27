from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from specialist_lineage import (
    SpecialistLineageError,
    build_specialist_generation_record,
    digest,
    validate_specialist_generation_record,
)


def _artifact(parent_model: str | None = None) -> dict[str, object]:
    envelope = {
        "max_iterations": 4,
        "maximum_context_observations": 32,
    }
    envelope["envelope_identity"] = digest(envelope)
    value: dict[str, object] = {
        "schema": "mnel-recurrent-specialist-artifact/0.1",
        "provider_id": "mnel-bounded-recurrent-specialist/0.1",
        "provider_abi": "mnel-specialist-provider-abi/0.1",
        "authority": "diagnostic-only",
        "target_role": "control.tool-family-routing",
        "artifact_identity": "",
        "model_identity": "",
        "parent_model_identity": parent_model,
        "generation_identity": digest("generation"),
        "training_dataset_identity": digest("dataset"),
        "training_spec_identity": digest("spec"),
        "checkpoint_identity": digest("checkpoint"),
        "calibration_identity": digest("calibration"),
        "operating_envelope": envelope,
        "negative_memory": ["ambiguous catalog must escalate"],
        "inherited_strategies": ["prefer schema-bound family identity"],
        "known_counterexamples": ["stale tool family"],
        "prior_failure_causes": ["role mismatch"],
    }
    model_content = dict(value)
    model_content.pop("model_identity")
    model_content.pop("artifact_identity")
    value["model_identity"] = digest(model_content)
    artifact_content = dict(value)
    artifact_content.pop("artifact_identity")
    value["artifact_identity"] = digest(artifact_content)
    return value


def _record(**kwargs):
    parent = {
        "generation_id": digest("parent-generation"),
        "model_identity": digest("parent-model"),
    }
    artifact = _artifact(parent["model_identity"])
    return build_specialist_generation_record(
        parent=parent,
        candidate_artifact=artifact,
        evaluation={
            "target_status": "PASS",
            "protected_status": "PASS",
            "evidence_epoch": 1,
            "current_epoch": 1,
        },
        contract_identity=digest("contract"),
        proposer_identity="proposer-v1",
        evaluator_identity="evaluator-v1",
        promotion_authority_identity="promoter-v1",
        rollback_target_artifact_identity=digest("parent-artifact"),
        rollback_status="READY",
        **kwargs,
    )


def test_generation_record_preserves_training_lineage_and_negative_memory() -> None:
    record = _record()
    validate_specialist_generation_record(record)
    assert record["status"] == "PROMOTED"
    assert record["candidate"]["training_dataset_identity"].startswith("sha256:")
    assert record["succession"]["authority_independent"] is True
    assert record["inheritance"]["historical_evidence_is_current"] is False
    assert (
        record["inheritance"]["negative_memory"][0]["eligible_for_promotion_evidence"]
        is False
    )
    assert record["rollback"]["test_status"] == "READY"


def test_stale_evidence_becomes_hold_unknown_and_keeps_parent_provenance() -> None:
    parent = {
        "generation_id": digest("parent-generation"),
        "model_identity": digest("parent-model"),
    }
    artifact = _artifact(parent["model_identity"])
    record = build_specialist_generation_record(
        parent=parent,
        candidate_artifact=artifact,
        evaluation={
            "target_status": "PASS",
            "protected_status": "PASS",
            "evidence_epoch": 1,
            "current_epoch": 2,
        },
        contract_identity=digest("contract"),
        proposer_identity="proposer-v1",
        evaluator_identity="evaluator-v1",
        promotion_authority_identity="promoter-v1",
        rollback_target_artifact_identity=digest("parent-artifact"),
        rollback_status="READY",
    )
    assert record["status"] == "HOLD_UNKNOWN"
    assert record["evaluation"]["target_status"] == "UNKNOWN"
    assert record["evaluation"]["reason"] == "DEPENDENCY_CHANGED"
    assert record["parent_generation_id"] == parent["generation_id"]


def test_authority_and_rollback_fail_closed() -> None:
    parent = {
        "generation_id": digest("parent-generation"),
        "model_identity": digest("parent-model"),
    }
    artifact = _artifact(parent["model_identity"])
    with pytest.raises(SpecialistLineageError):
        build_specialist_generation_record(
            parent=parent,
            candidate_artifact=artifact,
            evaluation={
                "target_status": "PASS",
                "protected_status": "PASS",
                "evidence_epoch": 1,
                "current_epoch": 1,
            },
            contract_identity=digest("contract"),
            proposer_identity="proposer-v1",
            evaluator_identity="evaluator-v1",
            promotion_authority_identity="evaluator-v1",
            rollback_target_artifact_identity=digest("parent-artifact"),
            rollback_status="READY",
        )
    with pytest.raises(SpecialistLineageError):
        build_specialist_generation_record(
            parent=parent,
            candidate_artifact=artifact,
            evaluation={
                "target_status": "PASS",
                "protected_status": "PASS",
                "evidence_epoch": 1,
                "current_epoch": 1,
            },
            contract_identity=digest("contract"),
            proposer_identity="proposer-v1",
            evaluator_identity="evaluator-v1",
            promotion_authority_identity="promoter-v1",
            rollback_target_artifact_identity=None,
            rollback_status="READY",
        )
