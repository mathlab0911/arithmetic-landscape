# Arithmetic Landscape Theory

Research repository for **"The gap series of an integer sequence: an arithmetic
invariant governing subset-sum landscapes"** (in preparation, arXiv math.NT).

For a finite sequence `A = (a_1, ..., a_k)` of positive integers, the **gap series**

```
Γ(A) = Σ_{j=1..k} a_j / 2^j
```

is an order-sensitive invariant that governs the local structure of the subset-sum
landscape of `A`. This repository contains the formal development, the paper draft,
and the numerical experiments.

**Status:** private while the paper is unpublished. All theorems are formally verified.

## Layout

| Path | Contents |
|---|---|
| `lean/pnp/Pnp/Theory/` | The formal development (7 files, 51 theorems) |
| `lean/pnp/*.lean` | Executables used for the exhaustive experiments |
| `lean/pnp/*.py` | Analysis scripts (correlations, flatness sweep, decay rates) |
| `lean/pnp/*.csv`, `*.log` | Experimental output — **the source of every number in the paper** |
| `paper1_draft.md` | Paper draft v1 (English body, Japanese notes to be removed before submission) |
| `paper1_outline.md` | Structural plan and editorial decisions |
| `ALT_report_2026-08-07_opus5.md` | Progress report (Japanese) |

## The formal development

Lean 4 (`leanprover/lean4:v4.32.2`) with Mathlib pinned to the matching tag.

```
cd lean/pnp
lake exe cache get     # first time only — do NOT skip, a full build takes hours
lake build
```

Every declaration is checked with `#print axioms`; none depends on `sorryAx`, and
none uses an axiom beyond `propext`, `Classical.choice` and `Quot.sound`.

| File | Content |
|---|---|
| `Theory/Landscape.lean` | Definitions; **classification theorem**; `lm` as an arithmetic count; `gapSeries` |
| `Theory/Symmetry.lean` | Reflection symmetry of `gs` and `lm`; no flat edges (parity); strict = weak for odd sequences |
| `Theory/Bridge.lean` | List ↔ `Finset (Fin k)` bridge; **window identity** `W_D = Γ + (2D+1)/2^k` |
| `Theory/Decomposition.lean` | **Exact stratification** of `lm` (no approximation) |
| `Theory/Fiber.lean` | Strata are representation counts of truncated subsequences |
| `Theory/Sandwich.lean` | Flatness ⟹ two-sided bounds on `lm/deg` |
| `Theory/Total.lean` | `d`-indexed stratification; **main theorem** `sandwich_total` |

The main theorem: if the representation counts of the truncated subsequences are
flat to within `1 + ε` on an explicit window, then

```
W_D(A) / (1+ε)  ≤  lm_A(n) / deg_A(n)  ≤  (1+ε) · W_D(A),      W_D(A) = Γ(A) + (2D+1)/2^k.
```

No independence (annealed) approximation is used anywhere.

## Reproducing the experiments

```
cd lean/pnp
lake build seeds
./.lake/build/bin/seeds.exe 100     # 100-seed sweep, ~11.5 s → results_landscape_r2.csv
python analyze_r2.py                # correlations, absolute formula, z-scores
python analyze_r2b.py               # Q = (lm/deg)/Γ convergence
python analyze_r3_cv.py             # comparison against the coefficient of variation
python flatness_sweep_r6.py         # exact flatness ε_d(k) for k = 8..24
python ripple_rate_r6.py            # decay rates vs the predicted √3/2
```

Each script writes a `.log` next to itself. The paper quotes those logs verbatim.
