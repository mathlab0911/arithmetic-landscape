#!/usr/bin/env python3
# skill_delta_r225.py -- fold F101-F108 into the canon.
#
# fable-5's r224 section 5: "pending list is now grant-complete -- fold at your next
# canonical fold, with the mover script, baseline 88259 (F102)."
#
# *** THE BASELINE IN THAT INSTRUCTION IS STALE, AND F102 IS WHAT SAYS SO. ***
# 88259 was the canon BEFORE r223 wrote Kentaro's absolute-path rule into it.  The saved
# canon is now 91456 bytes, md5 f7a60bc4063ef75f78b98deda0da7915.  F102's rule is "take
# the NEXT baseline from the saved side, or the following round will report a drift that
# is not there" -- so the rule corrects the head who granted it.  Recorded rather than
# silently fixed: the number fable wrote is the number fable had, and it was right when
# he wrote it.
#
# METHOD (F82, and F106 which was bought doing exactly this one round ago):
#   1. every edit is applied BY THIS SCRIPT, not by hand during transcription.  F106 says
#      any hand edit made during the application breaks the point of the mechanical step,
#      even a good one.  If something needs adding, it gets added HERE and re-run.
#   2. every anchor is asserted to occur EXACTLY ONCE; anything else aborts.
#   3. the case text moves to ledger_archive.md BEFORE ledger_pending.md is emptied
#      (the r200b ordering: a transfer that clears the source before the destination is
#      confirmed is not a transfer).
#   4. the result goes to tools/skill_backup_r225/SKILL_after_r225.md and the read-back is
#      diffed against it before anything is believed.

import hashlib
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = sys.argv[1] if len(sys.argv) > 1 else (
    "/sessions/youthful-loving-gauss/mnt/.claude/skills/pnp-research/SKILL.md")
OUTDIR = os.path.join(ROOT, "tools", "skill_backup_r225")
OUT = os.path.join(OUTDIR, "SKILL_after_r225.md")
PENDING = os.path.join(ROOT, "tools", "ledger_pending.md")
ARCHIVE = os.path.join(ROOT, "tools", "ledger_archive.md")
LOG = __file__[:-3] + ".log"
LINES = []

BASE_BYTES = 91456
BASE_MD5 = "f7a60bc4063ef75f78b98deda0da7915"


def say(s=""):
    print(s, flush=True)
    LINES.append(s)
    io.open(LOG, "w", encoding="utf-8", newline="\n").write("\n".join(LINES) + "\n")


src = io.open(CACHE, encoding="utf-8", newline="").read()
b = src.encode("utf-8")
say("baseline : %s" % CACHE)
say("bytes    : %d   (expected %d)" % (len(b), BASE_BYTES))
say("md5      : %s" % hashlib.md5(b).hexdigest())
if len(b) != BASE_BYTES or hashlib.md5(b).hexdigest() != BASE_MD5:
    say("ABORT: this is not the canon I was written against.  Refusing to edit something")
    say("       I have not identified (F102).")
    sys.exit(1)

EDITS = []

# ---------------------------------------------------------------- (1) C22 into the C-list
EDITS.append((
    "**C21**/F83 no file in the tree is\n"
    "  *named* like a credential — plus\n",
    "**C21**/F83 no file in the tree is\n"
    "  *named* like a credential, **C22**/F101 exactly one artefact in the WHOLE TREE claims to\n"
    "  be the live report per direction and the direction being written is not more than one\n"
    "  round behind the newest round in the tree — plus\n",
))

# ---------------------------------------------------------------- (2) the section heading
EDITS.append((
    "### 7.8 Scales, boundaries, and the artefacts nobody checks --- F83--F100\n"
    "\n"
    "Bought over rounds r181--r200:",
    "### 7.8 Scales, boundaries, and the artefacts nobody checks --- F83--F108\n"
    "\n"
    "Bought over rounds r181--r225.  F83--F100 came from rounds r181--r200:",
))

