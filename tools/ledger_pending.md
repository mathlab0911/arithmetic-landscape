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
