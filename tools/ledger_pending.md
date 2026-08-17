# Ledger — pending

Case text for lessons bought since the last fold into the skill. **Empty means the skill is
current, and it is empty.** Folded through **r200** at r200: twenty entries (r181–r200) into
`ledger_archive.md`, distilled by `tools/skill_delta_r200.py`, and the result written to the live
skill and **verified byte-identical** — 80197 bytes, 1075 lines, md5
`14b6321770e633b4e8f2fdc051216124`, `F01`–`F87` present. The record of that write is
`tools/skill_backup_r200/`.

**There is one canon: the skill.** Memory holds a pointer, not a copy.

*The standing rule (skill §7.0): a lesson is bought when it cost something. Write the case here
the hour it happens, in the words that were true at the time; distil it into the skill only when
folding, because the distillation is a different act from the record and doing both at once
produces neither.*

*And one from the r200 fold itself, kept here because it is about this file rather than about the
mathematics: the applier aborted three times before it ran, twice because an anchor straddled a
line break — the same defect (F69) for the third time in this project. **An abort before the write
is the cheap outcome, which is why the applier asserts every anchor occurs exactly once.***

## r202 — the instrument control fired on the reference, not on the instrument

**claimed** : falsifier 1 of `pinch_r202` compared both methods against `(1/2)tan(pi/k)`, the
value `rem:leeyanglacunary` *proves* exact, and demanded 25 agreeing digits.

**actual**  : it FAILED at 16 digits, while the two methods agreed with **each other** to 30.
The reference was computed one line before `mp.dps` was raised — a **15-digit constant printed
to 30 places and compared against 60-digit measurements.** The methods were right; the control's
own reference was the defect.

**check**   : evaluate the object at the reference point. `Gamma^(q)` there was `7.8e-61`, i.e.
the closed form was correct and the *number* was not — which localised it in one step.

**rule**    : **A control's reference is a measurement too, and it is the one nobody checks.**
Compute every reference at the precision of the thing it will be compared with, and prefer
computing it *inside* the same precision block rather than before it.
> This is F87's small sibling — *a number retyped at a different precision is a new number* —
> caught one level up: not in the paper, but in the apparatus written to police the paper.

**And the shape of the failure was the informative part.** Two independent methods agreeing to 30
digits while both missed the reference at 16 is not a symmetric situation: **when N independent
instruments agree with each other and disagree with the reference, the reference is the outlier
and should be audited first.** The first instinct was to loosen the threshold, which is F57
(*a check loosened until it stops complaining has been switched off with extra steps*).

## r202 — method B was measuring a different quantity, and only the certificate said so

**claimed** : method B — scan the critical line for the first sign change — is an independent
second measurement of *the distance from the fair coin to the nearest zero*.

**actual**  : it measures the nearest **on-line** zero. For every profile in the table with
`R > 1` the nearest zero is **off** the line: at `c = 1.00` the nearest on-line zero is at
`0.872` and the nearest zero at `0.504`. The assumption came from the boundary families
(`R = 1`), where r195's argument-principle count *had* shown every near zero to be on the line
— **an assumption imported across a regime boundary without being written down.**

**check**   : the winding-number certificate on `|q-1/2| = d(1-eps)` refused to certify, on every
row but one. Without it the two columns would have been read as a method dispute rather than as
two different quantities.

**rule**    : **When two methods disagree, ask what each one measures before asking which one is
wrong.** A "second method" that answers a different question is worse than no second method,
because the disagreement looks like a precision problem and invites the wrong repair.
> **Every method carries an unwritten domain assumption; the certificate is what makes it
> writable.** B without the winding number was a claim about where we scanned (F60); B with it
> is a claim about the disc — and it is the certificate, not the search, that failed.

**Two smaller things from the same round.**

- **A pre-registered falsifier passed on an empty population.** F3 (*ratio >= 1 and increasing
  in c*) reported PASS in a run where every row was "not resolved" and no ratio existed. Fixed to
  print the population and to fail at zero — **`expect_subjects` belongs in falsifiers too, not
  only in `check.py`** (F60/F78).
