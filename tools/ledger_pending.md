# Ledger — pending

Case text for lessons bought since the last fold into the skill. **Empty means the skill is
current.** Folded through **r180** at r181.

*The standing rule (skill §7.0): a lesson is bought when it cost something. Write the case here
the hour it happens, in the words that were true at the time; distil it into the skill only when
folding, because the distillation is a different act from the record and doing both at once
produces neither.*

## r181 — the fold, and the one step of it that was not taken here

Nineteen entries (r160–r180) folded into `ledger_archive.md`, and the distillation written to
`tools/skill_delta_r181.md`: five new entries F78–F82, strengthenings of F26/F27, F35, F38, F60
and F70, three rules for the division of labour, one for the referee pass, one for sequencing.

**The skill file itself was not rewritten in the same round, and the reason is the subject of
this entry.** `save_skill` replaces `SKILL.md` whole — there is no patch interface — so updating
it means reproducing 55 KB by hand. A silent transcription error there would corrupt the one
document this project uses to remember why it does things, and it would be invisible: the file
has no checker, no build, and nothing that would fail.

> **The instrument that records how we avoid mistakes is itself unchecked.** Every other artefact
> here is guarded — the papers by C1–C20, the Lean by the kernel replay, the numbers by their
> logs — and the ledger's distillation is guarded by nothing but care. **When a write is
> unverifiable and large, split it: make the permanent record safe first, write the delta exactly,
> and do the unverifiable write where it can be read back and diffed.**

That is F82 applied to ourselves rather than to a button, and it is the same trade: the archive
fold is complete and cost nothing, the delta is exact and reviewable, and the one step that could
fail quietly is the one that waits for room to fail loudly.

**Open item, and it should not sit long:** apply `skill_delta_r181.md`, then diff the saved skill
against the source before believing it.

## r182 — following the rule on the day it was written, when it was inconvenient

The r181 write was attempted. It stopped at the point where the 67 KB file could not be brought
into context without crowding out the room needed to emit it back — and stopping there was the
decision, not the failure.

> **A rule adopted the same week is a rule that has not yet cost anything.** F82 was written
> about a button and someone else's click; the first time it applied to us it asked us to abandon
> a task the person had asked for twice, with the work 95% done and the temptation to push
> through at its highest. **The test of a rule is whether it holds the first time obeying it is
> expensive.**

What made stopping cheap rather than costly is that the round front-loaded the recoverable parts:
the archive fold is complete, the distillation is exact and separate, the patch was applied
mechanically rather than by hand, both versions are committed, and `APPLY.md` reduces the
remaining work to one instruction with a checksum to verify against.

> **Make the recovery cheap before making the write.** Then the decision to stop costs a session
> boundary instead of a document.

And one honest note on the count. Two methods were tried, not one attempt repeated: the bash read
hit an output cap, which is information about the channel and not about the file. **A different
method is diagnosis; the same method again is denial.** The line between them is what F82 is
actually about, and it is thinner than the entry makes it sound.

## r183 — the goal was not the file

Asked a third time to fold the ledger into the skill, and the `Read` path — genuinely untried,
and therefore diagnosis rather than repetition — confirmed the constraint instead of removing
it: 130 lines cost about 3.5k tokens, so 913 lines cost 25k to read and 25k to write back, and
the session has neither.

**Then the actual question got asked, which should have been asked two rounds earlier: what is
folding *for*?** It is so that a future session has these lessons loaded without going to find
them. `SKILL.md` is one channel that does that. **Memory is another, it is loaded every session
by construction, and 6 KB fits where 67 KB does not.** So the distillation went there, with the
skill file left as the tidying operation it actually is, and a pointer saying which is the live
canon until the two are merged.

> **A blocked step is not automatically a blocked goal.** Twice this round the plan was pushed
> at instead of the objective being restated, and the restatement took one sentence and cost a
> tenth of the effort. **When a route closes, say out loud what the route was for before looking
> for another one** — the answer is often a different route to the same place rather than a
> better attempt at the same route.

