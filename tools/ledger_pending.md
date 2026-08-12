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

## r135 — the third control in three rounds, and the third different message (append to F51)

Measuring the constant in `|log f − P₄| ≤ C·pq·|v|⁵` over the phases the tilt produces, the
first run reported `C` reaching `10^9`, always at the smallest element and `v ≈ 10^{-4}`.

Not a blow-up. At that `v` the quantity being measured is `~10^{-20}`, double precision has
already lost it, and dividing by `v⁵ = 10^{-20}` amplifies the noise to O(1). This is F51's own
sentence — *identify the operation that amplifies rounding and restate the comparison without
it* — walked into while holding the ledger that contains it. Redone at 50 digits: `C ≈ 0.0053`
to `0.0093`, stable, worst at the **large** elements, exactly where the naive fear said it
would not be.

**And the sanity check caught a second defect, in the prediction rather than the code.** I
predicted the `v → 0` limit as `|1 − 12pq + 24(pq)²|/120`; it matched at no `p`. The fifth
Bernoulli cumulant is `κ₅ = pq(1−2p)(1−12pq)`, and against that the measurement agrees to
eight digits everywhere. The computation was right and my formula was wrong.

> Three rounds, three controls, three different places: **r133 the harness labels were
> crossed; r134 the estimate was not the quantity the theory is about; r135 the closed form
> I was checking against was wrong.** A control does not tell you *what* is broken — it tells
> you that the two things you thought were the same are not, and which two.

Operational note worth keeping: **put the analytic limit of the ratio in the harness as a
sanity line, not the ratio alone.** The `C` table by itself looked perfectly reasonable in both
runs; only the line predicting `|1−2p||1−12pq|/120` separated them.

## r136 — the hypothesis died, and its claim ceiling was the diagnostic (append to F45)

At r133 an out-of-sample prediction held to +0.72%: the residual constant `c_A` matched the
first-order Edgeworth coefficient across four profiles. The claim was capped at the time —
*"the profile dependence agrees to 0.7–2.4% and the x dependence does not"* — because the
x-dependence disagreed and there was no reason for it to.

At r136 the mechanism was checked by exact integer dynamic programming and **it does not
exist**: the Edgeworth corrections cancel between numerator and denominator, because the layer
`B_d` differs from the whole set only in its `N_d` smallest elements. The measured difference
is two to three orders below the factor that actually explains the residual, which the paper
already names.

The agreement was real and its cause was mundane: `K₄/(8σ⁴)` is proportional to `S₄/S₂²` with
a constant universal to 0.6% across profiles, and `S₄/S₂²` was already recorded as the shared
driver. **The same quantity appearing a third time, not a new mechanism.**

> **The part worth keeping is that the ceiling was the diagnostic.** The x-dependence
> disagreement was written down as a limitation three rounds before the explanation was known,
> and it was exactly the fingerprint of the true cause — a driver shared at leading order and
> not beyond it. A hedge written honestly is not padding; it is where the next finding comes
> from.

Corollary for the graveyard: **when an open question is answered, delete the question and
record the answer.** This one — *is `c_A` the second Edgeworth coefficient* — had survived
since r088 and would have been rediscovered a fourth time.

## r137 — we did not name the family our own lemma belongs to (append to F15)

Part III's coset identity is the **Kubert distribution relation** for `log|2 sin πt|`, shifted
by a half. Derived, and verified numerically to `1e-37` over `v ≤ 40`. The distribution relation
is the defining relation of the Kubert–Lang theory, underlying cyclotomic units and the
Kronecker limit formula — a number theorist recognises it in one line.

Nothing is wrong with the mathematics: our first proof *is* the multiplication formula, which is
how the classical relation is proved. What is wrong is that we advertised it as *"the one result
that reaches outside this programme"* without saying that it reaches outside because **it is**
outside.

> F15 says: search whether the quantity you invented already has a name. We named the object and
> not its **family**. A result can be correctly attributed at the level of the proof and
> unattributed at the level of the literature, and only the second one is what a reader checks.

The cost is not a lost claim — the use is still ours, and `cor:floor` as a substitute for
Erdős–Turán is the thing worth advertising. The cost is credibility: a reader who knows the
relation and sees us not name it will distrust the rest of the section, and that reader is
exactly the audience.

**Operational rule**: when a lemma is proved by a classical mechanism (a multiplication formula,
a reflection formula, a functional equation), search for the *relation's* name, not only for the
statement's. The proof technique is the pointer to the family.

## r138 — the hypothesis failed in exactly one place, and that place was the theorem

Testing the distribution-relation floor as a stand-alone tool, it failed at one cell of the
table: the primes at `q = 6`, true average 0.1457 against a floor of 0.4621.

Not a bug. The lemma's hypothesis is that the residues cover an **additive** coset, and the
primes' residues mod 6 are `{1,5}` — a multiplicative subgroup that is not an additive coset.
The failure is the modulus-6 phenomenon, which Part II spends a section on.

Chasing why gave a two-line proposition: **`(Z/q)^*` is an additive coset of a subgroup of
`Z/q` if and only if `q` is a power of 2.** (Both `1` and `−1` are units, so the modulus of the
coset divides 2; modulus 2 forces every odd residue to be a unit.) That single fact explains
why the extremal modulus is 4 for a random odd sequence and 6 for the primes — two theorems the
papers prove separately.

