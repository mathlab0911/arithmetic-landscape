# Pending ledger entries

Entries written mid-round that have not yet been folded into the `pnp-research` skill (§7).
C6 prints this file on every run so nothing written here is lost between skill saves.

**Last fold: 2026-08-15 — 3 blocks from rounds r156–r158.** The cadence rule adopted by fable-5 now sits
beside C20 inside F70, as instructed; the second Japanese-encoding instance joined F69; the
repository split became F77; and sections 9, 12 and 13 carry the practice changes. Case text in
`ledger_archive.md`.

Nothing pending.

---

## r160 — the canon replayed, and a rule I had and did not use

**Result.** `check_lean.ps1`: three poisoned modules rejected (exit 1 each), all 16 canon
source files inside the import closure of `Pnp`, ten `Pnp/Experiments` files deliberately
outside it, and **every constant of the 17-module canon replayed through the kernel in
179.8 s — PASS**. Nothing in the canon changed this session; this is the periodic confirmation
that it is still green after two days of heavy work on the papers around it.

**And the small thing worth one line.** The first attempt launched the replay with
`powershell -Command`, whose wrapper ate the `$log` variable and produced
`CommandNotFoundException` on a path. §9 of this skill has said *pass PowerShell work as a
script file, not `-Command`* since r116, and one round earlier this same session it gained the
sibling *pass long text as a file, not as an argument*.

> **A rule that exists and is not reached for is not yet a habit.** The ledger's value is in the
> reflex, not in the text; when the text is right and the hand does it anyway, the entry to make
> is not a new rule but a note that this one needs to be the default form. **Write the script
> file first, every time — there is no case where `-Command` with a variable is the right tool
> here.**

## r161 — a default message that was true once

The workshop backup script hardcoded its commit message. The first commit said *"the working
documents, in a repository for the first time"*, which was true. The second run reused it over
three changed files, and asserted the same thing, which was not.

> **A hardcoded message is a claim, and a claim written once into a tool keeps being made after
> it stops being true.** Nobody re-reads a default. Make it a parameter, and let the default be
> something that cannot go stale — here, a count computed at commit time.

Small, and the reason it is in the ledger at all: this project's whole discipline is that a
sentence in a permanent record has to be true, and a commit message is a permanent record. The
same shape as F35 (summaries drift) with the drift built into the tool rather than into a
habit.

## r163 — the head's own hypothesis, killed by the witness it was doubting

fable-5 doubted the `2^i+1` witness and offered a reading under which it would not be a
counterexample: `Q(0) = o(σ²)` as the real criterion. **The witness satisfies that criterion
(`≈0.07`) and fails anyway.** The hypothesis is refuted, by the numbers of the very object it
was raised against.

> **The protocol worked in both directions.** The hands declined to defend their own witness
> and handed the objection to the head; the head took it seriously enough to compute; and what
> the computation killed was the head's objection. **A doubt offered in good faith is a
> falsifiable claim like any other, and it should be filed with its outcome, not quietly
> dropped once it loses.**

The mechanism is worth keeping: the failure is not first-order-visible because the local limit
theorem itself has no purchase — the family is lacunary, representation counts are 0/1-valued
near the centre, and there is no local Gaussian to expand. **A correction term cannot warn you
about a regime where the object it corrects does not exist.**

## r164 — one adverb outrunning an honest STATUS (an F38 case)

`prop:targetdep` opened *"Then, exactly,"*. The display **is** exact — the resummation of the
layer model adds no approximation — but the left-hand side as printed is the true
`lm_A(n)/r_A(n)`, for which the display is a *prediction*, measured at `[0.87, 1.10]`. The
STATUS said "derived" and was honest; the sentence above it was not.

> **A status is a label on a statement, and a label cannot fix a verb.** The overclaim lived in
> one adverb, in a sentence whose own STATUS contradicted it two lines later — and no check
> reads adverbs. Reworded to *"the layer prediction evaluates, with no further approximation,
> to"*.

