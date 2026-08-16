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

## r187 — the first fit agreed with the prediction, and the agreement was noise

fable-5's r186 derived `ρ_k = Q_k/σ² ≍ (c/2)^k` and released the window experiment with the
discriminator stated: *the layer mechanism gives an exponential decay whose rate moves with `c`
as `log(2/c)`; the zeros give a `k`-independent constant and cannot.*

**The control law checks out.** `ρ_k(2/c)^k` is flat at `c = 1.6` (`0.8646…0.8542` over
`k = 12…28`), converging at `c = 1.4`, and still drifting at `c = 1.8` — confirmed where
confirmed, not beyond.

**And then the signal.** The first run took four `k` values per `c` and fitted decay rates of
`0.391` and `0.237` against `log(2/1.4) = 0.357` and `log(2/1.6) = 0.223`. **Ratios 1.096 and
1.064.** I had a confirmation.

Pushing to every reachable `k` — nine points at `c = 1.4`, six at `c = 1.6` — the same fits give
**`0.114` and `0.026`**, with a residual spread of `3.2` in `log e`. Over a `k`-range of 8 that is
an uncertainty of roughly `±0.4`, **larger than either predicted value.**

> **The agreement was an artefact of stopping at four points.** Not a wrong calculation, not a
> bug: a fit over a range too short to see its own scatter, reported as a ratio to three decimal
> places. **A ratio quoted to three decimals from four noisy points is a claim about precision
> that the data cannot support, and the decimals are what make it persuasive.**

This is F27 (*extend the range until the hypotheses are distinguishable*) firing on its author,
one round after that same author wrote *"a plateau is a claim about a range, and three points
inside one are not a range"* into the ledger. **The second time a rule catches you is not a
failure of the rule; it is the rule working on someone who already believed it.**

Two operational consequences:

- **Print the residual spread beside every fitted rate**, always. A rate without its scatter is
  an assertion wearing a number. The script now does; it should have from the start.
- **The reachable range must be established before the fit, not after.** At `c = 1.6`,
  `e/Γ` is still `O(1)` at every computable `k` — `0.275, 0.105, 0.763, 0.028, 0.182, 0.161` —
  so the limit has not begun and **no rate exists to measure.** Checking that costs one column
  and would have prevented the whole episode.

**Verdict as registered:** fable-5's control law **confirmed** on `c ∈ {1.4, 1.6}`. The
discriminating measurement **does not resolve**, and neither hypothesis is tested. The
pre-registered falsifier did not fire, and that is not evidence either way — an experiment that
cannot resolve cannot exonerate.

### r187, addendum — and the check caught the digit

C2 refused the report because twelve of its numbers were not in any log: I had quoted them at
four decimals from scientific notation printed at seven. Fixing that properly — a small script
that prints exactly the figures the prose quotes, so paper and report cannot drift from the
measurement or from each other — then exposed a thirteenth: **I had written `0.8646` where the
computation says `0.8645`.**

> **A number retyped at a different precision is a new number, and nobody checks it against the
> old one.** The defence is not care; it is to print the quoted form itself, once, in a log, and
> quote from there.

Small, and it landed in the same round as a fit that agreed by accident. **Both are the same
failure at different scales: a number that looked right because of how it was written down.**

## r189 — the instrument worked, and the verdict was "consistent", which is a third answer

fable-5's Ruling D found the way past r187's named gap by noticing what sparsity means: **in the
window the representation counts are small**, so exact arithmetic needs no big integers and the
binding constraint is table memory, not integer size. Vectorised `int64` reached `k = 46` against
`k = 28`, with overflow ruled out by a bound (`every entry ≤ 2^k`, `int64` holds `2^63`) asserted
in code rather than hoped for.

**The validation rung came first and it earned its place.** Ten values of `k`, identical
integers against the big-integer reference — *the same numbers, not close ones*. Had it failed,
nothing downstream would have been believed.

**And the result is a third kind of answer.** Not confirmed, not falsified: the decay rate
measures `0.2574 ± 0.1319` against a predicted `0.3567` — **0.75 standard uncertainties, and the
drift of `e·(2/c)^k` is `+0.0993 ± 0.1319`, consistent with zero.**

> **"Consistent with" is not "confirms", and the difference is the whole discipline.** A
> measurement whose uncertainty is 51% of itself would have failed to distinguish the predicted
> law from any law within a factor two of it. **Saying what a measurement could NOT have
> distinguished is part of reporting what it did.**

Two things to keep about how it was reported:

- **The first script ended with the sentence *"bounded over the range means the layer law
  survives this round"* — a definition that a reader takes as a verdict, with the script never
  saying whether the quantity is bounded.** The adverb class wearing a conditional. Fixed by
  *computing* the drift and printing it with its uncertainty instead of asserting a criterion.
  **A conditional whose antecedent is never evaluated is an assertion with deniability.**
- **The resolution gained is itself the reportable quantity**: `r187` said *no rate measurable*;
  `r189` says *`0.2574 ± 0.1319`*. **An experiment that moves a bound is a result even when it
  does not move a verdict**, and the honest headline is the uncertainty, not the central value.

Registered: layer law **consistent, not confirmed**; the falsifier did not fire and could not
have fired for a law within a factor two; per Ruling D's stop rule this thread now parks unless
the analytic route (the `k`-dependent form of `prop:correction` for profiles with `σ/N ≍ const`)
is taken up. **The gap keeps its name and gains a size.**

### r189, addendum — three rounds, three transcription catches, one cause