- **`F41` caught a self-contradiction two lines apart.** The rendered page showed the new text
  establishing that at `c = 1` the family is *not* the odd numbers, and two lines below, in a
  sentence nobody had touched, *"which is 1/2 at c = 1 (the odd numbers)"*. **Adding a
  clarification creates the contradiction it resolves, one paragraph away, and only reading the
  built page finds it.**

## r203 — two families were one theorem, and the difference was a single constant

**claimed** : the project held `a_i = 2^i−1`, `a_i = 2^i+1` and the layer family `c = 2` as
**three** boundary families, measured separately, cited separately, and counted separately as
evidence ("five profiles, two rates") for four rounds.

**actual**  : they are one identity with one constant. For `w_0 ≥ 0` and `w_j = w` on
`1 ≤ j ≤ k−1`, `F_k(½+it) = A + w ρ^k sin(kθ)/t` with `A = 1 + 2w_0 − 2w`, and the three profiles
are `A = 0, 2, 1`. The one with a closed-form zero set is exactly the one with `A = 0`, i.e. the
one whose `w_0` vanishes — because `a_1 = 1` contributes no layer. **The distinguishing feature
was a single number, and nobody had computed it.**

**check**   : write the general member of the class before measuring its instances. Two of these
had been in the same section of the same paper for twenty rounds.

**rule**    : **When a paper carries several examples of the same phenomenon, compute the general
case once and read the examples off it.** Separately measured instances look like independent
evidence and are not; the count "three families" was a count of *computations*, not of *cases*.
> **Parameterise before you tabulate.** A table of instances with no parameter in it is a table
> nobody has looked for the parameter of --- and here the parameter also *explained* which row
> was special, which no amount of further measurement would have.

*The consolation, and it is the honest half:* the merge does not weaken the evidence, it explains
it. Three coincidences became one mechanism with three inputs, and the closed-form row stopped
being a lucky family and became the `A = 0` case.

## r203 — the index became a copy, and the rule against it was already written

**claimed** : `MEMORY.md` is an index, one line per entry (skill §14, which says in as many
words that *an index that grows becomes a copy, and a copy of the thing it indexes is the
artefact most likely to be read and least likely to be maintained*).

**actual**  : **41.5 KB, ten round-entries of up to 6 KB each, and two "pointer" lines that had
themselves grown into copies of the files they point at.** It was caught by a tool warning about
a size limit, not by us — nothing in this project reads its own memory for shape.

**check**   : the fold was mechanical — move the fat entries verbatim into `pnp-progress.md`,
**assert every one of them is present in the destination**, and only then rewrite the source.
That ordering is r200b's lesson, and this time it was designed in rather than survived. Result:
41543 → 4306 bytes, all content preserved.

**rule**    : **A file that says what it must not become needs something that measures whether
it has become it.** The rule was correct, written down, and read at the start of every session
for months, and the file drifted anyway, because *no step of any procedure ever looks at it*.
> **Every artefact with a stated shape needs a check on the shape, or the statement is a wish.**
> Candidate: one assertion in `check.py` on the byte size and the one-line-per-entry form of
> `MEMORY.md`. Not written this round — naming it here rather than shipping it silently.

**And a repeat offence worth its own line.** §9 says *pass PowerShell work as a script file, not
`-Command`*, and *PowerShell mangles non-ASCII*. I hit both, in that order, in one session: first
the `$` variables were eaten by the wrapper, then the same script as a `.ps1` had its Japanese
string destroyed by PowerShell 5.1's encoding. **Having a rule and not reaching for it is not
having the habit** — the third instance of that sentence in this ledger, and the fix is the same
each time: for anything with non-ASCII or `$`, write Python and run it.

## r204 — the conjecture's dividing line was never on the line

**claimed** : (published in `v1.1.1`, `rem:rateregimes` STATUS) *"the dividing line is conjectured
to be `Σ_j w_j < ∞` rather than anything finer."*