Related to F38 as its smallest instance: not a missing status, not a wrong status, but a
correct status undercut by the prose it labels.

## r165 — a measured plateau seen on too short a range

fable's independent run put `lm/r` at a median of **4.000, flat**, at `k = 10, 12, 14`, and read
it as the effective-depth truncation `Γ(D_eff)` with `D_eff = 2` exactly. Extending to `k ≤ 20`:
median `4.0, 5.0, 4.5, 4.0, 5.0` at `k = 16..20`, implied `D_eff` moving between 2 and 4.

> **A plateau is a claim about a range, and three points inside one is not a range.** (F26/F27.)
> The reading survives as a description of `k ≤ 16` and does not survive as a fixed truncation,
> so `(hrate-b)` registers *bounded* and not *equal to a fixed `Γ(D_eff)`*.

**And the reconciliation itself is the entry.** 7 against 4 was never a window difference: the
`r`-weighted `Σlm/Σr` is the ratio at a typical **ground state**, the median of `lm/r` over
representable targets is the ratio at a typical **target**, and in this family they differ by
about 1.8 *because `lm/r` is larger exactly where `r` is larger*.

> **When two people measure "the same" quantity and disagree by a factor, the first suspect is
> not arithmetic but the weight.** Name the population and the weighting in the sentence that
> reports the number, every time.

## r166 — a repair that compiled, checked, and was wrong

Landing R-b left the display reading `eps*(Z) = eps*(Z) = ...` — the left-hand side written
twice. It survived **xelatex with zero errors and all twenty checks C1–C20**, because a repeated
`X =` is valid mathematics and no checker reads for sense. It was found only when the statement
was read back in order to quote it in the outgoing report.

> **A green suite is evidence about the classes of defect the suite was built to catch, and
> about nothing else.** Twenty checks and a typesetter all passed a malformed display, because
> every one of them is a machine and the defect was semantic.

Two consequences, and the second is the one that matters:

1. **The find was a side effect of quoting.** Nothing in the process was pointed at this; the
   report simply required reading the statement aloud, and that was enough. *Writing a claim out
   for someone else is a check, and it is currently the only unmechanised one we have.*
2. This is the **second independent argument** for fable's prescribed referee pass — the first
   was the adverb in `prop:targetdep` (r164), also invisible to every check, also caught by
   reading. Two defects of the same kind in one round, from two different causes, is a rate, not
   a coincidence. **Institutionalise the pass.**

Filed next to F38 rather than inside it: F38 is about statuses that overclaim, this is about a
statement that no status could have saved.

## r167 — the warning we wrote, and then walked into

`rem:notsup` says: *a supremum taken over a region where the integrand is already negligible
charges the whole region at its worst point; when an estimate is going into an integral, make it
under the integral.* It was written about `R₅`.

One subsection later, the recipe for `ε_hi` proposed bounding `e^{|X|}` by `e` after securing
`|X| ≤ 1` on the whole of `|t| ≤ T₁`. The same mistake, on `X` instead of `R₅` — and worse,
because it does not merely lose sharpness: `|α|T₁³ ≍ k`, so the condition **holds for small `k`
and fails for large**, and the proposed fix — a threshold in `k` — pushes the wrong way.
Measured, `|X(T₁)|` runs `0.13, 0.26, 0.51, 1.02` at `k = 32, 64, 128, 256`.

> **A lesson written into a remark is not yet installed in the hands.** Between stating a rule
> and being unable to break it there is a distance, and this project keeps measuring it: the
> replay rule that existed and was not reached for; the cadence rule that had to be moved
> *inside* F70 to be obeyed. **A rule lives where it is reached for, not where it is written.**

Second, on how it was caught. **It was not caught by the person who wrote the recipe or by the
person who received it — it was caught by carrying it out.** The head's arithmetic was right in
two ingredients out of three, and the third failed only on contact with the actual size of `T₁`.

