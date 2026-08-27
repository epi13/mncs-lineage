"""Deterministic generational records for MNEL-backed Lineage specialists.

The builder is deliberately runtime-independent: it consumes a serialized
specialist artifact and records provenance, inheritance, evaluation, and
rollback semantics without importing or executing the MNEL trainer.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from typing import Any

SCHEMA_VERSION = "mncs-lineage/specialist-generation-record/0.1"
IDENTITY_LENGTH = 71
AUTHORITY = "lineage-succession-authority"


class SpecialistLineageError(ValueError):
    """A malformed specialist artifact or generational transition."""


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def identity(value: object, label: str) -> str:
    if (
        not isinstance(value, str)
        or not value.startswith("sha256:")
        or len(value) != IDENTITY_LENGTH
    ):
        raise SpecialistLineageError(f"{label} must be a sha256 identity")
    return value


def digest(value: object) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def _text(value: object, label: str, maximum: int = 256) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise SpecialistLineageError(f"{label} must be bounded non-empty text")
    return value


def _status(value: object, label: str) -> str:
    if value not in {"PASS", "FAIL", "UNKNOWN"}:
        raise SpecialistLineageError(f"{label} must be PASS, FAIL, or UNKNOWN")
    return str(value)


def _artifact_fields(artifact: Mapping[str, Any]) -> dict[str, Any]:
    value = dict(artifact)
    if value.get("schema") != "mnel-recurrent-specialist-artifact/0.1":
        raise SpecialistLineageError(
            "candidate is not an MNEL recurrent specialist artifact"
        )
    if value.get("authority") != "diagnostic-only":
        raise SpecialistLineageError(
            "candidate specialist authority must remain diagnostic-only"
        )
    for key in (
        "artifact_identity",
        "model_identity",
        "generation_identity",
        "training_dataset_identity",
        "training_spec_identity",
        "checkpoint_identity",
        "calibration_identity",
    ):
        identity(value.get(key), f"candidate.{key}")
    artifact_identity = value.pop("artifact_identity")
    if digest(value) != artifact_identity:
        raise SpecialistLineageError("candidate artifact identity does not match content")
    model_identity = value.pop("model_identity")
    if digest(value) != model_identity:
        raise SpecialistLineageError("candidate model identity does not match content")
    value["model_identity"] = model_identity
    value["artifact_identity"] = artifact_identity
    _text(value.get("target_role"), "candidate.target_role")
    negative_memory = value.get("negative_memory", [])
    if not isinstance(negative_memory, list) or len(negative_memory) > 64:
        raise SpecialistLineageError("candidate negative memory is unbounded")
    return value


def _inherited_artifacts(
    parent: Mapping[str, Any] | None,
    candidate: Mapping[str, Any],
) -> list[dict[str, Any]]:
    parent_generation = parent.get("generation_id") if parent else None
    if parent_generation is not None:
        identity(parent_generation, "parent.generation_id")
    entries: list[dict[str, Any]] = []
    for key, artifact_kind, evidence_class in (
        ("inherited_strategies", "strategy-bundle", "diagnostic-only"),
        ("known_counterexamples", "counterexample-bundle", "diagnostic-only"),
        ("prior_failure_causes", "failure-cause-bundle", "diagnostic-only"),
    ):
        values = candidate.get(key, [])
        if not isinstance(values, list) or len(values) > 64:
            raise SpecialistLineageError(f"candidate.{key} is unbounded")
        for index, item in enumerate(values):
            entries.append(
                {
                    "artifact_identity": digest(
                        {
                            "kind": artifact_kind,
                            "source": parent_generation,
                            "index": index,
                            "value": item,
                        }
                    ),
                    "artifact_kind": artifact_kind,
                    "source_generation": parent_generation,
                    "content_identity": digest(item),
                    "evidence_class": evidence_class,
                    "eligible_for_promotion_evidence": False,
                    "intended_role": "successor-development-guidance",
                }
            )
    return entries


def _negative_memory(
    parent: Mapping[str, Any] | None, candidate: Mapping[str, Any]
) -> list[dict[str, Any]]:
    parent_generation = parent.get("generation_id") if parent else None
    values = candidate.get("negative_memory", [])
    result = []
    for index, item in enumerate(values):
        result.append(
            {
                "memory_identity": digest(
                    {
                        "source_generation": parent_generation,
                        "index": index,
                        "value": item,
                    }
                ),
                "source_generation": parent_generation,
                "failure_cause": _text(str(item), "negative_memory.failure_cause", 512),
                "evidence_class": "diagnostic-only",
                "eligible_for_promotion_evidence": False,
                "retest_required": True,
            }
        )
    return result


def _disposition(
    target_status: str,
    protected_status: str,
    authority_independent: bool,
    rollback_status: str,
) -> str:
    if target_status == "FAIL" or protected_status == "FAIL":
        return "REJECTED"
    if target_status == "UNKNOWN" or protected_status == "UNKNOWN":
        return "HOLD_UNKNOWN"
    if not authority_independent:
        return "REJECTED"
    if rollback_status != "READY":
        return "REJECTED"
    return "PROMOTED"


def build_specialist_generation_record(
    *,
    parent: Mapping[str, Any] | None,
    candidate_artifact: Mapping[str, Any],
    evaluation: Mapping[str, Any],
    contract_identity: str,
    proposer_identity: str,
    evaluator_identity: str,
    promotion_authority_identity: str,
    rollback_target_artifact_identity: str | None,
    rollback_status: str,
) -> dict[str, Any]:
    """Build and validate one immutable specialist generation transition."""

    candidate = _artifact_fields(candidate_artifact)
    identity(contract_identity, "contract_identity")
    _text(proposer_identity, "proposer_identity")
    _text(evaluator_identity, "evaluator_identity")
    _text(promotion_authority_identity, "promotion_authority_identity")
    target_status = _status(evaluation.get("target_status"), "evaluation.target_status")
    protected_status = _status(
        evaluation.get("protected_status"), "evaluation.protected_status"
    )
    evidence_epoch = evaluation.get("evidence_epoch")
    current_epoch = evaluation.get("current_epoch")
    if not isinstance(evidence_epoch, int) or not isinstance(current_epoch, int):
        raise SpecialistLineageError("evaluation epochs must be integers")
    if evidence_epoch != current_epoch and target_status == "PASS":
        target_status = "UNKNOWN"
        evaluation_reason = "DEPENDENCY_CHANGED"
    else:
        evaluation_reason = str(evaluation.get("reason", "NONE"))
    authority_independent = (
        proposer_identity != promotion_authority_identity
        and evaluator_identity != promotion_authority_identity
    )
    disposition = _disposition(
        target_status, protected_status, authority_independent, rollback_status
    )
    parent_generation_id = parent.get("generation_id") if parent else None
    parent_model_identity = parent.get("model_identity") if parent else None
    if parent_generation_id is not None:
        identity(parent_generation_id, "parent.generation_id")
        identity(parent_model_identity, "parent.model_identity")
        if candidate.get("parent_model_identity") != parent_model_identity:
            raise SpecialistLineageError(
                "candidate parent model identity does not match lineage"
            )
    if rollback_target_artifact_identity is not None:
        identity(rollback_target_artifact_identity, "rollback_target_artifact_identity")
    if disposition == "PROMOTED" and rollback_target_artifact_identity is None:
        raise SpecialistLineageError(
            "promoted generation must retain a rollback artifact"
        )
    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generation_id": candidate["generation_identity"],
        "parent_generation_id": parent_generation_id,
        "specialist_role": candidate["target_role"],
        "status": disposition,
        "candidate": {
            "artifact_identity": candidate["artifact_identity"],
            "model_identity": candidate["model_identity"],
            "parent_model_identity": candidate.get("parent_model_identity"),
            "training_dataset_identity": candidate["training_dataset_identity"],
            "training_spec_identity": candidate["training_spec_identity"],
            "checkpoint_identity": candidate["checkpoint_identity"],
            "calibration_identity": candidate["calibration_identity"],
            "operating_envelope_identity": candidate["operating_envelope"][
                "envelope_identity"
            ],
            "authority": candidate["authority"],
        },
        "succession": {
            "contract_identity": contract_identity,
            "proposer_identity": proposer_identity,
            "evaluator_identity": evaluator_identity,
            "promotion_authority_identity": promotion_authority_identity,
            "authority_independent": authority_independent,
            "proposal_is_not_promotion_authority": True,
        },
        "inheritance": {
            "parent_model_identity": parent_model_identity,
            "artifacts": _inherited_artifacts(parent, candidate),
            "negative_memory": _negative_memory(parent, candidate),
            "historical_evidence_is_current": False,
        },
        "evaluation": {
            "target_status": target_status,
            "protected_status": protected_status,
            "reason": evaluation_reason,
            "evidence_epoch": evidence_epoch,
            "current_epoch": current_epoch,
            "evidence_reclassified": evidence_epoch != current_epoch,
        },
        "rollback": {
            "target_generation_id": parent_generation_id,
            "target_artifact_identity": rollback_target_artifact_identity,
            "test_status": rollback_status,
            "required_before_promotion": True,
        },
        "authority": AUTHORITY,
        "semantics": "lineage-generation-record; inherited-guidance-is-not-promotion-evidence",
    }
    record["record_identity"] = digest(record)
    validate_specialist_generation_record(record)
    return record


def validate_specialist_generation_record(record: Mapping[str, Any]) -> None:
    value = dict(record)
    supplied = value.pop("record_identity", None)
    identity(supplied, "record_identity")
    if digest(value) != supplied:
        raise SpecialistLineageError(
            "generation record identity does not match content"
        )
    if value.get("schema_version") != SCHEMA_VERSION:
        raise SpecialistLineageError("unsupported specialist generation record schema")
    if value.get("authority") != AUTHORITY:
        raise SpecialistLineageError("generation record authority is invalid")
    candidate = value.get("candidate")
    succession = value.get("succession")
    inheritance = value.get("inheritance")
    evaluation = value.get("evaluation")
    rollback = value.get("rollback")
    if not all(
        isinstance(item, Mapping)
        for item in (candidate, succession, inheritance, evaluation, rollback)
    ):
        raise SpecialistLineageError("generation record sections are malformed")
    if value.get("status") == "PROMOTED" and rollback["test_status"] != "READY":
        raise SpecialistLineageError(
            "promoted generation lacks a passing rollback test"
        )
    if succession["promotion_authority_identity"] in {
        succession["proposer_identity"],
        succession["evaluator_identity"],
    }:
        raise SpecialistLineageError("promotion authority is not independent")
    for section in (inheritance["artifacts"], inheritance["negative_memory"]):
        if not isinstance(section, list):
            raise SpecialistLineageError("inheritance section is not an array")
        for item in section:
            if item.get("eligible_for_promotion_evidence") is not False:
                raise SpecialistLineageError(
                    "inherited guidance cannot become promotion evidence"
                )


__all__ = [
    "AUTHORITY",
    "SCHEMA_VERSION",
    "SpecialistLineageError",
    "build_specialist_generation_record",
    "canonical_bytes",
    "digest",
    "validate_specialist_generation_record",
]
