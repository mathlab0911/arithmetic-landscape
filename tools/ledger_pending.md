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

---

## r143 — the floor belongs to the orbit's subgroup, not to the ambient modulus

Applying the coset floor to A = odd numbers at even denominators v, I used the
average over the full group Z/v, i.e. `(1−1/v)log 2`. For A odd and v even the orbit
`{a h mod v}` is entirely odd — a coset of the index-2 subgroup — so the floor is the
one belonging to *that* subgroup, `(1−2/v)log 2`. The control fired on six rows.

The signature is worth recording because it identifies the error without any thought:

```
   v = 8   truth 0.51986   claimed 0.60650  ← which is the CORRECT floor at v = 16
   v = 16  truth 0.60650   claimed 0.64983  ← which is the CORRECT floor at v = 32
```

> **A floor that is systematically one step down a ladder is a floor computed in a
> group one step too big.** The claimed value was never a random overshoot; it was
> always exactly the right answer to the wrong question, and that is what made the
> diagnosis a minute's work rather than an afternoon's.

This is prop:twopower speaking a third time (after the q=6 failure and the
classification itself), and it is the same shape as F60 in a different medium: the
object exists, and it is not where the argument is looking.

**Operational rule:** when a lemma's hypothesis is *"the residues form a coset of a
subgroup"*, the conclusion's constant is a function of that subgroup's order. Read
the order off the orbit — `len(numpy.unique(...))` — never off the modulus.

*What the chase produced.* The primes were loose against the corrected floor at small
odd v, because they avoid 0 mod v and are therefore unbalanced over the coset. That
is not a defect of the primes: being unbalanced *away* from the minimum makes their
energy larger. Following it gave the exact evaluation over the reduced residues
(prop:redresidue), which subsumes thm:modfour and re-derives prop:twopower.

> **A loose bound in a case you expected to be tight is a question, not a defect.**
> Twice now the interesting statement has come from asking why the floor was slack
> rather than from trying to tighten it.

---

## r143b — the literature pass found the claim was fine and the *next* sentence was not

`rem:surrogate` asserts that the standard minor-arc route for these generating
functions goes through a Weyl-sum bound. F12/F14 say check that against a document,
so I did: the partitions-into-prime-powers minor-arc lemma bounds the generating
function by quoting an exponential-sum estimate for `Σ_p e(j p^k α)`, exactly the
surrogate route, and saves a power of `log X`. The claim survives.

What did not survive was a sentence of mine two lines further on. Reading the paper's
minor arc — a *neighbourhood* of a rational — against `prop:redresidue`, which
evaluates at the rational itself, exposed a gap I had not flagged:

> `cor:floor` makes a single coset's floor uniform in the shift. The reduced residues
> are a **Möbius-signed** combination of cosets, and a signed combination of lower
> bounds is not a lower bound.

Measured, it is a trichotomy: uniform and provable at `v = 2^j` (one coset), uniform
but unproved at `4 | v` with odd part > 1, and **false** at odd `v` — at `v = 3` the
average drops from `log 2` to `½log 2` at `t = 1/3`, because the shift carries a
reduced residue onto 0 where `X` vanishes. `rem:shift` now states all three.

> **Reading the literature is not only for attribution.** The document did not
> correct my citation; it corrected my *reading of my own result*, by putting the
> result next to the shape of argument that would consume it. A claim looks different
> when you place it where it would actually be used.

*Timing note, and it is the uncomfortable part: the gap was found ten minutes after
the push, not before it. The check suite has no test for "is this evaluation also a
bound", and could not have — the defect was in the prose around a correct theorem.
What caught it was doing the literature pass I had already listed as a task and had
not yet done.*

---

## r144 — the same remark, wrong twice, and the second time the measurement was the liar

`rem:shift` said the `4 | v`, odd part > 1 case was *measured uniform*. It is **false**,
and the counterexample is not exotic: at `v = 12`, `t = 1/5` the reduced-residue
average is `0.4525` against `log 2 = 0.6931` at `t = 0`.

The measurement scanned `t` over `[0, 1/v]`.

