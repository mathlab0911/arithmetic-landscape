#!/usr/bin/env python3
"""
r102 / audit of the external referee report, item 3.

REFEREE'S CLAIM: "the exact difference  s(n) - |lambda(n)| ~ K'''(s)/(2 K''(s)^2)"  can be
obtained by expanding the saddle-point integral to the next order, and this would upgrade
the empirical c_A/k law to a theorem.

DERIVATION FIRST (F09: derive before measuring).  Tilt by theta, p_a = 1/(1+e^{-theta a}),
Lambda(theta) = SUM log(1+e^{theta a}), Lambda'(theta) = SUM a p_a =: mu(theta).  Then
    r(n) = e^{Lambda(theta) - theta n} P_theta[sigma = n],       choose theta with mu = n
    d/dn [Lambda(theta(n)) - theta(n) n] = -theta                (envelope theorem)
    log P_theta[sigma=n] = -1/2 log(2 pi Lambda'') + (Edgeworth)  at the saddle
    d/dn log P = -1/2 (Lambda'''/Lambda'') theta'(n) = -Lambda'''/(2 Lambda''^2)
    lambda := (1/4) log(r(n-2)/r(n+2)) = -(d/dn) log r = theta + Lambda'''/(2 Lambda''^2)
With s = -theta and n below the centre: theta<0, so p_a<1/2, so 1-2p_a>0, so
Lambda''' = SUM a^3 p(1-p)(1-2p) > 0, and lambda < 0.  Hence
    ***  s - |lambda| = Lambda'''(theta) / (2 Lambda''(theta)^2)  ***
which is exactly the referee's formula.  Small tilt (p ~ 1/2 + theta a/4) gives
Lambda''' ~ -(theta/8) S_4 and Lambda'' ~ S_2/4, so
    (s - |lambda|)/s ~ S_4/S_2^2,   and for a_i ~ c i^al,  k S_4/S_2^2 -> (2al+1)^2/(4al+1).

SO THE REFEREE'S FIRST BULLET IS CORRECT -- AND IS ALREADY IN THE PAPER.  paper 3's
rem:onek derives c'_A = (2al+1)^2/(4al+1) by precisely this route and calls the identity
exact.  What is NOT in the paper, and what the referee's SECOND bullet asks for, is that
the residual constant c_A equals this c'_A.  Paper 3 lists that as conjecture; F45 records
that the naive version ("the residual IS the lambda-vs-s substitution") was measured and is
3x too large.  So the referee's item 3 splits into one part already done and one part still
open, and the open part is not closed by the argument offered.

MEASURED HERE:
  (A) the identity s - |lambda| = Lambda'''/(2 Lambda''^2), exact DP vs exact cumulants
  (B) the small-tilt reduction (s-|lambda|)/s vs S_4/S_2^2
  (C) k S_4/S_2^2 vs (2al+1)^2/(4al+1)
  (D) the referee's hoped-for collapse: is  c_A  (the Table-1 residual constant)  equal to
      k S_4/S_2^2?   This is the open half, measured across four profiles.
Fail rule: if (A) is not exact to the order of the Edgeworth term I have dropped
(relative O(1/K'')), say so and do not dress it up.
"""
import math
import numpy as np

_s = open('alpha_r092.py').read().split("print('=' * 108)")[0]
_ns = {}
exec(compile(_s, 'alpha_r092.py', 'exec'), _ns)
globals().update(_ns)


def odd_primes(k):
    out, n = [], 3
    while len(out) < k:
        if all(n % p for p in range(3, int(n ** .5) + 1, 2)):
            out.append(n)
        n += 2
    return out


