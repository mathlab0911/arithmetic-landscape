# Arithmetic Landscape Theory

The **gap series** of a finite integer sequence `A = (a₁, …, a_k)` is

```
    Γ(A) = Σ_{j=1..k} a_j · 2^(-j) ∈ ℚ ,
```

the generating function of `A` evaluated at `x = 1/2`. It is order-sensitive, it is read off `A`
without solving anything, and — this is the point of the programme — it governs the local
structure of the subset-sum problem for `A`.

Give the subsets `S ⊆ A` the energy `E(S) = |σ(S) − n|` for a target `n`, with single-element
flips as moves. Write `lm_A(n)` for the number of strict local minima and `deg_A(n)` for the
number of ground states. Then `lm_A(n)/deg_A(n) → Γ(A)`, for every target, under a hypothesis
that can be checked rather than assumed.

A recurring theme: **replace the annealed (independence) approximation standard in the
statistical-mechanics treatments by an exact identity plus a finite, checkable hypothesis.**

---

## Papers

| | Title | State |
|---|---|---|
| 1 | *The gap series of an integer sequence: an arithmetic invariant governing subset-sum landscapes* | 20 pp. Complete. Classification of local minima, the window identity `W_D(A) = Γ(A) + (2D+1)2^(−k)`, the exact stratification, and the modulus-4 obstruction. |
| 2 | *Asymptotic flatness of subset-sum landscapes of primes: the sub-peak spectrum and the constant √3/2* | 30 pp. Complete, no hypotheses; one constant is ineffective, via Siegel–Walfisz, and the paper says where. |
| 3 | *The transfer function of subset-sum landscapes* | 14 pp. Complete. The transfer function `Φ`, the tilt, and the `λ²` correction law. |
| 4 | *Bias, randomness, and an exact coarse-graining identity* | 16 pp. In progress. The Bernoulli(q) deformation `Γ^(q)`, the modulus-4 theorem, the minor-arc rate `1/√2` for random odd sequences, and the identity below. |

The technical spine of paper 4, and the one result that reaches outside this programme:

```
    (1/v) Σ_{k<v} X(t + k/v)  =  (1 − 1/v)·log 2  +  (1/v)·X(v·t + τ_v) ,     X(t) = −log|cos πt| ,
```

exactly, for every `v ≥ 1` and every `t`. Averaging the energy over a coset of index `v` returns
the same function at `v` times the frequency, plus a constant — so the rational points are the
*minima* of the coset average, and the step of a minor-arc argument that normally costs a
quantitative equidistribution estimate costs nothing. Proved twice, by the multiplication
formula and by Fourier.

---

## The formal development

Everything settled lives in `lean/pnp/Pnp/Theory/` — **13 files, 120 theorems and lemmas**, Lean 4
with Mathlib (`leanprover/lean4:v4.32.2`).

- No declaration depends on `sorryAx`, or on any axiom beyond Lean's standard `propext`,
  `Classical.choice` and `Quot.sound`. Each file ends with the `#print axioms` calls that say so.
- The canon additionally passes an **independent kernel replay** (`lean4checker`, 14 modules),
  which discards the elaborator and the tactic framework and rebuilds every constant from the
  imports through the kernel alone. The harness runs three deliberately poisoned modules first
  and refuses to report a pass unless all three are rejected: `tools/check_lean.ps1`.
- Formal validity and statement fidelity are treated as **two different questions**. The kernel
  replay answers the first. For the second, load-bearing statements are proved twice by unrelated
  routes — an independent kernel cannot tell you a theorem is not vacuously true.

Each formal statement is named in the papers at the point it is used, and `tools/check.py`
verifies mechanically that every name the papers cite actually exists here.

---

## Reproducing the numbers

Every number that appears in a paper comes from a script in `lean/pnp/` that writes a log beside
itself — **114 scripts, 172 logs**, all committed. A number with no log is treated as a number
that does not exist, and `tools/check.py` enforces it:

```
python3 tools/check.py
```

| check | what it enforces |
|---|---|
| C1 | every experiment script has a stored log next to it |
| C2 | every number quoted in a report is a substring of some log |
| C3 | report bookkeeping |
| C4 | no `\label{}` disappears from a paper unnoticed |
| C5 | naming convention |
| C6 | pending methodology notes are surfaced, not lost |
| C7 | every Lean name the papers cite exists in the canon |

Papers are built with `pdflatex` (`paper/Makefile`). The Lean development builds with `lake build`.

---

## Layout

| Path | Contents |
|---|---|
| `paper/` | The four papers, LaTeX source and built PDFs, with the figures. |
| `lean/pnp/Pnp/Theory/` | The formal development — the canon. |
| `lean/pnp/Pnp/Experiments/` | Throwaway Lean experiments, kept for the record. |
| `lean/pnp/*.py`, `*.log` | Numerical experiments and their logs. |
| `tools/` | `check.py` (pre-commit checks) and `check_lean.ps1` (kernel replay). |
| `references/` | Working notes on the formalisation, including the traps met along the way. |

---

## Author

Kentaro Amauchi — independent researcher, Japan.
[mathlab0911.github.io](https://mathlab0911.github.io/) · amkn.sub03@gmail.com

Code is Apache-2.0 (compatible with Mathlib); the papers are the author's until publication.
See `LICENSE`.