> **`1/v` is the period of the *full-group* average — `t ↦ t + 1/v` permutes
> `{k/v : k mod v}`. It is not a period of the reduced-residue average, because
> `t ↦ t + 1/v` carries `r/v` to `(r+1)/v` and the units are not closed under `+1`.
> The symmetry used to shrink the search belonged to a different object.**

The scan was blind to the region containing the counterexample, and returned a number
rather than a warning. That is the whole danger: **a search restricted by a symmetry
the object does not have does not fail — it succeeds, on a subset.**

Related to F51 (a computation right at the wrong precision) and to the r134 sup-norm
episode (an estimate right about the wrong quantity); the family is *the computation
is correct and is about something else*. What is new here is the mechanism: the error
entered through an **optimisation**, not through the model. Nobody writes down a
restricted domain as a modelling assumption; you write it down to save time.

**Operational rule:** before restricting a search by periodicity, name the group action
that realises the period and check the object is invariant under it. Two lines. Cheaper
than a correction that ships.

*What redeemed the round: settling it properly needed the product form of `lem:coset`,
which gives `Q(v,t) = 2^[w=1] ∏_{d|w} |cos(π(v/2d)t)|^{μ(d)}` and answers BOTH
directions at once — uniform iff `w = 1`, i.e. iff `v` is a power of two, which is
`prop:twopower` for the fourth time. **The failed guess forced an exact computation
that a successful measurement would have left undone.***

---

## r145 — C20, and the rule it encodes

Kentaro's ruling after r144: **a claim of the form "measured but unproved" blocks the
push.** Now mechanical, as C20.

The rule has three outs, not two. Prove it, disprove it, **or move it to the open
register** — a `problem` environment, or a status that calls it a conjecture or an
open question. Naming a thing open is not a loophole; it is the third honest outcome,
and it relocates the claim to where a reader looks for what is missing. What is banned
is the fourth thing: a statement asserted in the paper's own voice whose only support
is a scan.

Five negative controls, all five fire, including the exact r143 defect and its Japanese
form. One carve-out was needed and it is instructive:

> **"not proved *here*" means proved elsewhere, in the literature — the opposite of
> "not proved". The adverb carries the whole distinction, and a checker that cannot
> read the adverb will fail the paper for its own honesty.**

The first draft fired on `prop:rate`'s Japanese status, which says three standard
estimates are stated and applied but not proved here. That is a citation, not a gap.
Note the shape: **the check fired on the Japanese and not on the English, and the
asymmetry was the symptom** — the two languages phrase the same benign fact
differently, so a marker set tuned on one language mistakes the other for a defect.
C19 exists because translations drift; C20 shows they also *differ*, legitimately, and
a bilingual check needs a benign list per language and not a translated one.

*Same round, worth one line: C20 immediately bit its author. The `Γ^(q)` zero results
of door 2 — a measured `2π` and an unidentified `6.5652` — are exactly the shape the
rule bans, so they went into a working note and not into Part III. **A rule that has
not yet cost you anything has not yet been tested.***

---

## r146 — the same function, wrong twice, and the ratios told me both times

Door 1b: compose `prop:chardecomp` with Dirichlet's class number formula and check that
`S(p)/(4 log ε_p)` comes out a positive integer. Two harness bugs, both in the routine
computing the fundamental unit, and in both cases **the wrongness was legible in the
answer**.

**First:** every ratio came out `1/6` or `1/2`. Ratios that clean are never a broken
theorem — `1.618^6 = 17.944` and `12.083² = 146.0` identified it in one line: the
continued-fraction routine was returning a *power* of the unit, and the denominators
`6` and `2` were the exponents.

**Second:** after the rewrite, seventeen primes gave the known class number and `p = 5`
gave `1/2`. Same shape, smaller: the Pell search tried `x² − py² = +4` before `−4`, and
at `p = 5` both solve at `y = 1`, so it returned `(3+√5)/2 = ε²` instead of
`(1+√5)/2 = ε`.

> **A search for the least element must enumerate in the order of the thing being
> minimised.** Mine enumerated `y` outermost — correct — and then took the first `s`
> that worked, which is not a minimisation at all. The bug only shows where both signs
> solve at the same `y`, which is why it survived seventeen primes and died at the
> smallest one.

