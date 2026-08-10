# Pending failure-ledger entries

Entries written mid-round, not yet folded into the `pnp-research` skill (§7).
`tools/check.py` (C6) prints this file on every run. Clear it at the next skill save.

---

## Append to F51 (a fail rule must state its measurement floor) — new instance, r110

```
claimed   : the coset identity Phi_q(s) = (1-1/v)log2 + (1/v)F(vs) holds, floor 1e-12
actual    : the identity is exact, but the float comparison of the two sides disagreed by
            3.9e-11 and the fail rule fired on arithmetic
check     : ask what the CONDITION NUMBER of the comparison is before choosing the floor.
            F = -log|cos| amplifies the 1e-16 rounding of its argument by 1/dist-to-pole, so
            no fixed floor in the logarithmic form is meaningful.  Compare in the ALGEBRAIC
            form instead (products, not logs), where nothing is amplified: the same identity
            then agrees to 4.4e-16, and to 2.2e-61 at 60 digits.
rule      : before setting the floor of a fail rule, identify the operation in the comparison
            that amplifies rounding, and restate the comparison in a form that does not
            contain it.  An identity has many equivalent forms and they are not equally
            conditioned; test the one that is.
```

---

## Append to F03 (evaluate at the worst case in range) — new instance, r112

```
claimed   : "min_L [log2 + Cl_2(2 pi L)/(2 pi L)] = log2 - 3 Cl_2(pi/3)/(5 pi) = 0.4993,
             attained at L = 5/6, because Cl_2 is minimal at 5 pi/3"
actual    : the minimum is 0.494530 at L = 0.7908.  L sits in the DENOMINATOR as well as
            inside Cl_2, so minimising the numerator locates the wrong point.
check     : one line -- scan the quantity itself over the parameter, not the factor you can
            recognise.  Written into the script as a prediction, it was falsified in the
            first run and cost nothing.
rule      : the extremiser of one factor of a product or ratio is not the extremiser of the
            product or ratio.  When a bound has the shape f(x)/x, or f(x) g(x), locate the
            extremum of the whole expression -- a named constant sitting inside it is a
            temptation to stop early, not a shortcut.  (Corollary of F03's "evaluate at the
            worst case in range": first find out where the worst case IS.)
```

## Append to F41 (render the PDF and look at it) — third instance, r115  [ASSERTED in build.py]

```
claimed   : book/build.py's two guards (unbalanced <div>, literal ** or #) make a successful
            build trustworthy
actual    : a ``` fenced block with no 'fenced_code' extension is not an error -- the parser
            silently emits it as ONE RUN-ON PARAGRAPH.  The diagram in volume 4 chapter 52
            came out as unreadable prose, the build printed "wrote", both guards passed.
            *** Volume 3 had shipped with the same defect, unnoticed. ***
check     : render the page to an image and look at it (F41's own rule, which is what found
            it), and then assert it: `if '```' in html: abort`.
rule      : F41 already says render and look.  The addition is about the GUARDS: a guard set
            catches the failure modes you have already met, so a build that passes its guards
            is not a build that is correct -- keep rendering.  And every new markdown feature
            used for the first time is a new failure mode: check that the extension list
            actually supports it.  (build.py now also sets a monospace family for `pre`;
            ASCII art in a proportional serif face is legible but misaligned.)
```

## Append to F32 (is the observable the one the hypothesis predicts?) — new instance, r115

```
claimed   : "the primes at q = 1/2 fail the quadratic test" (spread 15.4, against 1.0 for the
            odd numbers) -- recorded in the paper as a TODO to re-measure
actual    : the hypothesis was fine and the RANGE was not.  At q = 1/2 the response is even in
            the offset x, so dev - dev_0 cannot change sign for the reason under test; but at
            finite k the vertex sits at x_* != 0 and dev - dev_0 crosses zero at +-x_*
            (measured x_* ~ 0.03, with the signs symmetric in +-x, as the account predicts).
            A range containing the crossing makes BOTH ratios pass through zero, so the spread
            of either is set by how close a grid point landed to x_* -- an accident of the
            grid.  On x in [0.10, 0.30] the primes give 1.012, the same as everyone else.
check     : before running a spread/ratio test, scan the NUMERATOR for a sign change inside the
            intended range.  One cheap scan on both sides of the centre.
rule      : *** a ratio test must not straddle a zero of its own numerator. ***  F32 says ask
            whether the observable is the one the hypothesis predicts; this adds: ask whether
            the RANGE lets that observable answer.  And when it does not, the repair is the
            range, never the omission of the offending point.
