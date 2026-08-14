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
