# Lineage ownership boundary

What “lineage” means in modern MNCS, what `mncs-lineage` owns, and what
it deliberately does not. The Atlas registry settles the top-level
question: capability `successor-lineage` (“successor synthesis,
inheritance, promotion evidence, rollback, and controlled generational
replacement”) is **exclusive** to `mncs-lineage` as canonical
authority, with RAVEL as consumer.

## Lineage is generational succession, not a derivation graph

This repository does not own a general artifact → execution →
evidence derivation graph, and modern MNCS does not need it to. That
ground is covered by canonical infrastructure this repository
consumes:

- compiler artifact identity (semantic/HIR/SSA, backend artifacts,
  cross-backend comparison) comes from the toolchain;
- execution records and PASS/FAIL/UNKNOWN receipts come from Forge;
- evidence freshness assessment comes from the toolchain
  `evidence-manifest` / `evidence-check` commands.

What Lineage uniquely owns is **succession derivation**: generation
graphs with parent links (`G2 → G1 → G0`), candidate freeze records
binding source/manifest/corpus content hashes to one succession
round, inheritance manifests with evidence classification, promotion
dispositions with authority separation, rollback targets, and
evidence-validity reasoning *within* succession (a changed successor
identity invalidates parent evidence and forces re-evaluation).
The `invalidate_evidence_probe` pattern — consume toolchain evidence
commands, never re-implement them — is the template for all
derivation_validity work here.

Chronology, Git history, and timestamps are inputs, never the model:
a Git commit cannot say which execution used which artifact or which
observation supports which pressure. The generation graph and freeze
records say exactly that, for the succession domain, with content
hashes instead of path or timestamp correlation.

## System-by-system boundary

- **Forge** owns execution, admission, resource policy, verification
  state, and execution history. Lineage exposes its verifications
  as a bounded Forge provider (`tools/mncs_lineage_forge_provider.py`,
  `mncs-forge.toml`) and consumes Forge identities; no Lineage
  component holds promotion authority — the evaluator reads frozen
  identities with repair feedback withheld.
- **Store** owns persistence. Lineage keeps no lineage database:
  `artifacts/` is gitignored and deterministically regenerable
  (`build_lineage_artifacts.py --check` proves byte-identical
  replay, now including the cross-backend comparison). Retention of
  succession evidence across machines belongs in Store, not in a
  second lineage store.
- **Commons** owns typed project/evidence relationships. Lineage
  succession contracts (`schemas/succession-contract.schema.json`,
  `language/lineage-core.mncs`) are domain semantics — promotion
  gates, authority independence, rollback — not project-graph
  relationships. The JSON schemas remain as transport/reference;
  MNCS Language is the semantic authority.
- **RAVEL** consumes succession evidence for obligations. The
  candidate freeze record (tested — never verified — contract
  claims with verifier identity) is shaped so an obligation can
  cite it; RAVEL owns the obligation itself.
- **Test** provides the evidence product: sealed experiment corpora
  over the full five-backend envelope, executed through the
  reference toolchain. Native `test` declarations were considered
  and not adopted: the corpus + freeze-record + generation-graph
  chain *is* the succession evidence, and a second harness would
  duplicate it without adding promotion-relevant claims.
- **Debug** owns diagnosis. Lineage anomalies (REJECT/HOLD_UNKNOWN
  dispositions, invalidation assessments) carry evidence paths a
  debugger can consume; lineage performs no diagnosis.
- **Atlas/TUI/agents** consume: generation graphs, freeze records,
  and disposition verdicts are presentation-neutral JSON shaped for
  future navigation (revision → candidate → evidence → disposition
  → promotion), owned by consumers, not implemented here.
- **Git** supplies revision identity as content hashes carried in
  freeze records. Commit ancestry is never the succession model.
- **Compiler/runtime** supply artifact and callable identities.
  Lineage pins them per round (source/manifest/result hashes) and
  re-verifiesagreement across backends; it modifies neither.

## Query model

From freeze records plus the generation graph, bounded questions
are answerable without graph dumps: what produced this candidate,
what evidence bound this contract clause, which generations descend
from this parent, why is this evidence stale (invalidated_by
reasons), which rollback target is retained, which candidates were
rejected or held unknown and why. Traversal is bounded by
generations, not by global history: `check_generation_graph`
enforces single-parent chains, exactly one active generation, and
retained rollback targets.

## What would change this boundary

If Forge grows first-class succession rounds with promotion
authority separation, the builder's round-packaging moves there
and Lineage keeps the semantic core. If Store offers deterministic
regenerable-artifact retention, freeze records reference it instead
of local files. If the toolchain deprecates sealed-profile 0.5
contract clauses, the language sources migrate forward. None of
those conditions holds today; the boundary above is current.
