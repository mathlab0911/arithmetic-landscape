# Pending failure-ledger entries

Entries written mid-round, not yet folded into the `pnp-research` skill (§7).
`tools/check.py` (C6) prints this file on every run. Clear it at the next skill save.

Full text of entries already folded in lives in `tools/ledger_archive.md`.

---

## r119 (fable-5) — append to F18/C11

```
  claimed   : fverify_r119a "E claimed digits: FAIL" — r118's 33-digit Γ(P) string wrong
  actual    : true digits …8058823…; the string is a correct TRUNCATION; my predicate
              demanded rounding-only, so it flagged a correct constant
  check     : evaluate the printed literal under BOTH acceptances (truncation, rounding)
              at the printed precision — i.e. run C11's own predicate
  rule      : a verification written against a rule must reuse the rule's own acceptance
              predicate; a paraphrase of the predicate is a new predicate
```

---

## r120 — F60 (new): a check scoped to one artefact tree

```
  claimed   : "check.py C1-C12 pass" -- taken to mean the papers are checked
  actual    : every check was scoped to paper/.  paper-ja/ had never been read by any
              of them.  The constant erratum corrected in English at r118 was still in
              paper2_ja four times, through two months of green runs
  check     : C13 -- a decimal literal printed in a translation must occur in its source
              (translations restate numbers, they do not compute them, so a number in
              only one edition is drift by construction).  Plus: C11 now scans paper-ja/,
              and an exemption is inherited by the translation, because an exemption is
              a fact about the number and not about the language it is printed in
  rule      : a check has a scope, and the scope is part of the claim.  "All checks pass"
              means nothing until you can say what they looked at.  Print the file count
```

## r120 — the CV-twin lesson (append near F47)

```
  claimed   : "CV is order-blind and Gamma is not" -- paper 1's reason, in three places,
              for why the standard statistic is only a proxy
  actual    : true under the old definition and false under the new one, where Gamma is
              a set invariant too.  Losing it forced the real reason (CV is a global
              second moment, Gamma is dominated by the bottom of the set), which is
              decouplable and therefore testable -- and the test came out 2.3 : 1 for
              Gamma with a clean control
  rule      : an explanation that cannot fail is not protecting the claim, it is
              occupying the slot where a real one would go.  When a definition change
              kills an argument, the argument was cheap; look for what it was standing
              in front of
```

## r128 — F65 (new): coined vocabulary, counted before it was changed

```
  claimed   : the papers are precise; the terminology is what the subject needs
  actual    : 387 occurrences of vocabulary this programme coined against 166 of the
              shared vocabulary -- more than two to one -- and 22 of 24 coined terms
              were met somewhere before they were introduced.  Three objects had two
              names each: deg_A(n) / r_A(n); the window series / the window measure;
              the coset identity / the coarse-graining identity.  Each pair costs a
              reader the work of discovering they are the same thing
  check     : C17 -- every coined term used in a live paper must be glossed in a
              terminology table the reader can find.  Each paper now carries one
  rule      : a coined name is a cost paid by every reader and a convenience for the
              author.  Two names for one object is that cost, doubled, for nothing.
              Count the vocabulary before defending it
```

```
  claimed   : C17 works; its first negative control passed
  actual    : it passed because the check could not fail.  The gloss was searched for
              in a "terminology table" region that ran to the next \section, so it
              swallowed the rest of the introduction -- including Theorem D, whose name
              is Sandwich.  Removing the actual table row changed nothing.  Narrowing
              the region to the next sectioning command of ANY level made the control
              fire, and the now-honest check immediately found three real gaps
  rule      : when a check searches a REGION, the region is part of the check.  A
              region drawn too wide is the same failure as a scope drawn too narrow,
              and only the negative control tells them apart from a pass
```

## r126 — F64 (new): the disclosure was one artefact away from its reader

The day an endorsement was declined. Two findings, and the second is the larger one.

```
  claimed   : the use of AI tools is disclosed, prominently, in the README, under a
              heading written specifically so a reader would meet it
  actual    : it appeared in NONE of the four papers.  The referee read PDFs.  His
              words: "I suspect that AI tools may have been used ... if AI was used,
              then it has to be acknowledged appropriately"
  check     : C16 -- every paper must carry a "Use of AI tools" section in itself.
              Negative control taken
  rule      : the fourth instance of one shape in two days (C13, C14, the C9 row
              labels, this) and the first that cost anything.  A statement that lives
              one artefact away from its reader has not been made.  When something
              must reach a reader, name the artefact the reader will hold -- not the
              repository, not the memory, not the report
```

```
  claimed   : the papers are hard to assess because the mathematics is deep
  actual    : the reviewer could not find a door.  Two symbols were carrying one
              object -- deg_A(n) (a physics name for the ground-state count) and
              r_{B_d}(m) (the standard name for the same thing on a truncation) --
              and the abstract opened by defining our own invariant before naming a
              single object the reader already had.  The main theorem turns out to be
              statable with no landscape vocabulary at all: a weighted sum of
              representation counts of the truncations of A, divided by r_A(n),
              converges to a number read off A.  Verified as an identity on 176 cases
              (door_r126)
  rule      : coined vocabulary is a cost paid by every reader and a convenience for
              the author.  Before inventing a name, check whether the object already
              has one -- and open with the objects the reader brought, not the ones
              we brought.  An earlier technical review engaged deeply with this same
              material, so the work is not unintelligible; there was simply no way in
```