# ---------------------------------------------------------------- (3) F101-F108
NEW = """  The tell was there from the first round: the whole difficulty was the competition between
  decaying `w_j` and growing `ρ^j`, and summation by parts is the standard instrument for
  exactly that competition.

**F101--F108 were bought over r221--r225**, the fortnight in which a false protocol failure was
reported and withdrawn the same day, the canon was rewritten twice, and the `s > 1` branch got
an argument. Case text in `ledger_archive.md`.

- **F101** **Two places can both hold "the live one", and a check that reads the canonical path
  will certify the stale copy forever.** *(C3 --- one live report per direction --- passed for
  seven rounds while five files headed "**Live outgoing.**" sat in `outgoing/to-fable5/`, a
  directory neither the check nor the recipient reads. fable-5, looking in `reports/`, wrote
  that the work existed "without a report". The writing had happened; the delivery had not, and
  **from the author's side those are the same event** --- F64 in its purest form.)* Asserted as
  **C22**, and it needs BOTH clauses because either one alone passes that incident: exactly one
  artefact in the whole tree claims live status per direction, AND the direction being written
  is not more than one round behind the newest round in the tree.
  > **When you catch a check for having too narrow a scope, the next sentence you write is the
  > one most likely to have the same scope.** You are, at that moment, holding exactly the
  > listing that misled it.

  That is not a flourish: the round that found the stale file went on to assert the reports had
  **never been written**, after listing exactly one directory. F37's recursion clause, and F60's
  eighth instance. The false sentence was withdrawn the same day, in the same file, **struck
  through rather than deleted** (F35) with the correction at the head where a cold reader meets
  it first.
- **F102** **When a write goes through an interface that RESTRUCTURES what it is given ---
  splitting frontmatter from body, re-serialising, normalising --- the source file and the saved
  artefact are related by that transform and not by equality.** State the transform, and **take
  the next baseline from the SAVED side**, or the following round will report a drift that is not
  there. *(A second instance arrived immediately and from an unexpected direction: the ruling
  that ordered this very fold named the pre-r223 byte count. **The rule corrected the head who
  had just granted it** --- and the stale number was right when he wrote it, which is why it is
  recorded rather than quietly fixed.)*
- **F103** **A derivation that names its own error term has already written the criterion.**
  Registering a round number instead tests the CONVERGENCE RATE while claiming to test the LAW,
  and the verdict then depends on which parameter values happen to be in the population. *(One
  flat 10% tolerance recorded PASS at `s=4` and FAIL at `s=1.5` for the same law; three of five
  relative errors matched the dropped term to two significant figures.)* Sibling of F91. **The
  repair is not a looser tolerance --- put the named term INTO the prediction and test what is
  left**, which costs no fitted constant and turned a FAIL into 56 of 56 inside the observable's
  own quantum.
- **F104** **"Negligible" is a two-place relation and the sentence usually names only one
  place.** A term dismissed against the leading term can still dominate every correction you
  plan to compute. *(A tail dropped for being smaller than the top term by `1/√(k log k)` --- true
  --- turned out to be seventeen times the second-order term the round was trying to resolve.)*
  > **The comparison that justifies dropping a term must be made against the precision of the
  > answer you will eventually claim, and that precision does not exist when the term is
  > dropped.**

  So every such drop is provisional and has to be revisited once the target precision exists.
- **F105** **A singularity that CANCELS is a property of how you wrote the formula; one that
  SURVIVES is a property of the object.** Reduce before you conclude, and when a run dies at a
  special parameter value, ask whether the value is special for the mathematics or only for the
  expression. *(A crash at `s=4` on `2^s Γ(1−s) sin(πs/2)`; the reflection formula turns it into
  `2^{s−1}π/(Γ(s)cos(πs/2))`, the Γ poles at even `s` cancel against the sine zeros, and what is
  left is a pole at ODD `s` --- exactly where `t^{s−1}` collides with the analytic powers
  `t^0, t², t⁴, …`. **The bug named a structure no criterion in the file was looking for.**)*
- **F106** **"Apply it mechanically" is violated by ANY hand edit made during the application,
  including a good one.** The purpose of the mechanical step is that the record and the artefact
  agree afterwards; an improvement invented mid-transcription breaks that even when the
  improvement is right. Either put it in the script and re-run, or make it next round.
  > **When you reconcile a record to an artefact rather than the other way round, say which
  > direction you went. Both produce agreement; only one of them is evidence.**
- **F107** **A harness written to test a check is itself untested code, and its two
  characteristic failures are ENCODING at the boundary and a CONCLUSION that does not read its
  own results.** *(A control read the suite with `text=True`, inherited `cp932`, died on the
  suite's Japanese, captured EMPTY output, and reported that the check had not fired on
  corruptions it had demonstrably fired on ten minutes earlier. **"Said nothing" and "could not
  hear" are different facts.** Then, under a table of two FAILs, it printed "the check has now
  been observed red on both of the corruptions it exists to catch.")* Decode every process
  boundary explicitly. **What saved the check was F58**: the harness disagreed with something
  already measured, so the harness was tested first --- reversed, the check would have been
  loosened until it stopped failing, which is F57 reached by a different road.
- **F108** **"Test the rate" is well defined only for a single-rate error.** When the error is a
  sum of terms with different rates, a one-rate criterion silently tests whichever term happens
  to dominate in your population, so the verdict is a fact about the parameter range and not
  about the argument. *(Registered against `t^{s−1}` for an error the same file's header states
  as `O(t^{s−1}) + O(k^{−1/2}/log k)`; stable to 1.02 at `s=1.5` where the first dominates,
  drifting by 2.9 at `s=3.5` where the second does.)* **This is F103 committed inside the
  criterion written to apply F103, by F103's author, one round later --- and F47's corollary
  (*when the quantity is a sum, ask whether the summands can be measured separately*) was
  already canon, with the two summands in adjacent printed columns three tables above.**
  > **Having the rule, and having the data already in the right shape, was not enough. The
  > application is a separate act, in a different place, and that is the place to check.**

  Second clause, from the control in the same run: **a control's threshold is a claim too.** It
  demanded a factor of three of separation without anyone computing what separation the
  mechanism predicts; the direction was right and the number was invented. Filed as a FAIL
  rather than reinterpreted, because a threshold rewritten after seeing the data is what the
  asterisk exists to prevent (F99).

### 7.4 Writing and documents — F35–F42
"""
EDITS.append((
    "  The tell was there from the first round: the whole difficulty was the competition between\n"
    "  decaying `w_j` and growing `ρ^j`, and summation by parts is the standard instrument for\n"
    "  exactly that competition.\n"
    "\n"
    "### 7.4 Writing and documents — F35–F42\n",
    NEW,
))

