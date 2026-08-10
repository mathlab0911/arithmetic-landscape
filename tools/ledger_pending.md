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
