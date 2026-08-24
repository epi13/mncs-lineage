# MNCS Language Implementation

Lineage is now an active **MNCS Language proving ground**. The succession
semantics described in [SUCCESSION_MODEL.md](SUCCESSION_MODEL.md) and
[MACHINE_NATIVE_ARTIFACTS.md](MACHINE_NATIVE_ARTIFACTS.md) have a typed,
executable, testable realization in MNCS Language source, validated and
executed through the reference toolchain.

## What is executable today

| Artifact | Status |
|---|---|
| `language/lineage-core.mncs` | executable vocabulary: `Verdict`, structured `UnknownReason`, `ClaimVerdict` well-formedness, evidence freshness reclassification, authority independence |
| `language/synthetic-lineage-g0.mncs` | deterministic G0 -> G1 succession experiment: identity freshness over the dependency tuple, fail-closed candidate disposition, branching selection policy, authority gates |
| `examples/execution/synthetic-lineage-g0-corpus.json` | 24 sealed corpus cases covering the full topology (C1 REJECT / C2 UNKNOWN / C3 PROMOTE), evidence invalidation, authority violations, rollback gates |
| `tools/build_lineage_artifacts.py` | deterministic builder: compile -> bind contract evidence -> freeze manifest -> run experiments on both backends -> cross-backend comparison -> freeze record + G0->G1->G2 generation graph |
| `tools/invalidate_evidence_probe.py` | proves a changed successor artifact invalidates parent evidence and requires re-evaluation |
| `tools/mncs_lineage_forge_provider.py` + `mncs-forge.toml` | Forge Provider Protocol 0.1 adapter exposing lineage verifications as bounded workflows |
| `tests/` | pytest suite running everything against the real toolchain |

The legacy JSON schema remains available as transport/reference
(`schemas/`, `examples/succession-contract.example.json`); MNCS Language is
now the semantic authority. See "JSON compatibility" below.

## Quick start

Prerequisites: a checkout of `mncs-language` next to this repository (or
`MNCS_LANGUAGE_DIR`), plus `MNCS_BIN` pointing at a built `mncs` binary if you
do not want the tools to invoke `cargo run` themselves.

```bash
# validate both succession modules through the reference front end
cargo run -p mncs-cli --manifest-path ../mncs-language/Cargo.toml -- \
    validate language/synthetic-lineage-g0.mncs

# build frozen artifacts, run sealed experiments on research bytecode and
# portable WASM, reconstruct the G0->G1->G2 generation graph
python3 tools/build_lineage_artifacts.py            # add --check to also verify replay determinism

# prove stale evidence cannot certify a changed successor
python3 tools/invalidate_evidence_probe.py

# full pytest coverage
python3 -m pytest tests/
```

Outputs land under `artifacts/lineage/`:

- `synthetic-lineage-g0/synthetic-lineage-g0.manifest.json` - frozen semantic
  manifest with corpus-tested evidence claims bound to every succession
  contract clause;
- `synthetic-lineage-g0/experiment-*/result.json` - sealed per-backend
  experiment results (status PASS);
- `synthetic-lineage-g0/cross-backend-comparison.json` - same semantics/HIR/
  SSA, agreeing bounded behavior across backends;
- `synthetic-lineage-g0/candidate-freeze-record.json` - content hashes of
  source, manifest, corpus, plus result identities;
- `synthetic-lineage-g0/generation-graph.json` - reconstructed three-generation
  lineage with parent links, rollback targets, retained rejected/unknown
  candidates;
- `invalidation-probe/evidence-assessment.json` - per-record staleness report
  for the changed successor artifact.

## How the central principle is represented

> Proposal authority is not promotion authority.

Three reinforcing layers, none documentation-only:

1. **Static:** `language/negative/g0-proposer-self-certification.mncs` calls
   an evaluation-authority function from a proposal-authority function; the
   compiler rejects it with `MNE134`. The fixture is protected in
   `mncs-forge.toml`.
2. **Decision-level:** `promotion_authority_independent` blocks succession
   whenever the promoting principal proposed or certified the candidate;
   corpus case `self-certification-admits-nobody` seals it.
3. **Operational:** Forge's evaluator authority reads frozen identities only,
   with repair feedback withheld; no Lineage component holds promotion
   authority.

## Evidence lifecycle

Contracts are declared on decision functions (`ensures
protected_regression_blocks_promotion`, ...). Unbound contracts hold
compilation at UNKNOWN by design. The builder binds one `tested` claim per
clause from the deterministic corpus verifier, obligations discharge, and the
experiment seals PASS. When an identity-bearing dependency changes, the
invalidation probe shows the parent's dependency-fingerprinted evidence going
stale (`evidence-check`) and inherited expectations failing against the
changed artifact - so promotion evidence must be re-established under the
successor's own identity.

## JSON compatibility

The original JSON contract remains useful for transport and external
inspection. Round-trip behavior is preserved where it matters:
source text -> canonical semantic form (fingerprinted) -> frozen manifest ->
freeze record; every hop keeps authority, evidence, identity, inheritance,
and provenance explicit. The builder demonstrates the pipeline deterministically.

## Relationship to the family

- **mncs-language** - hosts the language fixes this work demanded (see
  [MNCS_LANGUAGE_FINDINGS.md](MNCS_LANGUAGE_FINDINGS.md)).
- **mncs-language-service** - regression suite exercising agent-facing queries
  on these modules.
- **Forge** - runs lineage verifications as provider workflows; development
  evidence only, never promotion authority.
- **MNEL / RAVEL** - unchanged boundaries: lifetime learning vs generational
  succession; proposers never gain promotion authority. An MNEL-style
  artifact may enter an inheritance manifest only as classified provenance.
- **Fabric / Harness** - the corpus-driven experiment format already matches
  the language's Fabric packaging boundary (`experiment execute`); no
  distributed execution is built yet, by design.