out = src
for i, (old, new) in enumerate(EDITS, 1):
    n = out.count(old)
    say("edit %d   : anchor occurs %d time(s)  [%s...]" % (i, n, old.split("\n")[0][:60]))
    if n != 1:
        say("ABORT: anchor for edit %d occurs %d times, not exactly once." % (i, n))
        sys.exit(1)
    out = out.replace(old, new)

# ------------------------------------------------- case text to the archive, BEFORE clearing
pend = io.open(PENDING, encoding="utf-8", newline="").read()
arch = io.open(ARCHIVE, encoding="utf-8", newline="").read()
MARK = "## Case text folded at r225 (F101-F108)"
if MARK in arch:
    say("archive  : the r225 block is already present; not appending twice (idempotent)")
else:
    arch = arch.rstrip("\n") + "\n\n\n" + MARK + "\n\n" + \
        "Moved verbatim out of `ledger_pending.md` when F101-F108 entered the canon.\n" + \
        "The canon keeps the rule; this file keeps what it cost.\n\n" + \
        pend.split("---\n", 1)[-1].strip() + "\n"
    io.open(ARCHIVE, "w", encoding="utf-8", newline="\n").write(arch)
    say("archive  : appended %d bytes of case text -> %d bytes total"
        % (len(pend.encode("utf-8")), len(arch.encode("utf-8"))))

# verify the destination really holds it before clearing the source (the r200b ordering)
back = io.open(ARCHIVE, encoding="utf-8", newline="").read()
need = ["F101", "F102", "F103", "F104", "F105", "F106", "F107", "F108"]
missing = [x for x in need if ("## %s " % x) not in back and ("%s (proposed" % x) not in back]
if missing:
    say("ABORT: the archive does not contain %s; NOT clearing the pending file." % missing)
    sys.exit(1)
say("archive  : all eight entries confirmed present in the destination")

io.open(PENDING, "w", encoding="utf-8", newline="\n").write(
    "# Ledger: pending entries\n"
    "\n"
    "Rules earned since the last fold, not yet in the canon (the canon is the skill).\n"
    "Folded through **F108** at r225; `tools/ledger_archive.md` holds the case text.\n"
    "**The baseline for the next fold is the SAVED canon, not this repository's backup**"
    " (F102).\n"
    "\n"
    "*(empty)*\n")
say("pending  : cleared, after the destination was verified and not before")

os.makedirs(OUTDIR, exist_ok=True)
io.open(OUT, "w", encoding="utf-8", newline="").write(out)
ob = out.encode("utf-8")
say("")
say("written  : %s" % OUT)
say("bytes    : %d   (was %d, delta %+d)" % (len(ob), BASE_BYTES, len(ob) - BASE_BYTES))
say("md5      : %s" % hashlib.md5(ob).hexdigest())
say("body md5 : %s" % hashlib.md5("\n".join(out.split("\n")[4:]).encode("utf-8")).hexdigest())
say("")
say("NEXT, AND NOT OPTIONAL: pass this file's body to save_skill, re-read the cache, and diff")
say("it against this file.  Expected: zero differences.  F106 -- if something needs adding,")
say("it gets added to THIS SCRIPT and re-run, never typed into the transcription.")
say("done.")
