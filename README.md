# MNCS Lineage

**Recursive successor synthesis for machine-native AI systems.**

MNCS Lineage is an experimental research project exploring **generational machine intelligence** within the Machine-Native Complexity Standard (MNCS) ecosystem.

The central hypothesis is that recursive improvement does not require a continuously operating intelligence to rewrite itself in place. A running generation can instead produce isolated successor candidates, transfer selected inheritance, develop those candidates under bounded conditions, and promote a successor only when independently governed evidence satisfies an explicit succession contract.

```text
active generation
      |
      v
observe verified experience and limitations
      |
      v
successor specification
      |
      +--> architecture / representation
      +--> inheritance package
      +--> developmental initialization
      +--> training / adaptation curriculum
      +--> required claims and protected properties
      |
      v
isolated candidate generation
      |
      v
development + bounded experiments
      |
      v
independent verification / evaluation
      |
      +---- insufficient evidence ----> reject / retain as evidence
      |
      v
promotion gate
      |
      v
new active generation
```

The enduring object is therefore not necessarily one model instance. It is the **lineage**: the succession contracts, candidate identities, inheritance records, evidence, promotion decisions, rollback points, and accumulated verified experience that connect generations.

> **Project status:** active MNCS Language implementation + research program. The succession core is now written in MNCS Language, executes deterministically through the reference toolchain on two backend realizations, and its requirements are driving fixes in the language, compiler, CLI, and language services. No autonomous model replacement, recursive self-improvement, weight generation, training runtime, or promotion authority exists. See [docs/LANGUAGE_IMPLEMENTATION.md](docs/LANGUAGE_IMPLEMENTATION.md) for what runs today and [docs/MNCS_LANGUAGE_FINDINGS.md](docs/MNCS_LANGUAGE_FINDINGS.md) for what the conversion taught us about the language.

## Why this project exists

"Self-evolving AI" is often described as live self-modification: a running model or agent changes its own implementation while remaining responsible for ongoing work. That combines improvement with one of the hardest systems problems available: modifying the mechanism that is currently carrying the state and authority needed to judge the modification.

Lineage explores a different arrangement:

> **Do not require the active generation to become its own replacement in place. Require it to produce a successor candidate whose right to inherit control can be evaluated independently.**

This turns recursive improvement into a succession problem rather than a live-patching problem.

## Machine-native premise

Lineage is not intended to reproduce a human software-development organization with anthropomorphic agent labels. Parent, child, inheritance, and generation are convenient research terms. The implementation direction is machine-native:

- content-addressed candidate and artifact identities;
- typed, machine-readable succession contracts;
- explicit authority and capability boundaries;
- evidence attached to claims rather than prose confidence;
- deterministic state transitions where possible;
- append-only provenance for inheritance and promotion;
- isolated candidate states rather than mutation of the trusted baseline;
- bounded resource, mutation, evaluation, and promotion envelopes;
- representation-independent semantics so inheritance need not mean copying neural weights;
- explicit `PASS`, `FAIL`, and `UNKNOWN` outcomes instead of forcing binary confidence;
- rollback as a first-class succession property.

The parent generation may **propose** a successor, developmental program, initialization, or inheritance package. Proposal authority is not promotion authority.

## Core proposition

A candidate successor should not become active because its predecessor believes it is better.

It should become active only when a separately governed promotion policy can establish enough evidence for the candidate's declared succession contract.

Conceptually:

```text
successor S of parent P

requires
    identity_bound(S)
    provenance_complete(S)
    protected_properties_preserved(S, P)
    required_capabilities_satisfied(S)
    critical_regressions(S) == 0
    evidence_current(S)
    promotion_authority_independent_of_proposal(S)
    rollback_available(P)

permits
    promote(S)
```

This is illustrative semantic notation, not current MNCS Language syntax.

## What may be inherited

Lineage deliberately does **not** define inheritance as "copy the parent's weights." A successor may inherit any governed machine artifact whose semantics and provenance are understood, including:

- complete or partial parameter tensors;
- transformed parameter tensors;
- low-rank or sparse parameter deltas;
- architecture or topology descriptions;
- learned representations or feature spaces;
- optimizer state where justified;
- initialization generators or hypernetworks;
- training curricula and data-selection policies;
- verified strategies distilled from experience;
- negative memory and known counterexamples;
- tool/capability contracts;
- semantic artifacts produced by the MNCS Language;
- verifier requirements and protected-property sets;
- no model parameters at all.

A future system may therefore inherit a **developmental program** rather than an adult model state.

## Relationship to MNEL

Machine-Native Experimental Learning (MNEL) and Lineage address different time scales.

- **MNEL** investigates bounded learning during the lifetime of a generation: hypotheses, interventions, observations, causal attribution, negative memory, and verified-experience distillation.
- **Lineage** investigates how eligible accumulated experience can influence the construction and admission of a later generation.

The intended relationship is:

```text
MNEL verified experience
        |
        v
eligible inheritance proposals
        |
        v
Lineage successor synthesis
        |
        v
candidate development
        |
        v
independent evidence and promotion gate
        |
        v
next generation
        |
        v
MNEL continues experimentation
```

MNEL observations are not automatically inheritance, and inheritance is not automatically promotion evidence. Each transition requires an explicit authority boundary.

See [MNEL integration](docs/MNEL_INTEGRATION.md).

## Relationship to the MNCS project family

Lineage is intended to compose with, not duplicate, sibling responsibilities:

