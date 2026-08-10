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

## Traps met in our own canon

### T1. `%` inside a real-valued expression is REAL modulo (r111, `OddProd.lean`)
`|Real.sin (π * (2 * j % q) / q)|` with `j q : ℕ` does **not** mean what it looks like. Lean
unifies at `ℝ` and reads `%` as `Real.instMod`, so `Nat.mod_eq_of_lt` and friends never fire and
the errors say only *"did not find an occurrence of the pattern"*. Cast the natural-number
reduction explicitly: `((2 * j % q : ℕ) : ℝ)`. The same trap waits for `/` (integer versus real
division) in any statement that mixes `ℕ` indices with `ℝ` values.

### T2. `rw [← h]` rewrites *every* occurrence, including the one you meant to keep
Deriving `S = c * (S * C)` from `P = S` and `P = c * (S * C)` by `rw [← hleft, hright]` rewrites
the `S` inside `(S * C)` as well and produces a self-referential goal. Compose the equalities
instead: `hleft.symm.trans hright`. Rule of thumb: when the same term appears on both sides of
the goal, use `Eq.trans`/`calc`, not `rw`.

### T3. `set x := e with h` after the fact, not before
`set` abstracts only the occurrences present when it runs; products created later by
`Finset.prod_mul_distrib` are *not* abstracted, and then `rw [h]` goes the wrong way. Prove the
lemmas with the full expressions first and `set` at the end, when everything is in place.

### T3b. The route for `lem:coset`, prepared but NOT attempted (r114)
The general coset identity `∏_{k<v}|cos π(t+k/v)| = 2^{1-v}|cos π(vt+τ_v)|` is now paper 4's §2
and is **not formalised**; `OddProd.lean` covers only `t = 0`, `v` odd. The double-angle
bijection does **not** generalise to `t ≠ 0`: it relates `S(2t)` to `S(t)C(t)`, where `S` is the
sine product, and closing it needs the sine multiplication formula — which is the statement
itself. So roots of unity are unavoidable here. The shortest paper proof, written out so the
next session starts warm:

```
|cos πu| = |1 + e^{2πiu}|/2 ,  w = e^{2πit} ,  ζ = e^{2πi/v}
∏_{k<v}(X - ζ^k) = X^v - 1                      -- Polynomial.X_pow_sub_one_eq_prod
X = -1/w  ⟹  ∏_{k<v}(1 + w ζ^k) = 1 - (-1)^v w^v
v odd  : |1 + w^v| = 2|cos πvt|          v even : |1 - w^v| = 2|sin πvt| = 2|cos π(vt+½)|
```

**r116: the reduction is now checked numerically, so only the prime case is at risk.**
`coset_mult_r116.py` verifies, in product form, that with
`P_v(t) = ∏_{k<v}|2cos π(t+k/v)|` and `τ_v = ½` for `v` even, `0` for `v` odd:

- the identity `P_v(t) = 2|cos π(v t + τ_v)|` holds for `v ≤ 40` (worst `2e-14`), and a
  deliberately wrong `τ ≡ 0` is detected — the check is not blind to the constant;
- **`P_{ab}(t) = ∏_{i<a} P_b(t + i/(ab))`**, the Finset reindexing `k = i + a j`, holds over
  64 pairs `(a,b)` and 10 shifts (worst `7.8e-14`);
- the `τ` bookkeeping closes in all four parity cases: `a τ_b + τ_a ≡ τ_{ab} (mod 1)`.

**So the Lean job splits into three, and only the third needs roots of unity:**
**(1)** `v = 2`, the double-angle formula; **(2)** multiplicativity, a Finset reindexing;
**(3)** `v` an odd prime. Steps 1 and 2 then give every `v` built from the primes of step 3.
Do (1) and (2) first: they are elementary, they are now known to be true, and they turn the
remaining risk into a single classical evaluation.

**Reconnaissance done in r115 — read this before starting, it saves the first hour.**

- `Polynomial.X_pow_sub_one_eq_prod (hpos : 0 < n) (h : IsPrimitiveRoot ζ n) :
  X ^ n - 1 = ∏ ζ ∈ nthRootsFinset n (1 : R), (X - C ζ)` exists, in
  `RingTheory/Polynomial/Cyclotomic/Basic.lean`. **It is indexed by `nthRootsFinset`, not by
  `Finset.range n` with `ζ ^ i`**, so the first real step is a conversion between the two. That
  conversion is not a one-liner in the source I could find.
- `Complex.isPrimitiveRoot_exp` is in `RingTheory/RootsOfUnity/Complex.lean`.
- **Mathlib has no sine/cosine multiplication formula.** Searched
  `Analysis/SpecialFunctions/Trigonometric/*` for products over `Finset`: nothing.
