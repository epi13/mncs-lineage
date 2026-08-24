# Roadmap

> **Direction change (2026-08):** MNCS Language integration has been pulled
> forward from Stage 8 to the current development front. Lineage is now an
> active MNCS Language proving ground: the succession core is written in MNCS
> Language, executes through the reference toolchain, and its requirements are
> driving language, compiler, tooling, and service fixes. See
> [LANGUAGE_IMPLEMENTATION.md](LANGUAGE_IMPLEMENTATION.md) for what runs
> today and [MNCS_LANGUAGE_FINDINGS.md](MNCS_LANGUAGE_FINDINGS.md) for the
> recorded impact on the language. The staged research plan below remains
> valid; stages now *assume* native semantics rather than deferring them.

Lineage should remain deliberately conservative until its abstractions can be tested with small, reproducible systems. The roadmap therefore starts with records and controlled experiments rather than autonomous replacement.

## Stage 0 — Concept and vocabulary — COMPLETE

**Goal:** define what Lineage means before implementing it.

- define succession, inheritance, candidate, promotion, rollback, and lineage fitness;
- document authority separation;
- define relationship to MNEL, Forge, Fabric, Harness, RAVEL, MNCDS, MNCS, and MNCS Language;
- sketch machine-readable succession contracts;
- identify explicit non-goals and falsifiers.

**Exit condition:** the architecture can describe a multi-generation experiment without relying on ambiguous anthropomorphic language.

## Stage 1 — Deterministic record model — SUBSTANTIALLY COMPLETE IN MNCS LANGUAGE

**Goal:** make succession auditable without training any model.

Status against the original checklist:

- canonical generation descriptors — done (freeze records, generation graph);
- candidate descriptors — done (`frozen_candidate` identity bindings);
- succession-contract validation — done (declared contract clauses validated
  and evidence-gated by the compiler);
- inheritance manifests — modeled as dependency tuples in the executable core;
  full artifact manifests remain future work;
- frozen-candidate records — done (`candidate-freeze-record.json`);
- evidence-manifest references — done (dependency-fingerprinted evidence,
  `evidence-check` invalidation);
- promotion/rejection/unknown records — done at decision level
  (`Disposition`, sealed experiment results); a dedicated promotion-control
  record family is next;
- rollback records — done (rollback targets in the generation graph; rollback
  gates in the disposition rule);
- lineage graph verification — done (`check_generation_graph`);
- evidence invalidation on dependency change — done at both language level
  (corpus cases) and artifact level (invalidation probe).

No model can promote itself: authority separation is enforced statically
(`MNE134`), at decision level, and operationally.

**Exit condition:** met for the synthetic round - the lineage replays and
validates deterministically from records alone (`--check`).

## Stage 2 — Single-transition reference experiment

**Goal:** test one parent-to-successor transition on a small system.

Suggested experiment:

```text
small parent model P
  |
  +--> control candidate: default initialization
  +--> inherited candidate: direct parameter inheritance
  +--> generated candidate: lineage-conditioned initialization
        |
        v
fixed development budget
        |
        v
visible validation + hidden transfer evaluation
        |
        v
succession contract verdicts
```

Measure causal contribution of inheritance rather than only final score.

**Exit condition:** the experiment produces reproducible evidence showing whether a chosen inheritance mechanism helps, hurts, or is inconclusive.

## Stage 3 — MNEL-informed inheritance

**Goal:** consume real eligible MNEL outputs without collapsing evidence boundaries.

Explore:

- supported strategy inheritance;
- negative-memory inheritance;
- counterexample inheritance;
- causal-attribution-informed candidate design;
- visibility preservation across MNEL -> Lineage boundaries;
- explicit distinction between historical evidence and successor evidence.

**Exit condition:** an MNEL-derived artifact can influence candidate development while its original evidence status and provenance remain intact.

## Stage 4 — Candidate populations

**Goal:** support multiple successor proposals under one parent.

Add:

- candidate population manifests;
- bounded search/mutation budgets;
- hard protected-property gates;
- Pareto or constrained selection policies;
- diversity measurements;
- rejection-memory retention;
- comparative lineage evidence.

Avoid reducing all evaluation to one opaque scalar fitness score.

**Exit condition:** multiple candidates can be compared, rejected, or admitted using frozen rules and traceable evidence.

## Stage 5 — Generated developmental initialization

**Goal:** test the specific hypothesis that a parent/lineage mechanism can create useful starting states for a successor.

Potential mechanisms:

- transformed parent weights;
- low-rank/sparse deltas;
- module-specific initializers;
- hypernetwork-generated parameters;
- learned initialization distributions;
- architecture-conditioned developmental priors;
- curriculum generation.

