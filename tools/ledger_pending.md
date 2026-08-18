# Ledger: pending entries

Rules earned since the last fold, not yet in the canon (the canon is the skill).
Folded through **F108** at r225; `tools/ledger_archive.md` holds the case text.
**The baseline for the next fold is the SAVED canon, not this repository's backup** (F102).

*(empty)*

---

## F109 (proposed, r225b) — F106 was violated by the write that installed F106

```
claimed   : the r225 fold applied its changes mechanically, per F106 -- the entry being
            installed by that very write.
actual    : four more edits reached the canon by hand during the transcription, 888 bytes
            the delta record did not describe: two practice notes in section 9 (decode a
            child process's output; the sandbox can create in the mount but not delete),
            one line in section 13 Never (do not hand-edit the canon during a mechanical
            application -- F106 ITSELF), and the fold-ordering clause in section 14.
            Every one of them is correct and I would write them again.
check     : the F82 read-back diff, against a reference the script had produced
            mechanically from a baseline whose md5 was fixed beforehand.  Four hunks,
            nothing else -- which is also the whole audit, because a mechanical product
            of an identified baseline is a sound reference in a way a hand-kept one is not.
rule      : A rule does not begin to bind when it is written down, and it does not begin
            to bind when it enters the canon either.  F106 was granted, transcribed, and
            broken in a single act.  **The moment of maximum exposure to a rule is the
            moment you are handling the paragraph that states it** -- because that is
            exactly when the surrounding text is in front of you and an improvement is
            one keystroke away.
```

**Three things worth keeping, and the third is the useful one.**

- **The recurrence is not carelessness twice; it is the same affordance twice.** Both times
  the hand edits were made while re-reading paragraphs that *invited* them — F101's lessons
  belonged in F60/F64/F35 (r223), and today's practice notes belonged in §9/§13/§14. **The
  transcription is the one moment when the whole document is in working memory, so it is
  simultaneously the best time to improve it and the only time doing so is forbidden.**
- **The repair is structural, not intentional.** "Try harder next time" has now failed twice.
  What would actually work: **the delta script writes the body to a file, and the transcription
  is a copy of that file and nothing else** — with no reading of the surrounding text at all.
  Whether that is achievable through `save_skill` is an open question and is named here as one.
- **A verification script that cannot run is worse than none**, and I started one: it imported
  the delta script to recover its `EDITS`, but that script aborts at its own baseline guard
  before `EDITS` exists. Deleted rather than repaired, because the diff already in hand was a
  complete audit. **Before building an instrument, check whether the measurement has already
  been made.**

## F110 (proposed, r226) -- a ratio is a margin only if the measured thing is the required thing

```
claimed   : M6 registered "over a window of length L = pi(1+4t^2)/k the phase k theta
            advances by at least 2 pi", and the run printed advance/2pi = 2.000 at every
            point -- read, and nearly reported, as a factor-two safety margin.
actual    : the code measured [t_1 - L, t_1 + L].  That is width 2L, so the advance was
            4 pi and the "2.000" was the WIDTH, not margin.  Measured over the window
            actually registered -- forward from t_1 by L -- the advance is 0.999995 of
            2 pi at k=32768 and 0.998664 at k=1024.  THE REGISTERED CLAIM IS FALSE, by a
            hair, and in the direction nobody checks: arctan is concave, so the forward
            sweep is slightly SLOWER than the linearised rate 2k/(1+4t^2) that produced
            the constant pi.
check     : measure the interval the criterion names.  A symmetric window around a point
            is not the forward window from it.
rule      : A ratio of measured to required is a margin ONLY IF the measured quantity is
            the required quantity.  When it is not, the discrepancy presents itself AS
            safety -- which is the one disguise that stops anybody looking.
```

**The repair costs a constant and nothing else.** State the window as `2 pi (1+4t^2)/k`; the
bracket (Z) picks up a factor two in a term that is `O(1/k)` against a `T ~ sqrt(log k / k)`,
so it remains `o(T)` and the conclusion `lambda -> s - 1/2` is untouched. **The argument was
never in danger; the printed evidence for one of its steps was.**

Two things worth keeping. **A claim derived from a linearisation inherits the sign of the
linearisation's error**, and here concavity meant the honest constant is larger than the
linearised one — so "exactly 2 pi in exactly the linearised time" was always going to fail by
a hair. **And this is F49's shape** (*when a quantity carries an index, measure it AT that
index*) moved from an index to an interval: the criterion named a set, and a different set
was measured.

## F111 (proposed, r227) -- PowerShell's location is not the process's working directory

```
claimed   : `cd <dir>; [System.IO.File]::ReadAllText("Pnp.lean")` reads that directory's
            file.  The command then printed "added to Pnp.lean".
actual    : .NET methods resolve a relative path against the PROCESS working directory,
            which Set-Location does not change.  It looked in the outputs folder, threw
            FileNotFoundException, and the import was never added -- while the success
            message printed anyway, because it sat in the same if-branch as the write
            rather than being conditional on it.
check     : absolute paths with every .NET call; and make a success message conditional
            on the thing succeeding.
rule      : PowerShell's location and the process's working directory are two different
            things and only cmdlets track the first.  **And a message printed in the same
            branch as an operation is not evidence the operation happened -- it is
            evidence the branch was entered.**
```

