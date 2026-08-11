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