```

## F55 — second instance, r114: the control must be on the SEARCH, not on the function

```
claimed   : "positive control passed" on an end-to-end scan for max F_A(theta)^(1/b)
actual    : the scan reported a MAXIMUM of 0.5690 while having itself evaluated 0.7071 at
            theta = 1/4 — a maximum below a value it had computed.  The net had spacing
            1.7e-5 and the peak is O(1/N) = 7.8e-6 wide.
check     : the control asserted `|F_A(1/4) - 1/sqrt2| < 1e-12`, which is a property of the
            FUNCTION and is true whatever the net does.  The control that works asserts
            `|argmax - 1/4| < 3/N`, which is a property of the SEARCH.
rule      : F55 written one round earlier said "a search needs a control point whose answer is
            known".  It is not enough for the control point to be evaluated: the control must
            be the assertion that THE SEARCH RETURNS IT.  Write the control as a statement
            about the search's output, never about the integrand.  (F37's recursion, again:
            the round that writes a lesson is the round most likely to violate it.)
```

## F55 — third instance, r115: "does it exist" is not "is it restored"

```
claimed   : the six working directories were safely restored after the history rewrite --
            the restore loop printed "restored" or "already present" for each and I believed it
actual    : paper-ja held 7 files of 24 and docs held 1 of 5.  The rewrite had deleted the
            TRACKED files from the working tree while the gitignored build artefacts (.aux,
            .out, .toc) stayed behind, so the directory still existed -- and my guard was
            `if (-not (Test-Path $d))`, which therefore skipped exactly the two directories
            that needed the copy most.
check     : compare the file COUNT against the backup, per directory, and print both numbers.
            Three lines, and it names the two bad directories immediately.
rule      : F55 says the control must be on the search, not the function.  Same shape here:
            the control must be on the QUANTITY YOU CARE ABOUT, not on a proxy that correlates
            with it.  "The directory exists" is a proxy for "the directory was restored" and
            they come apart exactly when a partial deletion has occurred -- which is the only
            situation in which you were checking.  Whenever a guard short-circuits work, ask
            what it would do in the failure case you are guarding against.
```

## F35 — new instance, r115: a true sentence can license a false inference

```
claimed   : paper 2's abstract -- "the deep-minor bound ... which is proved here" and "The
            theorem carries no hypothesis"
actual    : both true.  But section L5c's own opening says the substitution in step 2 and the
            excision in step 4 are NOT written to referee standard, prop:deepminor rests on
            those steps, and thm:t2main rests on the proposition.  An external reviewer read
            the abstract, read the section, and concluded the paper had no established
            theorem.  My first reaction was that the reviewer had conflated an open Problem
            with the main theorem -- i.e. I defended the paper against a reader who had read
            it more carefully than I had (F50, F18).
check     : for each judgement word in the abstract, find the place in the body that qualifies
            it, and ask whether the abstract carries that qualification too.  Here: "no
            hypothesis" is in the abstract, "two steps not written to referee standard" was
            only in section 5.
rule      : F35 says compare the abstract with the body's judgement words.  The sharpening:
            *** an abstract can state only true things and still license a false inference. ***
            Check what the reader is ENTITLED TO CONCLUDE, not only whether each sentence is
            true.  "Carries no hypothesis" and "written out in full" are different claims and
            the first is routinely read as the second.
            Corollary for the log: the same drift happened in memory, which had recorded
            paper 2 as a complete theorem and paper 3 as finished while paper 3's two headline
            theorems carry STATUS{proof skeleton}.  The papers' status tags were honest
            throughout; the summaries were not.
```

## F50 — the other half of the rule (r116): check that the reader read it

```
claimed   : a second external review (2026-08-10) listing "critical concerns": that the Lean
            work faces Caratheodory / Fubini-Tonelli / dominated-convergence burdens, that the
            argument relies on Weyl equidistribution whose rate must be quantified for the
            family Gamma^(q), that explicit non-asymptotic error bounds are still needed, and
            that the modulus 4-versus-6 transition might be a truncation artifact.
actual    : checked against the documents.  The canon contains ZERO measure theory -- P_q is a
            finite product on the subsets of a finite set and rem:measurefree writes the
            weighted count out.  Paper 4 says FOUR times, including in the abstract, that no
            equidistribution input is needed, and names Erdos-Turan and Koksma only to decline
            them.  The error bound is already explicit and non-asymptotic (E <= 10qM/N +
            8M/(Q+1)).  The 4-vs-6 transition is thm:modfour, a proved theorem whose
            maximisation is Lean-verified, framed in the paper as "not an accident of the
            ensemble".  Gamma^(q) is a measure deformation, not a family of frequencies.