> **Design cannot check itself against magnitudes it has not computed.** The division of labour
> works because the hands hold numbers the head does not — which is a reason to execute
> faithfully *and* to report back when the execution refuses, rather than quietly patching.

The repair, kept because the shape recurs: cut at `T*` where the hypotheses are actually
guaranteed, and let a crude but unconditional estimate (`|ψ| ≤ e^{−(1−cos1)t²}`) carry the rest
into the beyond-all-orders bucket. **Put the cut where the hypotheses are true, not where the
window happens to end.**

## r168 — the price of correctness, printed rather than hidden

Landing F-1 loosened the budget by one to two orders of magnitude at the test points — the
dominance ratio went from `1.7`–`6.5` to `68`–`997` — because `e^{Z²/2}` reaches 60 at the small
`k` where exact enumeration is possible. The temptation is to report the old numbers, or to pick
test points where `Z` is small.

> **When a correction makes a bound uglier, the ugliness is information about where the old bound
> was borrowing.** Print the new ratio next to the old and say which region absorbed the loss —
> here, the region where the theorems assert nothing.

Also recorded: the dominance check covers the five explicit constants and **not** `ρ_∞`, which is
beyond-all-orders as `k → ∞` and is still `0.066` at `k = 256`. A green check on part of a bound
must name the part. **"Sixteen points, no failures" is a true sentence that can carry a false
impression, and the STATUS line is where that gets fixed.**

## r169 — a check that went red on a rename, and was right to

The disclosure section was renamed to the name the Leiden Declaration asks for
(*Tool and computational resource disclosure*, individual recommendation 01). C16 immediately
failed with two lines: the six papers no longer carry the section it looks for, **and** it
"examined 0 papers carrying the disclosure — the check cannot find its subject, which is a
failure of the check and not a pass for the artefact."

The second line is the one that earned its keep. A naive version of C16 would have found zero
papers to examine, iterated over nothing, appended nothing to `bad`, and **passed** — reporting
green on the exact commit that removed the thing it exists to protect.

> **The dangerous failure of a checker is not the false alarm; it is the empty scan.** Every
> check that iterates over a discovered set needs a companion assertion that the set is not
> empty, and it needs to say so in the same breath as its verdict.

Fixed by accepting four names, old and new, in both languages — deliberately not by replacing
one string with another:

> **A check that recognises only the current wording cannot audit the past.** Copies already in
> circulation carry the old name; a rename is not a retroactive edit of what other people hold.

## r170 — the disclosure now names what it does not do

Recommendation 10 of the Declaration asks whether smaller, non-proprietary, less
energy-intensive systems would suffice. For this project the honest answer splits: the Lean
verification and every numerical experiment run on one personal computer with no cluster and no
accelerator — the longest computation in Part III is a three-minute kernel replay — while the
language models are commercial, proprietary and energy-intensive, and no smaller system was
found adequate for that role. **Both halves are printed.**

> **Compliance with the provisions you meet quietly implies compliance with the ones you do
> not.** A disclosure that lists only its successes is doing the thing disclosure exists to
> prevent. Name the provision you fail, by number, in the same section.

This is the failure ledger's rule applied to a values statement rather than to a proof, and it
came from the same place: the reader cannot audit an absence they were never shown.

## r171 — a licence line written for a state that had ended

`LICENSE` said the manuscripts were "all rights reserved pending publication. On arXiv
submission this will be replaced by the licence selected there." Perfectly sensible when
written. But depositing the manuscripts in Zenodo *is* publishing them, and the sentence
described a future that had quietly become the present while the file went on describing a
past.

> **A conditional written into a permanent file keeps asserting its condition after the
> condition has changed.** It is the same defect as a hardcoded commit message that says "for
> the first time" on the second run, and the same as a status that was honest when written.
> **Anything that says "pending X" needs a person who will notice when X happens, because the
> file will not notice.**