> **When a lemma's hypothesis fails on real data, check whether the failure is a known
> phenomenon before treating it as an error.** A hypothesis that fails exactly where the
> subject is exceptional is not a defective hypothesis; it is a hypothesis that has located
> the exception. Ours found the one modulus the whole of Part II is about.

The general habit this suggests: **run a new lemma against the cases you already understand
before running it against the ones you do not.** The table that produced this had six moduli
and two profiles, and the value came entirely from the single cell where the answer was
already known and the lemma disagreed with it.

## r140 — the degenerate case was a theorem, and it nearly closed the lead (append to F30)

Testing whether Γ says anything about numerical semigroups, the first control ruled out the
obvious confounder: at fixed smallest generator the correlation with the Frobenius number
survives at 0.65–0.80, null control 0.17.

The second control was the one that mattered. Γ has a closed form,
`Γ = a₁/2 + a₂/4 + ⋯ + a_{k−1}/2^{k−1} + a_k/2^{k−1}`, and from it:
**at `k = 2` Γ is exactly the mean, and at `k = 3` with `a₁` fixed it is affine in `a₂+a₃`, so
it is perfectly correlated with the mean.** Not "approximately" — provably. That is why the
measured correlations at `k = 3` matched the mean's to four decimals, and it means no amount of
data at small `k` could ever have shown Γ carrying its own signal.

> **Where a closed form exists, the degenerate cases are theorems rather than data points, and
> they are the cheapest place to discover that your statistic is something else wearing a
> different name.** Evaluate the closed form at the smallest cases *before* running the
> correlation, not after.

F30 already says: before a decisive test, check algebraically that the quantity is independent
of what you have already measured. This is the same rule at the other end — check algebraically
what the quantity *degenerates to*, because a statistic that collapses to a familiar one in the
small cases is probably a perturbation of it in the large ones. Γ turned out not to be, but
only from `k ≥ 5` and only by 0.01–0.04.

## r140 — the index had become a second copy of the thing it indexes (append to F35)

`MEMORY.md` is the index loaded into context at the start of every session: one line per memory
file, pointing at where the detail lives. It had reached **41 KB, of which a single line was
19 KB** — the pointer to the research log had accumulated a full summary of every round for
forty rounds, and was approaching the size at which the file would stop being readable at all.

Every word of it was already in `pnp-progress.md` (367 KB, 133 rounds). Verified before
deleting, by sampling the specific rounds the line cited and the specific lessons it quoted, and
confirming each appears in the log, the failure ledger, or the skill. Compacted to 2.4 KB.

> **An index that grows becomes a copy, and a copy of the thing it indexes is worse than no
> index: it is the artefact most likely to be read and least likely to be maintained.** The
> shape is F35's — a summary drifting away from what it summarises — but in the other
> direction: not over-claiming, over-*including*, until the summary is the document.

Operational rule, and it is a size check rather than a judgement call: **the index gets one line
per entry, and a line that no longer fits on a screen belongs in the file it points at.** Where
the current position genuinely needs to be in the index — it does, because a cold session reads
the index first — it gets one sentence naming the state, not a history of how the state was
reached.

*Caught by the tooling rather than by me: the write hook warned at 19.8 KB against a 24.4 KB
read limit. Without it the next cold session would have found an index it could not read.*

---

## r141 — F60, instance six: the translation lags the appendix, and C19 caught it in four days

Appendix A went into `paper4.tex`; `check.py` returned two FAILs and neither was in the appendix:

```
FAIL C9/F59: README says 34 pp., PDF has 32 pp.
FAIL C19/F60: paper4_ja.tex is missing 12 label(s) its source has …
```

C9 fired because the 34-page build lived in `/tmp/aux` and had not been copied back — *the PDF a
reader downloads is not the PDF I compiled.* C19 fired because the Japanese edition had none of
the appendix.

> **C19 was built at r131 to catch exactly this and caught it at r141, on its author, ten rounds
> later.** That is the argument for mechanical checks in one line: the check was not written
> because I was careless once, it was written because I will be careless again, and the second
> time I was the one it caught.

The same round also produced the C9 variant worth naming separately: I *fixed* the README to 35
pp. from the Japanese build, and C9 failed again because the English PDF is 34. The count in the
README is a count of a specific artefact, and "the paper is 35 pages" was true of a different
file. **A number is only checkable if it names which file it counts.**

## r142 — the external verification could not see what it was verifying

Post-push, the SHA-pinned raw fetch of `paper4.tex` returned 1,369 lines against 2,378 local, and
a grep for `Appendix` in the fetched text found nothing. Two readings were available: the push
did not contain the appendix, or the fetch was truncated. The distinguishing test was cheap —
`Use of AI tools`, which has been at the end of that file since r116, was also absent — so the
tail was missing, i.e. the fetch was truncated, not the commit. Verified instead by fetching the
small new artefact `r1proof_r141.log`, which came back complete.

> **When a verification tool disagrees with the thing it verifies, find a fact you already know
> and check whether the tool can see *that*.** A tool that cannot see a known fact is not
> reporting on the unknown one. The cheap version of this is: verify with the smallest artefact
> that the commit is supposed to contain, not the largest.
