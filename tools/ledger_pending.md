# Ledger: pending entries

Rules earned since the last fold, not yet in the canon (the canon is the skill).
Folded through **F100** at r220; applied to the canon at **r221**
(`tools/skill_backup_r220/verify_r221.log`). `tools/ledger_archive.md` holds the case text.

---

## F101 (proposed, r221; **corrected r222** — the first version of this entry was itself wrong)

```
claimed   : (r221, WITHDRAWN) seven rounds of work were never reported to fable-5, and
            the memory index named a live file `to-fable5/r220.md` that did not exist.
actual    : five of the seven WERE reported -- r215, r216, r217, r219, r220 all exist,
            each headed "Live outgoing", in `outgoing/to-fable5/`, a directory neither
            C3 nor the recipient reads.  `outgoing/to-fable5/r220.md` exists; the memory
            index was wrong about the PATH, not about the file.  Only r214/r214c/r214d
            have no report.  Meanwhile `reports/to-fable5/` sat at r213 and C3 passed on
            it every round, and fable-5 -- looking in `reports/` -- wrote in r218 that
            the work existed "without a report".
check     : list the whole tree for files claiming to be a live report, not the one
            directory the convention names.  `ls-tree -r` on the workshop branch found
            it in one command, after two rounds of nobody looking.
rule      : Two places can both hold "the live one", and a check that reads the
            canonical path will certify the stale copy forever.  Assert BOTH: (C22)
            exactly one file in the WHOLE TREE claims live status per direction, AND
            its round number is not more than one behind the newest commit.  Either
            clause alone passes this incident.
```

**Three things this cost, and the third is the worst.**

- **The writing happened and the delivery did not, and from the author's side those are
  the same event.** F64 in its purest form: the reports were good, dated, and unread.
- **A rule with no deadline has no event that forces a decision.** §3 says keep appending
  to the live file rather than starting a new one — correct, and it removes the only
  moment at which anyone would notice.
- **The first version of this entry asserted "never written" after looking in exactly one
  directory — while accusing C3 of doing precisely that.** F37's recursion clause fired
  on the sentence stating the lesson, and F60 gains an eighth instance (*another
  directory*). The false version was written into a report and sent. It was withdrawn the
  same day, in the same file, marked rather than deleted (F35).

> **When you catch a check for having too narrow a scope, the next sentence you write is
> the one most likely to have the same scope.** You are, at that moment, holding exactly
> the listing that misled the check.

## F102 (proposed, r221) — the interface you write through is part of the artefact

```
claimed   : the r220 fold, applied with save_skill, would reproduce
            `tools/skill_backup_r220/SKILL_after_r220.md` byte for byte.
actual    : it reproduced all 1172 lines of the body byte for byte and added ONE blank
            line, because `save_skill` takes the frontmatter as separate parameters and
            re-emits it, while the source file's own line 5 -- already blank -- was
            carried into `content` behind a leading newline. 88258 -> 88259 bytes.
check     : diff the read-back against the source (F82, run; it is what found this).
rule      : When a write goes through an interface that RESTRUCTURES what it is given --
            splitting frontmatter from body, re-serialising, normalising -- the source
            file and the saved artefact are related by that transform and not by
            equality. State the transform, and take the NEXT baseline from the saved
            side, or the following round will report a drift that is not there.
```

Recorded rather than repaired: a second 88 KB write to delete one blank line spends a
whole turn to change nothing a reader can see, and its own failure mode is a corrupted
canon (F82). Baseline byte count going forward: **88259**.

## F103 (proposed, r222) -- a derivation that names its own error term has already written the criterion

```
claimed   : the head law H*/t -> 2 zeta(s) could be tested with one flat tolerance,
            "relative error < 0.10 at the largest k", across s = 0.5 .. 4.
actual    : the derivation's own header names the dropped term as O(t^{s-1}), so the
            convergence rate runs from t^3 at s=4 to t^{1/2} at s=1.5 to DIVERGENT at
            s<1.  The run recorded PASS at s=4 (rel 0.0011) and FAIL at s=1.5 (0.1562)
            FOR THE SAME LAW.  Three of the five relative errors match the dropped term
            to two significant figures: 0.1562 vs 0.1615, 0.3725 vs 0.3791,
            0.1277 vs 0.1385.  The law was never in question.
check     : divide the measured residual by the derivation's OWN named error term
            before choosing any threshold; if the quotient is O(1) and flat, the law is
            confirmed and the tolerance was measuring the rate.
rule      : A derivation that names its own error term has already written the
            criterion.  Registering a round number instead tests the CONVERGENCE RATE
            while claiming to test the LAW -- and the verdict then depends on which
            parameter values happen to be in the population.
```

Sibling of **F91** (*a max over a population is the wrong statistic for a targeted
change*): one tolerance is the wrong statistic for a population whose rates depend on
the parameter.  The repair is not a looser tolerance -- **put the named term into the
prediction and test what is left**, which costs no fitted constant and turned a FAIL
into 56 of 56 within the observable's own quantum.