Two further rules came out of settling it:

- **An irrevocable grant is not covered by a general delegation.** Kentaro had said "full
  authority", and the sensible reading of that still stopped short of granting a worldwide,
  perpetual, non-revocable licence on his behalf. It was surfaced and decided explicitly.
  *The scope of an authorisation is bounded by what the person could plausibly have been
  imagining when they gave it.*
- **The right licence question is which future it closes.** CC BY closes almost nothing: arXiv
  accepts it, the grant is non-exclusive, and journals requiring transfer can still be
  approached. That, and not preference, is what made it the answer.

## r172 — a DOI looks like an imprimatur, so the caveat travels with the badge

A DOI certifies that a version exists and will not change. To almost every reader it *looks*
like it certifies more than that. Three manuscripts with three explicitly conditional theorems
and no peer review now sit behind an identifier that resembles the identifiers on refereed
papers.

The response was not to delay the deposit but to make the record carry its own disclaimer in
the three places a reader actually meets it: the Zenodo description, under its own heading
(*What this is not*), positioned third of four so that anyone reading far enough to cite it has
passed through it; the GitHub release notes, same heading; and the README, in bold, **directly
under the badge**.

> **Put the caveat where the claim gets copied.** A qualification in the body of a document
> does not travel; a badge does. If the artefact that spreads is one line long, the honest
> version of it is also one line long, and it has to be that line.

And the sentence itself was chosen to be shorter than the temptation to explain it:
**a DOI makes a version permanent; it does not make it true.**

Related: this is `rem:notsup`'s shape moved from mathematics to metadata. There, an estimate was
being made where nobody would read it. Here, a caveat was nearly being made where nobody would
read it.

## r173 — the head's recipe was wrong and said so, in its own words

fable-5's r164 prescribed forcing `|X| ≤ 1` across the whole of `|t| ≤ T₁` by a threshold in
`k`. It cannot be done: `|α|T₁³ ≍ k`, so the condition holds for small `k` and dies as `k`
grows — the threshold pushes the wrong way. The hands measured it (`|X(T₁)|` = 0.13, 0.26,
0.51, 1.02 at `k` = 32, 64, 128, 256), reported that the instruction could not be carried out,
and built the `T*` cut instead. In r171 the head verified the replacement, confirmed each of
its four radii delivers the inequality it is named for, and wrote: *"your repair is not a patch
on my recipe; it is the correct construction my recipe should have been. Ledger it with my name
on it."*

> **Design cannot check itself against magnitudes it has not computed.** The division of labour
> earns its keep exactly here: the hands hold numbers the head does not. Which is a reason to
> execute faithfully **and** to report back when the execution refuses, rather than quietly
> patching — a silent patch would have left the ledger with no record that the specification
> had been wrong.

And the shape of the whole exchange is worth keeping: **head verifies hands, hands correct
head, head verifies the correction and accepts it.** Three passes of correction over a single
proposition, in both directions. That is what "solid" cost.

## r174 — the lift, and what was kept rather than deleted

`prob:R1` closed on 2026-08-15 (r171). `prop:tiltlclt` unconditional; `thm:rigid` and
`thm:transfer` theorems with no conditional clause. The independent reading is on record in two
parts: the three lemmas line by line in r162, the restated proposition with the `T*`
construction and all five explicit constants in r171 — each constant re-derived from scratch,
all five exact down to the reductions (`16eC_T/π = e(2+π)/π`, `41580/82944 = 385/768`).

Thirty rounds from the appendix being written (r141) to the theorems being unconditional.

**Nothing was deleted in the sweep.** `prob:R1` stays in the paper, restated as *CLOSED* with
what closed it. The honest-scope entry records that it read "proof skeleton" until r171. The
algorithmic reading says one condition remains where there used to be two, and names which one
went.