check     : does the review cite anything that can be checked -- theorem numbers, page
            references, quoted sentences?  The FIRST review of the same papers cited seven
            theorem numbers and all seven existed and matched, including one created that day;
            that is what made it worth acting on.  This one cites none, and its single concrete
            constant is our RATIO sqrt(3/2) = 1.2247 mistaken for a peak height.
rule      : F50 says that when a reader misses something the paper contains, that is a
            presentation defect.  *** The other half: a review's authority comes from evidence
            that it read the artifact, and that evidence is cheap to check. *** Verify it
            before editing anything.  Acting on an unread review costs real work and, worse,
            can talk you out of things you have already proved.  Neither half licenses the
            other: do not dismiss a careful reader, and do not defer to an incurious one.
```

## r117: a sweep driven by the examples you were handed is not a sweep

```
claimed   : "the F38 sweep is done" -- after fixing the four places an external review named
            or implied: thm:t2main, prop:ripple, and paper 3's two headline theorems
actual    : enumerating the population instead of the examples found that 8 of paper 4's 11
            theorem-like environments carried no status at the statement, including
            lem:coset, thm:modfour and thm:rate -- the load-bearing ones.  Paper 2 had 7 more.
            The statuses existed, correctly, in each paper's Honest scope section at the END,
            which is exactly the defect the review described and I had just claimed to fix.
check     : count the population before declaring coverage.  A twenty-line script listing every
            theorem/proposition/lemma/corollary and whether a status marker sits near it took
            less time than fixing one of them by hand, and it is now C8 in check.py.
rule      : *** a reviewer gives you INSTANCES; the fix is for the CLASS. ***  Before reporting
            a sweep complete, enumerate the set being swept and state its size -- "4 fixed" is
            not a coverage claim, "4 of 4" and "6 of 68" are.  Corollary: the moment the fix is
            mechanical enough to script, script it, because the same drift will recur in the
            next paper written and no reviewer will be reading that one.
note      : designing C8 took three passes, and each pass was the r117 scoping lesson again --
            v1 flagged 70/70 (paper 1 has no \STATUS macro and does not need one), v2 still
            flagged 13 statements in paper 1 whose status is a \Lean{} citation, v3 flagged
            conjectures, whose environment name IS their status.  A check is not finished when
            it fires; it is finished when everything it fires on is really a defect.
```

## F55 — fourth instance, r117: "listed as canon" is not "checked"

```
claimed   : the canon is N Lean files in Pnp/Theory, all of them replayed through the kernel
            by tools/check_lean.ps1 with a negative control -- said in the project memory, and
            said in paper 4's Honest scope section
actual    : Pnp/Theory/Cyclotomic.lean was imported by NOTHING.  lean4checker replays the
            import closure of the root module `Pnp`, and `lake build` builds that same closure,
            so the file was neither built nor replayed -- it simply sat in the canon directory
            looking canonical.  It had been there for several rounds.  No paper cites it, so no
            published claim was affected; the bookkeeping was wrong, not the mathematics.
check     : compute the import closure of the root module and diff it against the directory.
            Twenty lines, and it names the orphan immediately.  Negative control: delete one
            import line and confirm the check reports exactly that module.
rule      : F55's shape again -- the control must be on the property you mean, not a proxy.
            "The file is in the canon directory" is a proxy for "the kernel replayed it", and
            the two come apart precisely when someone adds a file and forgets the import, which
            is the only case you were checking for.  *** A membership list maintained by hand
            is not a property of the build.  Make the build compute it. ***  check_lean.ps1 now
            exits 4 if a Pnp/Theory file is outside the closure.
```

## r117: when a discipline is applied unevenly, look for the missing tool before blaming the habit

```
claimed   : (external review) papers 3 and 4 label the status of every claim while paper 2
            leaves its caveats in the abstract and in remarks -- read as a discipline we apply
            inconsistently, and I accepted that reading and started fixing prose
actual    : paper 2 had no \STATUS macro.  Papers 3 and 4 define \STATUS and \TODO in their
            preambles; paper 2 defined neither, so a status tag there was not merely unwritten,
            it did not compile.  Found only because the first tag I typed threw "Undefined
            control sequence" -- i.e. the compiler diagnosed the cause after the reviewer had
            diagnosed the symptom.
check     : before concluding that an artefact fails to follow a practice, grep the artefacts
            for the MACHINERY of that practice and compare.  One grep across four files:
            `def:0 uses:1` for paper 2 against `def:1 uses:33` for papers 3 and 4.
