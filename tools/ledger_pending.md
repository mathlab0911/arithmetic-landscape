# Ledger: pending entries

Rules earned since the last fold, not yet in the canon (the canon is the skill).
Folded through **F100** at r220; applied to the canon at **r221**
(`tools/skill_backup_r220/verify_r221.log`). `tools/ledger_archive.md` holds the case text.

---

## F101 (proposed, r221) — an existence check is not a currency check

```
claimed   : the live outgoing report was `reports/to-fable5/r220.md`, carrying the
            r214-r220 work. The memory index asserted this for two rounds running.
actual    : the live file was `reports/to-fable5/r213.md`, last appended at r213.
            SEVEN rounds -- r214, r214c, r214d, r215, r216, r217, r219, r220 -- were
            never written into it. fable-5 read the commits and logs instead, at
            Kentaro's direction, and said so in r218: "your r214-r217 work exists as
            commits and logs WITHOUT a report ... your report is still owed."
check     : C3/F21 asserts one live report per direction. It passed on every one of
            those rounds, because a live file existed. Nothing anywhere compares the
            round number IN the live filename to the round number of the newest commit.
rule      : A check on the EXISTENCE of an artefact is not a check on its CURRENCY.
            Where the procedure says "rename it to the current round", the rename is
            the ONLY observable that separates a report which is up to date from one
            that stopped being written -- so assert it: the live filename's rNNN must
            not trail the newest committed round by more than one. (Proposed as C22.)
```

**Three things worth keeping with it.**

- **The accretion rule has no deadline in it.** §3 says to keep appending to the live
  file rather than starting a new one. That is the right rule and it removes the only
  event that ever forced a decision — creating a file. An append that never happens
  looks exactly like an append that was not needed yet.
- **The stale claim was in memory, which is the artefact with no checker.** F35 says the
  summary population drifts together and faster than the papers; here it drifted *away
  from a document that did not exist*. **A memory line naming a file is a testable claim,
  and `ls` is the test.** Nothing ran it for two rounds.
- **The compensating action hid the cost.** fable read the primary sources and produced a
  correct r218, so nothing downstream broke — which is precisely why nobody looked. **A
  gap that someone else routes around stops generating symptoms while still being a gap**;
  the only trace it left was one sentence in fable's preamble, in a file addressed to me.

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