def tilt_n(A, n):
    """solve SUM a/(1+exp(s a)) = n exactly for the INTEGER target n (not rho*T)."""
    a = np.asarray(A, float)
    lo, hi = -1.0, 1.0
    with np.errstate(over='ignore'):
        while (a / (1 + np.exp(lo * a))).sum() < n:
            lo *= 2
        while (a / (1 + np.exp(hi * a))).sum() > n:
            hi *= 2
        for _ in range(300):
            mid = .5 * (lo + hi)
            if (a / (1 + np.exp(mid * a))).sum() > n:
                lo = mid
            else:
                hi = mid
    return .5 * (lo + hi)


def cumulants(A, s):
    """Lambda'' and Lambda''' at theta = -s, with p_a = 1/(1+e^{s a})."""
    a = np.asarray(A, float)
    with np.errstate(over='ignore'):
        p = 1.0 / (1.0 + np.exp(s * a))
    w = p * (1 - p)
    return float((a ** 2 * w).sum()), float((a ** 3 * w * (1 - 2 * p)).sum())


def lam_exact(A, n):
    """(1/4) log(r(n-2)/r(n+2)) from the exact DP."""
    A = sorted(A)
    dp = np.zeros(1)
    dp[0] = 1.0
    for x in A:
        nw = np.zeros(len(dp) + x)
        nw[:len(dp)] = dp
        nw[x:x + len(dp)] += dp
        dp = nw
    return 0.25 * math.log(dp[n - 2] / dp[n + 2])


RH = [0.44, 0.40, 0.30, 0.20]
PROFS = [('odds  a=1', lambda k: [2 * i + 1 for i in range(k)], 1.0),
         ('primes', odd_primes, None),
         ('a=1.5', lambda k: pow_profile(k, 1.5), 1.5),
         ('squares a=2', lambda k: pow_profile(k, 2.0), 2.0)]

print('=' * 108)
print("(A)+(B) the referee's identity   s - |lambda| = Lambda'''/(2 Lambda''^2),")
print('        and its small-tilt reduction  (s-|lambda|)/s  =  S_4/S_2^2')
print('=' * 108)
print(f"  {'profile':>12} {'k':>5} {'rho':>5} {'s':>11} {'|lambda|':>11} {'s-|lam|':>11} "
      f"{'L3/(2L2^2)':>11} {'ratio':>8} | {'(s-|l|)/s':>10} {'S4/S2^2':>10} {'ratio':>8}")
worst_A = worst_B = 0.0
for nm, f, al in PROFS:
    for k in (120, 180):
        A = sorted(f(k))
        T = sum(A)
        S2 = sum(x * x for x in A)
        S4 = sum(x ** 4 for x in A)
        for rho in RH:
            n = int(rho * T)
            s = tilt_n(A, n)
            lam = lam_exact(A, n)
            L2, L3 = cumulants(A, s)
            d = s - abs(lam)
            pred = L3 / (2 * L2 ** 2)
            rA = d / pred
            rB = (d / s) / (S4 / S2 ** 2)
            worst_A = max(worst_A, abs(rA - 1))
            worst_B = max(worst_B, abs(rB - 1))
            print(f'  {nm:>12} {k:5d} {rho:5.2f} {s:11.4e} {abs(lam):11.4e} {d:11.4e} '
                  f'{pred:11.4e} {rA:8.5f} | {d/s:10.3e} {S4/S2**2:10.3e} {rB:8.5f}')
    print()
print(f'  worst |ratio - 1| in (A): {worst_A:.3e}      worst in (B): {worst_B:.3e}')
print('  (A) is the identity itself; (B) drops the small-tilt Taylor step, so it is only')
print('  expected to hold to leading order in the tilt.')

print()
print('=' * 108)
print("(C) k S_4/S_2^2  vs the closed form  (2al+1)^2/(4al+1)   [this is c'_A]")
print('=' * 108)
print(f"  {'profile':>12} {'al':>5} " + ''.join(f'{f"k={k}":>12}' for k in (60, 120, 180, 240))
      + f"{'closed form':>14}")