| Project | Potential Lineage relationship |
|---|---|
| **MNCS Language** | Express machine-native succession contracts, protected properties, inheritance semantics, obligations, and evidence-bound transformations. |
| **MNEL** | Produce governed experimental experience that may become candidate inheritance input. |
| **MNCS Forge** | Supply bounded probes, verifiers, witnesses, regression checks, and evidence over candidate claims. |
| **MNCS Fabric** | Execute distributed candidate-development and evaluation work under explicit manifests and budgets. |
| **MNCS Harness** | Route bounded roles/capabilities without exposing every tool to every participant. |
| **RAVEL** | Supply adaptive mechanisms and candidate-generation strategies without acquiring promotion authority by implication. |
| **MNCDS** | Preserve deterministic structural records, evidence eligibility, feedback boundaries, and lineage/provenance artifacts where applicable. |
| **MNCS** | Define and evaluate bounded claims and conformance relationships; Lineage does not certify itself. |

Exact interfaces are future work and should remain explicit rather than implemented as hidden coupling.

## Repository map

```text
language/
  lineage-core.mncs           Executable succession vocabulary: verdicts,
                              structured UNKNOWN reasons, evidence freshness,
                              authority independence
  synthetic-lineage-g0.mncs   Deterministic G0 -> G1 succession experiment:
                              identity freshness, fail-closed dispositions,
                              branching selection policy
  negative/                   Modules that MUST be rejected (authority gates)
  variants/                   Deliberate policy-change successor used by the
                              evidence-invalidation probe
examples/execution/
  synthetic-lineage-g0-corpus.json  Sealed 24-case deterministic corpus
tools/
  build_lineage_artifacts.py  Deterministic freeze/experiment/graph builder
  invalidate_evidence_probe.py Evidence invalidation demonstration
  mncs_lineage_forge_provider.py Forge Provider Protocol 0.1 adapter
mncs-forge.toml               Forge workflows and evaluator boundaries
tests/                        pytest suite over the real toolchain
artifacts/                    Generated frozen records (not committed)
docs/
  CONCEPT.md                  Research hypothesis and system boundaries
  TERMINOLOGY.md              Stable vocabulary for generational artifacts
  SUCCESSION_MODEL.md         Candidate lifecycle, authority, promotion, rollback
  INHERITANCE_MODEL.md        Weight and non-weight inheritance model
  MACHINE_NATIVE_ARTIFACTS.md Machine-readable artifact direction
  MNEL_INTEGRATION.md         Lifetime-learning / generational-learning boundary
  RESEARCH_QUESTIONS.md       Open questions and falsifiable hypotheses
  ROADMAP.md                  Staged research path (Stage 8 pulled forward)
  LANGUAGE_IMPLEMENTATION.md  What is executable and how to run it
  MNCS_LANGUAGE_FINDINGS.md   Language/compiler/services discoveries record
schemas/
  succession-contract.schema.json
examples/
  succession-contract.example.json
```

## Running the synthetic lineage experiment

With `mncs-language` checked out next to this repository:

```bash
# build frozen artifacts, run sealed experiments on both reference backends,
# reconstruct the G0 -> G1 -> G2 generation graph
python3 tools/build_lineage_artifacts.py --check   # --check also re-verifies replay determinism

# demonstrate that changed dependencies invalidate evidence
python3 tools/invalidate_evidence_probe.py

# full test suite
python3 -m pytest tests/
```

Details, outputs, and the evidence lifecycle are described in
[LANGUAGE_IMPLEMENTATION.md](docs/LANGUAGE_IMPLEMENTATION.md).

## Design principles

1. **Succession over live self-patching.** Improvement is first explored through isolated successor candidates.
2. **Semantics before substrate.** Lineage must not assume transformers, gradient descent, or even neural models are permanent requirements.
3. **Proposal is not authority.** A generator cannot certify its own candidate merely by producing a favorable evaluation.
4. **Evidence is attached to claims.** Model confidence is not promotion evidence.
5. **Inheritance is explicit.** Every inherited artifact identifies source, transformation, intended role, and eligibility.
6. **Unknown stays unknown.** Missing or stale evidence cannot be silently converted into success.
7. **Promotion is a state transition.** Candidate generation, evaluation, admission, activation, retirement, and rollback are distinct operations.
8. **Protected properties survive generations.** Improvement claims must be evaluated alongside non-regression obligations.
9. **Machine-native does not mean opaque.** Canonical forms should remain auditable without depending on an LLM interpretation layer.
10. **Lineage is durable.** Rejected candidates, negative evidence, counterexamples, and previous generations remain part of the research record.
11. **Learning and heredity remain separable.** MNEL-style lifetime adaptation and Lineage-style generational inheritance may inform one another without collapsing their authority boundaries.
12. **Recursive improvement is a claim, not an assumption.** The project should be capable of falsifying the hypothesis that a proposed succession mechanism produces durable improvement.

## Non-goals at this stage

This repository does not currently attempt to:

- run an unattended self-improving system;
- let a model edit or replace its own live process;
- grant a parent model promotion authority;
- claim general recursive self-improvement;
- claim that generated weight initialization will outperform conventional initialization;
- define a final MNCS Language syntax;
- train foundation models;
- implement a production model-serving control plane;
- infer safety from benchmark improvement alone.

## Research direction

The first useful experiments should be intentionally small. A tiny model or machine learner can act as a generation, produce one or more successor initialization/development proposals, and be evaluated under frozen tasks and hidden transfer tests. The purpose is not to demonstrate artificial general intelligence. It is to determine whether the **succession abstraction itself** produces measurable, reproducible value without corrupting evidence boundaries.

See [Research questions](docs/RESEARCH_QUESTIONS.md) and [Roadmap](docs/ROADMAP.md).

## License

No license has been selected in this seed PR. Add one deliberately before treating the repository as reusable outside its current research context.
