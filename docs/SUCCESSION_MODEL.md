# Succession Model

> **Status:** the lifecycle and authority rules described here are now
> enforced by executable MNCS Language modules (`language/`) and sealed
> corpora (`examples/execution/`). See
> [LANGUAGE_IMPLEMENTATION.md](LANGUAGE_IMPLEMENTATION.md).

## Purpose

The succession model defines how a potential next generation moves from proposal to active status without requiring the currently active system to modify itself in place or become the sole judge of its own replacement.

The model is intentionally compatible with future MNCS Language semantics but does not require a final language syntax.

## Lifecycle

A candidate should move through explicit states:

```text
PROPOSED
   |
   v
ADMITTED_FOR_DEVELOPMENT
   |
   v
DEVELOPING
   |
   v
FROZEN
   |
   v
EVALUATING
   |
   +--> REJECTED
   +--> UNKNOWN
   |
   v
ELIGIBLE_FOR_PROMOTION
   |
   v
PROMOTED
   |
   v
ACTIVE
   |
   +--> RETIRED
   +--> ROLLED_BACK
```

No state transition should be inferred from a model's narrative output. Each transition should be represented by a machine-readable record with actor/authority identity, predecessor state, successor state, relevant artifact identities, and evidence references.

## Candidate proposal

A proposal should minimally bind:

- parent generation identity;
- candidate identity or deterministic construction recipe;
- target properties;
- protected properties;
- permitted mutation/development scope;
- resource envelope;
- inherited artifacts;
- declared evaluation envelope;
- required evidence classes;
- prohibited authority combinations where applicable;
- rollback requirements.

The proposal itself is not evidence that the candidate satisfies any target.

## Development admission

Before training or transformation begins, a candidate should be admitted to a bounded development envelope. Admission should answer:

1. What may change?
2. What may be read?
3. Which tools/capabilities are available?
4. What resource budget applies?
5. Which artifacts are frozen inputs?
6. Which evaluation data are hidden from the candidate-producing process?
7. What outputs are allowed to cross the development boundary?

Development authority may transform candidate state but must not silently alter the active generation.

## Candidate freeze

A candidate becomes **frozen** when the artifact to be evaluated is identity-bound and no further development mutation is permitted within that evaluation round.

Freezing should include:

- executable/model identity;
- architecture/configuration identity;
- inherited-artifact manifest identity;
- dependency identities;
- runtime envelope;
- evaluation protocol version;
- evidence eligibility rules.

If any identity-bearing input changes, applicable evidence should be invalidated or conservatively reclassified.

## Evaluation

Evaluation operates against explicit claims rather than an undifferentiated score.

Example claim classes:

```text
TARGET
  planning.transfer >= parent + margin

PROTECTED
  tool_authority <= parent.tool_authority
  critical_regression_count == 0
  deterministic_contract_suite == PASS

RESOURCE
  peak_memory <= declared_limit

LINEAGE
  inheritance_provenance == complete
  evaluator_visibility == allowed
```

Each claim should resolve to `PASS`, `FAIL`, or `UNKNOWN` under a named verifier/evaluator and evidence class.

A weighted benchmark aggregate may be useful for research, but it cannot erase a failed hard protected-property gate unless the contract explicitly permits that trade.

## Hidden transfer evaluation

Where empirical learning is involved, Lineage should reserve evaluation surfaces that the proposal/development process cannot inspect directly.

The goal is to distinguish:

- genuine transfer;
- benchmark memorization;
- evaluator adaptation;
- overfitting to parent-generated tests;
- inheritance contamination.

Hidden evaluation does not make an evaluator infallible. It provides one stronger evidence partition.

## Promotion eligibility

A candidate becomes eligible for promotion only when the succession contract's hard requirements have sufficient current evidence.

Illustrative rule:

```text
eligible(C) =
    all(hard_target_claims(C) == PASS)
    AND all(protected_claims(C) == PASS)
    AND no(required_claim(C) == UNKNOWN)
    AND provenance_valid(C)
    AND rollback_ready(parent(C))
```

Different research studies may choose other policies, but the policy must be declared before candidate results are interpreted when possible.

## Promotion

Promotion changes the active-generation identity. It should be treated as a privileged control-plane operation, not a side effect of training or evaluation.

A promotion record should bind:

- previous active generation;
- promoted candidate;
- succession contract;
- complete eligible evidence set or evidence-manifest identity;
- promotion policy version;
- promotion authority identity;
- activation time/sequence;
- rollback target;
- unresolved non-blocking claims, if any.

The promoted generation does not erase the previous generation.

## Rollback

Rollback is first-class because succession is an operational state transition, not merely a research conclusion.

A rollback policy should define:

- retained predecessor artifacts;
- state compatibility or migration constraints;
- rollback triggers;
- who/what has rollback authority;
- maximum acceptable rollback delay where operationally relevant;
- evidence produced by the rollback event.

A candidate that cannot be safely rolled back may require a substantially higher promotion threshold.

## Competing candidates

Lineage should support a candidate population without requiring biological evolutionary mechanics.

```text
parent P
   |
   +--> C1
   +--> C2
   +--> C3

C1/C2/C3 receive bounded development
            |
            v
independent evaluation
            |
            v
zero, one, or multiple promotion-eligible candidates
```

Selection policy should be explicit. A candidate can fail because it violates a protected property even if it has the highest target score.

## Parent-generated evaluations

A parent may generate tests, adversarial examples, hypotheses, or curricula. These are valuable proposal artifacts, but they should be labeled by origin.

Parent-generated tests may support development and diagnostic claims. Strong promotion claims should preferentially include evaluation not controlled by the candidate-producing lineage path.

## Authority matrix

A future deployment should be able to express combinations such as:

| Operation | Parent | Candidate | MNEL investigator | Forge verifier | Promotion controller |
|---|---:|---:|---:|---:|---:|
| propose candidate | yes | no | possible | no | no |
| mutate candidate | bounded | bounded self-adaptation if allowed | possible | no | no |
| emit observation | yes | yes | yes | yes | yes |
| declare bounded verifier verdict | no by default | no | no | yes | possible for policy-only claims |
| promote candidate | no | no | no | no | yes |
| rollback | no by default | no | no | no | yes |

This table is conceptual. Exact capability allocation belongs to future integration contracts.

## Failure semantics

Lineage should fail closed on promotion-critical ambiguity:

- stale evidence -> `UNKNOWN`;
- missing verifier -> `UNKNOWN`;
- invalid provenance -> `FAIL` or ineligible, according to contract;
- hidden-test contamination -> affected evidence invalid;
- unbounded mutation -> candidate ineligible;
- authority violation -> candidate/evidence quarantined;
- rollback artifact missing -> promotion blocked when rollback is required.

A failed candidate remains useful research evidence and should not be silently discarded from the lineage record.