And the honest edge, kept because it cuts the other way too: **this is also how corners get
cut.** "The goal was not the file" is exactly what someone says when abandoning a hard step and
calling the easy substitute equivalent. The distinction here is that the substitute is *strictly
better on the stated objective* — memory loads unconditionally, the skill loads when the skill
triggers — and the harder step is still queued, still exact, still one instruction away. **When
you re-aim at the goal, say what the abandoned step was still going to buy, or you have not
re-aimed, you have retreated.** What the skill fold still buys: one canon instead of two, and
one file to read instead of a file plus a memory that says which one is live.

## r182 — the question handed to the head, answered by asking what the sum could do

r180 asked fable-5 three things, and the second was *what decides, for general `m_j`, whether the
two geometric series can cancel on `Re q = 1/2`?* — with the note that it looked like a question
about the growth of `m_j`, which is (H)'s own subject. It is, and the easy half is two lines.

Everything sits in one series, `g(x) = Σ_j m_j 2^{−j} x^j`, because on `|q − ½| = r` both `|q|`
and `|1−q|` are at most `½(1+2r)`. And `g(1) = (Γ(A) − 1)/2` — **so the radius of convergence
being ≥ 1 says exactly that `Γ` is finite, and being > 1 says the strictly stronger thing that
the layer weights decay geometrically.** Comparing `Γ^(q)` to `Γ(A)` rather than to zero turns
that into a disc with no zeros, uniformly in `k`, with `r = 1/6` for the odd numbers.

> **The conjecture was about zeros and the answer was about a generating function.** The zeros
> were never the object; they were a shadow of `Σ m_j 2^{−j}x^j`, which is the object the whole
> paper has been about since Part I. **When a new phenomenon appears, ask which of your existing
> quantities it is a shadow of before inventing a quantity for it.**

**And the part that was not looked for.** The proved radius is conservative by a factor of
3.03 for the odd numbers — and by 2.81, 1.65, 3.97 for the other profiles, and by **3.10 for the
lacunary family, where the hypothesis fails and the radius is not uniform at all but shrinks like
`1/k`, exactly as the measured distance does.** So the certificate tracks the truth on the side
where it does not apply.

> **A sufficient condition that stays proportional to the answer where it is not sufficient is
> telling you it was never really a sufficient condition; it was the mechanism.** That is a
> reason to look for the converse, and it is evidence about where to look — at `g₁` itself, not
> at the zeros.

Registered as: proposition **proved**; the proportionality **measured** on five profiles; the
converse **open**. And `Γ(A) ≥ 3 − 2^{2−k}` fell out of the proof for free, from `m_j ≥ 1`:
**the odd numbers are the densest admissible profile and they minimise the invariant.**

## r183 — the two families were one scale, and the scale had been in the paper since Part I

r179 measured a dichotomy on two families and registered it as conjectured. r182 proved one half
and noticed the certificate tracked the answer on the side where it did not apply. r183 wrote
`Γ^(q)` the obvious way — `1 + G(2q) + G(2−2q)` with `G(z) = Σ m_j 2^{−j} z^j` — and the whole
picture collapsed into one line: **the limit is analytic exactly on `|q| < R/2 ∩ |1−q| < R/2`,
and the fair coin is interior iff `R > 1`.** Since `G(1) = (Γ−1)/2`, that condition is *`Γ` is
finite* with one bit to spare.

The two families are the two ends of `c ∈ [1,2]`, layer gaps `2c^j`, and the distance from the
fair coin to the nearest zero goes to `1/c − 1/2` — measured at seven values of `c` with ratios
`1.008, 1.011, 1.017, 1.030, 1.072, 1.273`, approaching 1 from above and degrading exactly where
a finite `k` must degrade, namely where the predicted quantity is going to zero.