**actual**  : **disproved.** The harmonic profile `w_j = (j+1)^{-1}` has `Σ w_j = ∞` and takes the
`√(s log k / 2k)` rate, not `π/2k`: `k·t_1` runs `11.9, 18.0, 27.3, 37.0, 55.6` at
`k = 64…1024` — growing, not settling at `π/2 = 1.571`. The same for
`w_j = ((j+2)log(j+2))^{-1}`. **The line is `w_j → 0` versus `w_j ↛ 0`.**

**check**   : *test the dividing line on the line.* Every divergent-side profile ever measured
here had **constant** weights, and every convergent-side one decayed like a power, so the data
were equally consistent with a different statement — *constant versus decaying* — that nobody had
written down. The two hypotheses separate only on profiles that **decay without summing**, and
until r204 not one had been computed.

**rule**    : **A dividing line is a claim about the profiles that lie ON it, and evidence from
profiles far to either side does not test it.** Before conjecturing a boundary, ask which objects
sit closest to it and compute one of those.
> The two hypotheses had been *observationally equivalent on everything we owned*. That is not a
> reason to prefer either; it is a reason to go and find the case that separates them, and the
> cost here was one script.

**And the mechanism had already said so.** The derivation reads: `w_k ρ^k ≈ k^{−s}e^{2kt²}` is
`O(1)` when `2kt² = s log k`. **It uses `w_k` and never `Σ_j w_j`.** The summability clause was
never one of its hypotheses; it was imported from the examples and attached to a derivation that
does not need it.
> **When a conjecture and its own mechanism disagree about what the hypothesis is, the mechanism
> is the one that was derived.** Read the derivation back against the statement before publishing
> the statement — the scope of a mechanism is legible in the mechanism.

