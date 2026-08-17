#!/usr/bin/env python3
"""Apply the r182-r200 ledger fold to the skill, mechanically.

F82, applied to ourselves: the distillation is written exactly and separately, applied by
machine rather than by hand, and the result is diffed before it is believed.  This file IS
the distillation; `skill_delta_r200.md` is generated from it so the record and the patch
cannot drift apart (r187: a number retyped is a new number -- so is a paragraph).

    python3 tools/skill_delta_r200.py

Reads  tools/skill_backup_r181/SKILL_after_r181.md   (the current live skill, byte-identical)
Writes tools/skill_backup_r200/SKILL_after_r200.md   (what save_skill must be given)
       tools/skill_delta_r200.md                     (the human-readable record)

Every anchor must occur EXACTLY ONCE or the run aborts: a replace that matches nothing does
not raise by itself, and missing looks exactly like success (F71).
"""

import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'tools', 'skill_backup_r181', 'SKILL_after_r181.md')
OUTDIR = os.path.join(ROOT, 'tools', 'skill_backup_r200')
OUT = os.path.join(OUTDIR, 'SKILL_after_r200.md')
DELTA = os.path.join(ROOT, 'tools', 'skill_delta_r200.md')

# The live skill as verified byte-identical at r194.  If this does not match, the source is not
# what the ledger says it is and nothing below should run.
SRC_MD5 = '2b35e1bdd08c669892224eb1917e6846'

# --------------------------------------------------------------------------- the new section