C2 refused r189 over `0.0072`, where the log says `0.007176`. That is the third round running in
which the same check caught the same act: r187 had `0.8646` for `0.8645` and twelve figures
quoted at a precision no log carried; r189 has a whole table retyped one significant figure short
of its source.

> **It keeps happening for a reason and the reason is not carelessness: it is that tables are
> built for the reader and logs are written for the record, and rounding is the act of turning
> one into the other.** Every time a number is made easier to read it is made new, and the new
> one has no provenance.

The fix is not "be careful". It is: **quote the log's digits verbatim, and if a table needs
rounder numbers, round them in the script so the rounded form is itself logged** — which is what
`figures_r187` did after the second catch and what should have been done again here without
being told.

**And the deeper reading, worth more than the rule.** Three catches in three rounds by the same
check is not three near-misses; it is a measurement of the rate at which prose drifts from
measurement when a human is compressing for readability. **A check that fires repeatedly on the
same author for the same act is telling you about a process, not about an accident** — and the
right response is to change the process, which here means: no number reaches a report except by
copy from a log.

## r191 — the wave, and a literature pass that transported half

**`prop:gqgen` landed in Part I** as fable-5's Ruling 3 specified, but not in the form either of
us first wrote. What belongs in Part I is not the deformed identity — `Γ^(q)` is a Part III
object — but the sentence underneath it: **`Γ` is the value at `1` of a generating function
`G_A(z) = Σ_j m_j 2^{−j} z^j`.** Part I gets that, with the two consequences that follow at once
(`R ≥ 1 ⟺ Γ finite`; `G = z/(2−z)` for the odd numbers); Part III cites it and adds the only new
content, which is that the deformation *reads the same function at two points instead of one*.
`cor:oddsclosed` is now a corollary of it.

> **The right home for a result is where its smallest true statement lives, not where it was
> discovered.** The discovery was about the deformation; the statement is about `Γ`.

C15 caught the cross-reference printing `1.2` for a proposition that had become `1.3` — the check
doing exactly the job it exists for, on the same commit that created the reference.

**The literature pass, run before any proof attempt as instructed, returned a half.**

- **Transported:** *Jentzsch's theorem* (1914) — every point of the circle of convergence is a
  limit point of the zeros of the sections; Szegő's refinement gives angular equidistribution
  along a subsequence; extensions exist to Dirichlet, Kapteyn and Neumann series, analytic
  curves, ultrametric fields. Applied to `G`, the accumulation of the zeros of **each section**
  at `q = ½` when `R = 1` is classical.
- **Not transported:** our object is `1 + G_k(2q) + G_k(2−2q)` — two sections under affine
  substitutions plus a constant — and **adding functions can cancel zeros**. No source covering
  sums of sections was found.

> **A half-transport is the most useful of the three outcomes, because it converts a conjecture
> into a named gap.** We now know which sentence is missing and that it is about power series
> rather than about landscapes.

**And the measured ladder turned out to be the fingerprint of the missing half.** Sections of a
single geometric series have zeros at angular spacing `2π/k`. Ours sit at `(2n+1)π/2k` — spacing
`π/k`, offset by half. **That is what `cos(kθ)` does and what `e^{ikθ}` does not**, so the
half-integer ladder is precisely the part the single-section theory does not describe.

> **The number that did not fit the classical picture was the one pointing at what was new.** It
> had been sitting in the log for four rounds, labelled as a rate; the literature pass is what
> made it a signature.

## r193 — a governance document that had to say where the mapping fails

Kentaro commissioned the three-layer model (deterministic orchestrator / non-participating
auditor / mutually-evaluating agents); fable-5 designed the mapping; `references/governance.md`
writes it up. The mapping is real — C1–C20 plus the status vocabulary plus the report protocol
*are* a deterministic orchestrator, the referee pass *is* a non-participating auditor, the
head/hands cross-verification *is* mutual evaluation.

> **A model adopted wholesale is a model nobody checked against the thing it describes.** The
> value of the exercise was not the adoption; it was being forced to write the two places where
> the mapping is imperfect: our orchestrator is deterministic about *form* and silent about
> *sense*, and our auditor is invoked rather than standing. Both are weaker than the model, and
> both are now stated instead of glossed.

Two provisions adopted (**A-1** evidence-path declaration, **A-2** status-transition table), two
declined with reasons, one **priced rather than declined** — continuous auditing costs one
fresh-context session per round, and saying that is more honest than either adopting or refusing
it.

The declines are the part worth keeping:

> **A numeric score is a currency, and a currency invites optimisation of the currency.** The
> currency here is a named artefact and a named falsifier — *"this dies if the ratio at k = 40
> exceeds 2"* — which can be spent by someone who distrusts us. **We have already paid for our
> opinions; a score would let us mint more without paying.**

> **Role rotation would rotate away the asymmetry that makes correction possible.** The split is
> not fairness, it is a division of instruments: the head holds design, the hands hold
> magnitudes, and *design cannot check itself against magnitudes it has not computed*.

And A-2's shape, which came out of the exercise rather than from the model:

> **Raising a status requires the other party; lowering it does not.** Guard the expensive
> direction. *Lowering a status needs no permission, only a reason.*

**Also recorded: the standing order that was not obeyed this round.** fable-5's r192 opens by
making the skill APPLY the first item of the next session, before any mathematics, with the
pending entries folded in the same sitting — *overdue housekeeping is how good systems rot*. It
has now waited five rounds. This round did the two commissions that fit and did not start the
mathematics, but it also did not do the APPLY, for the same measured reason as before. **A
standing order deferred with a reason is still deferred, and the count is now in the ledger where
it can be read against the excuse.**
