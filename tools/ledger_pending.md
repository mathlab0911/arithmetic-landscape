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