SECTION_78 = r"""### 7.8 Scales, boundaries, and the artefacts nobody checks --- F83--F87

Bought over rounds r181--r200: two errors found in a paper that already carried a DOI, a
credential file in the repository root, and a run whose three hypothesis-falsifiers all passed
while its instrument was broken. Case text in `ledger_archive.md`.

- **F83** **Detect credential files by NAME, and say out loud that this is a net with a known
  mesh.** *(A `github-recovery-codes.txt` sat untracked in the root of a repository whose `main`
  is pushed to a public remote, through several `git add -A`. Never committed --- which was luck,
  not a property of the system.)* *(Asserted, **C21**, over tracked and untracked files alike,
  with a named exception list so the list itself can be audited.)* The check cannot see a secret
  that is innocently named, and it says so in its own note, because here a check that implies
  coverage it does not have is worse than no check --- the failure mode is publishing someone's
  account. Two corollaries, both about the gap between telling and enforcing. **Advice given to a
  person is not a control; it is a hope with good manners.** **And when someone hands you a
  hazard, declining to hold it is not the same as making it safe** --- refuse the custody, then
  ask where the thing currently is.
- **F84** **A claim of the form `x >= a <=> P` is three claims, and the one at `x = a` is the one
  nobody checks.** The strict inequality is where the proof lives, the strict reverse is where the
  counterexample lives, and equality is where the sentence gets written without either. *(`R >= 1`
  is exactly the statement that `Gamma` is finite --- carried `STATUS{proved}`, shipped under a
  DOI, and false precisely at `R = 1`, where both cases occur among profiles the paper was already
  using.)* **A status inherited through a citation is only as strong as the quantifier the
  citation carries**: the proof read *"item 1 is Part I's proposition evaluated at `z = 1`"*, and
  Part I's statement is about a finite profile, where the quantity is a finite sum. **And a new
  example is a test of every claim the paper makes about the class it belongs to --- but nothing
  prompts you to run those tests**, which is why both of that section's errors were found while
  doing something else entirely. *The uncomfortable half: the false equivalence was also in this
  ledger, asserted as a finding, in the entry written to celebrate the insight.* **The place a
  wrong idea is stated most confidently is the entry congratulating you for having it**, so a fold
  is an occasion to re-derive and not only to compress.
- **F85** **A limit computed along one scaling is a statement about that scaling.** When the
  conclusion is *"the quantity tends to something positive, so there is no zero"*, the missing
  words are *"at this scale"* --- and the next question is which scale makes the neglected factor
  `O(1)`. *(F32's second clause applied to an analytical limit rather than to a numerical scan,
  where it is easier to miss because no grid makes the range visible. The wrong prediction was
  load-bearing: it named the scale that does not work, which is what made the scale that does work
  findable in one step.)* Two siblings, from the same section in the same fortnight. **When a
  closed form exists, do not characterise it by its largest term** --- that keeps the modulus and
  throws away a phase, and the quarter turn discarded here moved a ladder by half a rung, which
  was then written up as the discovery. **And number your zeros from the origin, not from your
  prediction**: a prediction that names a location will be confirmed by any zero near that
  location, and a dense ladder has one near everywhere.
- **F86** **Every pre-registration needs a falsifier that tests the INSTRUMENT against an exact
  answer already known, and that is the one which must pass first.** *(Five falsifiers were
  registered; the three testing the law all passed on a run whose weight vectors were indexed one
  step too far. Only the two instrument controls fired, and between them they localised one defect
  in the script and one in the paper.)*
  > **A pre-registration that only tests the hypothesis cannot tell you the apparatus is broken,
  > and an apparatus that is broken while still confirming your hypothesis is the worst outcome an
  > experiment can produce, because nothing about it looks wrong.**

  That is F45 sharpened by naming *which* falsifier. Three further clauses about reporting a
  measurement, each bought separately: **print the residual spread beside every fitted rate** ---
  a rate without its scatter is an assertion wearing a number, and a fit over four points agreed
  with the prediction to three decimals while the full range moved it by a factor of three.
  **"Consistent with" is not "confirms"**, and saying what a measurement could *not* have
  distinguished is part of reporting what it did. **And print numbers at the precision at which
  two independent methods agree, naming the two** --- six digits from one scan is a claim about
  the scan and not about the quantity.
- **F87** **A formula and the number it is supposed to produce, printed in the same sentence, are
  not a check on each other. They are two artefacts with one author, who computed one of them and
  typed the other.** The only check is to run the formula. *(A displayed profile that does not
  generate the constant printed beside it survived two releases and an audit sweep commissioned to
  brute-force that very section.)*
  > **A condition forced by the object is the one most likely to be missing from the display,
  > because the author knows it cannot be otherwise and therefore never says it.**

  Positive multiplicities, integer gaps, non-empty supports. **Every check we own compares the
  paper against the paper, so this whole class is invisible to all of them.** Its small sibling,
  caught by C2 in three consecutive rounds: **a number retyped at a different precision is a new
  number, and nobody checks it against the old one.** Rounding is the act of turning a log into a
  table, and every time a number is made easier to read it is made new. Round in the script, so
  that the rounded form is itself logged.

"""

# --------------------------------------------------------------------------- patches