The general form, and it is the reason this is worth a ledger entry rather than a fix:

> **When a wrong answer is a clean function of the right one — a power, a small rational
> multiple, a constant factor — the discrepancy names the bug.** `1/6` is not noise; it
> is a receipt saying *you cubed and squared something*. Look at the shape of the error
> before looking at the code.

Related to F51 (right computation, wrong precision) and r144 (right computation, wrong
domain). Here: right computation, wrong *representative*.

*The result survived both: 18/18 primes give a positive integer equal to the known class
number, including `h(229) = 3`.*

---

## r147 — we had our own theorem's meaning backwards, and it took an outsider's question

Kentaro asked whether there is anything here the mathematical community can use. The
answer turned out to be sitting inside the main theorem, stated the wrong way round.

The README said the recurring theme was **replacing** the annealed approximation with an
exact identity. Three lines of arithmetic from Part I's own classification show that

> **`Γ` IS the annealed prediction.** Offset `d` forbids exactly `N_A(d)` elements; the
> independence heuristic gives `2^(−N_A(d))` per layer; sum and you get
> `1 + 2Σ 2^(−N_A(d)) = Γ(A)`, on the nose.

So the theorem is not *we avoided the heuristic*. It is *the heuristic is asymptotically
exact here, and (H) says when*. Annealed-exactness results are rare and wanted; the
version we were printing was the same fact phrased so that nobody outside would notice.

> **A result can be correctly proved, correctly stated, and pointed the wrong way.** No
> check catches this: every number was right, every status was honest, C1–C20 pass on
> both wordings. What was wrong was which sentence went in front.

The trigger is worth recording too. **It was not a check, a control, or a review — it was
being asked "is this useful to anyone?" by someone outside the derivation.** Two rounds
running, the thing that improved the mathematics was a question about audience: r146's
literature pass, and this. *Add to the round loop: at least once per programme, state the
main theorem the way the reader who does not care about your method would want it.*

**Also r147, and it is the third instance of one lesson.** `log|2cos πt| = (T₂−1)log|2 sin πt|`
by the double-angle formula, so the factor `1 − χ(2)` in `prop:chardecomp` is the
eigenvalue of `1 − T₂` and the proposition is Dirichlet's classical evaluation
transported. Coset identity → Kubert. Class number → Kubert–Sinnott. Character
decomposition → Dirichlet plus trigonometry. **Three for three.** The standing posture is
now explicit in `rem:doubleangle`: assume classical, name the transport, keep only the
landing.

---

## r148 — the question three papers never asked, and a check that fired on honesty

**The gap.** Three papers prove the conclusion *under* (H), and `prop:alphalb` cuts the
power profiles at `α = 1`. **Nowhere did we ask whether the conclusion fails when (H)
does.** It took r147's reframing — the theorem is an annealed-exactness theorem — to make
the question audible, because it is the first thing a physicist asks and not a thing a
prover asks.

> **A hypothesis you have proved things under for months is invisible.** You check whether
> it holds; you stop asking what it is *for*. The question "is this hypothesis about the
> phenomenon or about my proof?" has to be scheduled, because nothing in the work raises it.

Measured: over `20 ≤ k ≤ 90` the annealed prediction is approached even where (H) fails —
the fitted exponent drops from `k^(−2.89)` to `k^(−0.98)`. So (H) looks like a *rate*
condition. Stated as `prob:hrate`, not asserted; C20's third out.

**The methodology bit.** The first attempt used a single central target and produced
`0.93, 1.16, 0.94, 1.02, 1.01` — a sequence that would have supported any story. At one
target the parity and lattice effects are larger than the effect being measured.
Averaging over 41 targets turned noise into a clean exponent.

> **Before fitting a trend, check that one sample point is not noisier than the whole
> trend.** The tell was that the sequence was not monotone in either direction.

**And C20 fired on this commit's own honest text**, which is the more interesting failure.
`prob:hrate`'s status says its evidence is *measured, not proved* and then says it
therefore goes to the open register — precisely the escape the rule provides. The check's
prose half was re-scanning STATUS blocks the status half had already cleared, under a
stricter rule set.

