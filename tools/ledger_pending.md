# Pending failure-ledger entries

Entries written mid-round, not yet folded into the `pnp-research` skill (§7).
`tools/check.py` (C6) prints this file on every run. Clear it at the next skill save.

Full text of entries already folded in lives in `tools/ledger_archive.md`.

---

(empty: emptied at the skill save in r131, which folded fourteen blocks covering r119–r131
into F18, F39, F47, F52, F60, F61, F62 and the three new entries F63, F64, F65)

---

## r132 (fable-5) — the verifier is not exempt from the cache (append to F61)

```
  claimed   : (draft r132) the README on main still writes deg_A(n); C18 passes over it
  actual    : fixed at a544f9b; the fetch of raw/main served the previous render from an
              edge cache.  The verifier's own evidence was one cache window old
  check     : verify at the immutable revision (raw/<sha>/…), never at the mutable path,
              whenever the claim is about the current state; keep the mutable-path fetch
              only as evidence about what SOME readers may still be seeing
  rule      : a mutable path inside its cache window can show any recent state, including
              one that resurrects fixed defects — and the verifier is not exempt.  Pin
              the revision first, then discuss the caches
```

This is the second half of the entry whose first half was written the round before, and the
symmetry is the point. At r130 the *author* was misled by a stale surface into thinking a
published page was clean when a reader saw otherwise. At r132 the *verifier* was misled by a
stale surface into nearly filing a defect that had already been fixed. Same mechanism, both
directions, one day apart.

> **Pin the revision, then discuss the caches.** The immutable path answers "is the published
> state correct?"; the mutable path answers "is that what a reader sees right now?". They are
> different questions and the second one has a time in its answer.

Recorded also because the draft report existed: a verifier who retracts before publishing has
still done the work of retracting, and the retraction is more informative than the finding
would have been. The post-TTL sweep (`lean/pnp/surfacesweep_r132.log`) is the other half of
the repair — all three surfaces caught up about twenty-two hours after the push.

## r132 — a tool that cries wolf on its own output (append to F58)

`python3 -W always tools/check.py` printed **230 ResourceWarnings** — twenty sites doing
`open(...).read()` without closing. Harmless: CPython closes them on collection, and the
checker has never misbehaved because of it.

That is exactly why it is worth fixing. A tool whose own diagnostic channel is full of noise
it generates itself trains its reader to skip that channel, and the next warning to appear
there will be a real one. Everything now goes through `_read` / `_lines`; the count is zero.

## r132 — a comment that asserted what the theorem below it denies

`Bridge.lean`'s section heading read "窓級数 = gapSeries 恒等式" and its body said the window
series "coincides exactly with Γ = gapSeries". The theorem underneath states
`windowSeries A D = gapSeries A + (2D+1)/2^{|A|}` — so the comment dropped the boundary term
— and, since r120, the canon's identifier `gapSeries` is the *enumeration* form while the
paper's Γ is the *layer* form, so "= Γ" also conflated two different objects. One sentence,
both mistakes.

> A comment is not checked by anything. C7 verifies that every Lean name a paper cites
> exists; nothing verifies that a sentence next to a theorem says what the theorem says.

Fixed by making the comment point at the theorem instead of paraphrasing it — the cheapest
form that cannot go stale in the same way. The naming collision itself is recorded at the
definition in `Landscape.lean`; renaming the canonical identifier is deferred until there is
another reason to redo the kernel replay.

## r133 — the negative control fired 240x, in the wrong direction (append to F55)

Checking the Edgeworth form that the R1 attack design rests on, against exact dynamic
programming. The harness assigned the second-order coefficient twice and the second assignment
negated it, so the column labelled *true sign* carried the corruption and the column labelled
*flipped* carried the truth. The control reported the fit **improving by 240× under
corruption**.

That is how the sign bug was found. The control did not catch a defect in the theory; it caught
one in the instrument. Both count.

> **A negative control that fires the wrong way is not a failed control. It is a control
> reporting that the labels are crossed** — and it is the only instrument that can report
> that, because every other output looks the same either way.

Two operational rules from it. **Write the sign out once, in one assignment**; the bug survived
reading because the second line looked like a refinement of the first. And **state the
direction the control must move before running it** — "the fit must get worse" is checkable,
"the control fires" is not. The corrected harness prints the ratio and the word OK, and 12 of
12 fire at 21× to 455×.

Without it, sections 3 and 4 of `spec_r1_r133.md` would have shipped with an inverted sign, and
the out-of-sample prediction in section 4 would have been fitted to the wrong quantity — which
is the failure mode where a control matters most, because the surrounding numbers all look
reasonable.

## r134 — a bound that cannot work, and the control that said so (append to F51)

Step 1 of the R1 attack was to bound the fourth-order Taylor error of `log Ĝ` uniformly over
region R1. Measured against the exact product, that supremum is **≈ 840, and it does not
decrease with k** (817 / 846 / 843 / 816 at k = 100 / 200 / 300 / 450). No choice of radius
repairs it: at the radius where the integrand has already fallen to `k^{-10}` it is still
2.7–9.4.

Meanwhile the Edgeworth expansion predicts the same probabilities to a relative `3·10⁻⁵` at
k = 64, checked against exact dynamic programming.

Both are true. The integral is dominated by `|θ| ≲ 1/σ`, and the error out at the edge of the
region is never integrated against anything. Weighting by the density, `∫|Ĝ|E / ∫|Ĝ|` is
`9·10⁻⁴` at k = 100 and `9·10⁻⁵` at k = 450 — **six to seven orders of magnitude below the
supremum**, decaying at `k^{-3/2}`, which is *faster* than the leading terms of the budget it
was supposed to be a remainder for.

> **A sup-norm bound over a region where the integrand is already negligible charges the whole
> region at its worst point. When the estimate is going into an integral, estimate it under
> the integral.**

The general form for the ledger: **before bounding, ask what the bound is going to be used
for.** A quantity that will be integrated against a weight, summed against coefficients, or
evaluated at one point does not need — and often cannot survive — a uniform bound over the
region it lives on. The failure is invisible from the estimate itself; it shows up only when
the uniform bound refuses to decay while the thing it bounds plainly does.

**How it was caught.** The negative control — drop the `K⁽⁴⁾` term and the error must get
worse — **did not fire**: removing the term *improved* the sup-norm by 30%. That is a control
reporting that the quantity being measured is not the quantity the theory is about. At r133
an inverted control said the labels were crossed; here a non-firing control said the estimate
was. Two rounds, two different messages, both from the same instrument.