PATCHES = [

    # ---- 1. the new section, inserted before 7.4 (which sits last, after 7.7) ----
    ("new section 7.8 (F83-F87)",
     "### 7.4 Writing and documents — F35–F42\n",
     SECTION_78 + "### 7.4 Writing and documents — F35–F42\n"),

    # ---- 2. C21 into the enumerated check list in 7.0 ----
    ("C21 added to the check list",
     "**C20**/F70 no statement rests on measurement alone — plus",
     "**C20**/F70 no statement rests on measurement alone, **C21**/F83 no file in the tree is\n"
     "  *named* like a credential — plus"),

    # ---- 3. the evidence-path field, 7.0 ----
    ("A-1 evidence path, in 7.0",
     "- **When a rule fires and prevents a mistake, note it in the report.**",
     "- **When a rule fires and prevents a mistake, note it in the report.**\n"
     "- **Every verification declares what it touched and what it is independent OF** (`A-1`,\n"
     "  `references/governance.md`). The honest entry is often *\"independent of: nothing --- this\n"
     "  report describes documents its author wrote\"*, and writing that sentence is the point:\n"
     "  **verification against a description verifies the description** (F52), and the only way to\n"
     "  notice you are doing it is to be made to name the artefact each time."),

    # ---- 4. A-2, into 2. Roles ----
    ("A-2 status transitions, in 2. Roles",
     "**A proof written by one model becomes \"proved on paper\" only after the other model has verified\n"
     "it independently.**",
     "**Raising a status requires the other party; lowering it does not** (`A-2`). Guard the\n"
     "expensive direction: an elevation --- open to closed, conjectured to proved --- is the other\n"
     "model's to grant, while *lowering a status needs no permission, only a reason*, and\n"
     "**withdrawing a false clause from a statement is a correction and not an elevation**, so it is\n"
     "done at once and said out loud. Role rotation was considered and declined: the split is not\n"
     "fairness but a division of instruments, and *design cannot check itself against magnitudes it\n"
     "has not computed*.\n"
     "\n"
     "**A proof written by one model becomes \"proved on paper\" only after the other model has verified\n"
     "it independently.**"),

    # ---- 5. the report structure gains the evidence-path field ----
    ("EVIDENCE PATH in the report structure",
     "**Structure** (all three are required)\n",
     "**Structure** (all four are required)\n\n"
     "0. **EVIDENCE PATH** (`A-1`): the artefacts this round touched, what the verification is\n"
     "   independent *of*, and its grain (byte-exact / statement by statement / authorship only).\n"),

    # ---- 6. 6. The research cycle: two questions bought by r182-r183 ----
    ("shadow / one-point / smaller question, in 6",
     "**A justification found after the choice is still worth recording as having been found after.**",
     "**Three questions that turned a conjecture into an identity in two rounds, in the order they\n"
     "were asked --- each smaller than the last.**\n"
     "\n"
     "- **When a new phenomenon appears, ask which of your existing quantities it is a shadow of\n"
     "  before inventing a quantity for it.** The zeros were never the object; they were a shadow of\n"
     "  the generating function the papers had been summing since Part I.\n"
     "- **A quantity you only ever evaluate at one point is a function you have not noticed you\n"
     "  have.** The identity was two lines and had been available for thirty-four rounds; nobody\n"
     "  needed it, because the invariant was only ever read at the fair coin.\n"
     "- **When a conjecture resists, look for the smaller question whose answer it would follow\n"
     "  from** --- not the bigger framework it might fit into.\n"
     "\n"
     "**A justification found after the choice is still worth recording as having been found after.**"),

    # ---- 7. F45 -> name which falsifier ----
    ("F45 gains 'which falsifier'",
     "- **F45** **When two independently measured constants coincide, write the falsifier into the\n"
     "  script before running it.**",
     "- **F45** **When two independently measured constants coincide, write the falsifier into the\n"
     "  script before running it.** **And name WHICH falsifier**: at least one must test the\n"
     "  instrument against an answer already known to be exact, and it must be the one that passes\n"
     "  first (F86). Falsifiers for the hypothesis alone cannot see a broken apparatus."),

    # ---- 8. F27 -> establish the reachable range before fitting ----
    ("F27 gains the reachable range",
     "population and the weighting in the sentence that reports the number, every time.**",
     "population and the weighting in the sentence that reports the number, every time.**\n"
     "  **And establish the reachable range BEFORE fitting, not after**: where the limit has not\n"
     "  begun there is no rate to measure, and a column saying so costs nothing --- a fit over four\n"
     "  points matched the prediction to three decimals, and the full range moved it by a factor of\n"
     "  three."),

    # ---- 9. F52 -> the tool built to enforce it contained it ----
    ("F52 gains the parser case",
     "  **When a table is the deliverable, at least one pass must go row → primary source, and it must\n"
     "  be the row that would cost most to get wrong. A deletion is that row by default**, because\n"
     "  *additions announce themselves at build time and deletions do not*.",
     "  **When a table is the deliverable, at least one pass must go row → primary source, and it must\n"
     "  be the row that would cost most to get wrong. A deletion is that row by default**, because\n"
     "  *additions announce themselves at build time and deletions do not*.\n"
     "  **And the tool written to enforce that sentence contained the defect the sentence names**: a\n"
     "  parser for `git add --dry-run` stripped only the `add '` verb, so every *deletion* reached\n"
     "  the whitelist guard still wearing `remove '` and was refused. It was written for the case\n"
     "  that announces itself.\n"
     "  > **A rule you can quote is not a rule you have applied. The application is a separate act,\n"
     "  > in a different place, and it is the place that has to be checked.**\n"
     "\n"
     "  *Two details worth keeping.* The guard **failed safe** --- friction on the dangerous side\n"
     "  (F77) turns a parser bug into a refused push instead of an unnoticed publication. And the\n"
     "  repair **prints the removals** rather than merely admitting them; stripping the verb alone\n"
     "  would have folded deletions silently into a count, which is the same blind spot one layer\n"
     "  down. **A parser written from one observed output is a parser for one case** --- ask what\n"
     "  else the command can say, not only what it said the day you looked."),

    # ---- 10. F58 -> test the check before withdrawing the measurement ----
    ("F58 gains the false-guard clause",
     "smallest artefact it is supposed to contain, not the largest.**",
     "smallest artefact it is supposed to contain, not the largest.**\n"
     "  **And when a check disagrees with something you have just measured, test the check before\n"
     "  withdrawing the measurement.** *(A guard asserting a field was absent matched the substring\n"
     "  inside `cff-version:` --- the format's version, not the work's --- and its author retracted a\n"
     "  true statement in public on its say-so.)* **A false guard costs more than the work it\n"
     "  blocked: it also spends the credibility of the true statement it contradicted.** Anchor such\n"
     "  patterns to line starts, and print the line that matched."),

    # ---- 11. F60 -> exhaustive beats scanned ----
    ("F60 gains 'the set is exactly this'",
     "  **Derive a scope from a list of artefacts, never from memory**",
     "  **Where the object allows it, replace \"we scanned and found none\" with \"the set is exactly\n"
     "  this\".** A polynomial's roots can be enumerated, which converts a claim about where we\n"
     "  looked into a claim about the whole set. *(It also exposed a symmetry nobody had written\n"
     "  down: a crash in the root-finder was the first mention of it. **An exhaustive method reports\n"
     "  structure a targeted one cannot, including structure you were not looking for.**)*\n"
     "\n"
     "  **Derive a scope from a list of artefacts, never from memory**"),

    # ---- 12. F79 -> the sweep has a measured yield ----
    ("F79 gains the sweep's yield",
     "  `CITATION.cff`, the README, the homepage, the previous version's release notes. None of them is\n"
     "  the paper, so none of them is checked.",
     "  `CITATION.cff`, the README, the homepage, the previous version's release notes. None of them is\n"
     "  the paper, so none of them is checked.\n"
     "  **The sweep has a measured yield, so it is not ceremony**: run before one release it returned\n"
     "  **four** stale artefacts and not one of them was the paper --- a page count, a version string,\n"
     "  a `README` still calling the *previous* release the archived one, and a design document still\n"
     "  advertising a result that had been refuted that morning. **And a rule recorded as applied is\n"
     "  not a rule applied**: the caveat this ledger says was placed under the README badge was in\n"
     "  neither the README nor the deposit. *The ledger records the decision; only the artefact\n"
     "  records the act.*"),

    # ---- 13. F82 -> the cost measurement, the goal restatement, decoration ----
    ("F82 gains the r182-r194 material",
     "  (`tools/skill_delta_rNNN.md`), apply it mechanically rather than by hand, and **diff the saved\n"
     "  result against the source before believing it.**",
     "  (`tools/skill_delta_rNNN.md`), apply it mechanically rather than by hand, and **diff the saved\n"
     "  result against the source before believing it.**\n"
     "\n"
     "  **What that cost, in full, because it took six rounds.** The excuse offered five times was\n"
     "  *\"67 KB in plus 67 KB out does not fit alongside anything else\"* --- true as stated, and\n"
     "  **never once tested as a claim about the whole turn**, because every one of the five\n"
     "  deferrals was a turn that already had other work in it. It fits when it is the only thing in\n"
     "  it.\n"
     "  > **A cost measured only against turns that already had work in them is not a measurement of\n"
     "  > the cost. When a standing order is deferred more than twice for the same resource reason,\n"
     "  > the next attempt gets the resource to itself before the reason is repeated again.**\n"
     "\n"
     "  Three more, from the same six rounds. **Make the recovery cheap before making the write** ---\n"
     "  front-load the parts that cannot fail quietly, and then stopping costs a session boundary\n"
     "  instead of a document; *the test of a rule is whether it holds the first time obeying it is\n"
     "  expensive.* **A blocked step is not automatically a blocked goal**: say out loud what the\n"
     "  route was *for* before looking for another one --- but **when you re-aim at the goal, say\n"
     "  what the abandoned step was still going to buy**, or you have not re-aimed, you have\n"
     "  retreated. And **a spot check that runs beside an exact comparison is decoration, and\n"
     "  decoration that can fail silently will eventually be quoted as evidence** --- one grep\n"
     "  printed nothing while its subject was present, defeated by a line break at column 96. Where\n"
     "  a hash is available, a grep adds nothing but a way to be wrong; make it exact or delete it."),
]


