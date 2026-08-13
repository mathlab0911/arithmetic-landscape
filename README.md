# Arithmetic Landscape Theory

The **gap series** of a finite set `A` of odd positive integers with largest element `M` is

```
    Γ(A) = 1 + 2 · Σ_{d=1..(M−1)/2} 2^(−N_A(d)) ∈ ℚ ,     N_A(d) = #{a ∈ A : a ≤ 2d} ,
```

equivalently a dyadically weighted sum of the gaps of `A`, dominated by its smallest elements.
It is read off `A` without solving anything, it lies between `3 − 2^(1−(M−1)/2)` and `M` with
both extremes characterised, and — this is the point of the programme — it governs the local
structure of the subset-sum problem for `A`.

Write `r_A(n) = #{S ⊆ A : σ(S) = n}` for the number of representations of `n` as a subset sum.
Give the subsets `S ⊆ A` the energy `E(S) = |σ(S) − n|` for a target `n`, with single-element
flips as moves; then `r_A(n)` counts the ground states. Write `lm_A(n)` for the number of
strict local minima. Then `lm_A(n)/r_A(n) → Γ(A)`, for every target, under a hypothesis that
can be checked rather than assumed.

A recurring theme: **replace the annealed (independence) approximation standard in the
statistical-mechanics treatments by an exact identity plus a finite, checkable hypothesis.**

---

## Papers

Each statement in each paper carries an explicit status at the statement — *proved in Lean*,
*proved*, *derived*, *experimentally confirmed with the range stated*, or *conjecture* — and
`tools/check.py` (C8) fails the build if a theorem, proposition, lemma or corollary declares
none. The table below says the same thing at the level of whole papers, and it is meant to be
read as the least flattering true description of each.

| | Title | State |
|---|---|---|
| I | *Arithmetic landscapes I: the gap series* | **25 pp. Complete**, and its structural part is verified in Lean. Classification of local minima, the window identity `W_D(A) = Γ(A) + (2D+1−M)2^(−k)`, sharp bounds `3 − 2^(1−(M−1)/2) ≤ Γ(A) ≤ M` with both extremal sets characterised, the exact stratification, and the modulus-4 obstruction. **r120 changed the definition of Γ** from the enumeration series `Σ aⱼ2^(−j)` to the layer form `1 + 2Σ_d 2^(−N_A(d))`; the two differ by `a_k2^(−k)` and have the same limit, so every asymptotic statement in Parts II and III is unaffected. The Japanese edition tracks the change. |
| II | *Arithmetic landscapes II: asymptotic flatness of subset-sum landscapes of primes* | **34 pp. No hypothesis, and now written out.** The two steps of the deep-minor-arc proposition that were previously owed to the reader — the substitution of a quoted exponential-sum bound, and the excision near the zeros of the cosine — are written in full as of r121: the quoted estimate is stated with its hypotheses as its own lemma, the three checks the substitution needs are made in order, and the summation by parts in the excision is carried out. **Exactly one statement is quoted from the literature without proof** (Vinogradov–Vaughan), and the argument is written so that no numerical value of its logarithmic exponent is needed. One constant is ineffective via Siegel–Walfisz; the effective substitute is the weaker rate `e^(1/8)·√3/2 = 0.98134…`, which still gives the conclusion. |
| III | *Arithmetic landscapes III: deformed measures, random sequences, and the coset identity* | **36 pp. Draft**, mixed by section, and §8 (*Honest scope*) itemises which is which. **Appendix A writes out region R1 with every constant proved**, so the one open problem the three conditional theorems shared is now a written argument awaiting the second, independent reading this project requires rather than a computation to be done. **The reduced residues are now evaluated exactly** (`prop:redresidue`): the mean of `−log|cos πt|` over `(Z/v)*` is `log 2` for every `v` except the powers of two, where it is `(1 − 2^(1−j))log 2` — which makes the modulus-4 theorem the case `w = 1` and recovers the powers-of-two classification from an exact evaluation instead of a group-theoretic one. It is an evaluation at the rational and becomes a bound on the surrounding arc **exactly at the powers of two** — `rem:shift` proves both directions from the product form of the identity, and exhibits the failure at `v = 12`. That is the same 2-adic boundary a third time. The Bernoulli(q) deformation `Γ^(q)`, the modulus-4 theorem, the minor-arc rate `1/√2` for random odd sequences, and the identity below — that one is proved, twice. |

The manuscript that was paper 3 — *The transfer function of subset-sum landscapes* —
was absorbed into Part III at r130. All thirty-three of its theorem-like statements
moved: twenty-two as content with their statuses, eight as calibration material with
their ranges, two as named open problems, one split. Nothing was dropped, and the
mapping is `lean/pnp/p3map_r121`. The files are in the git history, not in the tree.

The technical spine of Part III:

```
    (1/v) Σ_{k<v} X(t + k/v)  =  (1 − 1/v)·log 2  +  (1/v)·X(v·t + τ_v) ,     X(t) = −log|cos πt| ,
```

