#!/usr/bin/env python3
# c22_control_r223.py -- the negative control for C22.  A check is not finished when it is
# written; it is finished when it has been watched to go RED on the corruption it exists to
# catch (skill section 7.0, F47, F57).
#
# THE CORRUPTIONS ARE BUILT THE WAY THE WORLD BUILT THEM, not the way the check happens to
# notice (F47).  Both reproduce the r222b incident exactly:
#
#   A.  a report file appears OUTSIDE `reports/`, headed "**Live outgoing.**".  This is
#       literally what `outgoing/to-fable5/` held, five times over, for seven rounds while
#       C3 reported one live report per direction and passed.
#   B.  rounds ship and the live report stops moving.  Simulated by adding an experiment
#       script and log for a round far ahead of the live report -- which is what "the work
#       exists as commits and logs without a report" means on disk.
#
# A POSITIVE CONTROL RUNS FIRST AND LAST (F61): the suite must be green before each
# corruption and green again after it is removed, or a red run proves nothing about C22.
#
# Everything is restored in a `finally`, and the script prints what it created so that a
# crash leaves a trail rather than a mystery.

import io
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = __file__[:-3] + ".log"
LINES = []


def say(s=""):
    print(s, flush=True)
    LINES.append(s)
    io.open(LOG, "w", encoding="utf-8", newline="\n").write("\n".join(LINES) + "\n")


def run_suite():
    """Read the suite's output as UTF-8, explicitly.

    First version used text=True and inherited the console codec.  On Windows that is
    cp932, check.py prints Japanese and en-dashes, and the reader thread died with
    UnicodeDecodeError -- so `out` came back empty and the control reported that C22 had
    NOT fired on corruptions where it demonstrably had.  F58: when the verification tool
    disagrees with something you have just measured, test the tool before believing it.
    """
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "check.py")],
                       capture_output=True, cwd=ROOT, env=env)
    dec = lambda b: (b or b"").decode("utf-8", "replace")
    return r.returncode, dec(r.stdout) + dec(r.stderr)


def fails_named(out, tag):
    return [l.strip() for l in out.splitlines() if l.strip().startswith("FAIL") and tag in l]


say("=" * 96)
say("c22_control_r223 -- negative control for C22.  A check that has never been seen red")
say("                   is a check nobody has tested.")
say("=" * 96)

verdicts = []

# ----------------------------------------------------------------- positive control, before
say()
say("--- P0  POSITIVE CONTROL: the suite is green BEFORE any corruption ---")
rc, out = run_suite()
say("    exit=%d   %s" % (rc, "all checks pass" if rc == 0 else "NOT GREEN"))
if rc != 0:
    for l in out.splitlines():
        if l.strip().startswith("FAIL"):
            say("      " + l.strip())
    say()
    say("ABORT: the tree is not clean, so a red run below would prove nothing about C22.")
    sys.exit(1)
verdicts.append(("P0 green before", True))