def main():
    src = open(SRC, encoding='utf-8').read()
    md5_in = hashlib.md5(src.encode('utf-8')).hexdigest()
    print('source: %d bytes, %d lines, md5 %s' % (len(src.encode()), src.count('\n'), md5_in))
    if md5_in != SRC_MD5:
        print('ABORT: source md5 is not the one verified at r194 (%s)' % SRC_MD5)
        sys.exit(1)

    out = src
    for name, anchor, repl in PATCHES:
        n = out.count(anchor)
        if n != 1:
            print('ABORT: anchor for %r occurs %d times, expected exactly 1' % (name, n))
            sys.exit(2)
        out = out.replace(anchor, repl, 1)
        print('  applied: %s' % name)

    # the section header line lists which entries live in 7.7; 7.8 is new and self-labelled.
    fs = sorted(set(re.findall(r'\*\*(F\d\d)\*\*', out)))
    print('F-entries present: %d  (%s .. %s)' % (len(fs), fs[0], fs[-1]))
    missing = [('F%02d' % i) for i in range(1, 88) if ('F%02d' % i) not in fs]
    if missing:
        print('ABORT: missing entries: %s' % missing)
        sys.exit(3)

    os.makedirs(OUTDIR, exist_ok=True)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(out)
    md5_out = hashlib.md5(out.encode('utf-8')).hexdigest()
    print('result: %d bytes, %d lines, md5 %s' % (len(out.encode()), out.count('\n'), md5_out))
    print('growth: +%d bytes, +%d lines'
          % (len(out.encode()) - len(src.encode()), out.count('\n') - src.count('\n')))

    with open(DELTA, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Skill delta r200 — the r182–r200 fold\n\n')
        f.write('Generated by `tools/skill_delta_r200.py`; do not edit by hand. The patch and the\n'
                'record are one artefact so they cannot drift apart.\n\n')
        f.write('Source `tools/skill_backup_r181/SKILL_after_r181.md` (md5 `%s`)\n' % md5_in)
        f.write('Result `tools/skill_backup_r200/SKILL_after_r200.md` (md5 `%s`, %d bytes, %d lines)\n\n'
                % (md5_out, len(out.encode()), out.count('\n')))
        f.write('**Twenty pending entries folded** (r181–r200): five new ledger entries `F83`–`F87`\n'
                'in a new §7.8, and eleven strengthenings of existing text.\n\n')
        f.write('| # | what | where |\n|---|---|---|\n')
        for i, (name, anchor, _repl) in enumerate(PATCHES, 1):
            f.write('| %d | %s | `%s…` |\n' % (i, name, anchor.strip().split('\n')[0][:60]))
        f.write('\n## The new section, verbatim\n\n')
        f.write(SECTION_78)
    print('wrote %s' % DELTA)
    print('\nNEXT: save_skill(name="pnp-research", overwrite=True, description=<the YAML '
          'description in the file>, content=<the body after the front matter>), then diff.')


if __name__ == '__main__':
    main()