- **The identity is multiplicative in `v`, so only primes are needed.** With
  `P_v(x) = ∏_{k<v}|2 sin π(x+k/v)|` and `v = ab`, splitting `k = i + a j` gives
  `{x + k/v} = ⋃_{i<a}{(x + i/v) + j/b}`, hence `P_v(x) = ∏_{i<a} P_b(x + i/v)`, and if
  `P_b(y) = 2|sin πby|` this is `P_a(bx) = 2|sin πvx|`. The case `v = 2` is the double-angle
  formula. **So an induction that handles odd primes closes everything** — that is the shape to
  aim for, and it may well be cheaper than the root-of-unity route.
- What the paper actually needs is the INEQUALITY `∏_{k<v}|cos π(t+k/v)| ≤ 2^{1-v}`
  (`cor:floor` in multiplicative form). State it that way, **not** as a bound on
  `∑ -log|cos|`: Lean's `Real.log 0 = 0` makes the additive form FALSE at a pole (take `v = 2`,
  `t = 1/2`: the sum reads `0`, the claimed floor is `½log2`). The multiplicative form is true
  there and is the form the minor-arc argument uses anyway.

### T4. `try ring` leaves its suggestion in the log
When `ring` fails inside `try`, the error is swallowed but the *"Try this: ring_nf"* message is
still printed, which looks like a failure in a log that is meant to be clean. Use `try ring_nf`.

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

---

## nanoda — a genuinely independent kernel (r111): built, verified, not yet usable on our canon

**Built.** `nanoda_bin 0.4.13` and `lean4export 3.1.0`, both on this machine. Four things had
to be got right, and each is a trap worth recording:

1. **`nanoda_bin` is not on crates.io.** `cargo install nanoda_bin` fails with *could not find
   `nanoda_bin` in registry*. Build from `github.com/ammkrn/nanoda_lib` instead.
2. **The MSVC linker is absent.** Rust's default Windows toolchain needs `link.exe` from
   Visual Studio Build Tools. Rather than install several GB of Visual Studio,
   `rustup default stable-x86_64-pc-windows-gnu` — the GNU toolchain ships its own linker and
   `nanoda_lib` then builds in 20 s. *(This changed the machine's default Rust toolchain;
   `rustup default stable-msvc` reverses it.)*
3. **`nanoda_bin` has no CLI.** Its single argument is a path to a JSON config,
   `{"export_file_path": "..."}`. Passing the export file directly makes it panic in the JSON
   parser — which looks like a corrupt export and is not.
4. **PowerShell `>` writes UTF-16.** `lake env lean4export Mod > out.export` produces a file
   nanoda rejects with *stream did not contain valid UTF-8*. Redirect through
   `cmd /c "... > out.export"`. Also, running `lean4export.exe` outside `lake env` fails with
   exit `-1073741515` (DLL not found): put `$(lean --print-prefix)\bin` on `PATH`.

**Verified end to end, with a negative control.** On a self-contained `prelude` module
(two inductives, two theorems, no Mathlib): export 9,396 bytes, nanoda **exit 0**. Then the
control — swap the `value` fields of the two theorems in the JSON so each claims the other's
proof term — and nanoda **exit 101**. *Honest caveat:* the rejection came from the parser
(`assertion failed: idx < self.dag.exprs.len()`), not the type checker, because the swapped
index is not yet defined when the first theorem is read. The harness rejects a corrupted
export; it has not yet been shown to reject a well-formed but ill-typed one.

Two earlier passes were **discarded rather than reported**: the first ran nanoda on an empty
export (the tiny module had failed to compile) and got exit 0; the second corrupted a
bookkeeping field (`all`) rather than the proof term and got exit 0. Both were caught only
because the control was written first. This is F47 three times in one afternoon.

**Not run on the canon, and the reason is scale.** `lean4export` exports the whole transitive
environment as text. Core `Init` alone is **671 MB in 66 s**; a `Pnp` export had reached
**692 MB after 90 s** and was still growing. nanoda would then have to type-check all of
Mathlib, not our 12 files.

**The distinction worth keeping:**

| | granularity | cost here |
|---|---|---|
| `lean4checker` | replays the listed modules' constants against an already-loaded environment | 13 modules, 170 s |
| `nanoda` | must be handed the entire environment as text | multi-GB export, all of Mathlib |

So the two are not substitutes: `lean4checker` is the one that fits a working loop, and
`nanoda` is the one that would remove the last trust assumption — if someone first solves the
export-size problem.

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
