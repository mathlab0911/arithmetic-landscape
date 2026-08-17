#!/usr/bin/env python3
"""Apply the r214-r220 ledger fold (F88-F100) to the skill, mechanically.

F82 applied to ourselves: the distillation is written exactly and separately, applied by
machine rather than by hand, and the result is diffed before it is believed.  This file IS
the distillation; `skill_delta_r220.md` is generated from it so the record and the patch
cannot drift apart (r187: a number retyped is a new number -- so is a paragraph).

    python3 tools/skill_delta_r220.py

Reads  tools/skill_backup_r200/SKILL_after_r200.md   (verified byte-identical to the live skill)
Writes tools/skill_backup_r220/SKILL_after_r220.md   (what save_skill must be given)
       tools/skill_delta_r220.md                     (the human-readable record)
       tools/ledger_archive.md                       (APPENDED with the pending case text)
       tools/ledger_pending.md                       (emptied, LAST)

ORDER IS LOAD-BEARING.  The archive is written BEFORE the pending file is emptied, because
at r200b the pending file was emptied first and the case text had to be recovered from the
previous commit.  A fold that loses the evidence keeps only the conclusion, which is the
half a later reader cannot check.

Every anchor must occur EXACTLY ONCE or the run aborts: a replace that matches nothing does
not raise by itself, and missing looks exactly like success (F71).  And F69, three times
over: anchors are grepped out of the real text, never retyped from memory, because an
anchor that straddles a line break matches nothing.
"""

import hashlib
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'tools', 'skill_backup_r200', 'SKILL_after_r200.md')
OUTDIR = os.path.join(ROOT, 'tools', 'skill_backup_r220')
OUT = os.path.join(OUTDIR, 'SKILL_after_r220.md')
DELTA = os.path.join(ROOT, 'tools', 'skill_delta_r220.md')
PENDING = os.path.join(ROOT, 'tools', 'ledger_pending.md')
ARCHIVE = os.path.join(ROOT, 'tools', 'ledger_archive.md')

# The live skill as verified byte-identical at r220 (md5 of the plugin cache == md5 of this
# backup).  If this does not match, the source is not what is running and the fold must stop.
EXPECT_SRC_LEN = 80197

# The anchor: the last line of F87's block, immediately before the next subsection heading.
# Grepped from the file, not retyped (F69).
ANCHOR = "### 7.4 Writing and documents — F35–F42"

