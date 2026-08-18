#!/usr/bin/env python3
# skill_delta_r223.py -- Kentaro's instruction of 2026-08-18, applied to the canon.
#
# INSTRUCTION (chat, 2026-08-18, after r222b):
#   "報告書の確認は、絶対パス
#      C:\\Users\\amake\\Claude\\Projects\\study\\reports\\to-opus5
#      C:\\Users\\amake\\Claude\\Projects\\study\\reports\\to-fable5
#    を確認し、読むようにしてください。スキルに入れ込んでください。
#    私から、fableからの報告書読んで、もしくはopusからの報告書を読んで
#    といった際は、[実際を]見に行くようにしてください。"
#
# WHY IT IS BEING GIVEN.  r222b: I told him five reports did not exist.  They did, in
# `outgoing/to-fable5/`, and I had answered from memory plus one directory listing.  The
# instruction removes the discretion that made that possible: there is one pair of
# absolute paths, and "read the report" means open the file at one of them.
#
# METHOD (F82).  save_skill replaces the canon whole and nothing checks it, so:
#   1. this script makes the change MECHANICALLY from the saved canon (baseline 88259
#      bytes, md5 c921a3d54af59e1b2a1e8f6d9e7d2986) -- not by hand;
#   2. every anchor is asserted to occur EXACTLY ONCE, and the script aborts otherwise;
#   3. the result is written to tools/skill_backup_r223/SKILL_after_r223.md;
#   4. after save_skill, the read-back is diffed against that file before it is believed.
# Baseline is taken from the SAVED side, not from the r220 backup (F102).

import hashlib
import io
import os
import sys

CACHE = sys.argv[1] if len(sys.argv) > 1 else (
    "/sessions/youthful-loving-gauss/mnt/.claude/skills/pnp-research/SKILL.md")
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skill_backup_r223")
OUT = os.path.join(OUTDIR, "SKILL_after_r223.md")
LOG = __file__[:-3] + ".log"
LINES = []


def say(s=""):
    print(s, flush=True)
    LINES.append(s)
    io.open(LOG, "w", encoding="utf-8", newline="\n").write("\n".join(LINES) + "\n")


src = io.open(CACHE, encoding="utf-8", newline="").read()
say("baseline : %s" % CACHE)
say("bytes    : %d" % len(src.encode("utf-8")))
say("md5      : %s" % hashlib.md5(src.encode("utf-8")).hexdigest())
if len(src.encode("utf-8")) != 88259:
    say("ABORT: baseline is not the 88259-byte saved canon (F102 says take it from the")
    say("       saved side).  Refusing to edit something I have not identified.")
    sys.exit(1)

# --------------------------------------------------------------- the four edits
EDITS = []

# (1) section 3: the paths become absolute, and the rule is stated where they are.
EDITS.append((
    "```\n"
    "study/reports/to-fable5/rNNN.md     written by opus-5, for fable-5\n"
    "study/reports/to-opus5/rNNN.md      written by fable-5, for opus-5\n"
    "study/reports/to-*/archive/         everything older\n"
    "```\n",
    "```\n"
    "C:\\Users\\amake\\Claude\\Projects\\study\\reports\\to-fable5\\   written by opus-5, for fable-5\n"
    "C:\\Users\\amake\\Claude\\Projects\\study\\reports\\to-opus5\\    written by fable-5, for opus-5\n"
    "C:\\Users\\amake\\Claude\\Projects\\study\\reports\\to-*\\archive\\   everything older\n"
    "(the same tree from the sandbox: /sessions/<session>/mnt/study/reports/...)\n"
    "```\n"
    "\n"
    "> **Kentaro's instruction, 2026-08-18: those two absolute paths are the only place a\n"
    "> report lives, and checking a report means LISTING THE DIRECTORY AND OPENING THE\n"
    "> FILE.** When he says *fable の報告書を読んで* or *opus の報告書を読んで*, go to the\n"
    "> path and read it. Never answer from memory, from this file, or from a summary of\n"
    "> the round — and never from one directory when the question is *what exists*.\n"
    "\n"
    "He gave that instruction the day a report claimed five reports did not exist. They\n"
    "did, in `outgoing/to-fable5/`, each labelled *live outgoing*, five at once; memory\n"
    "named one of them at the wrong path and the correction then denied all five (F101).\n"
    "**A rule that says \"the reports are in X\" is worth nothing until X is a path you\n"
    "actually type.** If a file addressed to you turns up anywhere else, that is a defect\n"
    "to report, not a place to start reading from.\n",
))

# (2) section 5: locating yourself means listing, not remembering.
EDITS.append((
    "   model you are, and read the live report addressed to you first.\n",
    "   model you are, and read the live report addressed to you first — **by listing the\n"
    "   absolute directory in \u00a73 and opening the file**. A report you did not list is a\n"
    "   report you are guessing about, and memory is the artefact with no checker.\n",
))

# (3) section 13: the prohibition, where the prohibitions live.
EDITS.append((
    "- **Report a check as passing when it examined nothing** (F60).\n",
    "- **Report a check as passing when it examined nothing** (F60).\n"
    "- **Say what a report contains, or whether one exists, without opening the absolute\n"
    "  path in \u00a73 in this session** (F101). \"I believe it says\" is not an answer.\n",
))