**What caught it was not the message; it was the next line.** `Get-Content` (a cmdlet, so it
*does* follow the location) printed the tail of the real file, and `AbelWeights` was not in
it. **A read-back by a different mechanism than the write is worth more than any status
string** — the same shape as F58 and as F107's harness, one layer down.

**And then the closure guard caught it a second time**, from the outside: `check_lean.ps1`
exited on *"outside the closure of Pnp — NOT built, NOT replayed, but present:
Pnp.Theory.AbelWeights"*. That guard exists because of F55 (r117 had a canon file nothing
imported). **It has now caught a second, entirely different route to the same state**, which
is the argument for building guards on the property rather than on the incident.

**F111, second clause (r227) — a count can wear the name of an instrument that never printed it.**
C9 fired on the README's Lean counts, and fixing them showed the *replayed modules* line had been
citing **`lean4checker`** against a number `lean4checker` does not print: C9 computes the import
closure of `Pnp` (18: sixteen `Theory` files, `Basic`, and the root), while the checker's banner
counts source files (17). Both are right; the README asserted one and credited the other, and C9
never noticed because **C9 was comparing the README against C9**. *(F55 — the control is on a
proxy — and F87 — a number and the thing that supposedly produced it, printed side by side, are
not a check on each other.)* Repaired by naming both populations in the sentence, which is F27's
standing clause moved from measurements to counts: **name the population where the number is
reported, every time.**


---

## F112 (proposed, r233) — a status is a claim about the repository, and `.gitignore` is a scope no check reads

```
claimed   : thm:decayrate in the public note carries STATUS{proved}, the programme's
            strongest tier, whose definition in the note's own sec:verified is "a written
            proof, plus an independent re-derivation along a disjoint route".
actual    : the written proof was lean/pnp/spec_stheorem_r229.md, which .gitignore
            excludes (the rule dates from r117, when twenty-four design documents were
            found inside the public repository).  Both halves were right on their own
            terms: the status was earned, and the exclusion was correct policy.  What was
            wrong was that the FILE'S ROLE HAD CHANGED -- from a design document waiting
            for ratification into the proof of record for a published theorem -- and its
            location had been chosen under the old role.
check     : for every statement whose status names evidence, fetch that evidence by the
            route a reader has: the public raw URL.  Costs one request per status.
rule      : **A status is a claim about the repository as much as about the mathematics.**
            When a statement declares a tier, the artefact that discharges it must be
            reachable from the artefact the reader holds -- and no check in this project
            reads .gitignore, so an exclusion silently un-discharges every status that
            depends on the excluded file.  **When a document is promoted in role, re-ask
            where it lives; the old location was chosen to answer a question that has
            changed.**
```

**Why no instrument saw it.** C16 asks whether the paper discloses AI use *in the paper*;
C12 asks whether cited scripts exist with logs; C1 asks whether a script has a log. **None
of them asks whether a named piece of evidence is in the repository at all** — and C1's blind
spot in exactly this direction had been recorded four rounds earlier, at r229c, when fable's
`fverify_r224` turned out to be untracked. *The same gap, found twice by hand, on two
different artefacts, without the intervening round producing a check.*

**The repair is not mathematics and took one file move**, which is the uncomfortable part:
the cost of the defect was entirely in *not having looked*.

---

## F113 (proposed, r233) — compression loses factors, and the compressed form is the one the reader gets

```
claimed   : "the sine series concentrates near j ~ 1/2t rather than near j ~ k; ITS LIMIT
            IS 2 zeta(s), and the top term must supply the rest."  (note1.tex, the
            mechanism paragraph for thm:decayrate, both editions.)
actual    : FALSE AS WRITTEN.  The sine series tends to 0 with t.  The quantity whose
            limit is 2 zeta(s) is the series DIVIDED BY t, which is how it enters the
            identity: sum_{j>=1} j D_j = sum_j w_j = zeta(s) and sin(j theta)/t -> 2j.
            The factor 1/t is present and correct in the written proof, one paragraph
            upstream in a different document, and was lost in the compression to prose.
check     : restate the compressed sentence from the mathematics WITHOUT the source in
            view, then compare.  Reading the summary against the derivation verifies the
            summary against a description of itself (F52), because the eye supplies the
            missing factor from the neighbouring display.
rule      : **A summary is a new claim, not a shorter copy of an old one, and it must be
            re-derived rather than checked against its source.**  Both authors read this
            sentence and both read it correctly, because both knew which quantity was
            meant -- which is precisely the reason neither could see it.  Sibling of F60's
            eps*(Z) = eps*(Z): valid mathematics, wrong claim, invisible to every check and
            to the typesetter.
```

**The pass that found it is the same instrument as r175 and r209**, and the signature is now
three for three: *every finding was a claim about our own evidence or our own quantifiers,
and none was an error in the mathematics.* **What this project lacks is not a better checker.
It is a reader who is not us**, and the referee pass is the only mechanism that supplies one.

**Second clause, from the same pass — an all-red result is a measurement of scope, not of
quality.** Nine of nine units were flagged on text that was green on twenty-two mechanical
checks and clean in two builds. **The number to report is not "nine defects" but "nine
defects in the region no check looks at"**, and the honest form of a green suite is therefore
always *"green on the classes it was built for"*.