# ---------------------------------------------------------------------------
# The thirteen entries, written as canon: one rule in bold, the evidence that bought it in
# parentheses, and only the follow-up that a later reader could not reconstruct.
# ---------------------------------------------------------------------------
ENTRIES = """- **F88** **A fact every reader already knows is a fact nobody checks.** *(v1.2.0 was published
  dated one day in the future. The date was never computed — it was copied forward from a
  drifting round header until three artefacts agreed with it: three agreeing sources, one
  origin. Zenodo caught it, because Zenodo does not take our word for the date.)*
  > **When a claim is about the world rather than about our computation, ask the world.**

  C2 requires every number quoted in a report to be a substring of a committed log, and that
  rule silently assumes the number is a **measurement**. `date` costs nothing and does not
  remember yesterday's answer. **This was the first defect in this project detected from
  outside the apparatus**; every earlier one, it caught itself. The archived deposit keeps the
  wrong date permanently, because the tag now carries a DOI — recorded rather than hidden.
- **F89** **Never define an instrument's sampling grid in units of the quantity it measures.**
  *(The constant-weight control scanned `[0, 4r]` where `r` is the exact answer, so a uniform
  grid has a node AT `r` for every grid size — the instrument was aiming its samples at the one
  point where a sign-change detector has nothing to detect. It passed at 200000 points and
  failed at 20000, and the failure looked like a resolution problem, which it was not.)*
  > **A red light whose cause is unrelated to the thing being certified is worse than no light,
  > because people learn to explain it away.**
- **F90** **A refuted falsifier retires the hypothesis it named, not the neighbourhood it was
  drawn from.** *(r206 registered "the zeros sit on an evenly spaced ladder", shot it down
  correctly, and concluded that no quantisation argument is available. The zeros need not be
  evenly spaced for the FIRST one to be pinned to a phase grid of spacing `π/k` — which it is,
  and which bounded the residual at 69 of 69 points.)* The wider claim was never tested.
- **F91** **A max over a population is the wrong statistic for a targeted change.** *(A
  refinement aimed at one column of five was registered on worst case and on "the improvement
  must be concentrated at `s=1`". The second passed, the first failed — the worst case had
  migrated into a control column the refinement was never aimed at.)* Register the criterion at
  the resolution of the claim.
- **F92** **A safety margin that jumps around must be measured in every run, not extrapolated.**
  *(Every `t_1` this project had published came from a 1500-point scan whose resolution had
  never been stated. A 200000-point re-scan moved none of the 25 values — but the margin,
  measured for the first time, was as low as 1.88 steps, and ran 54, 20, 21, 1.9, 7.6 with no
  trend, because it depends on how nearly tangent the excursion is.)* "It worked last time" is
  not evidence.
- **F93** **Before registering a criterion, list the outcomes it can express and check that the
  interesting ones are on the list.** *("Does not apply", "applies and is right" and "applies and
  is wrong" are three outcomes, not two. A criterion written to expect a large error recorded
  FAIL when the honest answer was that the predictor has no domain there — a STRONGER
  confirmation than the criterion could say.)*
- **F94** **When a residual has structure, the first suspect is a simplification you made
  yourself.** *(A model equation was written at r211 and never solved; a threshold version of it
  was solved instead. Three rounds later the threshold version's residual was measured, bounded
  at 69/69 by a quantum derived on paper, and named a property of the observable. Solving the
  equation as written took the worst error from 0.165 to 0.0021 and left 1.9% of that quantum.)*
  > **A derivation that fits a residual you created will look exactly like a discovery.**

  Both halves belong in the same entry: the quantum was correctly derived, correctly bounded,
  and mostly ours. What survived is that the oscillation is real; what did not is that it makes
  anything unmeasurable — it is deterministic, so it can be removed rather than tolerated.
- **F95** **An idiom that works because of a value's TYPE rather than its value has no test
  protecting it.** *(`mpf(repr(x))` ran in three scripts because `x` was a Python float; one
  branch left it a `numpy.float64`, whose `repr` under numpy 2 is `np.float64(0.178…)`, and the
  failure surfaced after the header had printed, so it looked like a timeout.)* Convert at the
  boundary; never rely on `repr` to produce a number.
- **F96** **An effect attributed to one steep term is only attributed once the terms called flat
  have been differentiated.** *(A slope was taken from the oscillator alone. The head was a
  Dirichlet kernel — an oscillation with the same `k` — whose derivative at the same point is
  equal to it at leading order, measured ratio 0.926 → 0.9988 over `k = 64…4096`. Including both
  doubles the slope and turns a rate `O(1/k)` into a constant `1/(2k)`, matching seven points.)*
  > **A function that is SMALL at a point can be STEEP there.** `Hp(π/k) = 0` exactly, slope
  > `O(k²)`.

  "It varies slowly" is a claim about a derivative and costs one line to check.
- **F97** **Before registering a criterion, ask whether its quantity could have come out
  otherwise.** *(In one run, three of four criteria measured quantities an identity in the setup
  had already fixed. One read `L + Ω = 2T sin(kθ₁)` while claiming to test a candidate; its
  control ran the same statistic at a point where `kθ₁ = π` exactly, so it was measuring `sin π`,
  zero to 38 digits.)*
  > **If an identity in the setup determines it, the criterion has no power — and a PASS from it
  > is worse than no criterion, because it will be cited.**

  This is F93 sharpened, and its fourth occurrence in three rounds is what made it a habit
  rather than a run of accidents.
- **F98** **In a product of two factors, the concentration of one is not the concentration of the
  product.** *(A missing term `Ω = 2Σ w_j(ρ^j−1)cos jθ` was argued to be positive because "the
  weights concentrate at small `j`, where `cos > 0`". It is negative at 12 of 12 points: the
  factor `ρ^j − 1` VANISHES at small `j`, so `Ω` lives where the weights do not.)* Ask where the
  product lives before naming a term after one of its halves.
- **F99** **State tolerances relative unless the magnitude is known in advance.** *(A criterion
  demanded `1e-45` ABSOLUTE agreement for an identity the same script evaluates from `1e0` to
  `1.3e62`, and recorded FAIL on an identity that was exact to 60 significant digits.)*
  > **The check that is easiest to pass is the one most likely to set the tolerance.**

  The far-from-zero points were nearly worthless as a test — one term dominates — and they are
  what broke the tolerance. Where absolute IS right (at a zero, where the sum cancels totally),
  say why it is right there and not elsewhere. **And when a criterion is replaced after a run,
  keep and cite the original log**: a pre-registration edited after seeing data is not one, and
  leaving the first one standing is how that stays true.
- **F100** **When a sum resists, before approximating it, ask what it looks like after summation
  by parts.** *(Four rounds built, refined, diagnosed and rescued a head-plus-geometric-tail
  model of `Re G_k`. One Abel summation replaces all of it with an exact identity for arbitrary
  weights, whose coefficients are the weight DECREMENTS, which contains the project's existing
  theorem as the case where the new sine series is empty, and which yields a two-line theorem
  covering every non-increasing profile.)*
  > **We reached for a model because the model was the thing we had just built, not because the
  > sum demanded one.**

  The tell was there from the first round: the whole difficulty was the competition between
  decaying `w_j` and growing `ρ^j`, and summation by parts is the standard instrument for
  exactly that competition.
"""


