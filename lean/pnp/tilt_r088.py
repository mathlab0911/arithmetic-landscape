#!/usr/bin/env python3
"""
r088 / task 2 of spec_t3rigid_r087 §5.2  +  the squares k-scan (r087 judgement 2)
  (a)  s (exact bisection on  sum a/(1+e^{sa}) = rho T)  vs  measured lambda_true
  (b)  s*N  vs  6x
  (c)  the additive-repair decay rate on minor arcs
  (d)  squares: Table-1 residual as a function of k  (does it fall or plateau?)
"""
import math
import numpy as np
from fractions import Fraction

TWO_PI = 2.0 * math.pi


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
    a = np.asarray(A, float); T = a.sum(); tgt = rho * T
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


def measured(A, rhos):
    """exact lm/deg and the local log-slope at each rho (float64 DP, validated r080)."""
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


# ---------------------------------------------------------------- (a) (b)
print('=' * 100)
print('(a)(b)  s  vs  the measured local log-slope, and  s*N  vs  6x')
print('=' * 100)
print(f"{'ens':>8} {'k':>5} {'x':>5} {'s (bisection)':>14} {'|lambda_true|':>14} "
      f"{'s/|lambda|':>11} {'s*N':>8} {'6x':>6} {'s*N/6x':>8}")
for nm in ('odds', 'squares', 'primes'):
    for k in (100, 140, 180, 220):
        if nm == 'squares' and k > 170:
            continue
        A = sorted(ENS[nm](k)); N = A[-1]
        m = measured(A, [0.40, 0.20])
        for rho in (0.40, 0.20):
            x = 0.5 - rho
            s = tilt(A, rho); lam = abs(m[rho][1])
            print(f'{nm:>8} {k:5d} {x:5.2f} {s:14.6e} {lam:14.6e} '
                  f'{s / lam:11.6f} {s * N:8.4f} {6 * x:6.2f} {s * N / (6 * x):8.4f}')
    print()

# ---------------------------------------------------------------- (c)
print('=' * 100)
print('(c)  additive repair: minor-arc decay rate  |G~| <= exp(-t_min * SUM sin^2 / 2)')
print('=' * 100)
print(f"{'ens':>8} {'k':>5} {'x':>5} {'t_min':>8} {'min (1/b)SUM sin^2':>20} "
      f"{'rate/element':>13} {'-(1/b)log|G~| (measured)':>26}")
rng = np.random.default_rng(1)
for nm, k in (('odds', 200), ('squares', 150), ('primes', 200)):
    for rho in (0.40, 0.20):
        A = np.array(sorted(ENS[nm](k)), float); b = len(A); N = A[-1]
        s = tilt(A, rho); p = 1.0 / (1.0 + np.exp(s * A)); t = 4 * p * (1 - p)
        th = np.concatenate([np.linspace(2.0 / N, 0.5, 8000), rng.random(8000) * 0.5,
                             np.array([j / q + 1e-7 for q in (3, 5, 6, 7, 11, 13, 101, 1009)
                                       for j in range(1, q) if j / q < 0.5])])
        best = np.inf; bestlg = np.inf
        for ch in np.array_split(th, 60):
            y = np.sin(math.pi * np.outer(ch, A)) ** 2
            best = min(best, float((y.sum(axis=1) / b).min()))
            lg = 0.5 * np.log(np.clip(1 - t[None, :] * y, 1e-300, None)).sum(axis=1)
            bestlg = min(bestlg, float((-lg / b).min()))
        rate = math.exp(-t.min() * best / 2)
        print(f'{nm:>8} {k:5d} {0.5 - rho:5.2f} {t.min():8.4f} {best:20.6f} '
              f'{rate:13.6f} {bestlg:26.6f}')

# ---------------------------------------------------------------- (d)
print()
print('=' * 100)
print('(d)  squares k-scan: Table-1 residual as a fraction of the centred signal')
print('=' * 100)
RH = [0.44, 0.40, 0.30, 0.20]
print(f"{'ens':>8} {'k':>5} {'|A|':>5} " + ''.join(f'   x={0.5 - r:.2f}' for r in RH))
for nm, ks in (('squares', (50, 70, 90, 110, 130, 150, 170, 190)),
               ('odds', (60, 100, 140, 180, 220)),
               ('primes', (60, 100, 140, 180, 220))):
    for k in ks:
        A = sorted(ENS[nm](k))
        m = measured(A, RH)
        r0, l0 = m[0.5]; p0 = Phi(A, l0)
        cells = []; kr = []
        for r in RH:
            rm, lam = m[r]; pp = Phi(A, lam)
            cells.append(f'  {abs(((rm - pp) - (r0 - p0)) / (rm - r0)) * 100:6.2f}%')
            kr.append(abs(((rm - pp) - (r0 - p0)) / (rm - r0)) * 100 * k)
        print(f'{nm:>8} {k:5d} {len(A):5d} ' + ''.join(cells)
              + '   | k*R: ' + ''.join(f'  {v:6.2f}' for v in kr))
    print()
