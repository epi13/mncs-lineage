# Research Questions

Lineage should progress by testing falsifiable mechanisms rather than assuming that generational recursion will produce open-ended improvement.

## 1. Does successor synthesis outperform in-place adaptation?

For bounded tasks where both are possible:

- compare live adaptation of one generation;
- compare isolated successor development;
- normalize compute and information access;
- measure recovery, rollback, provenance quality, and regression isolation in addition to task score.

**Falsifier:** isolated succession provides no measurable benefit or imposes unacceptable overhead relative to bounded in-place adaptation.

## 2. Can parent-informed initialization improve child development?

Compare:

```text
A: default/random initialization
B: direct parent parameter inheritance
C: transformed parent initialization
D: parent/lineage-generated initialization
E: parent/lineage-generated developmental program
```

Measure:

- steps to threshold;
- total compute/time to threshold;
- final performance;
- hidden transfer;
- calibration;
- protected-property regressions;
- sensitivity across seeds.

**Falsifier:** lineage-informed initialization does not outperform appropriate controls after equalizing budget and information.

## 3. Can a lineage learn better developmental priors?

Test whether generation `n` can use prior succession outcomes to improve how it constructs generation `n+1`.

This is stronger than improving task capability. It tests **lineage fitness**: the ability to produce useful successors.

**Falsifier:** successor-production performance does not improve across controlled generations or only improves on exposed evaluation tasks.

## 4. What is the correct inheritance unit?

Potential units include:

- full parameters;
- modules;
- sparse/low-rank deltas;
- representation mappings;
- architecture graphs;
- curricula;
- optimizers;
- MNEL strategies;
- negative memory;
- semantic MNCS Language artifacts;
- combinations of the above.

The best unit may vary by capability or architecture.

## 5. How should inheritance cross architecture boundaries?

If parent and successor differ structurally, test:

- representation alignment;
- distillation;
- learned parameter mappings;
- function-space inheritance;
- semantic-program inheritance;
- generated developmental priors.

**Key question:** can useful information transfer without requiring parameter-coordinate compatibility?

## 6. How much should the parent know about evaluation?

Parent-generated evaluations are useful but create overfitting pressure.

Study partitions such as:

```text
visible development tests
visible selection tests
hidden transfer tests
future-generation final tests
```

Measure whether proposed successors continue to improve when important evaluation remains inaccessible to the generator.

## 7. Can hidden evaluation remain hidden across generations?

This is harder than ordinary train/test separation because an earlier generation may have seen information that a later candidate inherits indirectly.

Research needs to distinguish:

- direct data leakage;
- memory leakage;
- strategy leakage;
- evaluator adaptation;
- curriculum leakage;
- structural information inferred from repeated promotion decisions.

## 8. Which evidence can transfer across generations?

Some evidence is historical context; some may remain valid if dependencies are unchanged; some must always be re-established.

Potential classes:

```text
structurally reusable
identity-bound
runtime-bound
hardware-bound
data-partition-bound
non-transferable
```

The system should conservatively invalidate rather than infer transferability.

## 9. What counts as a protected property?

Possible protected dimensions include:

- semantic contracts;
- tool/capability authority;
- resource ceilings;
- deterministic behavior;
- verifier compatibility;
- safety properties;
- task capabilities;
- calibration;
- operational latency;
- rollback compatibility.

Hard protected properties should remain separate from optimization targets.

## 10. How should multiple objectives be handled?

A single scalar fitness score may hide unacceptable regressions.

Compare:

- hard gates + Pareto ranking;
- lexicographic objectives;
- constrained optimization;
- explicit trade envelopes;
- scalarized fitness with non-negotiable invariants.

## 11. Can rejected candidates improve later generations?

A lineage should preserve failures.

Study whether explicit inheritance of:

- rejected configurations;
- counterexamples;
- failed initialization patterns;
- budget overruns;
- verifier disagreements;

reduces repeated failure and improves search efficiency.

## 12. Can the succession mechanism itself become a candidate?

Eventually the initializer, curriculum generator, candidate selector, or succession policy may itself be subject to improvement.

This introduces a higher-order question:

> How can Lineage improve the mechanism that produces successors without allowing the mechanism to redefine its own promotion standard?

The evaluation/promotion boundary must remain independently anchored.

## 13. How should lineage depth be measured?

A demonstration of `G0 -> G1` is not recursive improvement.

Useful measures may include:

- number of independently admitted generations;
- improvement slope across generations;
- stability of protected properties;
- transfer to held-out task families;
- development efficiency trend;
- lineage-fitness trend;
- rate of rejected candidates;
- evaluator drift;
- inherited information growth.

## 14. What is the smallest credible experiment?

The initial experiment should not require a large language model.

Candidate systems:

- small MLP on synthetic tasks;
- tiny transformer;
- tabular classifier/regressor;
- transition predictor compatible with MNEL study artifacts;
- symbolic or program-synthesis task;
- small policy model in a deterministic environment.

A small system makes full lineage, controls, hidden partitions, and repeated generations affordable enough to study causality.

## 15. When should Lineage *not* be used?

The project should identify domains where:

- live adaptation is safer/simpler;
- successor state transfer is too expensive;
- evaluation cannot distinguish improvement reliably;
- rollback is impossible;
- hidden transfer cannot be protected;
- generational overhead exceeds benefit.

A useful standard includes conditions under which its own mechanism should be rejected.
