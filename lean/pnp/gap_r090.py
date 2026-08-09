#!/usr/bin/env python3
"""
r090 / F04 check: does a range fall BETWEEN lem:eta and the principal arc?

lem:eta covers  K/N <= theta <= 1 - K/N.
Inside |theta| < K/N the eta bound is vacuous (Re S_A -> b), and the decay must come
from the quadratic regime instead:
    sin^2(pi u) >= 4u^2  for |u| <= 1/2, so for |theta| <= 1/(2N)
    SUM_a sin^2(pi a theta) >= 4 theta^2 S_2 = 16 V theta^2
    |G~(theta)| <= exp(-4 t_min V theta^2).
That is <= exp(-c b) once |theta| >= theta_1 := sqrt(c b / (4 t_min V)).

So the two rows meet iff  theta_1 <= K/N  for a usable K.  This script measures
theta_1 * N and the true  -(1/b) log|G~|  across the crossover, per ensemble.
Falsifier: if -(1/b)log|G~| dips to ~0 anywhere in [theta_1, K/N], there is a gap
and lem:eta as stated is not enough.
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


ENS = {'odds': lambda k: [2 * i + 1 for i in range(k)],
       'squares': lambda k: sorted(set(2 * ((i * i) // 2) + 1 for i in range(1, k + 1))),
       'primes': odd_primes}


def tilt(A, rho):
    a = np.asarray(A, float); tgt = rho * a.sum(); lo, hi = 0.0, 1.0
    with np.errstate(over='ignore'):
        while (a / (1 + np.exp(hi * a))).sum() > tgt:
            hi *= 2
        for _ in range(300):
            mid = .5 * (lo + hi)
            if (a / (1 + np.exp(mid * a))).sum() > tgt:
                lo = mid
            else:
                hi = mid
    return .5 * (lo + hi)


C = 0.01           # target |G~| <= exp(-C b) counts as "already decayed"
print('=' * 96)
print(f'crossover check, target decay exp(-{C}*b) ;  crossover tested at theta = K/N, K = 0.5/1/2')
print('=' * 96)
for nm, k in (('odds', 200), ('squares', 150), ('primes', 200)):
    for rho in (0.40, 0.20):
        A = np.array(sorted(ENS[nm](k)), float); b = len(A); N = A[-1]
        V = (A ** 2).sum() / 4
        s = tilt(A, rho); p = 1 / (1 + np.exp(s * A)); t = 4 * p * (1 - p); tmin = float(t.min())
        th1 = math.sqrt(C * b / (4 * tmin * V))
        print(f'\n  {nm}, k={k}, x={0.5 - rho:.2f}:  t_min={tmin:.4f}  '
              f'theta_1*N = {th1 * N:.3f}   (quadratic bound valid only for theta*N <= 0.5)')
        # eta over the whole remaining range, starting from the crossover K/N with K = 0.5
        rng = np.random.default_rng(3)
        for K in (0.5, 1.0, 2.0):
            th = np.concatenate([np.linspace(K / N, 1 - K / N, 40000),
                                 np.array([j / q + e for q in (3, 4, 5, 6, 7, 11, 13, 101, 1009)
                                           for j in range(1, q)
                                           for e in (0.0, 1e-7, -1e-7)
                                           if K / N <= j / q + e <= 1 - K / N])])
            eta = max(float((np.cos(2 * math.pi * np.outer(ch, A)).sum(axis=1) / b).max())
                      for ch in np.array_split(th, 200))
            print(f'    K={K:4.1f}:  eta = max Re S_A/b over [K/N, 1-K/N] = {eta:9.6f}'
                  f'   {"OK" if eta <= 0.55 else "GAP"}')
        print(f"    {'theta*N':>9} {'-(1/b)log|G~|':>15} {'Re S_A/b':>11}  verdict")
        for m in (0.25, 0.5, 1, 2, 5):
            th = m / N
            y = np.sin(math.pi * th * A) ** 2
            lg = -0.5 * np.log(np.clip(1 - t * y, 1e-300, None)).sum() / b
            res = float(np.cos(2 * math.pi * th * A).sum() / b)
            v = 'decayed' if lg >= C else ('GAP' if abs(res) > 0.5 else 'weak')
            print(f'    {m:9.2f} {lg:15.6f} {res:11.6f}  {v}')
