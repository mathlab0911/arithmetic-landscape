#!/usr/bin/env python3
"""
r098 / E5 of spec_paper4_concept_r097: the biased invariant Gamma^{(q)}.

Seed under test (fable, spec section 2):
    Gamma^{(q)}(A) = 1 + SUM_{d>=1} [ q^{N_d} + (1-q)^{N_d} ],     q=1/2 recovers Gamma.

Audit of the derivation, done before measuring (paper 1's classification is measure-free):
  overshoot at depth d : every a <= 2d is EXCLUDED  -> weight (1-q)^{N_d}
  undershoot at depth d: every a <= 2d is INCLUDED  -> weight  q^{N_d}
  P_q(S) factorises over I_d and B_d, so with
      r^q_B(m) = SUM_{U subset B, sum U = m} q^{|U|} (1-q)^{|B|-|U|}
      over_q  = (1-q)^{N_d} r^q_{B_d}(n+d)
      under_q =  q^{N_d}    r^q_{B_d}(n-d-sigma_d)
      deg_q   = SUM_{J subset I_d} q^{|J|}(1-q)^{N_d-|J|} r^q_{B_d}(n-sigma(J))
  and the binomial sum over J is 1, so a flat r^q gives the d-th term
  q^{N_d} + (1-q)^{N_d}.  The seed is right.

*** BUT fable's proposed discriminator cannot work. ***
Gamma^{(q)} is manifestly SYMMETRIC in q <-> 1-q, and so is the complementation identity
lm_q(n) = lm_{1-q}(T-n) at the q-tilted centre (since T - qT = (1-q)T).  So neither the
point prediction nor the free check can tell an over/under swap from the truth.
The test that DOES discriminate is per stratum, and it is free from the same DP:
      over_q/deg_q  vs (1-q)^{N_d}        under_q/deg_q  vs  q^{N_d}
Under a swap these two swap, which at q != 1/2 is a difference of orders of magnitude.

Checks run here:
  (A) complementation lm_q(n) = lm_{1-q}(T-n), exact       [fable's free check]
  (B) float64 DP vs exact rationals at one (k,q)           [F34]
  (C) point prediction Gamma^{(q)} vs measured lm_q/deg_q  [the seed]
  (D) PER-STRATUM assignment test                          [the real discriminator]
Fail rule: anything off by more than its predicted scale -> report raw and stop.
"""
import math
from fractions import Fraction


def odd_primes(k):
    out, n = [], 3
    while len(out) < k:
        if all(n % p for p in range(3, int(n ** .5) + 1, 2)):
            out.append(n)
        n += 2
    return out


ENS = {'odds': lambda k: [2 * i + 1 for i in range(k)], 'primes': odd_primes}


def strata_q(A, q, n, exact=False):
    """Biased weighted DP.  Returns (deg_q, lm_q, per-stratum lists).

    dp holds r^q_{B_d} as elements are added from the top down, exactly as in the
    unbiased pipeline (validated r080), but with weights (1-q) for 'absent' and q for
    'present'.
    """
    one = Fraction(1) if exact else 1.0
    qq = Fraction(q).limit_denominator(10 ** 6) if exact else float(q)
    p0 = one - qq
    A = sorted(A); k = len(A); T = sum(A); D = (A[-1] - 1) // 2
    dp = [one]
    cur = k
    over, under, Nds = [], [], []
    g = lambda m: dp[m] if 0 <= m < len(dp) else one * 0
    for d in range(D, 0, -1):
        j = 0
        while j < k and A[j] <= 2 * d:
            j += 1
        while cur > j:
            cur -= 1
            a = A[cur]
            nw = [one * 0] * (len(dp) + a)
            for m, v in enumerate(dp):
                if v:
                    nw[m] += p0 * v
                    nw[m + a] += qq * v
            dp = nw
        Nd = j
        sig = sum(A[i] for i in range(j))
        over.append((d, Nd, g(n + d) * p0 ** Nd))
        under.append((d, Nd, g(n - d - sig) * qq ** Nd))
        Nds.append((d, Nd))
    while cur > 0:
        cur -= 1
        a = A[cur]
        nw = [one * 0] * (len(dp) + a)
        for m, v in enumerate(dp):
            if v:
                nw[m] += p0 * v
                nw[m + a] += qq * v
        dp = nw
    deg = g(n)
    lm = deg + sum(x for _, _, x in over) + sum(x for _, _, x in under)
    return deg, lm, over, under


def gamma_q(A, q):
    A = sorted(A); k = len(A); D = (A[-1] - 1) // 2
    tot = 1.0; j = 0
    for d in range(1, D + 1):
        while j < k and A[j] <= 2 * d:
            j += 1
        t = q ** j + (1 - q) ** j
        if t < 1e-18:
            break
        tot += t
    return tot