> **Two rule sets over one string is a bug, not a belt and braces.** The stricter one wins
> silently, and what it convicts is whichever text was most explicit about its own
> limits — that is, the most honest text in the file. Fixed by stripping statuses before
> the prose scan: *one voice per fact*, which is the project's rule everywhere else.

Controls rerun, and one was added for the escape itself: five defects fire, and a status
that names its claim open stays silent. **A check with an escape hatch needs a control
proving the hatch still opens**, not only controls proving the door is shut.

---

## r149 — a bilingual check cannot match on text it has not unwrapped

C20 convicted `prop:schur`'s Japanese status, whose exempting phrase was
`確認のための測定` — *measurement for confirmation only* — split as `確認のための\n測定のみ`.

> **Japanese has no inter-word spaces, so a hard line break falls wherever the
> typesetter put it, in the middle of a phrase.** An English marker survives `\s+`
> because English breaks at spaces. Its Japanese counterpart does not survive at all.
> A bilingual check must **unwrap before matching**: drop the newline when both
> neighbours are non-ASCII, turn it into a space otherwise.

This is the second time in two rounds that C20 convicted the most honest text in the
file — first because two rule sets fought over one string, now because one of them could
not read a line-wrapped exemption. Both times the false positive landed on a status that
was *more* explicit about its own limits than its neighbours. **A checker's false
positives are not uniformly distributed: they concentrate on the text that says the most.**

**And the fix bred its own bug, immediately.** Unwrapping the status blocks broke the
prose half, which had been blanking statuses with `prose.replace(block, ...)` — the
unwrapped block no longer occurs verbatim in the source, `replace` found nothing, failed
silently, and handed every status back to the stricter prose rule.

> **A `replace` that finds nothing does not raise.** Where the intent is "remove this
> region", address it by span and not by content — content-based removal is a lookup that
> can miss, and missing looks exactly like success.

Controls now seven: five defects fire, and two escapes are proved still open — the
open-register escape and a benign phrase split across a line break.

---

## r150 — the correction term was already in the paper, tabulated for the opposite reason

Applying the local limit theorem layer by layer at the centre gives, to first order,

```
   lm/r = Γ(A)·(1 − Q(0)/σ²),      Q(0) = Γ⁻¹ Σ_d 2^(−N_d)(δ_d² − s_d/4)
```

and `Q(0)` is **the quantity §counterexample already tabulates** — 20.3 for the odds, 50.4
for the primes, 916 for the squares, 3.8e5 for the cubes. It was put there to show *how far
out of reach* a profile is. It is, up to `σ⁻²`, **the error itself**.

> **A quantity computed to argue that something is hopeless can be the thing that measures
> it.** We had the correction term in a table for two years' worth of rounds and read it as
> a difficulty index. The reframing of r147 is what made it legible: once the theorem is
> "the annealed count is exact", the obvious next question is *how exact*, and the answer
> was already printed.

Verified against exact DP: measured/predicted → 0.98 on three families at `k = 90`,
including the one where (H) fails. It also **corrects r148's own fitted exponent**: `0.98`
for `α = 1/2` was contaminated by the smallest size, where the measured error changes sign;
the honest fit is `1.7` and the *predicted* value is `3α = 1.5`.

**And a measurement bug that nearly became a discovery.** The translated block
`{2m+1, …, 2m+2k−1}` returned a relative error of `−3.7` — lm/r nearly five times `Γ` —
which for ten minutes looked like the counterexample the open problem was asking for. It
was not. Every subset sum of that family clusters near multiples of `2m`, so a window of 41
consecutive targets is mostly **empty**, and the unweighted mean of ratios over the
survivors averages an atypical subset. Switching to the `r`-weighted statistic
`Σlm(n)/Σr(n)` — the ratio at a typical *ground state*, which is also what the theorem is
about — makes the anomaly vanish.

> **When a family produces a spectacular result, check the support before checking the
> theory.** The diagnostic that would have caught it immediately is now printed in the log
> as a column: how many targets in the window are non-empty.
