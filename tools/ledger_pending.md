# Pending ledger entries

Entries written during a round but not yet folded into the `pnp-research` skill's §7.
`tools/check.py` prints these on every run so they cannot be lost. Clear this file at the
next skill save.

---

## F46 — check the instance against the hypothesis before using it as a test case

```
claimed : (i) "an alpha = 1/2 profile gives a no-free-parameter double test of c_A = c'_A"
          (ii) "cubes fail (H)"  -- carried in the spec for several rounds
actual  : (i) no alpha < 1 profile can satisfy (H) at all. Distinct odd integers with
              a_i ~ c i^alpha need c >> k^{1-alpha}, so a_1 -> infinity, so N_d = 0 for
              d < a_1/2, so SUM 2^{-N_d} delta_d^2 >= SUM_{d<a_1/2} 2d^2 -> infinity.
              The profile is outside the theory's domain, so it can neither confirm nor
              refute a statement about that domain.  Measured: 4923 -> 24464, like k^{3/2}.
          (ii) the cube series is BOUNDED (1.112e7, k-independent from k ~ 140). Cubes fail
              effectively, not asymptotically. The paper had this right; the spec did not.
check   : evaluate the hypothesis numerically on the instance -- one loop, seconds -- before
          designing anything around it. In both directions: on instances claimed to satisfy
          it and on instances claimed to violate it.
rule    : a test case must be checked against the theory's own hypotheses before it is used
          as evidence, and a named hypothesis must be evaluated at least once on every
          profile the paper says satisfies or violates it. A qualitative claim that has
          never been computed is a conjecture wearing a hypothesis's clothes.
```
