# Failure-ledger case files — full text

The `pnp-research` skill (§7) carries the *rules*. This file carries the *cases* they were
distilled from, in full, so a rule can be re-derived if it is ever doubted or needs sharpening.
Entries are appended when they are folded into the skill and never edited afterwards.

Folded into the skill at the r117 save (rounds r110–r117, 15 entries).

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

---

Folded into the skill at the r118 save (rounds r117–r118, 6 entries).

## r117: "force push" is not "deleted", and the identity in a commit is a published claim

```
claimed   : after git filter-repo and a force push, the design documents were gone -- every
            local check agreed: 0 tracked, 0 paths anywhere in history, 404 on main
actual    : GitHub keeps unreachable objects, and the OLD COMMIT SHA still served the full file.
            The local checks were all true and all irrelevant: they measured the repository I
            control, not the one the reader sees. Only deleting and recreating the repository
            actually removed it. The same thing then happened a second time with commit
            identity -- the visible history was clean and an orphaned SHA still showed the wrong
            account.
check     : fetch the artefact from OUTSIDE, by the route a reader would use, with a positive
            control alongside it -- an empty response means nothing until a URL you expect to
            work returns content. Then repeat for an old SHA, not just for the branch tip.
rule      : *** rewriting history changes what is REACHABLE, not what is STORED. *** For content
            that must actually be gone from a hosted repository, delete and recreate it; there
            is no client-side operation that does the job. And check from the outside: a
            verification run against your own working copy cannot see a hosting layer.
extra     : the second half of this entry is a plain mistake of mine. I committed with
            `-c user.email=<the account address from my environment>` instead of the address the
            repository was configured with, and GitHub attributes commits by email -- so ninety
            commits were credited to an unrelated account of the author's. **A commit identity
            is published metadata, not a local setting.** Read `git config user.email` in the
            repository and use that; never substitute an address from somewhere else.
```

## r118: a check that examined nothing has not passed  [ASSERTED in check.py]

```
claimed   : "25 scripts cited by the papers, all present with logs" -- except the first run of
            that check printed "0 cited ... all present", and I read the words 'all present'
            before I read the zero.  The regex required the round suffix twice and matched
            nothing.  A clean bill of health over an empty set.
actual    : the papers cite 25 scripts and they are all fine, but the check that said so was,
            for one run, incapable of saying anything else.  This is the third time in one
            afternoon: C11 v1 keyed on the correct digits and so never looked at the wrong
            ones; a broad "unsourced claim" scan flagged 130 lines of which almost none were
            defects and so could not be acted on either.
check     : read the COUNT before the verdict.  Every check that reports how many things it
            examined must fail when that number is zero.
rule      : *** silence from a check is good news only if the check spoke. ***  Zero subjects
            is a failure of the check, not a pass for the artefact -- and it is the failure
            mode a green suite hides best, because nothing looks wrong.  Asserted:
            `expect_subjects()` in check.py, wired into C1, C7, C8, C10, C11 and C12, with a
            negative control (break C12's regex, get "examined 0 ... which is a failure of the
            check and not a pass for the artefact").
            Corollary for the other direction: a check whose positives are mostly not defects
            is equally useless, and must be narrowed until they are (F57), or dropped.
```

## F20 — new instance, r118: preparing a check is not performing it

```
claimed   : the OEIS question is covered.  `oeisseq_r30.py` exists, its header says the point
            of it -- "if anyone else studies this object these sequences are probably in OEIS;
            if they are not, that is fairly strong evidence" -- and its log dutifully prints the
            sequences.  It has sat in the repository for eighty-eight rounds.
actual    : the log contains the sequences and NO RESULT.  There is no record that anyone ever
            pasted them into oeis.org.  The script prepares the query; nothing performs it.  So
            the project has carried an unexamined belief that the prior-art question was closed
            when the only artefact is the question, neatly typed.
check     : for any "we checked X" claim, ask which line of which log holds the ANSWER, not the
            question.  Grep the log for the outcome, not for the setup.
rule      : F20 says a result with no log does not exist.  The sharpening: *** an artefact that
            PREPARES a check is not the check, and it is more dangerous than nothing, because it
            looks like diligence and closes the question in the reader's mind. ***  A script
            whose output is an input to a human step must say so and must have a place for the
            human's answer to be recorded, or the step will silently never happen.
what      : the queries are written out ready to paste in `outgoing/oeis_queries.md`, with what
            to do for each outcome.  I could not run them: this session cannot reach oeis.org
            (positive control -- searching the decimal expansion of sqrt2 -- also returned
            empty, so "not found" would have been a lie).  Paper 1 now says in the text that the
            gap series has not been looked up as an integer sequence in a way we can point at.
```

## F47 — new instance, r118: a check keyed on the right answer cannot see a wrong one