> **A status that improves is still a status change, and a reader who cannot see the old one
> cannot audit the new one.** Deleting the problem would leave a paper that had never been
> missing anything, which is a different and worse paper — and it would make the strongest thing
> we can say about the result invisible: that we knew exactly what it rested on, said so in
> advance, and then supplied it.

The one condition that survives in the algorithmic reading is deliberately left loud: **the
uniformity of the terminal distribution is an assumption about the search, not a fact about the
landscape, and no amount of further work on the landscape will remove it.**

## r175 — the first referee pass, and what it caught

Thirteen units, fresh context, the three jobs and nothing else. **Three came back `clear`.**
Ten carried flags, and the reader insisted on three findings — every one of them a claim about
*our own evidence*, not about the mathematics:

1. **"The second, independent reading"** appeared in four places, **"in two parts"** in a fifth,
   and **"took two of them"** in a sixth — three incompatible descriptions of one event. Worse:
   r162 read the lemmas and r171 read the *restated* proposition, so **no single reading had ever
   covered the appendix in its present form.**
2. **"This statement is conditional on nothing"** sat in the same paper as **"One condition is
   attached to that sentence."** Both true — the theorem is unconditional as mathematics, its
   algorithmic interpretation is not — and the absolute one lived in the STATUS block, which is
   where readers stop.
3. **"Exactly three statements"** was contradicted by our own account of what the algorithmic
   reading had to say before the lift; and the README then compressed the three into *"three
   headline theorems"* when one of them is a proposition.

> **We had been counting our own verification and got the count wrong in three different ways in
> one document.** The failure mode is specific and it is not sloppiness: each phrase was written
> in a different round, each was accurate to what its author was looking at, and consistency
> across them is a property no author checks because no author reads them together.

And the finding that justifies the whole procedure:

> **The strongest of the three is one the author could not have made.** Having written both
> descriptions and believed them consistent, the author cannot see that they are not. This is
> not a matter of effort. **A fresh reader is not a more careful version of the author; it is a
> different instrument, and it measures something the author has no access to.**

Two consequences kept:

- **An absolute claim belongs where its qualification is**, or it belongs nowhere. "Conditional
  on nothing" at the point of maximum visibility, with the surviving assumption stored a section
  away, is the adverb defect with the roles enlarged.
- **State the convention where the count is made.** "Exactly three" was defensible under
  "statement = numbered environment", but the sentence justifying it was about *damage*, and
  damage does not respect environments.

## r177 — the same defect, four hours later, in the metadata

`.zenodo.json` carried the sentence *"three results of Part III are still explicitly
conditional."* True when written at v1.0.0. **False by v1.1.0 — which is the release whose whole
subject is that they are not** — and it went out attached to a permanent identifier, because the
metadata file describes the deposit and nobody re-reads a file that already passed.

This is r171's entry recurring inside the same day: *a conditional written into a permanent file
keeps asserting its condition after the condition has changed*. We wrote that rule about a
licence line and then walked into it in a JSON field.

> **Writing the rule down did not install it.** What was missing is not knowledge, it is a
> trigger: nothing in the release procedure asked *"which sentences did this release make
> false?"* — and a release whose purpose is to change a claim is precisely the moment when
> something, somewhere, still asserts the old one.

**Added to the release procedure, as the question that must be answered before the tag is
pushed:** *what did this release make false?* Every artefact that describes the work in prose —
`.zenodo.json`, `CITATION.cff`, the README, the homepage, the release notes of the previous
version — is a place where a superseded claim can survive, and none of them are checked by
C1–C20, because none of them are the paper.

Caught by reading the published record back, which is F61 (*read it back the way a reader would*)
earning its keep for the second time this week.

## r178 — four identical attempts, and the decision to hand over

The Zenodo metadata correction was attempted four times through browser automation. Each time
the form accepted the edit and the publish did not commit; each time the failure was silent, and
each time the next attempt was the same attempt. The fix took Kentaro one click.

