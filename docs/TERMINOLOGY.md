# Terminology

This vocabulary is intentionally substrate-neutral. Biological terms are retained only where they provide concise names for succession relationships.

| Term | Meaning |
|---|---|
| **generation** | One admitted executable configuration in an ordered succession history. |
| **active generation** | The generation currently authorized to provide the governed service or function. |
| **parent** | The generation or candidate identity from which a successor relationship is declared. Parentage is provenance, not authority. |
| **candidate** | An isolated potential successor that has not been promoted. |
| **successor** | A candidate that has satisfied the applicable promotion policy and been admitted as the next generation. |
| **lineage** | The ordered graph of generations, candidates, inheritance, evidence, decisions, and rollback relationships. |
| **succession contract** | Machine-readable declaration of target improvements, protected properties, required evidence, resource bounds, compatibility requirements, and promotion conditions. |
| **inheritance** | Explicit transfer of an artifact, representation, policy, state, evidence-derived strategy, or developmental prior from an earlier generation into a candidate. |
| **inheritance manifest** | Provenance record describing the source, transformation, identity, eligibility, scope, and intended role of inherited material. |
| **developmental program** | Procedure that turns an initial candidate state into a frozen candidate artifact, including training, adaptation, search, compilation, or other bounded transformations. |
| **developmental initialization** | Candidate starting state chosen or generated to make later development more effective. It may include weights but is not restricted to weights. |
| **candidate freeze** | Transition after which the candidate artifact and evaluation envelope are fixed for a specified evaluation phase. |
| **protected property** | Property that must not regress during succession, subject to a declared verifier and evidence standard. |
| **target property** | Property the candidate is intended to improve or newly satisfy. |
| **succession evidence** | Evidence eligible to support or reject a succession-contract claim. |
| **promotion** | Authority-bearing transition that admits a candidate as the active generation. |
| **rejection** | Decision that a candidate cannot be promoted under the current contract/evidence. |
| **unknown** | State in which available evidence is insufficient to establish pass or fail. |
| **rollback point** | Retained prior generation and state required for governed restoration. |
| **retirement** | Transition removing a generation from active service without deleting its lineage record. |
| **proposal authority** | Authority to create candidate or inheritance proposals. |
| **evaluation authority** | Authority to derive a verdict for a bounded claim. |
| **promotion authority** | Authority to change which generation is active. |
| **fitness** | A research shorthand for measured suitability under a declared evaluation envelope; never an implicit universal score. |
| **lineage fitness** | Evidence about a generation's ability to produce useful future successors, distinct from its own task performance. |
| **succession depth** | Number of admitted generational transitions from a declared lineage root. |

## Terms intentionally avoided as normative concepts

### Self-aware / wants / decides

These anthropomorphic descriptions are not needed for the architecture. Machine-native records should describe capabilities, proposals, transitions, and authority directly.

### Better

A candidate is never simply "better." It may satisfy a set of target claims under a specified evaluation envelope while preserving required protected properties.

### Knowledge

Where possible, use more precise terms such as evidence, strategy, parameter state, representation, memory record, hypothesis, or verified experience.

### Evolution

`Evolution` is useful colloquially but can imply population genetics, mutation/selection dynamics, or open-ended evolution that Lineage may not implement. Prefer **generational improvement**, **successor synthesis**, or a specific mechanism.

### Proof

Use `proof` only where an actual proof object and proof system justify the word. Empirical tests, benchmark results, static analyses, and verifier outputs should retain their own evidence classes.