rule      : an uneven practice across sibling artefacts usually has a mechanical cause, and the
            mechanical cause is cheaper to find and cheaper to fix than the habit.  Check
            whether the tool is present in all of them BEFORE writing prose fixes one by one --
            otherwise you repair instances of a defect whose source keeps producing more.
```

## r117: a check scoped to "everything" is a check that gets switched off

```
claimed   : the closure check should require every .lean file under Pnp/ to be reachable from
            the root -- the natural first statement of the rule
actual    : Pnp/Experiments holds ten files that are DELIBERATELY outside the closure (scratch
            work, not claims).  The rule as first written flags all ten, so the check fails on
            a correct tree, every run, forever.  A check that always fails is a check that is
            read once and then ignored -- worse than no check, because its presence is taken
            for coverage.
check     : run the new check on the CURRENT tree before believing its rule.  If it fails on a
            state you consider correct, the rule is wrong, not the tree.
rule      : scope a check to the property you actually mean, and make the exclusion visible
            rather than silent -- the harness prints "10 file(s) deliberately outside" instead
            of quietly skipping them, so the exclusion can be audited and cannot grow unnoticed.
            Related to F32 (is the observable the one the hypothesis predicts?): here the
            observable was right and the DOMAIN was too large.
```

## r117: a keyword search cannot tell a thing from the sentence denying it

```
claimed   : a `sorry` audit over the canon reported FIVE hits, in five different files
actual    : all five were the line
              -- Audit trail: no `sorry`, and no axioms beyond Lean's three.
            i.e. the search reported the DOCUMENTATION OF AN ABSENCE as the presence of the
            thing.  Had I trusted it, I would have gone looking for five proof holes that do
            not exist; had the polarity been reversed -- a whitelist search for a required
            marker -- a comment would have satisfied it and a missing marker would have passed.
check     : exclude comments, and then ask what the AUTHORITATIVE evidence is.  For `sorry` it
            is not the source text at all: it is the build's own `depends on axioms` output,
            which prints [propext, Classical.choice, Quot.sound] per theorem and cannot be
            written by a comment.  `sorryAx` would appear there.
rule      : a textual search for a keyword matches every mention of it, including the sentence
            asserting it is absent -- and files that are careful enough to document the absence
            are exactly the files that will trip the search.  *** Prefer evidence the artefact
            cannot produce about itself: a compiler's output over its source, a log over a
            claim in the log's header. ***  Where a grep is the only option, exclude comments
            and print the matched LINE, never just the count -- the count alone reads as five
            defects.
```

## r117: a claim about your own verification apparatus is a measurement

```
claimed   : paper 4's Honest scope read "lean4checker, 14 modules, with a negative control"
actual    : the closure is 15 modules, and the moment I fixed the Cyclotomic import it became
            16 -- so the corrected number would have gone stale inside the same round that
            corrected it.  Nothing in check.py covers this: C2/F19 checks numbers in TABLES
            against experiment logs, and a number in prose about our own infrastructure has no
            log to be checked against.
check     : ask what makes the number go stale.  If the answer is "an unrelated file", the
            number is the wrong thing to publish.
rule      : prefer a published claim that is invariant under routine work.  Paper 4 now states
            the PROPERTY -- every file it names is inside the replayed closure, and the harness
            fails if a canon file is outside it -- and states no count, because the count is a
            fact about the tree that changes and the property is a fact about the check that
            does not.  Counting is fine in a report, which is dated; a paper is not dated.
```

## F55 — a search over a net needs a positive control

```
claimed   : "the minimum of G over the minor arcs is 0.652, and it is not at theta = 1/4"
actual    : the minimum is 0.3466 AT theta = 1/4, exactly (1/2)log 2.  The scan used 1001
            evenly spaced points and the dip at 1/4 has width O(1/N) = 1.2e-4, so the net
            stepped straight over it and reported the value of a nearby ordinary point.
check     : put a point whose answer is already known inside the search space and require the
            search to FIND it.  Here theta = 1/4 was known to give (1/2)log 2 from
            Theorem thm:modfour; a scan that does not recover it has the wrong resolution and
            its output is noise, whatever it prints.
rule      : any search over a discretised domain -- a theta net, a grid of parameters, a
            random sample -- must contain a control point whose answer is known independently,
            and the search must be reported as invalid unless it recovers it.  Resolution is
            a parameter you chose (F26); the control is how you find out you chose it wrong.
            Sharper than F26 because the failure here was silent and self-consistent: the
            coarse scan returned the same wrong answer at all three exclusion radii.
```
