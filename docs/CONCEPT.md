# Concept

## Research hypothesis

MNCS Lineage investigates whether recursive machine improvement can be made more tractable by replacing **in-place self-modification** with **evidence-governed successor synthesis**.

A generation remains stable while one or more successor candidates are produced in isolated state. Candidates may inherit selected artifacts, undergo bounded development, and compete against frozen requirements. Promotion is a separate authority-bearing operation performed only after required evidence has been collected.

The hypothesis is intentionally broader than neural-network weight inheritance. The unit of succession may eventually be a model, agent runtime, model-plus-harness configuration, machine-native semantic program, adaptive subsystem, or another executable artifact.

## The problem Lineage is trying to avoid

A live self-modifying system combines several difficult operations:

1. preserve active state;
2. alter the mechanism carrying that state;
3. evaluate the alteration;
4. decide whether the alteration is valid;
5. recover if the alteration is harmful;
6. continue providing service throughout the change.

That arrangement entangles proposal, execution, evaluation, and authority.

Lineage separates them.

```text
trusted active generation P
          |
          | proposes
          v
isolated candidate state C
          |
          | develops
          v
frozen candidate artifact C'
          |
          | evaluated by bounded external mechanisms
          v
succession evidence E
          |
          | interpreted under promotion policy G
          v
promote / reject / unknown
```

The active parent can participate heavily in producing `C`, but it does not gain the right to declare `E` sufficient merely because it created the candidate.

## The enduring object

Lineage treats the **generational record** as more fundamental than any one running model.

A lineage may contain:

- generation identities;
- parent/candidate relationships;
- succession contracts;
- inherited artifact manifests;
- transformation provenance;
- development manifests;
- frozen evaluation envelopes;
- verifier outputs;
- promotion and rejection records;
- rollback points;
- negative evidence and counterexamples;
- MNEL-derived eligible experience;
- known uncertainty and unresolved claims.

A future generation should be able to determine not only *what it inherited*, but *why the inherited artifact was eligible* and *which claims remain unsupported*.

## Recursive successor synthesis

The central research loop is:

```text
Generation N
   |
   +--> inspect eligible evidence
   +--> characterize limitations
   +--> specify successor goals
   +--> propose inheritance/development program
   |
   v
Candidate population N+1
   |
   +--> develop
   +--> verify
   +--> compare
   +--> challenge with hidden transfer tests
   |
   v
promotion policy
   |
   +--> reject
   +--> unknown / collect more evidence
   +--> promote
   |
   v
Generation N+1
```

If the promoted successor later becomes capable of producing better successor specifications, the process can recurse. That does **not** by itself establish recursive self-improvement. Durable improvement must be measured across generations under controls designed to detect benchmark overfitting, evaluator gaming, inherited contamination, and regressions.

## Machine-native interpretation

The biological vocabulary is conceptual shorthand. The implementation should favor machine-readable identities and state transitions over simulated human roles.

A candidate is not a "child" because an agent says so. It is a content-addressed artifact whose record establishes a parent identity and a succession relationship.

An inheritance is not "knowledge passed down" in prose. It is an explicit manifest binding source artifacts, transformations, eligibility evidence, scope, and intended use.

A promotion is not "the parent steps aside." It is an authority-governed state transition from one active identity to another, with rollback state retained.

## Generalized successor state

A useful abstract model is:

```text
G_n = {
    executable_state,
    architecture,
    machine_semantics,
    capabilities,
    memory,
    learned_parameters,
    developmental_policy,
    verification_requirements,
    evidence,
    runtime_envelope
}
```

A successor generator need not modify every component. Some may be inherited unchanged, some transformed, some regenerated, and some deliberately omitted.

This permits experiments ranging from trivial parameter inheritance to architectural mutation or machine-native semantic regeneration while preserving one succession framework.

## Authority separation

Lineage should distinguish at least these authorities:

- **proposal authority** — may propose candidate artifacts or inheritance;
- **development authority** — may execute bounded training/adaptation;
- **observation authority** — may record measurements;
- **evaluation authority** — may derive verdicts for specific claims;
- **promotion authority** — may change the active generation;
- **rollback authority** — may restore an earlier active generation.

One component may hold multiple authorities in a research sandbox, but the artifact model must represent them separately so later deployments can enforce stronger partitions.

## Success criteria for the research program

Lineage becomes interesting if experiments show that a successor-producing system can, under controlled conditions:

1. preserve protected capabilities while improving declared targets;
2. use inherited experience to reduce development cost or improve final performance;
3. generate initializations or developmental programs that outperform appropriate controls;
4. transfer improvements to hidden tasks rather than only parent-visible benchmarks;
5. retain usable provenance across generations;
6. reject harmful or unsupported successors reliably;
7. improve the *ability to produce future successors*, not merely one task score.

Failure to demonstrate these properties is a useful result. Lineage should be designed so the central hypothesis can be disproven rather than protected by increasingly flexible evaluation.
