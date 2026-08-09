#!/usr/bin/env python3
"""
r092 / work items 1-3 of r091.

Item 1  point test of the saddle identity, EXACT, no asymptotics:
            s - |lambda|  ==  K'''/(2 K''^2) ?
        with  K'' = SUM a^2 p(1-p),  K''' = SUM a^3 p(1-p)(1-2p).
        The sign is DERIVED below, not fitted:

          Lam(s) = SUM log(1+e^{-s a}),  -Lam'(s) = SUM a p_a = n,  p_a = 1/(1+e^{s a})
          Lam''  = SUM a^2 p(1-p) = K''            > 0
          Lam''' = -SUM a^3 p(1-p)(1-2p) = -K'''   < 0  for p < 1/2  (i.e. rho < 1/2)
          log r(n) ~ Lam(s) + s n - (1/2) log(2 pi Lam'')
          d/dn log r = s + Lam'''/(2 Lam''^2) = s - K'''/(2 K''^2)      [s' = -1/Lam'']
          lambda := -d/dn log r  ==>  |lambda| = s - K'''/(2K''^2)
          ==>  s - |lambda| = + K'''/(2 K''^2),  so s > |lambda|.  The + sign is forced.

Item 2  k * S4/S2^2  (pure arithmetic, no measurement)  vs  k(s/|lambda|-1)  vs  c_A.
Item 3  the alpha = 1/2 double test.  Prediction (2a+1)^2/(4a+1) = 4/3 for BOTH constants.
        Faithfulness check first: k*S4/S2^2 of the CONSTRUCTED set must itself be ~ 4/3,
        otherwise the construction is not an alpha=1/2 profile and the test is void.
        (H) diagnostic printed too: SUM 2^{-N_d} delta_d^2 must not grow with k.
"""
import math
import numpy as np


def odd_primes(k):
    out, n = [], 3
    while len(out) < k:
        if all(n % p for p in range(3, int(n ** .5) + 1, 2)):
            out.append(n)
        n += 2
    return out


def sqrt_profile(k, C=None):
    """a_i ~ C i^{1/2}, odd, strictly increasing.  C >= ~4 sqrt(k) keeps the gaps >= 2."""
    if C is None:
        C = 6.0 * math.sqrt(k)
    out, prev = [], -1
    for i in range(1, k + 1):
        o = int(math.ceil(C * math.sqrt(i)))
        if o % 2 == 0:
            o += 1
        if o <= prev:
            o = prev + 2
        out.append(o); prev = o
    return out


ENS = {
    'odds':    lambda k: [2 * i + 1 for i in range(k)],
    'squares': lambda k: sorted(set(2 * ((i * i) // 2) + 1 for i in range(1, k + 1))),
    'primes':  odd_primes,
    'sqrt':    sqrt_profile,
}
ALPHA = {'odds': 1.0, 'squares': 2.0, 'primes': 1.0, 'sqrt': 0.5}


def tilt(A, rho):
    a = np.asarray(A, float); tgt = rho * a.sum(); lo, hi = 0.0, 1.0
    with np.errstate(over='ignore'):
        while (a / (1 + np.exp(hi * a))).sum() > tgt:
            hi *= 2
        for _ in range(400):
            mid = .5 * (lo + hi)
            if (a / (1 + np.exp(mid * a))).sum() > tgt:
                lo = mid
            else:
                hi = mid
    return .5 * (lo + hi)


def cumulants(A, s):
    a = np.asarray(A, float)
    with np.errstate(over='ignore'):
        p = 1.0 / (1.0 + np.exp(s * a))
    w = p * (1 - p)
    return float((a ** 2 * w).sum()), float((a ** 3 * w * (1 - 2 * p)).sum())


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
    return {r: ((g(n) + ex[r]) / g(n), 0.25 * math.log(g(n - 2) / g(n + 2)))
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


def Hseries(A):
    """(H) diagnostic:  SUM_d 2^{-N_d} delta_d^2 ."""
    A = sorted(A); k = len(A); D = (A[-1] - 1) // 2
    tot = 0.0; j = 0; sig = 0
    for d in range(1, D + 1):
        while j < k and A[j] <= 2 * d:
            sig += A[j]; j += 1
        w = 2.0 ** (-j)
        de = d + sig / 2.0
        if w * de * de < 1e-14 and d > 2 * A[0]:
            break
        tot += w * de * de
    return tot


def s4s2(A):
    a = np.asarray(A, float)
    return float((a ** 4).sum()) / float((a ** 2).sum()) ** 2


# ============================================================ item 1
print('=' * 112)
print('ITEM 1  exact point test of the saddle identity:  s - |lambda|  vs  K\'\'\'/(2 K\'\'^2)')
print('        the + sign is derived (see docstring), not fitted')
print('=' * 112)
print(f"{'ens':>8} {'k':>5} {'x':>5} {'s-|lambda|':>14} {'K3/(2K2^2)':>14} "
      f"{'ratio':>10} {'rel.err':>10}")
KS = {'odds': (100, 140, 180, 220), 'squares': (100, 140, 170),
      'primes': (100, 140, 180, 220), 'sqrt': (100, 140, 180, 220)}
for nm in ('odds', 'squares', 'primes', 'sqrt'):
    for k in KS[nm]:
        A = sorted(ENS[nm](k))
        m = measured(A, [0.40, 0.20])
        for rho in (0.40, 0.20):
            s = tilt(A, rho); lam = abs(m[rho][1])
            K2, K3 = cumulants(A, s)
            pred = K3 / (2 * K2 ** 2)
            got = s - lam
            print(f'{nm:>8} {k:5d} {0.5 - rho:5.2f} {got:14.6e} {pred:14.6e} '
                  f'{got / pred:10.6f} {abs(got / pred - 1):10.2e}')
    print()

# ============================================================ item 2
print('=' * 112)
print("ITEM 2  k*S4/S2^2 (no measurement)  vs  k(s/|lambda|-1)  vs  c_A = k*R")
print("        asymptotic prediction (2a+1)^2/(4a+1):  odds/primes 1.8, squares 2.778, sqrt 1.333")
print('=' * 112)
RH = [0.44, 0.40]
print(f"{'ens':>8} {'k':>5} {'|A|':>5} {'k*S4/S2^2':>11} {'k(s/lam-1)':>12} "
      f"{'c_A = k*R':>11} {'pred':>8} {'(H) series':>12}")
for nm in ('odds', 'squares', 'primes', 'sqrt'):
    al = ALPHA[nm]; pr = (2 * al + 1) ** 2 / (4 * al + 1)
    for k in KS[nm]:
        A = sorted(ENS[nm](k))
        m = measured(A, RH)
        r0, l0 = m[0.5]; p0 = Phi(A, l0)
        rm, lam = m[0.40]; lam = abs(lam)
        s = tilt(A, 0.40)
        pp = Phi(A, lam)
        cA = abs(((rm - pp) - (r0 - p0)) / (rm - r0)) * 100 * k
        print(f'{nm:>8} {k:5d} {len(A):5d} {k * s4s2(A):11.4f} '
              f'{k * (s / lam - 1):12.4f} {cA / 100:11.4f} {pr:8.4f} {Hseries(A):12.4g}')
    print()