*(Fourth correction in one section in five rounds: `cos`/`sin`, `R ≥ 1 ⟺ Γ finite`, the missing
clamp, and now this. Three of the four were found by building something new and noticing it
contradicted a sentence elsewhere — F84's clause about new examples, firing again.)*

## r206 — the observable was halving the discrepancy before anyone looked at it

**claimed** : the `s = 1` constant is anomalous — the ratio `t_1 / √(s log k/2k)` measured
`1.033, 1.024, 1.026, 0.927, 0.934`, non-monotone and ~7% low.

**actual**  : the mechanism does not predict `t_1`. It predicts the **scale**:
`k^{−s}e^{2kt²} = O(1)` ⟺ `2kt² = λ log k` with `λ = s`. The quantity the hypothesis names is
`λ_eff := 2k t_1²/log k`, and the ratio we had been printing is `√(λ_eff/s)` — **a square root
that halves every discrepancy before it reaches the page.** In `λ` the same data read
`|λ−s| = 0.02` to `0.16`, and `λ → s−½` (the naive stationary-phase balance) is refuted outright.

**check**   : write down what the derivation predicts, and report *that*, not a monotone function
of it.

**rule**    : **Report the quantity the mechanism names.** A monotone transform is not a neutral
change of units: `√` halves relative errors, so a law tested through it looks twice as good as it
is, and a discrepancy that would have been obvious hides for four rounds.
> F32 asks whether the observable is the one the hypothesis predicts. This is its quantitative
> half: **an observable that compresses the error is a weaker instrument, and the compression
> factor is computable in advance.**

## r206b — a diagnosis that refuted itself, and the refutation is the result

**claimed** : `λ_eff`'s wobble is integer granularity (F25) — `t_1` is stuck at troughs spaced
`π/k`, giving relative jitter `π/(k t_1)` ≈ 8% in `t`, 16% in `λ`, which is the size observed.
Proposed instrument: the envelope crossing `t*`, smallest `t` with `2|G_k(1+2it)| = 1`, smooth and
granularity-free.

**actual**  : **both wrong, and pre-registered clauses caught both.**
- **P1**: the zeros are *not* spaced `π/k` when the weights decay — measured gaps run `0.17` to
  `0.73` in units of `π/k`, at `s = 1` and `s = 2` alike. The even ladder is a **constant-weight**
  phenomenon (Theorem 2(e)), not a general one.
- **P0**: `t*` does not exist. `2|G_k| − 1` at `t = 0` is `+11.2` for `s = 1` — `|G_k|` starts
  *far above* the threshold, because it is essentially `Γ_k/2`. There is no crossing from below.
  **The zero is produced by the phase turning, not by the envelope growing**, so the picture the
  instrument was built on was wrong too.

**check**   : before building an instrument on a quantity, evaluate that quantity at the ends of
its range. `2|G_k| − 1` at `t = 0` is one line and it voids the whole design.

**rule**    : **An instrument defined by "the first crossing" needs its starting sign checked.**
More generally: **a diagnosis and the instrument built to confirm it fail together, because the
instrument is built from the diagnosis** — so the instrument cannot be the test of the diagnosis,
and something independent (here P1, a direct measurement of the spacing) has to be.
> And the honest bookkeeping: **P0 was added to the pre-registration after the first run printed
> "not found".** A pre-registration edited after seeing data is not a pre-registration; the clause
> is marked in the file as added late. **Saying so is the only thing that keeps the label worth
> anything.**

*Round outcome, stated as such:* the `s = 1` constant remains **unsettled**, which was one of the
three registered outcomes. What was gained is a refuted alternative (`λ → s−½`), a scope
correction that reached the paper (the ladder is constant-weight only), and one fewer wrong idea.

## r208 — the note's own worked example was typed, not computed

**claimed** : the Track M note's worked example table gave the first three zeros of the
`A = 0` family at `k = 32`, from the closed form `t_n = ½tan(nπ/k)` that the same note
proves.

**actual**  : **two of the three rows were wrong in the seventh digit**, and both
`k t_n / π` entries with them. They had been *typed from the formula* rather than
evaluated. The correct values are `0.0994561836898290035` and `0.151673341803671196`;
the draft said `0.099456464253591076` and `0.151936089156458`.

**check**   : a script that evaluates the closed form, prints the strings to be copied,
and — as its instrument control — confirms that the **direct sum** vanishes at each of
them to sixty digits. `note1tab_r208`.

**rule**    : **this is F87, committed inside the document that states F87.** The note's
own §"what is verified" says a formula and the number printed beside it are two artefacts
with one author; the author then produced exactly that pair, in the worked example chosen
to be the note's most concrete page.
> **A rule is not installed by being written down in the artefact it governs.** The
> installation is a script, a check, or a habit — and the paragraph explaining the rule
> is, if anything, the place where the author is most likely to feel the rule has already
> been satisfied.

*Scale of the near miss:* every other number in the note came from a log, because a log
existed for it. The one table with no script behind it is the one that was wrong. **The
provenance of a number predicts its correctness better than its importance does.**

## r210 — the pass exceeded its own cap, and said so

**claimed** : `tools/referee_pass.md` caps a pass at **15 units per session**, because past
that the context stops being fresh — which is the only thing the pass has going for it.

**actual**  : the r209 pass on `note1.tex` ran **53 units in one sitting**, the whole
document. The reader judged a ten-page note worth reading whole and did so.

**check**   : none fired. Nothing in the apparatus counts units, so the cap is a sentence
in a procedure document and not a property of anything.

**rule**    : **When a procedure is exceeded for a good reason, record the excess in the
log rather than in the decision.** A pass that quietly runs at 3.5× its cap and comes back
green is indistinguishable, later, from one that ran inside it — and the cap exists to
protect a property (freshness) that the reader cannot self-assess.
> The note's own log now carries the departure in its own words, so it can be disagreed
> with. **The alternative — adjusting the cap to match what we did — is F57's shape: a
> limit loosened until it stops complaining has been switched off with extra steps.**

*Open, deliberately:* whether 15 is the right number for a short self-contained document,
or whether the cap should be stated per *page* rather than per unit. Named, not decided.

## r210 — the disclosure heading, in the other language

**claimed** : the Japanese edition of the note carried a section titled
*道具および計算資源の開示*.

**actual**  : C16 requires the exact declared name, *道具と計算資源の開示*. One particle
different, and to a reader the same section — to the check, absent.

**rule**    : F18's clause, met from the artefact side: **a name that a check keys on is
part of the interface, not a matter of style.** Where a check names a required string, the
artefact copies it; a paraphrase of the predicate is a new predicate, in either direction.

## r211 — a refutation of our own, withdrawn by the model we built to satisfy a gate

**claimed** : (r206, and it reached both the note and Part III) the candidate
`λ_eff → s − ½` is **refuted**: `|λ_eff − (s−½)|` stays in `[0.34, 0.48]` over `k ≤ 2048`
at five exponents and does not shrink.

**actual**  : that band is **exactly what the candidate predicts at those `k`.** The
head/tail model written to clear fable's rung 0 gives
`λ_eff − s = −½ + (log log k)/(2 log k) + O(1/log k)`, and the correction term alone is
`0.13966` at `k = 1024`. So the model's own `λ` sits near `s` over the whole computable
range while tending to `s − ½`. **The two "candidate shapes" registered at r206 are one
statement at two values of `k`.**

**check**   : before recording a limit as refuted, compute the *predicted rate of approach*
and ask whether the tested range could have seen it. Here the approach is `1/log k`: over
`64 ≤ k ≤ 2048` the correction moves from `0.19` to `0.13`. **No decision rule keyed to
"is it shrinking" could have passed, and none should have been trusted to fail.**

**rule**    : **A refutation needs a resolution claim.** *"It did not converge"* is only
evidence if the hypothesis predicts convergence you could have seen; otherwise it measures
the range, not the hypothesis.
> This is F51's clause (*a fail rule must state its measurement floor*) moved from
> precision to **rate**: a decision rule about a limit must state the rate of approach it
> is capable of detecting, and a hypothesis that predicts a slower approach is untested,
> not refuted.

**And the shape of how it was caught is the part worth keeping.** The model was not built
to re-examine r206; it was built because fable-5 imposed a gate — *the phase picture must
postdict the known scale before it earns an instrument* — and the gate's answer came with
a consequence nobody was looking for. **The consequence was registered before the run**
(clause D1 in `rung0_r211`), precisely so that it could not be assembled afterwards to fit
whatever came out.
> **A gate designed to stop you doing something premature can hand you the thing you were
> not able to see.** fable's rung 0 was a brake, and the brake found the error.

*Scope, honestly:* the model is a heuristic. It reproduces twenty-five measured first
zeros to within `9.9%` with no fitted parameter, which is why its asymptote is worth
believing more than our refutation was — but it is `derived`, not `proved`, and the note
now says so at the statement.

## r213 — the condition on the approval removed a load-bearing sentence nobody had noticed

**claimed** : the note was self-contained. It said so twice — *"nothing below uses that"*,
*"this note carries no vocabulary of its own"* — while carrying two citations to the
companion papers, a terminology table whose only two entries existed **because** those
titles were cited, and a bibliography containing nothing else.

**actual**  : Kentaro approved it on one condition: **no sister papers, at all.** Removing
them removed the entire bibliography — and with it **the only place the repository URL
appeared.** `C10` fired immediately: *a reader of this note alone cannot find the code.*
The disclosure section said the verification apparatus is public and did not say where.

**check**   : `C10`, which asks of every paper whether a reader holding only that paper can
reach the repository. It fired on the commit that made the note more self-contained.

**rule**    : **Removing a dependency can remove a service the dependency was quietly
providing.** The citations were doing two jobs — attribution, which the condition rightly
struck, and *locating the evidence*, which nothing else was doing.
> **Before deleting a section, ask what else was reachable only through it.** A
> bibliography is a list of sources to one reader and a set of addresses to another.

*And the shape of the approval is worth its own line.* The condition was one sentence, it
was not about the mathematics, and it made the note **stronger**: a note that cites its
parents invites the reader to go and check whether the parents are any good. **The whole
point of this note is that it does not need them.** Saying so and then citing them twice
was a contradiction that four rounds of review — including a full statement-by-statement
referee pass — did not flag, because everyone reading it already knew the parents.