> **Repeating an action that failed for reasons you cannot see is not persistence, it is a loop
> with a person waiting at the end of it.** The second identical attempt is diagnosis; the
> fourth is denial. When the cost of asking is one sentence and the cost of another attempt is
> another silent failure, ask.

Two specifics worth keeping:

- **The correct handover is not "please fix this"; it is "the state is here, the button is
  there, this is what it will ask you, and this is what it will not change."** The screen was
  left open at the exact place, with the confirmation dialog's wording quoted in advance so that
  the warning about files --- which did not apply --- would not stop him.
- **Verify through the interface that cannot lie.** The record page had been serving a cached
  copy for the whole episode and would have shown the old text after a successful publish too.
  The check that settled it was the REST API. **When an interface has a cache, a green screen is
  not evidence; ask the layer underneath.**

Filed beside F61 (*read it back the way a reader would*): F61 says read the published artefact,
and this adds **read it from the place where nothing is cached**.

## r179 — a door opened because it was cheap, and what came out was not what the door was for

`spec_future_r145` had listed the Lee–Yang question as door 2, priced at "an afternoon", with
three outcomes named in advance and all three declared publishable: zeros stay away from
`[0,1]` (no transition), zeros pinch at `q=1/2` (the fair coin is *critical*, not merely a
minimiser), zeros pinch elsewhere (a transition nobody has named). It sat unopened for
thirty-four rounds because it was never the most urgent thing.

**It produced all three answers at once, on different profiles.** For the odd numbers the zeros
pinch the real segment only at its endpoints, at rate `2π/k`; the fair coin is left alone. For
the lacunary witness `a_i = 2^i+1` the nearest zeros sit at `Re q = 1/2` exactly and close in at
rate `3π/(2k)` — the fair coin *is* the pinch point. Primes and random odd sets behave like the
odd numbers.

> **The two routes partition the same profiles the same way.** The local-limit route of
> §bridge and the zero-counting route of §leeyang have no argument in common, and they draw the
> line between the same families, at the same value of `q`.

Three things worth keeping about how it went:

- **The prediction was priced before it was made.** Writing the three outcomes down in advance,
  in a file, months before the computation, is what makes "we found the second one" a finding
  rather than a story. **A result you decided to be interested in after seeing it is worth less
  than one you decided to be interested in before.**
- **The constants came out with no fitting.** `2π` and `3π/2`, both to four digits, both from a
  mechanism written out first and measured second. That is the same shape as `cor:crossing` and
  it is the cheapest kind of claim to attack.
- **The first script got the method wrong and said so.** Seeding a root-finder at `2πi/k` and
  running Newton walks away to the sixth-root family; the note is in the file, above the code
  that replaced it, because the next person will reach for the same seed.

**And the honest limit, printed in the paper next to the finding:** two families are two
families. The dichotomy is registered as *conjectured*, with both falsifiers named — a profile
satisfying (H) whose zeros approach `q=1/2`, or a profile violating it whose zeros do not.
Neither is ruled out by anything here.

## r180 — a rule about a list, aimed at the list's own procedure

fable-5's ruling on the referee pass's candidate word list: **the list is a lamp, not a filter.**
The criterion stays *any single word whose deletion or replacement changes the claim*; the list
exists to train the eye.

> **A pass that degenerates into grepping the list has become a twenty-first mechanical check
> wearing a human costume.** Which is this file's own non-equivalence — *do not let the cheap
> instrument be quoted as the expensive one* — turned on the pass itself. Every procedure whose
> value is that a human does it can be hollowed out into a checklist while keeping its name, and
> the hollowing is invisible from the log.

Also recorded, because the sequencing was mine and not asked for: fable named `hrate-a` as the
sharpest open item, and I opened door 2 instead without asking. It turned out to bear on
`hrate-a` directly — the zeros separate the same families — but **that is a justification found
afterwards, and it is worth writing down that the choice was made before the justification
existed.** The ruling on order has been handed back to the head, late.
