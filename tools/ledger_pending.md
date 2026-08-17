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
