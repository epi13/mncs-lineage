# Inheritance Model

## Principle

Lineage treats inheritance as a **typed transfer of governed machine artifacts**, not as a synonym for copying model weights.

A successor can inherit exactly what the experiment or deployment contract permits. Every inherited item should identify its source, transformation, intended role, and evidence/eligibility boundary.

## Inheritance classes

### 1. Direct parameter inheritance

Useful when parent and candidate parameter spaces are compatible.

```text
W_child[shared] <- W_parent[shared]
W_child[new]    <- initializer(...)
```

This may preserve learned representations while allowing architectural expansion or replacement of selected modules.

### 2. Parameter transformation

A transformation maps an earlier parameter state into a candidate parameter state:

```text
W_child^0 = T(W_parent, A_child, context)
```

`T` may be deterministic or learned. A learned transformer is itself an artifact with identity, provenance, training evidence, and scope.

### 3. Delta inheritance

Rather than synthesizing a full model, a lineage mechanism may produce a bounded update:

```text
W_child^0 = W_base + Delta
```

The delta may be low-rank, sparse, modular, or another explicit representation. The base and delta identities must both be preserved.

### 4. Representation inheritance

A candidate with a different architecture may inherit behavior indirectly through:

- representation matching;
- teacher/student distillation;
- feature-space alignment;
- behavioral traces;
- semantic artifacts;
- generated training examples.

This is inheritance of function or structure without requiring tensor compatibility.

### 5. Developmental inheritance

A parent may provide a procedure intended to make the successor easier to develop:

- generated initialization distribution;
- hypernetwork;
- optimizer schedule;
- curriculum;
- data-selection policy;
- task ordering;
- architecture growth schedule;
- mutation operator set;
- stopping conditions.

This is analogous to inheriting a **development program** rather than an adult state.

### 6. Experience inheritance

MNEL or other evidence systems may provide eligible artifacts such as:

- verified strategies;
- negative memory;
- counterexamples;
- failure signatures;
- causal attributions;
- transfer-supported principles;
- unresolved hypotheses.

These records must preserve their original evidence class. A useful strategy does not become a proved theorem merely because it is inherited.

### 7. Semantic inheritance

Future MNCS Language artifacts may enable inheritance at a semantic level:

- contracts;
- machine intent;
- capability/effect declarations;
- proof or evidence obligations;
- verified IR fragments;
- transformation envelopes;
- dependency/evidence graphs.

This could allow a successor to inherit machine-native behavior and constraints independent of the exact implementation used by the parent.

## Developmental initialization

One specific Lineage research direction is whether a parent or parent-informed generator can create an initialization that places a successor in a useful region of its search space before conventional development begins.

Abstractly:

```text
I_child = F(
    parent_state,
    candidate_architecture,
    eligible_experience,
    target_contract,
    resource_envelope
)
```

Then:

```text
candidate_0 = instantiate(candidate_architecture, I_child)
candidate_f = develop(candidate_0, developmental_program)
```

The important research question is not whether the parent can predict every final parameter exactly. A weaker and more practical hypothesis is:

> Can lineage-conditioned initialization reduce the cost or improve the outcome of producing a valid successor?

## Initialization as a distribution

An initializer may produce a distribution or low-dimensional constraint rather than exact tensors:

```text
I_child ~ P(parameters | module_role, parent_evidence, target_contract)
```

This allows optimization to resolve details while still testing whether inherited priors provide measurable advantage.

## Inheritance manifest

Each inherited item should eventually have a record shaped approximately like:

```json
{
  "artifact_id": "sha256:...",
  "artifact_type": "parameter-delta",
  "source_generation": "sha256:...",
  "source_artifact": "sha256:...",
  "transformation": {
    "kind": "low-rank-projection",
    "transform_id": "sha256:..."
  },
  "intended_role": "initialization",
  "eligibility_evidence": ["sha256:..."],
  "scope": "planner.module.v2",
  "known_limitations": ["not-evaluated-on-hidden-transfer-v1"]
}
```

Exact schemas are future work. The critical property is that inheritance is an inspectable relationship rather than an implicit file copy.

## Contamination and leakage

Inheritance creates a major experimental risk: information from evaluation partitions may leak into later candidates through parent memory, distilled strategies, generated curricula, or artifacts that do not look like training data.

Lineage must therefore track **information eligibility**, not merely file provenance.

A future inheritance record may need visibility labels such as:

```text
development-visible
selection-visible
transfer-hidden
future-final
```

This should align with MNEL's evidence partitioning rather than inventing a contradictory visibility model.

## Inheritance does not imply trust

An inherited artifact may be:

- eligible and trusted for a narrow purpose;
- eligible but empirical;
- diagnostic-only;
- experimental;
- stale;
- quarantined;
- prohibited from promotion-critical use.

The candidate may use an artifact during development even when that artifact is not itself eligible as promotion evidence.

## Measuring inheritance value

Every inheritance experiment should include appropriate controls where practical:

```text
candidate A: random/default initialization
candidate B: direct parent inheritance
candidate C: lineage-generated initialization
candidate D: lineage-generated developmental program
```

Compare at equal or explicitly normalized budgets:

- steps/time/compute to threshold;
- final target performance;
- protected-property regressions;
- hidden-transfer performance;
- calibration;
- resource use;
- reproducibility across seeds;
- downstream ability to produce another successor.

Without controls, a successful successor does not establish that inheritance caused the improvement.
