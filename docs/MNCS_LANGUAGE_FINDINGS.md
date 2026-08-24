# MNCS Language Findings — Lineage Conversion

A record of what converting Lineage into native MNCS Language taught us about
the language, compiler, tooling, and surrounding ecosystem. Each entry is a
concrete engineering fact, not a diary item:

> Requirement -> existing capability -> problem -> change made -> coverage ->
> remaining limitation.

Companion experiments: RAVEL (`RAVEL/mncs/`) and MNEL conversions maintain
their own comparable records.

---

## F1. Declarations could not be interleaved

- **Lineage requirement:** succession modules naturally declare enum and
  record vocabulary between functions.
- **Existing capability:** parser accepted declarations only in strict phases:
  all enums, then all records, then all functions.
- **Problem:** natural modules failed with misleading `MNP006`/`MNP007`
  ("requires at least one function" / "unexpected token after the final
  function").
- **Change:** declaration loop accepts enum/record/function keywords in any
  order; per-construct profile gating unchanged.
  [mncs-language#63](https://github.com/epi13/mncs-language/pull/63).
- **Coverage:** unit tests `declarations_may_be_interleaved_across_kinds`,
  `profile_03_interleaves_enums_and_functions_only`; fixture
  `examples/source/profile05-interleaved-declarations.mncs`.
- **Remaining limitation:** none known.

## F2. `Name {` was ambiguous between record literals and block openers

- **Requirement:** match scrutinees, `if` conditions, and bounded-iteration
  state may be bare names; Profile 0.5 record literals share that prefix.
- **Problem:** any `Name {` in expression position parsed as a record literal,
  mis-parsing control flow starting from a name.
- **Change:** two-token lookahead (`..base` update or `name :` field)
  disambiguates; landed upstream as commit `cc2efea` of mncs-language.
- **Coverage:** unit test `profile_05_disambiguates_record_literals_from_block_openers`;
  fixture `examples/source/profile05-branch-on-names.mncs`.

## F3. Record values were not first-class execution observations

- **Requirement:** typed Lineage artifacts (claim verdicts, freeze envelopes)
  want logical record values as arguments and results.
- **Problem:** the corpus boundary rejected record-typed arguments and
  expected values outright, and the body/SSA/backend agreement checker had no
  Record arm, so every record-returning program "diverged".
- **Change:** record matching added to execution-boundary validation and
  normalization (mncs-language commit `3a52cf5`); structural recursive record
  comparison added to `values_agree` in `mncs-codegen` (commit `bb746d6`).
- **Coverage:** mncs-language `crates/mncs-cli/tests/profile05_records.rs`
  executes record-valued corpora through both reference interpreters and the
  sealed research-bytecode experiment.

## F4. Semantic commands required hand-authored manifests

- **Requirement:** agents must reach canonical semantic artifacts from source
  text without maintaining parallel JSON by hand.
- **Problem:** only `source-study` and the `experiment` suite read `.mncs`;
  validate/canonicalize/graph/evidence-manifest/ir/ssa/obligations/verify/
  execute/compile demanded manifest JSON.
- **Change:** `load_program` accepts `.mncs` via the reference front end for
  every manifest-consuming CLI command (mncs-language commit `bb746d6`). The
  Lineage artifact builder depends on this bridge.

## F5. Module roots cannot begin with the `mncs` keyword

- **Problem:** `mncs` lexes as a keyword; qualified names accept identifiers
  only, so `module mncs.lineage.core.v1;` fails with `MNP030`.
- **Resolution:** Lineage uses `lineage.core.v1` / `lineage.synthetic.g0.v1`,
  consistent with RAVEL's `ravel.core.v1`. Contextual keywords in qualified
  names remain a possible future grammar improvement; deliberately unchanged
  for now because module identity strings are compatibility-sensitive across
  the family.

## F6. No boolean algebra

- **Requirement:** eligibility rules read naturally as conjunctions.
- **Existing capability:** comparisons produce `bool`, `if` consumes it; there
  is no `!`, `&&`, `||`, and no equality on `bool` or enums.
- **Workaround used:** nested ifs and match-derived flags inside
  `synthetic-lineage-g0.mncs`; the verbosity is visible in source rather than
  hidden in host code.
- **Language opportunity:** boolean combinators or `match` on `bool`.

## F7. Source-level arithmetic cannot express total-by-semantics intents

- **Requirement:** derived candidate identity wanted multiplicative mixing of
  dependency tokens.
- **Problem:** source profiles always emit checked arithmetic; with no range
  analysis the obligation engine correctly keeps integer-overflow obligations
  UNKNOWN, so the experiment stalls at UNKNOWN.
- **Resolution:** redesigned identity freshness as structural equality over
  the dependency tuple (`dependencies_unchanged`) - comparison-only, total,
  and more honest than decorative hashing inside the language; authoritative
  SHA-256 content identity stays at the artifact layer.
- **Language opportunity:** expose machine-intent expressions (`add.wrap`,
  `add.saturate`, widening) or constant-range discharge at source level.

## F8. Records do not cross backend realization boundaries - honestly

- **Observation:** record-typed function parameters fail backend realization
  with `CGN301`/`CGN302` instead of being silently miscompiled; records
  forward within single bodies and through both reference interpreters.
- **Consequence:** the executable G0 decision core uses flattened enum/scalar
  signatures; the typed record layer runs on reference paths. Documented,
  not papered over.
- **Backend note:** behavior agrees between research bytecode and portable
  WASM (`bounded_behavior_agrees: true`); nothing here assumes WASM only.

## F9. Claim/evidence binding gates compilation - and works

- **Observation:** every declared contract clause without a bound evidence
  claim holds compilation at UNKNOWN (`contract-evidence-bound` obligation).
  This is exactly the pressure Lineage wants.
- **Resolution:** the deterministic artifact builder binds one `tested`
  evidence claim per clause - produced by the corpus verifier - before
  freezing the candidate manifest; obligations discharge and experiments seal
  PASS. Evidence status stays honest (`tested`, never `verified`).

## F10. Artifact identities bind logical paths

- **Observation:** source-envelope identities include the logical name, so
  absolute paths leak host layout into otherwise reproducible artifacts.
- **Resolution:** the Lineage builder passes paths relative to the language
  checkout root; freeze records reproduce byte-for-byte across runs on the
  same checkout (enforced by the determinism probe).

## F11. Language services handled realistic decision modules well

- **Probes:** diagnostics, symbols, hover, definition, references, and
  obligations against the succession modules (service regression suite
  `crates/service-core/tests/lineage.rs`).
- **Results:** variant references resolve to declarations; authority
  laundering surfaces as `MNE134`; obligations report `unknown` verbatim
  instead of coercing it.
- **Remaining gaps:** no formatting query; cross-module navigation waits for
  imports (F12).

## F12. No cross-module import system yet

- **Requirement:** `synthetic-lineage-g0.mncs` mirrors the vocabulary of
  `lineage-core.mncs`; each source file is a closed world, so the vocabulary
  is duplicated deliberately and marked with a comment.
- **Impact:** semantic identity is per-program; a shared vocabulary module
  would let both artifacts share identities.
- **Status:** accepted duplication for now; top-priority language need
  exposed by Lineage.

## Summary scoreboard

| Area | Finding | Action |
|---|---|---|
| syntax | F1 interleaved declarations | fixed in language (#63) |
| syntax | F2 record-literal ambiguity | fixed in language |
| semantics | F3 record observations | fixed in execution + codegen |
| tooling | F4 `.mncs` input everywhere | fixed in CLI |
| grammar | F5 keyword module roots | worked around, documented |
| expressiveness | F6 boolean algebra | documented language need |
| expressiveness | F7 arithmetic intents at source level | redesigned; language gap recorded |
| backends | F8 record entry boundaries | honest failure confirmed; design adapted |
| evidence | F9 contract-evidence gating | exercised end-to-end |
| reproducibility | F10 path-bound identities | mitigated in builder |
| services | F11 agent-facing queries verified | regression suite added |
| modularity | F12 imports | recorded as top language need |
