# MNEL Integration

## Why MNEL matters to Lineage

Machine-Native Experimental Learning (MNEL) provides a natural upstream source of **eligible, evidence-bearing experience** for generational succession.

MNEL and Lineage should remain distinct because they solve different problems:

```text
MNEL
  lifetime experimentation
  causal attribution
  negative memory
  verified-experience distillation
  bounded learned-provider adaptation

Lineage
  successor specification
  inheritance selection
  candidate development
  succession evaluation
  promotion / rollback state
```

The clean boundary is:

> MNEL may produce evidence and strategies that inform a successor. Lineage decides how that information may participate in a succession process. Neither subsystem gains promotion authority by contributing evidence.

## Intended flow

```text
MNEL experiment records
        |
        v
eligible causal attributions
        |
        v
Verified Experience Distillation
        |
        v
provisional strategies / negative memory / counterexamples
        |
        v
Lineage inheritance eligibility filter
        |
        v
successor specification and candidate development
        |
        v
Lineage evaluation
        |
        v
promotion decision under separate authority
```

The flow must preserve the evidence status attached by MNEL. A diagnostic-only learned-provider observation remains diagnostic-only when Lineage consumes it.

## Learning versus heredity

A useful conceptual split is:

- **MNEL = adaptation within a generation.**
- **Lineage = heredity between generations.**

This enables a generation to accumulate useful experimental experience without forcing every discovery into its own live model state.

A result may instead become a candidate inheritance proposal for the next generation.

Example:

```text
MNEL observation:
  strategy X repeatedly improves bounded planning task T
  transfer evidence = provisional
  counterexample set = K

Lineage interpretation:
  X may be proposed as developmental inheritance
  K must travel with X
  X may not be treated as universally valid
  successor must re-establish required claims under its own identity
```

## Evidence does not automatically transfer

Evidence is generally identity- and context-bound.

A claim established for generation `G_n` should not silently become established for `G_n+1`, even if `G_n+1` inherits the artifact that motivated the claim.

Lineage should distinguish:

```text
inherited artifact
inherited rationale
inherited historical evidence
current successor evidence
```

Historical evidence can justify *why a successor experiment is worth running*. Current promotion-critical evidence must be evaluated against the successor's actual frozen identity and dependencies.

## Negative memory

MNEL's negative memory is especially valuable to Lineage.

A successor should be able to inherit:

- known failure configurations;
- falsified hypotheses;
- counterexamples;
- verifier weaknesses;
- resource/pathological cases;
- strategies that failed transfer;
- prior rejected candidate causes.

Negative inheritance can reduce repeated exploration of known-bad regions without pretending those records prove what will happen in a new candidate.

## Candidate generation from MNEL experience

A future candidate synthesizer may consume an MNEL-derived bundle such as:

```text
eligible experience bundle
  + supported strategies
  + negative memory
  + unresolved hypotheses
  + known capability gaps
  + transfer results
  + resource observations
```

and produce:

```text
successor proposal
  + target claims
  + architecture/development changes
  + inheritance manifest
  + expected effects
  + required falsifiers
```

The expected effects are predictions. They do not become evidence until tested.

## Feedback from Lineage into MNEL

Promotion and rejection outcomes should themselves become eligible experimental material for later MNEL studies.

Examples:

- inherited strategy transferred successfully;
- generated initialization reduced training steps but hurt calibration;
- candidate architecture preserved task score but violated resource bounds;
- inherited negative memory prevented rediscovery of a known failure;
- parent-generated curriculum overfit visible evaluation tasks;
- a succession heuristic predicted improvement but failed hidden transfer.

This creates a longer loop:

```text
MNEL_n
  |
  v
Lineage synthesis
  |
  v
Generation n+1
  |
  v
MNEL_n+1
  |
  v
new evidence about the succession mechanism itself
```

Eventually MNEL may not only improve the active system's task strategies; it may experimentally improve **how Lineage produces successors**.

## Avoiding authority collapse

The same agent/model may technically participate in multiple stages during early research, but records should retain logical separation among:

- hypothesis generation;
- inheritance proposal;
- candidate synthesis;
- evaluation;
- promotion.

A parent model that proposes an initialization and then predicts that the initialization is excellent has produced two proposals, not independent promotion evidence.

## Visibility and contamination

Lineage should reuse MNEL-compatible visibility concepts for data/evidence partitions where possible:

- development-visible;
- selection-observed;
- transfer-hidden;
- future-final.

A successor generator must not gain access to hidden evaluation simply because an older generation once observed it. This is difficult across generations and should become a first-class research question.

## Long-term opportunity

If MNEL can identify reliable causal relationships between machine configuration and outcomes, Lineage may eventually use those relationships to generate better developmental priors:

```text
verified experience
      |
      v
learned succession hypothesis
      |
      v
architecture / initialization / curriculum proposal
      |
      v
candidate development
      |
      v
hidden transfer evaluation
```

At that point, MNEL and Lineage together would form a controlled experimental loop for **learning how to produce future learners** while still preserving explicit evidence and authority boundaries.