# (4) section 14: memory must not be the source for report state.
EDITS.append((
    "- **Secrets never go into memory or any repository.**\n",
    "- **Secrets never go into memory or any repository.**\n"
    "- **Memory may point at a report; it may never stand in for one.** Every claim in\n"
    "  memory about which report is live is a claim about the filesystem, and `ls` is the\n"
    "  test (F101). Re-derive it at the start of every session rather than carrying it.\n",
))

# ---------------------------------------------------------- edits 5-7, ADDED BY HAND
# HONEST NOTE, r223b.  Edits 1-4 above were designed before the write and applied by this
# script.  Edits 5-7 were NOT: I added them while transcribing the body into save_skill,
# because F101's lessons plainly belonged in F60, F64 and F35 and I was already looking at
# those paragraphs.  The F82 read-back diff caught them -- 1561 bytes the delta record did
# not describe -- which is the whole reason that diff exists.
#
#   RULE (proposed F106): "apply it mechanically" is violated by ANY hand edit made during
#   the application, including a good one.  The point of the mechanical step is that the
#   record and the artefact agree afterwards; an improvement invented mid-transcription
#   breaks that even when the improvement is right.  Either add it to the script and re-run,
#   or make it next round.  I chose to add it to the script -- so the record now matches --
#   but the edits were made first and the script second, and that order is recorded here
#   rather than hidden by the fact that the diff is now clean.
EDITS.append((
    "  the project. Seven, each found only because someone happened to look:**\n",
    "  the project. Eight, each found only because someone happened to look:**\n",
))
EDITS.append((
    "  6. *The check catches its own author, ten rounds later.* C19 was built at r131 for exactly that\n"
    "     drift, and at r141 it caught the same hand shipping an appendix in English only. **A check is\n"
    "     written not because you were careless once but because you will be careless again**, and the\n"
    "     second time you are the subject.\n",
    "  6. *The check catches its own author, ten rounds later.* C19 was built at r131 for exactly that\n"
    "     drift, and at r141 it caught the same hand shipping an appendix in English only. **A check is\n"
    "     written not because you were careless once but because you will be careless again**, and the\n"
    "     second time you are the subject.\n"
    "  7. *Another directory, and the author repeats it in the sentence of the accusation.* C3 read\n"
    "     `reports/to-fable5/` and passed for seven rounds while five live reports sat in\n"
    "     `outgoing/to-fable5/`. The round that found the stale file then asserted the reports had\n"
    "     never been written \u2014 after listing exactly one directory. **When you catch a check for\n"
    "     having too narrow a scope, the next sentence you write is the one most likely to have the\n"
    "     same scope**, because you are holding the listing that misled it (F101, and F37's recursion\n"
    "     clause).\n",
))
EDITS.append((
    "  the reader will hold.** *(Asserted, C16, over both trees from the start.)*\n",
    "  the reader will hold.** *(Asserted, C16, over both trees from the start.)*\n"
    "  **The purest instance, r222b: five round reports were written, dated, correct \u2014 and put in a\n"
    "  directory the recipient does not read.** He replied that the work existed *\"without a report\"*.\n"
    "  **The writing happened and the delivery did not, and from the author's side those are the same\n"
    "  event.** So the rule has a second clause: *name the artefact the reader will hold, and then\n"
    "  check that the artefact is where the reader looks* --- \u00a73 now fixes that place by absolute path.\n",
))
EDITS.append((
    "  reader stops discounting the list and starts reading it.\n",
    "  reader stops discounting the list and starts reading it.\n"
    "  **The same applies to a claim you have just discovered is false: strike it where it stands,\n"
    "  put the correction where a cold reader meets it FIRST, and leave the wrong sentence visible.**\n"
    "  *(A report asserted five reports did not exist; the correction went at the head of the file and\n"
    "  the false sentence stayed, struck through. A reader who cannot see what was withdrawn cannot\n"
    "  tell a corrected document from one that was never wrong.)*\n",
))

out = src
for i, (old, new) in enumerate(EDITS, 1):
    n = out.count(old)
    say("edit %d   : anchor occurs %d time(s)  [%s...]" % (i, n, old.split("\n")[0][:58]))
    if n != 1:
        say("ABORT: anchor for edit %d occurs %d times, not exactly once." % (i, n))
        sys.exit(1)
    out = out.replace(old, new)

os.makedirs(OUTDIR, exist_ok=True)
io.open(OUT, "w", encoding="utf-8", newline="").write(out)
b = out.encode("utf-8")
say("")
say("written  : %s" % OUT)
say("bytes    : %d   (was 88259, delta %+d)" % (len(b), len(b) - 88259))
say("md5      : %s" % hashlib.md5(b).hexdigest())
say("")
say("body md5 (everything after the 4-line frontmatter, which save_skill re-emits):")
body = "\n".join(out.split("\n")[4:])
say("           %s" % hashlib.md5(body.encode("utf-8")).hexdigest())
say("")
say("NEXT, AND IT IS NOT OPTIONAL: pass this file's body to save_skill, then re-read the")
say("cache and diff it against this file.  The write is unverifiable until that diff runs")
say("(F82).  Expected: zero differences, because the baseline was taken from the saved")
say("side this time (F102).")
say("done.")