QS = [0.2, 0.3, 0.4, 0.5, 0.6]

print('=' * 100)
print('(A) free exact check:  lm_q(n) = lm_{1-q}(T-n)   [complementation]')
print('=' * 100)
print(f"{'ens':>8} {'k':>4} {'q':>5} {'lm_q(n_q)':>16} {'lm_{1-q}(T-n_q)':>18} {'rel diff':>10}")
for nm, k in (('odds', 40), ('primes', 40)):
    A = sorted(ENS[nm](k)); T = sum(A)
    for q in (0.2, 0.3, 0.4):
        n = int(round(q * T))
        _, lm1, _, _ = strata_q(A, q, n)
        _, lm2, _, _ = strata_q(A, 1 - q, T - n)
        print(f'{nm:>8} {k:4d} {q:5.2f} {lm1:16.9e} {lm2:18.9e} '
              f'{abs(lm1 / lm2 - 1):10.2e}')

print()
print('=' * 100)
print('(B) float64 DP vs exact rationals, one (k,q)')
print('=' * 100)
A = sorted(ENS['odds'](14)); T = sum(A); q = 0.25; n = int(round(q * T))
df, lf, _, _ = strata_q(A, q, n)
de, le, _, _ = strata_q(A, q, n, exact=True)
print(f'  odds k=14, q=0.25, n={n}:  deg rel diff = {abs(df/float(de)-1):.2e}, '
      f'lm rel diff = {abs(lf/float(le)-1):.2e}')

print()
print('=' * 100)
print("(C) the seed:  Gamma^{(q)} point prediction vs measured lm_q/deg_q at n_q = round(qT)")
print('=' * 100)
print(f"{'ens':>8} {'k':>4} {'q':>5} {'measured':>13} {'Gamma^(q)':>13} {'rel diff':>10}")
for nm, ks in (('odds', (60, 100, 140)), ('primes', (60, 100, 140))):
    for k in ks:
        A = sorted(ENS[nm](k)); T = sum(A)
        for q in QS:
            n = int(round(q * T))
            deg, lm, _, _ = strata_q(A, q, n)
            meas = lm / deg
            pred = gamma_q(A, q)
            print(f'{nm:>8} {k:4d} {q:5.2f} {meas:13.6f} {pred:13.6f} '
                  f'{abs(meas / pred - 1):10.2e}')
    print()

print('=' * 100)
print('(D) THE DISCRIMINATOR: per-stratum weights.  over/deg should be (1-q)^{N_d},')
print('    under/deg should be q^{N_d}.  A swap would exchange the last two columns.')
print('=' * 100)
for nm, k in (('odds', 100), ('primes', 100)):
    A = sorted(ENS[nm](k)); T = sum(A)
    for q in (0.3, 0.4):
        n = int(round(q * T))
        deg, lm, over, under = strata_q(A, q, n)
        print(f'\n  {nm}, k={k}, q={q}:')
        print(f"    {'d':>3} {'N_d':>4} {'over/deg':>13} {'(1-q)^N_d':>13} {'ratio':>9} "
              f"| {'under/deg':>13} {'q^N_d':>13} {'ratio':>9}")
        for (d, Nd, ov), (_, _, un) in list(zip(over, under))[::-1][:6]:
            po, pu = (1 - q) ** Nd, q ** Nd
            print(f'    {d:3d} {Nd:4d} {ov/deg:13.6e} {po:13.6e} {ov/deg/po:9.5f} '
                  f'| {un/deg:13.6e} {pu:13.6e} {un/deg/pu:9.5f}')

print()
print('=' * 100)
print('(E) closed form for the odd numbers.  N_d = d exactly, so')
print('      Gamma^(q)(odds) = 1 + SUM_d [q^d + (1-q)^d] = 1 + q/(1-q) + (1-q)/q')
print('                      = 1/(q(1-q)) - 1,   minimised at q=1/2 with value 3.')
print('=' * 100)
print(f"  {'q':>5} {'Gamma^(q) summed':>18} {'1/(q(1-q)) - 1':>16} {'diff':>10}")
A = sorted(ENS['odds'](400))
for q in (0.10, 0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80):
    s = gamma_q(A, q); c = 1.0 / (q * (1 - q)) - 1.0
    print(f'  {q:5.2f} {s:18.9f} {c:16.9f} {abs(s-c):10.2e}')
print('  q(1-q) <= 1/4 always, so Gamma^(q)(odds) >= 3 with equality only at q = 1/2:')
print('  the fair coin gives the LEAST rugged landscape of the odd numbers.')
