# Arithmetic Landscape Theory

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21941261.svg)](https://doi.org/10.5281/zenodo.21941261) &nbsp; ORCID [0009-0000-0890-4395](https://orcid.org/0009-0000-0890-4395)

*Archived release `v1.2.0` (2026-08-17). The DOI above resolves to the latest version; each release also gets its own. Manuscripts CC BY 4.0, code Apache-2.0. **Not peer-reviewed** — every statement carries its own status where it is stated.*

**A DOI makes a version permanent; it does not make it true.** `v1.1.1` corrected three false sentences about the Lee–Yang ladder of Part III. `v1.2.0` corrects **four more** — a table wrong from the fourth digit, a displayed formula that does not generate the constant printed beside it, a conjectured dividing line the mechanism never used, and **a refutation of our own that is withdrawn**. Each is corrected at its own statement, none deleted, and all four are itemised in [the `v1.2.0` release notes](https://github.com/mathlab0911/arithmetic-landscapes/releases/tag/v1.2.0). *Three of the four were found by building something new and noticing it contradicted a sentence written elsewhere — not by any of the twenty-two mechanical checks.*

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

That last sentence is worth saying twice, because it is the contribution most likely to be
useful outside this programme. **`Γ` is exactly what the annealed (independence) approximation
predicts** — the classification of local minima forbids `N_A(d)` elements at offset `d`, and the
independence heuristic then gives `1 + 2Σ_d 2^(−N_A(d))` on the nose. So the theorem is not that
we avoided the annealed approximation. It is that

> **the annealed count of metastable states is asymptotically exact for this model,**

under a hypothesis (H) that is *checked* rather than assumed, with an explicit profile in Part III
that violates it. Whether (H) is *necessary* is now a named open problem (`prob:hrate`): computed
exactly, the annealed prediction is approached even where (H) fails, and what changes is the rate
— the fitted exponent drops from about `k^(−3)` to about `k^(−1)`. So the accessible evidence says
(H) governs the rate rather than the truth *for power profiles* — and for families growing faster than any power it does not: for `a_i = 2^i + 1` the ratio `lm/r` stays near 7 while `Γ = k + 2` grows, so `lm/r / Γ` falls from 0.72 to 0.35 over `8 ≤ k ≤ 18`, with the same behaviour for `a_i = 2^i − 1` and with the dynamic programme checked against brute-force enumeration. **Some hypothesis is necessary**; the open problem is now to find the sharp one, and it is recorded as a conjecture because a range is not a limit. **`prop:correction` then explains it rather than fitting it**: the relative error is `Q(0)/σ²` to first order, where `Q(0)` is the quantity Part III
already tabulated for a different purpose. (H) asks `Q(0) = O(1)`; the limit needs only
`Q(0) = o(σ²)`, and for power profiles the ratio is `k^(−3α)`, so every `α > 0` works. At a general target the correction carries a factor `1 − z²` with `z = (n−μ)/σ`, so **the ratio sits below `Γ` inside one standard deviation and above it outside, crossing exactly at `|n − μ| = σ`** — a sign, at a stated place, with no constant to fit, and the cheapest way to falsify the expansion. Tested where the theorem is unconditional — the odd primes — the crossing appears exactly as predicted. Two constants fall out: `Q(0) = 61/3` **exactly** for the odd numbers (so the relative error at the centre is `61/k³`), and `50.4369…` for the odd primes. Since `σ²` is far larger for the primes at the same `k`, **the annealed prediction is more accurate for the primes than for the odd numbers**, by a factor growing like `(log k)²/4`. The first-order term is exactly `He₂(z)`, the same Hermite polynomial family that organises the paper's Edgeworth expansion — but **the natural second-order guess is wrong**, measured and recorded as such: the expansion is not in powers of `σ⁻²` alone, because the local limit theorem's own `O(k⁻¹)` corrections cancel between the two counts and the residue of that cancellation is not a single Hermite polynomial. The primes are the harder case to prove and the easier case to approximate, for the same reason: their elements are bigger. The annealed approximation is in constant use in the statistical mechanics of
disordered systems and is almost never controlled; this is one `NP`-complete ground-state problem
where it is provably right, together with the condition that delimits it.

---

## Papers

Each statement in each paper carries an explicit status at the statement — *proved in Lean*,
*proved*, *derived*, *experimentally confirmed with the range stated*, or *conjecture* — and
`tools/check.py` (C8) fails the build if a theorem, proposition, lemma or corollary declares
none. The table below says the same thing at the level of whole papers, and it is meant to be
read as the least flattering true description of each.

| | Title | State |
|---|---|---|
| I | *Arithmetic landscapes I: the gap series* | **26 pp. Complete**, and its structural part is verified in Lean. Classification of local minima, the window identity `W_D(A) = Γ(A) + (2D+1−M)2^(−k)`, sharp bounds `3 − 2^(1−(M−1)/2) ≤ Γ(A) ≤ M` with both extremal sets characterised, the exact stratification, and the modulus-4 obstruction. **r120 changed the definition of Γ** from the enumeration series `Σ aⱼ2^(−j)` to the layer form `1 + 2Σ_d 2^(−N_A(d))`; the two differ by `a_k2^(−k)` and have the same limit, so every asymptotic statement in Parts II and III is unaffected. The Japanese edition tracks the change. **`prop:schur`: `Γ` is Schur-concave** — Abel summation makes it an ordered weighted average with non-increasing weights, so it sits inside the Hardy–Littlewood–Pólya framework. That is the precise version of "`Γ` is a *bottom* statistic": it rewards equality and punishes spread, where variance is Schur-*convex* and moves the other way. |
| II | *Arithmetic landscapes II: asymptotic flatness of subset-sum landscapes of primes* | **35 pp. No hypothesis, and now written out.** The two steps of the deep-minor-arc proposition that were previously owed to the reader — the substitution of a quoted exponential-sum bound, and the excision near the zeros of the cosine — are written in full as of r121: the quoted estimate is stated with its hypotheses as its own lemma, the three checks the substitution needs are made in order, and the summation by parts in the excision is carried out. **Exactly one statement is quoted from the literature without proof** (Vinogradov–Vaughan), and the argument is written so that no numerical value of its logarithmic exponent is needed. One constant is ineffective via Siegel–Walfisz; the effective substitute is the weaker rate `e^(1/8)·√3/2 = 0.98134…`, which still gives the conclusion. |
| III | *Arithmetic landscapes III: deformed measures, random sequences, and the coset identity* | **54 pp. Draft**, mixed by section, and §8 (*Honest scope*) itemises which is which. **The three headline results — `prop:tiltlclt`, `thm:rigid`, `thm:transfer`, that is two theorems and a proposition — are now unconditional.** Appendix A writes out region R1 with every constant proved, and it has had the independent reading this project requires before an argument counts as proved, delivered in three parts each covering the text as it then stood: the three lemmas in r162, the repairs landed against them in r164, the restated proposition with the `T*` construction and all five explicit constants in r171, each re-derived from scratch. No single reading covered the appendix as a whole, and the appendix says so. The one open problem the three theorems shared is closed, so `prop:tiltlclt` is unconditional and `thm:rigid` and `thm:transfer` are theorems with no conditional clause. **The reduced residues are now evaluated exactly** (`prop:redresidue`): the mean of `−log|cos πt|` over `(Z/v)*` is `log 2` for every `v` except the powers of two, where it is `(1 − 2^(1−j))log 2` — which makes the modulus-4 theorem the case `w = 1` and recovers the powers-of-two classification from an exact evaluation instead of a group-theoretic one. It is an evaluation at the rational and becomes a bound on the surrounding arc **exactly at the powers of two** — `rem:shift` proves both directions from the product form of the identity, and exhibits the failure at `v = 12`. That is the same 2-adic boundary a third time. **And the fourth**: `prop:chardecomp` decomposes the coset energy over `(Z/v)*` into characters, and the trivial component is exactly `log 2` with no error while every other component is `−τ(χ̄)(1−χ(2))L(1,χ)` — a Dirichlet `L`-value. The factor `1 − χ(2)` kills the component whenever 2 lies in the kernel of χ, so it is again the prime 2 deciding what can be seen. One consequence is clean enough to state on its own: **for every prime `p ≡ 1 (mod 8)`, `Σ_a (a/p) log|cos(πa/p)| = 0` exactly.** Another is structural: the main term of the deficiency carries no error at all and every error is a character twist, which is precisely where Part II's one ineffective constant lives. And composed with Dirichlet's class number formula it gives **`Σ_a (a/p) log|cos(πa/p)| = 4 h(p) log ε_p` for `p ≡ 5 (mod 8)`** — a sum of logarithms of cosines that comes out four times a class number times a regulator, verified for all eighteen such primes below 320 with the fundamental unit computed independently from `x² − py² = ±4`. The ingredients are elementary and classical; what is recorded is that this programme's energy function lands there at all. The Bernoulli(q) deformation `Γ^(q)`, the modulus-4 theorem, the minor-arc rate `1/√2` for random odd sequences, and the identity below — that one is proved, twice. |
| — | *Two speeds at the boundary: zeros of sums of conjugate sections of power series* | **11 pp. Standalone note.** Takes one question out of Part III and states it in the standard language of power series, with **no prerequisites from this repository and no citations to the other manuscripts at all** — deliberately, so that a reader need not decide whether to trust the rest before deciding whether the question is interesting. Contains: the reduction (on the symmetry line the object is real-valued, so its zeros are sign changes, and a sign change cannot be cancelled — which is precisely the obstruction that stops Jentzsch's theorem transporting to a *sum* of sections); a closed form and an existence theorem for constant weights, with the zero set exact when one constant vanishes; a two-regime rate law for decaying weights; **what a proof of the decaying case would have to supply, including the attempts that failed**; and one constant left unsettled with the reason it will stay unsettled at computable sizes. Japanese edition in `paper-ja/note1_ja.tex`. |

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
committed log; every statement must declare its status where it is stated; and twenty-two mechanical
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
itself — **193 scripts, 272 logs**, all committed. A number with no log is treated as a number
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
| C20 | no statement rests on measurement alone: prove it, disprove it, or name it as open |
| C21 | no file in the tree has a name that says it holds credentials — and the check announces its own limit, since it cannot see a secret that is innocently named |
| C22 | exactly one artefact **in the whole tree** claims to be the live report, and the direction being written is not more than one round behind the newest round in the tree — C3 checked one directory and passed for seven rounds while five live reports sat in another |

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
