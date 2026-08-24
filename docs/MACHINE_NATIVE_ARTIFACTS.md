# Machine-Native Artifacts

> **Status:** much of what this document describes as future direction now
> exists in executable form under `language/` and `tools/`; start with
> [LANGUAGE_IMPLEMENTATION.md](LANGUAGE_IMPLEMENTATION.md). This document
> remains useful for intent and rationale.

## Goal

Lineage should be operable from machine-readable semantic records rather than requiring an LLM to reinterpret prose at every generational transition.

The human-facing documentation explains intent. The eventual control plane should consume canonical, typed artifacts with stable identities, explicit authority, and deterministic validation rules where possible.

## Artifact families

A minimal future Lineage implementation is likely to need distinct artifact families for:

1. **generation descriptors** — identify the admitted executable configuration;
2. **candidate descriptors** — bind parentage, construction inputs, and candidate identity;
3. **succession contracts** — declare target and protected claims plus required evidence;
4. **inheritance manifests** — describe transferred artifacts and transformations;
5. **development manifests** — define allowed mutation, resources, capabilities, and visibility;
6. **candidate freeze records** — bind the immutable candidate evaluated in a round;
7. **evaluation manifests** — bind evaluators, partitions, budgets, and claim mappings;
8. **evidence records** — record observations and claim verdicts without authority laundering;
9. **promotion records** — authorize an active-generation transition;
10. **rollback records** — authorize restoration of a retained predecessor;
11. **retirement records** — close active status while retaining lineage history.

These should be separate records because they carry different authority.

## Identity

Content-addressed identities are preferred for immutable artifacts:

```text
artifact_id = sha256(canonical_form(artifact))
```

The exact canonicalization mechanism should align with MNCS-family conventions rather than inventing an incompatible one.

Mutable operational pointers such as `active_generation` should reference immutable generation identities and change only through explicit state-transition records.

## Candidate identity

A candidate identity should be derivable from more than a display name. Relevant inputs may include:

```text
candidate_identity <- hash(
    parent_generation,
    succession_contract,
    architecture_or_program,
    inheritance_manifest,
    development_recipe,
    dependency_ids
)
```

A post-development frozen candidate receives an identity bound to the resulting executable/model artifact as well.

Changing an identity-bearing dependency should prevent accidental reuse of stale evaluation evidence.

## Claims and evidence

Claims should have stable identifiers and explicit classes:

```json
{
  "claim_id": "planner.transfer.hidden-v1",
  "class": "target",
  "relation": ">=",
  "baseline": "parent",
  "margin": 0.03,
  "evaluator": "sha256:...",
  "required_status": "PASS"
}
```

Evidence should reference claims rather than existing as free-floating success metadata.

A verifier result should be distinguishable from:

- raw observation;
- parent/generated prediction;
- diagnostic model score;
- empirical benchmark result;
- static-analysis result;
- formal proof object;
- human/operator approval.

## Authority as data

Every authority-bearing record should identify the capability or authority used to produce it.

Conceptual example:

```json
{
  "transition": "eligible-for-promotion -> promoted",
  "candidate": "sha256:...",
  "authority": {
    "kind": "promotion",
    "principal": "urn:mncs:controller:promotion-v1"
  },
  "evidence_manifest": "sha256:..."
}
```

A process being technically able to write a file is not the same as being semantically authorized to promote a generation.

## Machine-readable uncertainty

Lineage should preserve `UNKNOWN` as a first-class state.

```text
PASS     claim established to the declared evidence standard
FAIL     claim contradicted or hard requirement violated
UNKNOWN  insufficient, stale, ineligible, unavailable, or indeterminate evidence
```

Reasons should be structured where practical:

```text
UNKNOWN_STALE_EVIDENCE
UNKNOWN_MISSING_VERIFIER
UNKNOWN_BUDGET_EXHAUSTED
UNKNOWN_UNSUPPORTED_TARGET
UNKNOWN_CONTAMINATED_PARTITION
UNKNOWN_DEPENDENCY_CHANGED
```

This makes uncertainty actionable for machine planning without granting permission to infer success.

## Semantic deltas

A future MNCS Language integration should enable a succession evaluator to ask not only whether files differ but how the candidate differs semantically:

```text
parent -> candidate

capability delta
contract delta
authority delta
effect delta
resource delta
machine-intent delta
evidence delta
architecture delta
parameter/inheritance delta
```

Promotion policy can then require targeted re-verification of affected properties instead of treating every successor as an opaque binary blob.

## Succession graph

The lineage structure should support branching and rejected candidates:

```text
G0
|\
| C1 (rejected)
|\
| C2 (unknown)
 \
  G1 (promoted)
  |\
  | C3 (rejected)
   \
    G2 (promoted)
```

The graph should retain evidence links and inheritance edges separately from the simple active-generation chain.

## Human readability

Machine-native does not mean machine-secret.

Canonical artifacts should have:

- documented schemas;
- deterministic pretty-printing;
- stable identifiers;
- explicit units and enums;
- bounded nesting/size where feasible;
- no requirement for natural-language interpretation to determine authority;
- optional explanatory text that is never the sole carrier of a critical rule.

## Relationship to MNCS Language

The long-term goal is not to keep Lineage's semantics permanently trapped in ad hoc JSON.

If the MNCS Language matures enough, concepts such as succession contracts, protected properties, authority, evidence obligations, and permitted transformations could become native semantic objects. JSON can remain a transport or compatibility representation while the language supplies stronger semantics and verification.

Until that point, Lineage should prefer simple, conservative record formats that can later be mapped into the language without changing the underlying concepts.