## r123 — two independent audits passed the same wrong row, for the same reason

```
  claimed   : the paper-3 mapping table was audited and passed; fable-5's independent
              count matched the population exactly and every row was checked against
              the r121 rule.  lem:kappa was to be DROPPED as "the multiplicative
              kappa-transport, refuted"
  actual    : lem:kappa IS THE ADDITIVE BRIDGE.  It is proved, it is cited nine times
              -- by the introduction, by region R3, by prop:tiltlclt's own status, and
              by the honest-scope list as "proved ... in full" -- and dropping it would
              have deleted a lemma three results depend on.  What is refuted is the
              MULTIPLICATIVE transport, which is rem:noKappa's subject.  Two objects,
              one substring in their names
  why both   : each audit checked the row against its stated REASON, and the reason
  missed it : matched the graveyard memory, where the multiplicative bridge is indeed
              recorded as refuted.  Neither checked the reason against the paper.  An
              independent auditor reading the same description is not an independent
              check of the description
  check     : DROP_GUARD -- a DROP whose subject is still referenced anywhere refuses to
              classify, and must be given an account of where the references go.
              lem:kappa: 9 references.  Negative control taken
  rule      : verification against a description verifies the description.  When a table
              is the deliverable, at least one pass must go table row -> primary source,
              and it must be the row that would cost the most to get wrong.  A deletion
              is that row by default: additions announce themselves at build time,
              deletions do not
```

## r121 — a status label held too long is wrong in both directions

```
  claimed   : Part II owed the reader two steps of prop:deepminor, "not written to
              referee standard" -- carried in the abstract, the section head, the
              theorem's own status, and the honest-scope list
  actual    : most of both steps was written.  What was actually missing was three
              other things: the quoted lemma was never STATED (only cited by number),
              the passage from all primes up to N to the layer B_d was absent, and the
              summation by parts in the excision was indicated rather than assembled
              (its intermediate expression did not follow, though its conclusion did)
  check     : when a status label survives more than one round, re-derive it from the
              text rather than carrying it; the label is a claim like any other
  rule      : a debt label goes stale in both directions.  It over-reports what is
              missing where work has quietly been done, and it under-reports by naming
              the wrong thing -- and the second is worse, because it aims the next
              audit away from the defect
```

## r121 — two checks, two different reasons, one missed reference

```
  claimed   : cross-document references were covered (C15) and translation drift was
              covered (C13)
  actual    : the Japanese abstract still pointed at "Problem 10.1" after the English
              moved to 11.1.  C13 reads literals with three or more decimals, and 10.1
              has one; C15 read paper/ and not paper-ja/.  Each check missed it for its
              own reason, and between them the artefact had no cover at all
  check     : the Japanese editions now carry the same \Xref/\Xlab macros and C15 scans
              both trees
  rule      : coverage is not the union of what the checks are about, it is the union of
              what they LOOK AT.  Two checks that between them describe a rule do not
              between them enforce it
```

## r120 — where the defect was, versus where the ledger said to look

Written at r121 after fable-5 caught its absence: the lesson was in the report and not here,
though §7.0 says the entry comes first. The omission is itself the pattern — the entry that
does not get written is the one whose report section already felt finished.

```
  claimed   : the risk in Part II was steps 2/4 of prop:deepminor (the tracked debt)
  actual    : the defect was three lemmas upstream — θ vs θ/2π at the lemma interfaces —
              in statements carrying no flag at all
  check     : one variable-convention pass per paper: declare each circle variable once,
              then verify every lemma is stated and USED on the declared scale
  rule      : a status ledger biases attention toward known weaknesses; schedule audits
              of the unflagged interfaces, starting with variable conventions
```

## r120 — F61/F62 and the scope lesson repeating within the hour

```
  claimed   : C14 written to confine the retired enumeration form of Gamma to paper 1;
              it passed
  actual    : it scanned paper/ and paper-ja/, and the README's own headline was still
              defining Gamma by the enumeration series and calling it order-sensitive.
              Written by the same hand, in the same hour, immediately after writing the
              F60 ledger entry about checks scoped to one artefact tree
  check     : C14 and the C11 ban list now include README.md; every check prints what it
              looked at; C9 verifies the README's own claim about how many checks exist
              against the list that actually runs
  rule      : knowing the rule does not make you apply it.  The scope of a check is chosen
              while thinking about the RULE, and the artefacts are not in mind at that
              moment.  So the scope has to be derived from a list of artefacts, not
              recalled -- and the count has to be printed, so that a missing artefact is
              visible as a number rather than as an absence
```

```
  claimed   : cross-paper references in papers 2-4 were fine; nothing had flagged them
  actual    : "Problem 10.1 of the companion paper" became 11.1 the moment a section was
              inserted into paper 1, and "paper 1 §10 and paper 2 §10" had been wrong from
              the day it was written.  LaTeX cannot resolve a reference into another
              document, so these are strings, and strings do not fail
  check     : C15 -- \Xref{stem}{label}{number} and \Xlab{stem}{label}, resolved against
              the sibling's .aux, with the printed number required to match
  rule      : a reference that crosses a document boundary loses its checker.  Put the
              checker back before the boundary is crossed, not after
```

(previous state: emptied at skill save r118, which folded 6 entries covering r117–r118)
