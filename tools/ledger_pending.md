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
