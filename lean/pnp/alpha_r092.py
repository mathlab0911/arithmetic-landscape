#!/usr/bin/env python3
"""
r092 / supplement.  Why the alpha = 1/2 double test is void on the c_A side, and the
replacement profile that is not.

Claim (elementary):  no profile with alpha < 1 can satisfy (H).
  a_i ~ c i^alpha with distinct ODD integers needs c k^alpha >~ 2k, i.e. c >~ 2 k^{1-alpha}.
  So a_1 = c -> infinity with k, hence N_d = #{a <= 2d} = 0 for all d < c/2,
  hence  SUM_d 2^{-N_d} delta_d^2  >=  SUM_{d<c/2} 2 d^2  ~  (c/2)^3 * 2/3  ->  infinity.
  For alpha = 1/2 this is ~ k^{3/2}.

So alpha = 1/2 tests c'_A (a pure saddle/cumulant quantity, hypothesis-free) but NOT c_A
(which presupposes that Phi describes the landscape, i.e. (H)).

Replacement: alpha = 3/2.  Gaps grow, a_1 stays O(1), (H) holds.
Prediction for BOTH constants: (2a+1)^2/(4a+1) = 16/7 = 2.2857.
"""
import math
import numpy as np


def pow_profile(k, al):
    """a_i ~ c i^al, odd, strictly increasing;  c = max(1, 2 k^{1-al}) as forced above."""
    c = max(1.0, 2.2 * k ** (1 - al)) if al < 1 else 1.0
    out, prev = [], -1
    for i in range(1, k + 1):
        o = int(math.ceil(c * i ** al))
        if o % 2 == 0:
            o += 1
        if o <= prev:
            o = prev + 2
        out.append(o); prev = o
    return out


ENS = {
    'odds  a=1':    lambda k: pow_profile(k, 1.0),
    'a=1.5':        lambda k: pow_profile(k, 1.5),
    'squares a=2':  lambda k: pow_profile(k, 2.0),
    'cubes a=3':    lambda k: pow_profile(k, 3.0),
    'sqrt  a=0.5':  lambda k: pow_profile(k, 0.5),
}
AL = {'odds  a=1': 1.0, 'a=1.5': 1.5, 'squares a=2': 2.0, 'cubes a=3': 3.0,
      'sqrt  a=0.5': 0.5}


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


def Hstats(A):
    """(H): SUM 2^{-N_d} delta_d^2, and the window W(k) = max{delta_d : term >= 1/k}."""
    A = sorted(A); k = len(A); D = (A[-1] - 1) // 2
    tot = 0.0; W = 0.0; j = 0; sig = 0
    for d in range(1, D + 1):
        while j < k and A[j] <= 2 * d:
            sig += A[j]; j += 1
        w = 2.0 ** (-j); de = d + sig / 2.0
        term = w * de * de
        if term < 1e-14 and d > 2 * A[0]:
            break
        tot += term
        if term >= 1.0 / k:
            W = max(W, de)
    return tot, W


print('=' * 108)
print('(H) diagnostic across alpha:  SUM 2^{-N_d} delta_d^2  and the window W(k)')
print('   (H) asks: bounded in k, and W(k) = N^{o(1)}')
print('=' * 108)
print(f"{'profile':>14} {'k':>5} {'a_1':>6} {'N=a_k':>8} {'(H) series':>13} {'W(k)':>10} "
      f"{'W/N':>9}  verdict")
for nm in ('odds  a=1', 'a=1.5', 'squares a=2', 'cubes a=3', 'sqrt  a=0.5'):
    prev = None
    for k in (60, 100, 140, 180):
        A = sorted(ENS[nm](k))
        H, W = Hstats(A)
        v = '' if prev is None else ('grows' if H > 1.05 * prev else 'bounded')
        print(f'{nm:>14} {k:5d} {A[0]:6d} {A[-1]:8d} {H:13.5g} {W:10.4g} '
              f'{W / A[-1]:9.4f}  {v}')
        prev = H
    print()

print('=' * 108)
print("alpha = 3/2 replacement double test:  prediction  (2a+1)^2/(4a+1) = 16/7 = 2.2857")
print('=' * 108)
RH = [0.44, 0.40]
print(f"{'profile':>14} {'k':>5} {'k*S4/S2^2':>11} {'k(s/lam-1)':>12} {'c_A = k*R':>11} "
      f"{'pred':>8} {'(H)':>10}")
for nm in ('odds  a=1', 'a=1.5', 'squares a=2'):
    al = AL[nm]; pr = (2 * al + 1) ** 2 / (4 * al + 1)
    for k in (100, 140, 180, 220):
        A = sorted(ENS[nm](k))
        if A[-1] > 60000:
            continue
        m = measured(A, RH)
        r0, l0 = m[0.5]; p0 = Phi(A, l0)
        rm, lam = m[0.40]; lam = abs(lam)
        s = tilt(A, 0.40); pp = Phi(A, lam)
        cA = abs(((rm - pp) - (r0 - p0)) / (rm - r0)) * k
        a = np.asarray(A, float)
        s4 = float((a ** 4).sum()) / float((a ** 2).sum()) ** 2
        H, _ = Hstats(A)
        print(f'{nm:>14} {k:5d} {k * s4:11.4f} {k * (s / lam - 1):12.4f} {cA:11.4f} '
              f'{pr:8.4f} {H:10.4g}')
    print()