created = []
try:
    # ------------------------------------------------------------- control A
    say()
    say("--- A  C22a: a live report appears outside the report directories ---")
    say("       reproducing outgoing/to-fable5/, which held five of these for seven rounds")
    d = os.path.join(ROOT, "outgoing", "to-fable5")
    os.makedirs(d, exist_ok=True)
    f = os.path.join(d, "r299.md")
    io.open(f, "w", encoding="utf-8", newline="\n").write(
        "# r299 -- control, not a real report\n\n"
        "**Live outgoing.** Incoming from you is `to-opus5/r218.md`.\n\n"
        "Created by c22_control_r223.py and deleted by it.  If you are reading this in a\n"
        "commit, the control crashed and did not clean up.\n")
    created.append(f)
    rc, out = run_suite()
    hits = fails_named(out, "C22a")
    ok = rc != 0 and bool(hits)
    say("       exit=%d   C22a fired: %s" % (rc, bool(hits)))
    for h in hits:
        say("       " + h[:200])
    say("       -> %s" % ("PASS (the check went red)" if ok else "FAIL: C22a did not fire"))
    verdicts.append(("A  C22a fires on a live claim outside reports/", ok))
    os.remove(f)
    created.remove(f)
    try:
        os.rmdir(d)
    except OSError:
        pass

    # ------------------------------------------------------------- control B
    say()
    say("--- B  C22b: rounds ship and the live report stops moving ---")
    say("       adding an experiment script+log for r299 while the live report sits at r222")
    stem = os.path.join(ROOT, "lean", "pnp", "ctrl_r299")
    for ext in (".py", ".log"):
        io.open(stem + ext, "w", encoding="utf-8", newline="\n").write(
            "# control artefact for c22_control_r223.py -- deleted by it\n")
        created.append(stem + ext)
    rc, out = run_suite()
    hits = fails_named(out, "C22b")
    ok = rc != 0 and bool(hits)
    say("       exit=%d   C22b fired: %s" % (rc, bool(hits)))
    for h in hits:
        say("       " + h[:240])
    say("       -> %s" % ("PASS (the check went red)" if ok else "FAIL: C22b did not fire"))
    verdicts.append(("B  C22b fires when the live report trails the tree", ok))

    # ------------------------------------------------------------- control C
    say()
    say("--- C  THE CHECK MUST NOT FIRE ON THE PAST: archived reports keep their claim ---")
    say("       every archived report says 'Live outgoing' -- it did, honestly, when it was")
    say("       live.  A check that convicts the past cannot audit it (F78).")
    arch = os.path.join(ROOT, "reports", "to-fable5", "archive")
    n = 0
    for fn in os.listdir(arch):
        if fn.endswith(".md"):
            head = io.open(os.path.join(arch, fn), encoding="utf-8", errors="replace").read()
            if "ive outgoing" in head[:4000]:
                n += 1
    say("       archived reports carrying the phrase: %d" % n)
    say("       C22a fired on them in run A or B: %s"
        % any("archive" in h for h in fails_named(out, "C22a")))
    okc = n > 0 and not any("archive" in h for h in fails_named(out, "C22a"))
    say("       -> %s" % ("PASS (exempted, and the exemption has a subject)" if okc
                          else "FAIL: either nothing to exempt, or the past was convicted"))
    verdicts.append(("C  archived claims exempted, exemption non-empty", okc))

finally:
    for f in created:
        if os.path.exists(f):
            os.remove(f)
    d = os.path.join(ROOT, "outgoing", "to-fable5")
    if os.path.isdir(d) and not os.listdir(d):
        os.rmdir(d)

# ----------------------------------------------------------------- positive control, after
say()
say("--- P1  POSITIVE CONTROL: green again once the corruptions are removed ---")
rc, out = run_suite()
say("    exit=%d   %s" % (rc, "all checks pass" if rc == 0 else "STILL RED -- cleanup failed"))
if rc != 0:
    for l in out.splitlines():
        if l.strip().startswith("FAIL"):
            say("      " + l.strip())
verdicts.append(("P1 green after cleanup", rc == 0))

say()
say("=" * 96)
for name, v in verdicts:
    say("  [%s] %s" % (name, "PASS" if v else "FAIL"))
say()
if all(v for _, v in verdicts):
    say("C22 has now been observed red on both of the corruptions it exists to catch, and")
    say("green on the artefact it must not convict.  Before this run it had only ever agreed")
    say("with a tree that was already correct, which is no evidence at all.")
else:
    say("C22 IS NOT VERIFIED.  One or more controls did not do what it was built to do, so")
    say("nothing here licenses trusting the check.  Fix the control or the check and re-run.")
    say("(The first version of this script printed the confident sentence above")
    say(" unconditionally, under a table of FAILs -- an explanation that cannot fail is not")
    say(" protecting the claim, it is occupying the slot where a real one would go, F47.)")
say("done.")
sys.exit(0 if all(v for _, v in verdicts) else 1)