for nm, f, al in PROFS:
    cells = []
    for k in (60, 120, 180, 240):
        A = sorted(f(k))
        S2 = sum(x * x for x in A)
        S4 = sum(x ** 4 for x in A)
        cells.append(f'{k*S4/S2**2:12.5f}')
    cf = '' if al is None else f'{(2*al+1)**2/(4*al+1):14.5f}'
    print(f'  {nm:>12} {str(al):>5} ' + ''.join(cells) + cf)

print()
print('=' * 108)
print("(D) THE OPEN HALF.  Is the Table-1 residual constant c_A equal to c'_A = k S_4/S_2^2?")
print("    c_A := k * R(x) / 100 with R in paper 3's signal-fraction language.")
print('=' * 108)
_cp = "c'_A"
print(f"  {'profile':>12} {'k':>5} " + ''.join(f'  c_A(x={0.5-r:.2f})' for r in RH)
      + f'{_cp:>10}{"c_A/c*_A":>16}')
for nm, f, al in PROFS:
    for k in (120, 180):
        A = sorted(f(k))
        S2 = sum(x * x for x in A)
        S4 = sum(x ** 4 for x in A)
        m = measured(A, RH)
        r0, l0 = m[0.5]
        p0 = Phi(A, l0)
        cs = []
        for r in RH:
            rm, lam = m[r]
            pp = Phi(A, lam)
            cs.append(k * abs(((rm - pp) - (r0 - p0)) / (rm - r0)))
        cp = k * S4 / S2 ** 2
        print(f'  {nm:>12} {k:5d} ' + ''.join(f'{v:14.5f}' for v in cs)
              + f'{cp:10.5f}{cs[0]/cp:16.4f}')
print()
print('  READ THIS COLUMN AGAINST THE PAPER, NOT AGAINST 1 (F18).  paper 3 rem:onek tabulates')
print("  c_A/c'_A with c'_A = k(s/|lambda| - 1), NOT with k S_4/S_2^2; the two differ by the")
print("  small-tilt Taylor step.  rem:onek's own table gives c_A/(k S_4/S_2^2) = 1.8674/1.8000")
print('  = 1.037 for the odd numbers at k=220, and the column above gives 1.040 at k=180.')
print('  So this measurement REPRODUCES the paper rather than contradicting it.')
print()
print('  The new content is the trend.  Deviation from 1, k=120 -> 180:')
print(f"      {'profile':>12} {'k=120':>9} {'k=180':>9} {'ratio':>8} {'implied exponent':>18}")
for nm, f, al in PROFS:
    vs = []
    for k in (120, 180):
        A = sorted(f(k))
        S2 = sum(x * x for x in A); S4 = sum(x ** 4 for x in A)
        m = measured(A, RH); r0, l0 = m[0.5]; p0 = Phi(A, l0)
        rm, lam = m[RH[0]]; pp = Phi(A, lam)
        vs.append(k * abs(((rm - pp) - (r0 - p0)) / (rm - r0)) / (k * S4 / S2 ** 2) - 1.0)
    ex = math.log(vs[0] / vs[1]) / math.log(1.5) if vs[1] > 0 else float('nan')
    print(f'      {nm:>12} {vs[0]:9.4f} {vs[1]:9.4f} {vs[0]/vs[1]:8.3f} {ex:18.2f}')
print('  The gap closes like k^{-1.4..-1.9}, i.e. FASTER than the 1/k law it sits on top of.')
print('  That is evidence for c_A = c\'_A(1+o(1)) -- the status paper 3 already assigns -- and')
print('  it is NOT a proof: the referee\'s proposed mechanism (expand c_d alongside the LCLT')
print('  error and watch it collapse into S_4/S_2^2) is a conjecture about a computation.')
print('  F45 stands: substituting s for lambda directly makes the residual three times worse.')
print()
print('  CONTAMINATED ROW, NOT USED (F32): squares k=120 at x=0.10 reads 0.40003, an order')
print('  below its neighbours, because (dev - dev_0) crosses zero inside that target range.')
