# Pending ledger entries

Entries written during a round but not yet folded into the `pnp-research` skill's §7.
`tools/check.py` prints these on every run so they cannot be lost. Clear this file at the
next skill save.

---

## F47 — a check that is invariant under the thing you want to detect is not a check

```
claimed : "the complementation identity lm_q(n) = lm_{1-q}(T-n) discriminates immediately
          if I have the over/under assignment swapped"  (spec_paper4_concept_r097)
actual  : it cannot. Gamma^{(q)} = 1 + SUM [q^{N_d} + (1-q)^{N_d}] is symmetric in
          q <-> 1-q, and the complementation identity IS that symmetry: at the q-tilted
          centre, T - qT = (1-q)T. Point prediction, free check and measured ratio are all
          invariant under the swap. Confirmed in the data: the measured ratio at q=0.4 and
          q=0.6 agrees to every printed digit (3.166045).
check   : before adopting a test, apply the transformation you are trying to detect to the
          quantity the test compares. If the quantity does not move, the test is blind.
          Ten seconds, on paper, and it also tells you what to measure instead: here,
          splitting the sum into its two strata discriminates by a factor of 161.
rule    : a test must be checked for SENSITIVITY to the alternative, not only for
          correctness under the hypothesis. Symmetry in the observable is the usual
          culprit: if the claimed effect and its negation predict the same number, no
          amount of precision will separate them. Corollary: when a quantity is a SUM,
          ask whether the summands can be measured separately -- an aggregate can be
          blind to a permutation of its parts.
```

## F48 - "formalise X" must be diffed against the canon AND against the paper (r100)
  claimed : "E9: formalise Phi(0) = Gamma, i.e. 1 + SUM 2^{1-N_d} = gapSeries"
  actual  : Phi(0) = W_D = Gamma + (2D+1)2^{-k}.  The tail was dropped in the spec, is present
            in paper 3 (rem:lam0), and the correct identity windowSeries_eq_gapSeries has been
            Lean-verified since paper 1.  The task was both wrong and already finished.
  check   : before starting a formalisation, grep the canon for the statement and diff the
            spec's version against the paper's.  Two commands.
  rule    : a task that says "formalise X" must be checked against (a) what the canon already
            proves and (b) how the PAPER states X, not how the spec restates it.  Specs
            paraphrase; paraphrase drops terms.
  note    : r100 reported this entry as filed.  It was not.  C6 caught the omission one round
            later, by the entry simply not appearing in the pending list.  A report claiming
            an artefact exists is not evidence that it does -- that is F20 applied to the
            ledger itself.

## F49 — measure at the index the papers use (r102, mine)
  claimed : "measure the peak spectrum and compare primes to random odd sequences"
  actual  : the minor arcs live on B_d = {a > 2d}, not on A.  Measured on A the primes lose
            the modulus-6 peak too (3 is in A), so the measurement reported primes and random
            instances as identical -- erasing the one difference it existed to find.
  rule    : when a quantity in the papers carries an index, measure it AT that index.  The
            un-indexed version is a different quantity and can be invariant under exactly the
            distinction being tested.  F47's sibling: F47 is about the transformation, F49 is
            about the domain.

## F50 — a reader who misses what is there has found a defect in the writing (r102)
  observed: a careful external referee asked for two things paper 3 already contains -- the
            ineffective-constant acknowledgment (introduction, bullet 4, in italics) and the
            saddle-point identity s-|lambda| = K'''/(2K''^2) (rem:onek, verbatim) -- and found
            neither.
  rule    : when an external reader asks for something already present, that is a presentation
            defect, not a reader error.  Record where they looked and what they missed; do not
            reply "it is already there" and move on.

## F51 - a fail rule must state its measurement floor (r103, mine)
  observed: the c_d share for the squares came out at -0.51%, and the monotonicity fail rule
            fired -- on a quantity whose true size is 8.9e-10, i.e. on float noise.
  rule    : a fail rule must distinguish "the effect is absent" from "the effect is below the
            measurement floor".  State the floor together with the rule.  A monotonicity test
            applied to noise reports a failure that is really a confirmation: the prediction
            said the quantity would be unmeasurably small there, and it was.

## F52 - prove load-bearing formal statements twice (r105, fable's wording)
  practice: for a load-bearing formal statement, prove it twice by unrelated routes.
            Two proofs check the STATEMENT; one proof checks the tactic script.
            (TermwiseMin: convexity and Bernoulli.)

## F53 - know the error of your baseline before differencing against it (r105, mine)
  claimed : "measure the first-order response as (R(n) - Gamma^{(q)}) / lambda"
  actual  : the point prediction carries a known O(1e-3) offset at the biased centre -- E5
            measured it -- and the linear term at the targets used is the same size.  The
            estimator was measuring the offset, and Lhat swung from -11 to -70.
  rule    : before extracting a derivative, ask what the KNOWN error of the baseline is.  If
            it is not small compared with the effect, difference the effect against itself
            (central difference) instead of against the baseline.  The information needed to
            predict this failure was already in my own earlier log.

## F54 - keep the two verification axes apart (r107, mine)
  observed: an independent proof-checker (Comparator: lean4export + nanoda_bin) was described
            as mechanising F52.  It does not: it re-checks the proof TERM with a second kernel.
  rule    : "is the proof valid" and "is the statement the one I meant" are different
            questions with different tools, and the second is the likelier failure.  A tool
            that answers one must never be booked as answering the other.  An independent
            kernel cannot tell you a theorem is not vacuously true.