Required controls should include default initialization and direct inheritance where applicable.

**Exit condition:** a generated initialization shows reproducible benefit on hidden transfer or development efficiency under equalized budgets, or the hypothesis is rejected for the tested setting.

## Stage 6 — Multi-generation study

**Goal:** distinguish one successful replacement from genuine generational improvement.

Run controlled sequences such as:

```text
G0 -> G1 -> G2 -> G3 -> ...
```

Track:

- target-property trend;
- protected-property stability;
- hidden-transfer trend;
- compute/development efficiency;
- lineage-fitness trend;
- rejected-candidate rate;
- contamination indicators;
- evaluator drift;
- rollback events.

Use fixed future-final partitions when possible to detect cumulative benchmark adaptation.

**Exit condition:** enough generations exist to test whether improvement is durable rather than a single-step artifact.

## Stage 7 — Succession-mechanism improvement

**Goal:** allow parts of the successor-production mechanism to become research candidates themselves.

Possible candidates:

- initializer;
- architecture proposer;
- curriculum generator;
- inheritance selector;
- candidate router;
- experiment planner.

The promotion policy and critical evaluation authority must remain outside the mechanism being optimized.

**Exit condition:** a successor-production component can be replaced under the same evidence-governed semantics without redefining its own acceptance standard.

## Stage 8 — MNCS Language integration — PULLED FORWARD; FIRST MILESTONE COMPLETE

**Goal:** move from ad hoc research records toward native machine semantics. The language proved ready enough, and Lineage is now one of its primary proving grounds.

Delivered in the first milestone (see [LANGUAGE_IMPLEMENTATION.md](LANGUAGE_IMPLEMENTATION.md)):

- typed succession vocabulary as enums and records (`Verdict`, structured
  `UnknownReason` with seven actionable reasons, `ClaimVerdict`,
  `RollbackState`, `Disposition`);
- succession contracts as compiler-validated clauses, evidence-gated before
  anything seals PASS;
- promotion eligibility, rejection, and structured UNKNOWN as executable
  fail-closed decision rules;
- authority separation enforced statically (`MNE134`), at decision level, and
  operationally through Forge evaluator boundaries;
- candidate identity freshness over the identity-bearing dependency tuple,
  with evidence invalidation on change;
- branching lineage representation (rejected / unknown / promoted siblings)
  and a deterministically reconstructed G0->G1->G2 generation graph;
- deterministic replay sealed across two backend realizations.

Language changes this milestone forced are recorded in
[MNCS_LANGUAGE_FINDINGS.md](MNCS_LANGUAGE_FINDINGS.md): interleaved
declarations, record-literal disambiguation, record values as execution
observations, `.mncs` input to every semantic command.

Still open in this stage:

- cross-module imports so vocabulary is shared rather than mirrored (F12);
- promotion-control record family as first-class language artifacts;
- semantic deltas beyond dependency tuples;
- source-level arithmetic intents for in-language hashing (F7).

**Exit condition:** met - succession contracts round-trip source -> canonical
semantic form -> frozen manifest -> freeze record without losing authority,
evidence, identity, inheritance, or provenance semantics.

## Stage 9 — Fabric/Forge distributed evaluation

**Goal:** use mature MNCS infrastructure for bounded candidate development and independent evaluation.

Potential integration:

```text
Lineage contract
   |
   +--> Fabric development jobs
   +--> Forge verifier/probe jobs
   +--> MNEL evidence inputs
   +--> RAVEL candidate proposals
   +--> MNCDS lineage/provenance records
   |
   v
promotion controller
```

Execution records must remain execution evidence; they do not become promotion authority by virtue of being distributed.

## Stage 10 — Controlled operational succession

**Goal:** only after the prior abstractions have substantial evidence, explore replacement of a real long-running service or agent configuration.

Requirements should include:

- shadow/canary activation;
- state migration contract;
- rollback test;
- protected operational metrics;
- bounded authority;
- operator-visible audit trail;
- failure containment;
- independent promotion controller.

This is intentionally late in the roadmap.

## What is not a milestone

The following should not be treated as proof of Lineage's central hypothesis:

- one model editing another model;
- a child scoring higher on a benchmark chosen by its parent;
- successful fine-tuning from copied weights;
- an agent generating its own training data;
- a model declaring that its successor is improved;
- repeated generations evaluated only on the same exposed tests;
- increased parameter count or compute;
- a successful deployment without preserved evidence and rollback semantics.

The research target is not merely automated training. It is **evidence-governed generational improvement with explicit inheritance and succession semantics**.
