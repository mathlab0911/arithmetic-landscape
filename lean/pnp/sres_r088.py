#!/usr/bin/env python3
"""
r088 / unplanned decisive test.

Observation from tilt_r088:  both quantities below scale as c/k with the SAME c
per ensemble (odds 1.85, primes ~2.0, squares ~2.85):
    (i)  s/|lambda_true| - 1
    (ii) the Table-1 residual as a fraction of the centred signal
Hypothesis:  the 1% residual is not a missing term in Phi; it is the
             lambda_true-vs-s substitution.  Test: evaluate Phi at s instead.
Falsifier:   if the residual does NOT drop by an order of magnitude, the
             agreement of the two constants is a coincidence and I say so.
"""
import math
import numpy as np
from fractions import Fraction


def odd_primes(k):
    out, n = [], 3
    while len(out) < k:
        if all(n % p for p in range(3, int(n ** .5) + 1, 2)):
            out.append(n)
        n += 2
    return out


ENS = {
    'odds':    lambda k: [2 * i + 1 for i in range(k)],
    'squares': lambda k: sorted(set(2 * ((i * i) // 2) + 1 for i in range(1, k + 1))),
    'primes':  odd_primes,
}


def tilt(A, rho):
    a = np.asarray(A, float); tgt = rho * a.sum()
    lo, hi = 0.0, 1.0
    with np.errstate(over='ignore'):
        while (a / (1.0 + np.exp(hi * a))).sum() > tgt:
            hi *= 2.0
        for _ in range(300):
            mid = .5 * (lo + hi)
            if (a / (1.0 + np.exp(mid * a))).sum() > tgt:
                lo = mid
            else:
                hi = mid
    return .5 * (lo + hi)


def tilt_at_int(A, n):
    """s with tilted mean exactly n (the integer actually used as the target)."""
    return tilt(A, n / float(sum(A)))


def measured(A, rhos):
    A = sorted(A); k = len(A); T = sum(A); D = (A[-1] - 1) // 2
    ns = {r: int(r * T) for r in rhos}; ns[0.5] = T // 2
    dp = np.zeros(1); dp[0] = 1.0; cur = k; ex = {r: 0.0 for r in ns}
    g = lambda m: dp[m] if 0 <= m < len(dp) else 0.0
    for d in range(D, 0, -1):
        j = 0
        while j < k and A[j] <= 2 * d:
            j += 1
        while cur > j:
            cur -= 1; a = A[cur]
            nw = np.zeros(len(dp) + a); nw[:len(dp)] = dp; nw[a:a + len(dp)] += dp; dp = nw
        for r, n in ns.items():
            ex[r] += g(n + d) + g(T - n + d)
    while cur > 0:
        cur -= 1; a = A[cur]
        nw = np.zeros(len(dp) + a); nw[:len(dp)] = dp; nw[a:a + len(dp)] += dp; dp = nw
    return {r: ((g(n) + ex[r]) / g(n), 0.25 * math.log(g(n - 2) / g(n + 2)), n)
            for r, n in ns.items()}


def Phi(A, lam):
    A = sorted(A); k = len(A); D = (A[-1] - 1) // 2
    tot = 1.0; j = 0; sig = 0; s2s = 0
    for d in range(1, D + 1):
        while j < k and A[j] <= 2 * d:
            sig += A[j]; s2s += A[j] * A[j]; j += 1
        w = 2.0 ** (1 - j)
        if w < 1e-18:
            break
        arg = lam * (d + sig / 2.0)
        if abs(arg) > 700:
            break
        tot += w * math.exp(-lam * lam * s2s / 8.0) * math.cosh(arg)
    return tot


RH = [0.44, 0.40, 0.30, 0.20]
print('=' * 108)
print('Residual as a fraction of the centred signal:  Phi(lambda_true)  vs  Phi(s)')
print('   s = exact tilt with mean exactly n;  lambda_true = (1/4)log(r(n-2)/r(n+2))')
print('=' * 108)
hdr = ''.join(f'    x={0.5 - r:.2f}' for r in RH)
for nm, ks in (('odds', (100, 140, 180, 220)),
               ('squares', (110, 150, 190)),
               ('primes', (100, 140, 180, 220))):
    print(f'\n  --- {nm}')
    print(f"  {'k':>5} {'variable':>12} " + hdr)
    for k in ks:
        A = sorted(ENS[nm](k))
        m = measured(A, RH)
        r0, l0, n0 = m[0.5]
        s0 = tilt_at_int(A, n0)
        for tag, use_s in (('lambda_true', False), ('s (tilt)', True)):
            p0 = Phi(A, s0 if use_s else l0)
            cells = []
            for r in RH:
                rm, lam, n = m[r]
                v = tilt_at_int(A, n) if use_s else abs(lam)
                pp = Phi(A, v)
                cells.append(f'  {abs(((rm - pp) - (r0 - p0)) / (rm - r0)) * 100:7.3f}%')
            print(f'  {k:5d} {tag:>12} ' + ''.join(cells))
