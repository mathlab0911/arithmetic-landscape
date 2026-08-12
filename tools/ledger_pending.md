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

---

## r130 — a reader-facing artefact is a scope (append to F60)

The homepage carried, on the day it was read: the enumeration definition of Gamma (retired
r120), "order-sensitive invariant" (a C11 banned string since r120), `5.34920` (a C11
banned literal since r118), four papers with paper 3's old title, and no AI disclosure.
Every one had been corrected where a check could see it. C11 had been banning that number
for twelve rounds, over `paper/` and `paper-ja/` only.

Then, with the homepage clean, the README — a file every check here has read for rounds —
was found to define the ratio as `lm_A(n)/deg_A(n)`, the symbol purged from all four papers
at r126 for being a second name for `r_A(n)`. C9 counts its numbers; C14 guards one formula
in it. Neither has an opinion about its vocabulary.

**Being inside the tree is not the same as being inside a check.** C13 was the scope lesson
across artefact trees; this is the same lesson *within* one, and it is harder to see,
because the file is demonstrably being read. When a correction is made, the question is not
"is the artefact checked" but "is *this property of it* checked".

C18 reads both landing pages: banned literals, retired names, the disclosure.

## r130 — the push was green and the reader saw the old page (append to F61)

Both pushes reported success. `/index.html` served the rewrite; the bare URL — the one in
every author footnote and in the mail sent to two mathematicians — served the old page,
with the banned literal on it, for about a minute while GitHub Pages rebuilt.

**A push that reports success is not the same as a reader seeing the new state.** The
post-push fetch over the public internet is not ceremony; it is the only step that observes
the thing we actually care about. It found this on its first run.

Corollary for the fetch itself: the session fetcher deduplicates, so a re-read of the same
URL returns the first answer. Use a real browser for the confirming read.

## r130 — a too-wide exemption forgives, where a too-wide search only misses (append to F47,
## beside the C17 coda)

The README must be able to name paper 3 in order to retire it, so C18 excuses a retired
name when the text marks it as past. First draft: a retirement marker anywhere within 400
characters. **Two of five negative controls did not fire** — `four papers` reinstated three
lines from the retirement paragraph was forgiven.

This is C17's region-too-wide failure moved from the search into the exemption, and the
exemption is the dangerous direction:

> A region drawn too wide in a search only misses. A region drawn too wide in an exemption
> actively forgives.

The marker must stand in the same sentence as the name. Five of five fire. The excused
count is printed on every run: an exemption a reader of the output cannot see is an
exemption that rots.

## r130 — the blind spot no tree can cover (append to F60)

The GitHub repository *description* — the line under the repository name, and the browser
tab title — is the pre-series title of Part I. It is in GitHub's settings, not in a file.
No check in any tree can reach it and no commit can fix it. Topics and the social preview
are the same class.

The apparatus is structurally blind to everything that is configuration rather than
content, and the failure ledger should say so rather than let a green run imply otherwise.

## r131 — a check that reads the artefact but not the property (append to F60)

C13 was written *for* the Japanese editions, and reads them on every run. Translating Part III
meant measuring the skeleton of the other two against their sources, and the measurement found
what C13 structurally could not:

- `paper2_ja` was missing **six of its seven status declarations**, including the one on the
  main theorem, and two whole remarks;
- `paper1_ja` was missing the `\label` its siblings cross-reference.

Each was content the English gained after the translation was made. C13 compares *numbers*;
none of the missing material was a number.

> C13 was reading the file. It was not reading the property. "Is the artefact checked" and
> "is *this* property of it checked" are different questions, and only the second one is ever
> the one that matters.

C19 compares the skeleton: label set, count of each theorem-like environment, count of
`\STATUS`. Three negative controls (delete a label, delete a remark, delete a status) all fire.

Corollary worth keeping: a translation that silently drops the status labels is exactly the
overclaim C8 exists to prevent, made invisible by being in the other language. The Japanese
editions are what Kentaro reads and approves from, so an unlabelled Japanese theorem is an
approval given to a claim whose status the approver could not see.

Also found in the same pass, by a scan no check had run: a Hangul character (`검`) inside the
word 検査 in the AI-disclosure paragraph of **both** existing Japanese editions — one bad
keystroke, copied when the paragraph was. Fixed; the scan is worth keeping in the toolbox even
though it is not yet a check.
