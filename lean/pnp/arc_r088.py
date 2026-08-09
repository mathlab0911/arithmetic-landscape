#!/usr/bin/env python3
"""
r088 / repaired bridge lemma, measured properly.

lem:kappa as written is false (see kappa_r088).  Proposed replacement, additive form:

    |G~(th)|^2 = PROD_a (1 - t_a sin^2(pi a th))  <=  exp(-t_min * SUM_a sin^2(pi a th))
               = exp(-t_min * (b - Re S_A(th))/2),      S_A(th) = SUM_a e(a th)

so on any th with  Re S_A(th) <= eta*b :   |G~(th)| <= exp(-t_min (1-eta) b/4).

The input is the LINEAR exponential sum -- weaker than the multiplicative
prod|cos| control paper 2 already establishes.  This script measures eta.
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


print('=' * 104)
print('Repaired bridge:  eta := max Re S_A(th)/b  over the MINOR arcs  |th| >= C/N')
print('   rate/element = exp(-t_min (1-eta)/4);   any eta < 1 gives exponential decay')
print('=' * 104)
print(f"{'ens':>8} {'k':>5} {'x':>5} {'C':>4} {'t_min':>7} {'eta = max ReS/b':>17} "
      f"{'at theta':>11} {'rate/elt (bound)':>17} {'rate/elt (true)':>16}")
rng = np.random.default_rng(7)
for nm, k in (('odds', 200), ('squares', 150), ('primes', 200)):
    A = np.array(sorted(ENS[nm](k)), float); b = len(A); N = A[-1]
    for rho in (0.40, 0.20):
        s = tilt(A, rho); p = 1 / (1 + np.exp(s * A)); tmin = float((4 * p * (1 - p)).min())
        for C in (10, 30, 100):
            th0 = C / N
            th = np.concatenate([
                np.linspace(th0, 1 - th0, 60000),
                th0 + rng.random(40000) * (1 - 2 * th0),
                np.array([j / q + e for q in (3, 5, 6, 7, 11, 13, 101, 1009, 4001)
                          for j in range(1, q) for e in (0.0, 1e-7, -1e-7)
                          if th0 <= j / q + e <= 1 - th0]),
            ])
            eta = -np.inf; eth = 0.0; true_rate = 0.0
            for ch in np.array_split(th, 250):
                ph = 2 * math.pi * np.outer(ch, A)
                r = np.cos(ph).sum(axis=1) / b
                i = int(np.argmax(r))
                if r[i] > eta:
                    eta = float(r[i]); eth = float(ch[i])
                y = np.sin(ph / 2) ** 2
                lg = 0.5 * np.log(np.clip(1 - (4 * p * (1 - p))[None, :] * y, 1e-300, None)
                                  ).sum(axis=1) / b
                true_rate = max(true_rate, float(np.exp(lg).max()))
            print(f'{nm:>8} {k:5d} {0.5 - rho:5.2f} {C:4d} {tmin:7.4f} {eta:17.6f} '
                  f'{eth:11.6f} {math.exp(-tmin * (1 - eta) / 4):17.6f} {true_rate:16.6f}')
        print()
