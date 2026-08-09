# Lean recipes mined from other people's formalisations

Started r107 (2026-08-09). Append-only. Each entry says **where it came from** and **what it
would have saved us**, because a recipe with no cost attached is not worth keeping.

---

## Source: `openai/ten-proofs` (Lean 4.32.0 + Mathlib + Lake)

**What I actually read** (F-discipline: state the sample, not an impression):
`README.md` in full; `ComparatorChallenges/README.md` in full; the first 60 lines of
`MulticolorTriangleRamsey.lean`; lines 2370–2440 of `GapCVP.lean`; and structural greps
(`import`, `open`, top-level `theorem`/`def` names) across all three of
`MulticolorTriangleRamsey.lean`, `SpherePacking.lean`, `GapCVP.lean`.
**I did not read all 5,760 lines.** Everything below is from the sample above.

Their toolchain is Lean **4.32.0**; ours is **4.32.2** with Mathlib pinned to the matching
tag, so the idioms transfer essentially verbatim.

### R1. `import Mathlib` wholesale, then a per-result `namespace`
All three files open with a bare `import Mathlib` and immediately
`namespace ErdosProblems.MulticolourTriangleRamsey` (or similar). We import individual
modules.

**What it would have saved us**: r103. `convexOn_pow` and `strictConvexOn_pow` existed and
had exactly the names I guessed; the build failed only because they live in
`Mathlib.Analysis.Convex.Mul` and `Mathlib.Analysis.Convex.SpecificFunctions.Deriv`, not in
`SpecificFunctions.Basic`. That cost a round trip and a grep through Mathlib's source.
**Recommendation**: `import Mathlib` in `Pnp/Experiments/`, keep targeted imports in
`Pnp/Theory/` where build time matters and the dependency list is documentation.

### R2. A `@[simp]` characterisation theorem beside every `def`
`GapCVP.lean` defines `triple a b c := ![a, b, c]` and immediately proves
`@[simp] theorem clauseSatisfied_triple : clauseSatisfied assignment (triple a b c) ↔ ... ∨ ... ∨ ...`.
Every definition is paired with the `↔` that downstream `simp` needs, so no later proof ever
unfolds the definition by hand.

**Our canon does this unevenly** — `lm_eq_lmClassCount` is exactly this pattern, but several
`def`s in `Landscape.lean` and `Decomposition.lean` have no `@[simp]` characterisation and get
unfolded ad hoc at each use. Cheap to retrofit, and it is the difference between `simp` and
`simp [foo, bar, baz]` at every call site.

### R3. `decide_eq_true_eq` as the Bool↔Prop bridge
Pattern: `simp only [Namespace.somePredicate, decide_eq_true_eq]` to move from a
`Bool`-valued decidable definition into a `Prop` goal (`GapCVP.lean`, `triple_distinct`,
`paddedBinary_allDistinct`).

**Directly ours**: `IsStrictLocalMin` carries a `Decidable` instance precisely so `#eval` can
run it, and we then have to cross the same Bool/Prop line. Worth adopting as the standard
opening move.

### R4. `fin_cases i <;> fin_cases j <;> simp_all [...]`
Small finite index case-splits done in one line rather than by hand
(`GapCVP.lean`, `triple_distinct`). We have several hand-rolled `Fin` case analyses.

### R5. `![a, b, c]` for `Fin n → α`, plus `Fin.exists_fin_succ`
Matrix notation for short tuples, and `Fin.exists_fin_succ` to unfold `∃ i : Fin 3` into a
disjunction. Relevant wherever our strata are indexed by a small `Fin`.

### R6. Reductions as an `Equiv` between a "raw" and a "clean" instance type
`def gapCVPInstanceEquiv : GapCVPInstance ≃ RawGapCVPInstance`, with separate
`encodeGapCVPInstance : GapCVPInstance → List Bool` and a `decode` returning `Option`.
The mathematics is stated on the clean type; the encoding is a separate, boring layer.

**Relevant to paper 4 §6** if the algorithmic outlook is ever formalised: it is the standard
way to keep "what the object is" apart from "how it is written down".

### R7. The analytic idiom
`SpherePacking.lean`: `noncomputable section`, `open Filter MeasureTheory`,
`open scoped Topology`. This is the header our deferred analytic items (the effective pieces,
anything touching `Tendsto`/measure) would need.

---

## Comparator — assessment (r107)

`ComparatorChallenges/README.md`, in full, is short: install `landrun`, `lean4export` and
`nanoda_bin` on `PATH`, run `lake exe cache get`, then
`lake exe comparator ComparatorChallenges/<challenge>.json`. Comparator itself lives at
`github.com/leanprover/comparator`. `nanoda_bin` is an independent Lean 4 type-checker;
`lean4export` dumps the environment; `landrun` sandboxes the run.

**Feasibility for our canon — settled by doing it (r108).** Kentaro lifted the
ask-before-installing rule, so this was executed rather than estimated.

1. **The documented Comparator set cannot run on Windows.** `landrun` is a Linux sandbox
   built on Landlock; there is no Windows equivalent. `nanoda_bin` needs Rust, and this
   machine has no `cargo`/`rustc`. So the harness as published is out.
2. **But the half that matters is already installed.** `leanchecker.exe` ships *inside* the
   elan toolchain (`~/.elan/bin/leanchecker.exe`), and the lean4checker repository's most
   recent commit is a deprecation notice saying exactly that: *"leanchecker is now built into
   Lean"*. Nothing needed installing for the core capability.
3. The external `lean4checker` was built anyway because it takes an explicit module list.
   Its newest tag is `v4.29.0-rc8`, but overwriting `lean-toolchain` with
   `leanprover/lean4:v4.32.2` and running `lake build` succeeds (23 jobs, about a minute).
4. **Result on our canon**: `lake env lean4checker Pnp` → 11 modules, **exit 0 in 47 s**.
   Every constant in the canon has now been replayed through the kernel from the imports up,
   independently of the elaborator that produced it.
5. **Negative control, because a check that cannot fail is not a check (F47)**: their three
   poisoned test modules (`AddFalse`, `ReplaceAxiom`, `AddFalseConstructor`) are all rejected
   with exit 1, and their clean one (`QuotEq`) passes. The harness is doing work.
6. Wrapped as `tools/check_lean.ps1`, which runs the negative control first and refuses to
   report a pass if the control passes too.

**What this buys and what it does not.** It removes trust in the elaborator, the tactic
framework, and anything that could have altered the environment after the fact (`unsafe`,
`implemented_by`, `native_decide`, a swapped axiom). It does **not** remove trust in the
kernel itself — same implementation — which is the one thing `nanoda_bin` would add, at the
cost of a Rust toolchain.

**One correction to the brief, and it matters.** r106 calls Comparator "F52's philosophy as
infrastructure". It is the *orthogonal* axis:

| | question answered |
|---|---|
| Comparator / independent kernel | *is the proof term valid?* — removes trust in the elaborator and the tactic framework |
| F52 (two proofs, unrelated routes) | *does the statement say what I meant?* — removes trust in my own reading of my own theorem |

An independent kernel re-check cannot tell you that `termwise_min_iff` is the minimality
statement rather than something vacuous; only a second, differently-routed proof of the same
sentence (or a `#eval` against an independent implementation) does that. So Comparator
**complements** F52 and does not mechanise it. Both are worth having; conflating them would
leave the more likely failure mode — a true theorem that is not the theorem you wanted —
unguarded.