> **Two examples looked like a dichotomy because we had not written the object in the form where
> it has a parameter.** The zeros were a shadow of `G`; `G` is the generating function of the
> layer weights; the layer weights are what `Γ` has been a sum of since Part I. **Nothing new
> entered. What changed is that the same quantity was evaluated somewhere other than at `q = ½`.**

Three things to keep about the shape of the round:

- **The upgrade path was conjecture → half a proof → identity, and each step came from asking a
  smaller question than the last.** *What decides cancellation?* was smaller than *is the
  dichotomy true?*, and *what is `Γ^(q)` in closed form?* was smaller again. **When a conjecture
  resists, look for the smaller question whose answer it would follow from — not the bigger
  framework it might fit into.**
- **The identity was two lines and had been available from the first day `Γ^(q)` was defined.**
  It was not found for thirty-four rounds because nobody needed it: the invariant was only ever
  evaluated at the fair coin, where `G(1)` is a number and not a function. **A quantity you only
  ever evaluate at one point is a function you have not noticed you have.**
- **The measured law is stated with its failure mode showing.** The ratio column is printed
  *including* the row where it reaches 1.27, because a table that stops before the agreement
  degrades is a table chosen after the fact.

Registered: identity and its three consequences **proved**; the distance formula **measured**;
the accumulation *on* the boundary **open** — Hurwitz gives one direction on compact subsets, the
other needs non-vanishing of the limit, which is a statement about `G` and is not proved here.

## r185 — the experiment stopped, for a provable reason, and the reason was the finding

fable-5 released the Reading-3 experiment under F45/F30 discipline: falsifier in the header
before the first number, confound computed first, and stop if the two hypotheses cannot be
separated. **All three clauses fired, in that order.**

The confound is `Γ·Q(0)/σ²`. Computing it first — as instructed, before any `lm/r` — showed that
along the interpolating family the terms of `Q(0)` grow like `d^{2 − log2/log c}`, so

> **`Q(0)` exists if and only if `c < 2^{1/3} = 1.2599`, while `Γ` exists for all `c < 2`.**

There is a window in which the annealed prediction is finite and its first correction is not. And
`2^{1/3}` sits *below* the entire region where the zero-distance `1/c − ½` has moved
appreciably — so **the control evaporates before the signal appears.**

> **An experiment whose control ceases to exist before the effect becomes visible is not a weak
> experiment; it is a different question.** F20 says stop, and stopping was right — but the
> reason for stopping is worth more than the experiment would have been. It is a new critical
> exponent in a family we built for something else.

**And the discipline caught me inside the discipline.** The first Phase-A implementation cut the
`d`-sum at a fixed 4000 and 16000 and reported that `Q(0)` moved by a factor 53 *at `c = 1`*,
where the analysis says it converges. I nearly reported a numerical column contradicting my own
derivation. The derivation was right: `N_d` saturates at `k` once `2d` passes the largest
element, after which the terms are `2^{-k}d²` and grow — **an artefact of an arbitrary cap, not a
property of the profile.** With the canonical cut (`d < a_k/2`) and convergence tested in `k`
rather than in the cap, `Q(0)` for the odd numbers settles to `20.07, 20.30, 20.33` — converging
to `61/3`, `prop:correction`'s exact value.

> **When a measurement contradicts a derivation, the first suspect is the measurement's own
> free parameter.** The cap was mine, invisible, and outside the pre-registration — which is
> exactly the kind of choice pre-registration is supposed to expose and did not, because it is a
> choice about *how to compute the confound*, not about the hypothesis. **Pre-register the
> computation of the control, not only the prediction.**

Registered: `c < 2^{1/3}` **derived** and **measured**; the `61/3` recovery is an independent
check of `prop:correction`; the rate question is **open by a different route than the one
attempted**. Ruling 2's converse is now `prob:converse` in the paper, with the missing analytic
ingredient named at the statement, F38-style: non-vanishing of `G` on its circle of convergence.