exactly, for every `v ≥ 1` and every `t`. **The identity is classical** — it is the Kubert
distribution relation for `log|2 sin πt|`, transported to the cosine by `t ↦ t + ½`, and we
claim no part of it; we prove it twice, by the multiplication formula (which is how the
classical relation is proved) and by Fourier.

What is ours is the use. Because `X ≥ 0`, the rational points are the *minima* of the coset
average and not merely convenient sample points, so the relation becomes a uniform lower bound
and the step of a minor-arc argument that normally costs a quantitative equidistribution
estimate costs nothing. Measured against the classical route: at every rational with small
denominator the Koksma bound is *negative* — the points are not equidistributed there — while
this floor is exact. The two are complementary rather than competing.

---

## How this work is produced

I am one person without an institution, and I work with AI language models as tools, under my
direction. **Each paper now carries this statement itself**, under *Use of AI tools*, rather
than leaving it to a reader who happens to visit the repository — a referee reading the PDF
should not have to come here to learn how it was made. They do the long mechanical work — filling in Lean proofs, running and tabulating
experiments, drafting sections that I then check. The choice of direction, the design decisions
and the responsibility for every claim here are mine.

You will find traces of that in the repository rather than a tidied surface: the Lean canon
files carry Japanese headers naming the session and the round in which each was written, and
the experiment scripts and specifications do the same. They are left as they are.

Saying this plainly matters, because it is the entire reason the apparatus below exists at the
level it does. **Work produced this way cannot be trusted on the author's word; it has to be
checkable, and checkable by someone who does not trust the author.** So every settled theorem
goes into Lean and is replayed through the kernel by an independent checker that must first
reject three deliberately poisoned modules; every number quoted in a paper must exist in a
committed log; every statement must declare its status where it is stated; and nineteen mechanical
checks enforce those rules before each commit. The failure ledger in `tools/` records, in full,
every mistake this process has actually made — including the ones a check was built to catch
only after it had already happened, and the ones where the check itself was the defect.

## The formal development

Everything settled lives in `lean/pnp/Pnp/Theory/` — **15 files, 134 theorems and lemmas**, Lean 4
with Mathlib (`leanprover/lean4:v4.32.2`).

- No declaration depends on `sorryAx`, or on any axiom beyond Lean's standard `propext`,
  `Classical.choice` and `Quot.sound`. The authority for that is the build's own
  `depends on axioms` output, not a grep of the source: a keyword search cannot distinguish a
  `sorry` from the comment saying there is none.
- The canon additionally passes an **independent kernel replay** (`lean4checker`, **17 modules**),
  which discards the elaborator and the tactic framework and rebuilds every constant from the
  imports through the kernel alone. The harness runs three deliberately poisoned modules first
  and refuses to report a pass unless all three are rejected: `tools/check_lean.ps1`.
- **The canon is the import closure of the root module, not the contents of a folder.** A file
  that nothing imports is neither built nor replayed while still sitting in the canon directory
  looking canonical — that happened here, for several rounds, to a file no paper cited. The
  harness now computes the closure and exits non-zero if any `Pnp/Theory` file is outside it.
- Formal validity and statement fidelity are treated as **two different questions**. The kernel
  replay answers the first. For the second, load-bearing statements are proved twice by unrelated
  routes — an independent kernel cannot tell you a theorem is not vacuously true.

Each formal statement is named in the papers at the point it is used, and `tools/check.py`
verifies mechanically that every name the papers cite actually exists here.

---

## Reproducing the numbers

Every number that appears in a paper comes from a script in `lean/pnp/` that writes a log beside
itself — **136 scripts, 211 logs**, all committed. A number with no log is treated as a number
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
| C8 | every theorem, proposition, lemma and corollary declares its status at the statement |
| C9 | every count stated in this README matches the repository |
| C10 | every repository link in the papers is the canonical one, and every paper has one |
| C11 | every named constant is correct at the precision it is printed |
| C12 | every script the papers cite exists, with its log |
| C13 | every number in a Japanese edition occurs in its English source |
| C14 | the retired enumeration form of Γ appears only where paper 1 discusses it |
| C15 | every reference to a sibling paper's numbered result resolves against that paper |
| C16 | every paper discloses the use of AI tools **in the paper itself**, not only here |
| C17 | every term this programme coined is glossed in a terminology table the reader can find |
| C18 | the homepage, in its own repository, carries no retired name, no banned literal, and the same disclosure |
| C19 | every Japanese edition has the same labels, theorem environments and status declarations as its source |

A check that examined nothing **fails**: silence is good news only if the check spoke.

Papers are built with `pdflatex` (`paper/Makefile`). The Lean development builds with `lake build`.

---

## Layout

| Path | Contents |
|---|---|
| `paper/` | The three parts, LaTeX source and built PDFs, with the figures. |
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