```
claimed   : C11 asserts that every named constant in the papers is correct at the precision it
            is printed.  Written, tested with two negative controls, shipped, and it passed.
actual    : it passed a paper containing FOUR wrong constants -- 0.6916 for 7^(1/6)/2 (0.6915),
            0.9814 and 0.0188 for e^{1/8}sqrt3/2 and its margin (0.9813, 0.0187), 0.2136 for
            16 delta^2 (0.2135).  v1 keyed each constant on the leading digits of its CORRECT
            value ('0.9813' -> ...), so a literal wrong in exactly those digits matched no key
            and was never looked at.  The negative controls passed because I built them by
            corrupting a literal the check could already see.
check     : ask what the check keys on, and whether the error you are hunting changes the key.
            Here the error changes the digits, and the digits were the key.
rule      : F47 exactly -- *** a check invariant under the thing you want to detect is not a
            check *** -- but in the form that is easiest to walk into: a check that finds its
            subject by matching the correct answer can only ever confirm what is already right.
            Key on something the error does NOT change: the surrounding definition, or (as v2
            does) mere PROXIMITY, so that a near-miss is caught precisely because it is near.
            And build the negative control by corrupting the artefact in the way the real world
            corrupts it, not in the way the check happens to notice.
note      : v2 traded blindness for false positives -- one measured value lands 1.4e-4 from a
            constant by coincidence.  That is recorded as an exemption WITH ITS REASON rather
            than fixed by widening the tolerance, and the exemption is keyed to the literal, so
            corrupting that same position still fires (verified).  A check that is loosened to
            stop complaining has been switched off with extra steps.
```

## r118: a directory you create beside a mount is not inside it

```
claimed   : the r118 experiment scripts were "saved to study-private-lab", safe from the
            session ending -- I had made the directory with mkdir and written into it, and a
            listing showed all ten files
actual    : the sandbox exposes only the mounted folders. `mkdir ../study-private-lab` from
            inside the mount created a directory in the SANDBOX that merely sits beside the
            mount point and shares its name with a real folder on the user's machine. The two
            were different directories with different contents, and everything written to the
            sandbox one would have vanished when the session ended. Found only because a
            Windows-side listing showed two of the ten files instead of ten.
check     : list the directory from BOTH sides before trusting it, or write through a path
            that is known to be shared. The transfer route that works: sandbox -> the outputs
            folder (which is genuinely mounted) -> move on the Windows side.
rule      : *** persistence is a property of the path, not of the write succeeding. *** A
            successful write and a correct-looking listing prove only that some filesystem
            accepted the bytes. Before treating a file as saved, confirm it from the side that
            outlives the session -- the same shape as F55 (the control must be on the property
            you mean) and the same shape as "force push is not deletion" (a local check cannot
            see the other side of a boundary).
```

## F35 — the summaries are a POPULATION, and they drift together (r117, pre-endorsement sweep)

```
claimed   : after r117 the papers were honest -- status inside every theorem, C8 enforcing it --
            so the over-claiming was fixed
actual    : three summaries still said more than the papers, and were found one at a time, each
            only because someone was about to read it.
              memory   -- paper 3 recorded as "finished" while its two theorems are skeletons
              README   -- papers 2 and 3 called "Complete"; every count stale
              homepage -- "Every theorem I state is formally verified in Lean 4 with Mathlib,
                          with no sorry and no additional axioms", which is true of the
                          structural results and false of papers 2, 3 and 4; paper 2 listed
                          under a title it had not carried for weeks; papers 3 and 4 absent
            The homepage is the one linked from the signature of every endorsement email sent.
check     : enumerate the artefacts that DESCRIBE the work -- memory, README, homepage, the
            abstracts, any profile or bio -- and check them against the papers as a set, in one
            pass. There were four; I fixed them in three separate rounds because I kept treating
            each as the last one.
rule      : *** F35's population is not "the abstract": it is every artefact that summarises the
            work, and they drift TOGETHER because they were all written from the same optimistic
            draft. *** When one summary is found over-claiming, that is evidence about the
            others, not an isolated defect -- go and check them the same hour. Asserted where the
            artefact is in the repository (C9 for the README's counts); the homepage lives in a
            different repository and is therefore the one most likely to rot next, so it now
            carries the same status vocabulary as the papers, which makes drift visible.
```

---

## Folded into the skill at r131 (fourteen blocks, covering r119–r131)

Dispositions: **F63** new (status label stale in both directions; merged with r120's
defect-versus-ledger). **F64** new (the disclosure one artefact from its reader).
**F65** new (coined vocabulary, counted before defended). Appends: F18 (predicate
paraphrase), F47 (the CV twin, and the too-wide exemption), F52 (same-description audits
and the DROP_GUARD asymmetry), F60 (five scope instances consolidated, plus the
configuration blind spot), F61 (push green / reader stale), F62 (sandbox persistence and
the graveyard-label rule), F39 (the cross-boundary checker and the coverage union).

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