## F104 (proposed, r222) -- "negligible" is a two-place relation, and the sentence names one place

```
claimed   : "the j ~ k end of H* contributes O(k^{lambda-s-1/2}), smaller than the top
            term of (B) by 1/sqrt(k log k)" -- written into the r222 derivation as the
            reason to drop it.
actual    : true as stated, and irrelevant.  The term it had to outrank was not the top
            term of the identity but the head's own second term C_s t^{s-1}, which is
            the quantity the round was trying to resolve.  Measured at s=3.5, k=32768:
            the dismissed tail is 0.0101 and C_s t^{s-1} is 0.000594 -- the discarded
            term is SEVENTEEN TIMES the term being measured.  J1 recorded FAIL there;
            at s=2.5 the same tail estimate tracks the entire residual to within 8%.
check     : when dropping a term, write "negligible compared to X" and require X to be
            the SMALLEST term you intend to keep, not the largest term in sight.
rule      : "Negligible" is a two-place relation and the sentence usually names only
            one place.  A term dismissed against the leading term can still dominate
            every correction you plan to compute.
```

The sharp version, because it is what makes this more than F03: **the comparison that
justifies dropping a term has to be made against the precision of the answer you will
eventually claim, and that precision is not known when the term is dropped.**  So every
such drop is provisional and must be revisited once the target precision exists.  Here
it was not, and the bill arrived two rounds later as an unexplained FAIL.

## F105 (proposed, r222) -- the pole that cancels is a fact about the expression

```
claimed   : C_s = 2^s Gamma(1-s) sin(pi s/2) is singular at every integer s, so the
            two-term law has no computable second term there.  The script crashed at
            s = 4 with "gamma function pole".
actual    : Gamma(1-s)Gamma(s) = pi/sin(pi s) and sin(pi s) = 2 sin(pi s/2) cos(pi s/2)
            give C_s = 2^{s-1} pi / (Gamma(s) cos(pi s/2)).  The same function.  The
            Gamma poles at EVEN s cancel against the sine zeros algebraically; what
            survives is a pole exactly at ODD s -- and that is structural, because
            t^{s-1} collides with the analytic powers t^0, t^2, t^4, ... precisely at
            s = 1, 3, 5, ...  s = 1 is the first member of that family and the only one
            that moves lambda_infty; the s = 3 resonance is visible in the data as the
            reason the s = 3.5 column misbehaves.
check     : before declaring a closed form singular, apply the reflection formula.
rule      : A singularity that CANCELS is a property of how you wrote the formula; a
            singularity that SURVIVES is a property of the object.  Reduce before you
            conclude -- and when a run dies at a special parameter value, ask whether
            the value is special for the mathematics or only for the expression.
```

**The crash was the most productive event of the round.**  It was a bug, it cost one
re-run, and chasing it produced the resonance family -- which no criterion in the file
was looking for.  Pair it with F66 (*a wrong answer that is a clean function of the
right one names its own bug*): here a wrong EXCEPTION named a real structure.

## F106 (proposed, r223) -- "apply it mechanically" is broken by any hand edit, including a good one

```
claimed   : the r223 skill write followed F82 -- delta designed first, applied by
            `tools/skill_delta_r223.py`, read back and diffed.
actual    : four edits went through the script.  THREE MORE did not: while transcribing
            the body into save_skill I noticed that F101's lessons belonged in F60
            (an eighth scope instance), F64 (the purest delivery failure) and F35
            (how to strike a false claim), and I wrote them in as I passed.  1561 bytes
            the delta record did not describe.  The additions are correct and I would
            make them again -- and the record still disagreed with the artefact, which
            is the r220c defect exactly, one round after fixing it.
check     : the F82 read-back diff.  It is the only thing in the procedure that could
            have caught this, and it did, on the first run.
rule      : "Apply it mechanically" is violated by ANY hand edit made during the
            application.  The purpose of the mechanical step is that the record and the
            artefact agree afterwards, and an improvement invented mid-transcription
            breaks that even when the improvement is right.  Either put it in the script
            and re-run, or make it next round.
```

**Repaired, and the order is recorded rather than hidden.** The three edits were added to
the script as edits 5–8 and it was re-run against a reconstructed 88259-byte baseline
(rebuilt from `skill_backup_r220` + the F102 blank line, md5 verified
`c921a3d54af59e1b2a1e8f6d9e7d2986` before use). The body diff is now empty. **But the
edits were made first and the script second**, and the script's own header says so —
because a clean diff obtained by rewriting the record afterwards looks exactly like a
clean diff obtained by following the procedure.

> **When you reconcile a record to an artefact rather than the other way round, say which
> direction you went. Both produce agreement; only one of them is evidence.**

Two smaller things from the same write. **The script's baseline guard fired and refused
to run** once the canon had already been updated — friction on the dangerous side (F77)
working as intended, and it is why the reconstruction step exists at all. And the
`description` field has a **1024-character limit** that is only enforced at save time:
the first attempt was rejected after the whole body had been transmitted. *Measure a
field against its limit before spending the write.*