def die(msg):
    print("ABORT: " + msg)
    sys.exit(2)


def main():
    src = io.open(SRC, encoding='utf-8').read()
    if len(src.encode('utf-8')) != EXPECT_SRC_LEN:
        die("source is %d bytes, expected %d -- not the live skill"
            % (len(src.encode('utf-8')), EXPECT_SRC_LEN))

    if src.count(ANCHOR) != 1:
        die("anchor occurs %d times, expected exactly 1" % src.count(ANCHOR))

    for n in range(88, 101):
        tag = "**F%d**" % n
        if tag in src:
            die("F%d is already in the canon" % n)
        if ENTRIES.count(tag) != 1:
            die("F%d occurs %d times in the new entries" % (n, ENTRIES.count(tag)))

    out = src.replace(ANCHOR, ENTRIES + "\n" + ANCHOR)

    # ---- verify before writing anything ----
    for n in range(88, 101):
        if out.count("**F%d**" % n) != 1:
            die("after patch F%d occurs %d times" % (n, out.count("**F%d**" % n)))
    if len(out) <= len(src):
        die("patched skill is not longer than the source")

    # ---- 1. ARCHIVE FIRST.  The order is the lesson from r200b. ----
    pend = io.open(PENDING, encoding='utf-8').read()
    n_cases = pend.count("\n## F")
    if n_cases != 13:
        die("pending holds %d cases, expected 13" % n_cases)
    arch = io.open(ARCHIVE, encoding='utf-8').read()
    io.open(ARCHIVE, 'w', encoding='utf-8', newline='\n').write(
        arch.rstrip("\n")
        + "\n\n\n" + "=" * 78 + "\n"
        + "# Folded at r220: F88-F100 (rounds r214-r220)\n"
        + "# Case text, kept because the canon keeps only the rule.  A fold that loses the\n"
        + "# evidence keeps the half a later reader cannot check.\n"
        + "=" * 78 + "\n\n"
        + pend.strip() + "\n")

    # ---- 2. the skill ----
    if not os.path.isdir(OUTDIR):
        os.makedirs(OUTDIR)
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(out)

    # ---- 3. the record ----
    io.open(DELTA, 'w', encoding='utf-8', newline='\n').write(
        "# Skill delta r220 -- the F88-F100 fold\n\n"
        "Generated by `tools/skill_delta_r220.py`; do not edit by hand, edit the script.\n\n"
        "Source `%s` (%d bytes, md5 `%s`)\n"
        "Result `%s` (%d bytes, md5 `%s`)\n\n"
        "Thirteen entries inserted immediately before the heading `%s`, at the end of\n"
        "section 7.3, in canon form: one rule in bold, the evidence that bought it, and only\n"
        "the follow-up a later reader could not reconstruct.\n\n"
        "The case text moved to `tools/ledger_archive.md` BEFORE `tools/ledger_pending.md`\n"
        "was emptied.\n\n## The entries as inserted\n\n%s"
        % (os.path.relpath(SRC, ROOT), len(src.encode('utf-8')),
           hashlib.md5(src.encode('utf-8')).hexdigest(),
           os.path.relpath(OUT, ROOT), len(out.encode('utf-8')),
           hashlib.md5(out.encode('utf-8')).hexdigest(),
           ANCHOR, ENTRIES))

    # ---- 4. empty pending, LAST ----
    io.open(PENDING, 'w', encoding='utf-8', newline='\n').write(
        "# Ledger: pending entries\n\n"
        "Rules earned since the last fold, not yet in the canon (the canon is the skill).\n"
        "Folded through **F100** at r220; `tools/ledger_archive.md` holds the case text.\n\n"
        "*(empty)*\n")

    print("source  : %s  %d bytes" % (os.path.relpath(SRC, ROOT), len(src.encode('utf-8'))))
    print("result  : %s  %d bytes" % (os.path.relpath(OUT, ROOT), len(out.encode('utf-8'))))
    print("inserted: F88-F100, each exactly once")
    print("archive : appended %d lines of case text BEFORE emptying pending" % pend.count("\n"))
    print("pending : emptied")
    print()
    print("Now hand %s to save_skill (overwrite: true)." % os.path.relpath(OUT, ROOT))


if __name__ == '__main__':
    main()
