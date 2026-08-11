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

Each statement in each paper carries an explicit status at the statement — *proved in Lean*,
*proved*, *derived*, *experimentally confirmed with the range stated*, or *conjecture* — and
`tools/check.py` (C8) fails the build if a theorem, proposition, lemma or corollary declares
none. The table below says the same thing at the level of whole papers, and it is meant to be
read as the least flattering true description of each.

| | Title | State |
|---|---|---|
| 1 | *The gap series of an integer sequence: an arithmetic invariant governing subset-sum landscapes* | **20 pp. Complete**, and its structural part is verified in Lean. Classification of local minima, the window identity `W_D(A) = Γ(A) + (2D+1)2^(−k)`, the exact stratification, and the modulus-4 obstruction. |
| 2 | *Asymptotic flatness of subset-sum landscapes of primes: the sub-peak spectrum and the constant √3/2* | **31 pp. No hypothesis, but not fully written out.** Two steps of the deep-minor-arc proposition — a substitution of a quoted exponential-sum bound, and an excision — are not written to referee standard, and the main theorem says so in its own statement. One constant is ineffective via Siegel–Walfisz; the effective substitute is the weaker rate `e^(1/8)·√3/2 = 0.98134…`, which still gives the conclusion. |
| 3 | *The transfer function of subset-sum landscapes: rigidity of the gap series off centre* | **14 pp. Its two headline theorems are proof skeletons.** The analytic ingredients are proved; what is missing is the Edgeworth expansion of a classical local-limit computation, and each theorem names that gap in its own statement. The transfer function `Φ` is verified against exact computation on four profiles. |
| 4 | *Bias, randomness, and an exact coarse-graining identity* | **17 pp. Draft**, mixed by section, and §8 (*Honest scope*) itemises which is which. The Bernoulli(q) deformation `Γ^(q)`, the modulus-4 theorem, the minor-arc rate `1/√2` for random odd sequences, and the identity below — that one is proved, twice. |

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

## How this work is produced

I am one person without an institution, and I work with AI language models as tools, under my
direction. They do the long mechanical work — filling in Lean proofs, running and tabulating
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
committed log; every statement must declare its status where it is stated; and twelve mechanical
checks enforce those rules before each commit. The failure ledger in `tools/` records, in full,
every mistake this process has actually made — including the ones a check was built to catch
only after it had already happened, and the ones where the check itself was the defect.

## The formal development

Everything settled lives in `lean/pnp/Pnp/Theory/` — **14 files, 125 theorems and lemmas**, Lean 4
with Mathlib (`leanprover/lean4:v4.32.2`).

- No declaration depends on `sorryAx`, or on any axiom beyond Lean's standard `propext`,
  `Classical.choice` and `Quot.sound`. The authority for that is the build's own
  `depends on axioms` output, not a grep of the source: a keyword search cannot distinguish a
  `sorry` from the comment saying there is none.
- The canon additionally passes an **independent kernel replay** (`lean4checker`, **16 modules**),
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
itself — **116 scripts, 183 logs**, all committed. A number with no log is treated as a number
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

A check that examined nothing **fails**: silence is good news only if the check spoke.

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
