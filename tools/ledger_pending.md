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
