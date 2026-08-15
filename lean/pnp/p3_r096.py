#!/usr/bin/env python3
"""
r096 / verification of spec_p3majorarcs_r095 before writing P3.

Derivation being tested (this is spot 2 of the spec, carried further than asked --
the whole Phi term falls out, not just the mu_d shift):

  r_B(m) = P_s[SUM_B = m] * Z_B(s) * e^{s m},     Z_B(s) = PROD_{a in B}(1 + e^{-s a}).
  mu_d(s) = SUM_{a in B_d} a p_a = n - SUM_{a<=2d} a p_a = n - sigma_d/2 + (s/4) s_d + ...
  so with w := (s/4) s_d,
        (n+d)          - mu_d = +delta_d - w
        (n-d-sigma_d)  - mu_d = -delta_d - w          <-- the mu_d-shift equation
  Gaussian at the two points, times e^{s(n+d)} and e^{s(n-d-sigma_d)}, and using
  s*d + s*sigma_d/2 = s*delta_d:
        sum  =  2 e^{s n - s sigma_d/2} e^{-(delta_d^2+w^2)/(2V_d)} cosh(delta_d (s + w/V_d))
  Dividing by r_A(n) ~ Z_A e^{s n}/sqrt(2 pi V):
        Z_B/Z_A * e^{-s sigma_d/2} = 2^{-N_d} / PROD_{a<=2d} cosh(s a/2)
                                   = 2^{-N_d} exp(-s^2 s_d/8) (1+...)
  ==>   [r_B(n+d) + r_B(n-d-sigma_d)] / r_A(n)
             = 2^{1-N_d} exp(-lambda^2 s_d/8) cosh(lambda delta_d) * (1 + small),
  which is EXACTLY the general term of Phi, with lambda = s + w/V_d = s(1 + s_d/(4V_d)).

Checks, per spec section 4:
  (A) mu_d formula, exact vs the displayed expression
  (B) the two offsets vs -w +- delta_d
  (C) R1 Gaussian vs exact r_{B_d}(m) over the window; error vs the predicted eps_lclt
  (D) layer uniformity: eps_lclt at d = 1, 3, D(k)
  (E) parity: does r_{B_d}(m) oscillate with m mod 2?  (the two evaluation points differ
      in parity exactly when N_d is odd, so the cosh pairing needs this to be small)
  (F) the assembled term vs Phi's general term, layer by layer
Fail rule: anything off by more than its predicted scale -> report raw and stop.
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


ENS = {'odds': lambda k: [2 * i + 1 for i in range(k)], 'primes': odd_primes}


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


def dp_counts(B):
    """exact subset-sum counts of B, float64 (validated against int64 in r080)."""
    dp = np.zeros(1); dp[0] = 1.0
    for a in B:
        nw = np.zeros(len(dp) + a); nw[:len(dp)] = dp; nw[a:a + len(dp)] += dp; dp = nw
    return dp


def cum(B, s):
    a = np.asarray(B, float)
    with np.errstate(over='ignore'):
        p = 1.0 / (1.0 + np.exp(s * a))
    w = p * (1 - p)
    return (float((a * p).sum()), float((a ** 2 * w).sum()),
            float((a ** 3 * w * (1 - 2 * p)).sum()),
            float((a ** 4 * w * (1 - 6 * p * (1 - p))).sum()))


K = 180
print('=' * 104)
print(f'P3 verification, k = {K}.  W(k) = window half-width used for the LCLT test')
print('=' * 104)

for nm in ('odds', 'primes'):
    A = sorted(ENS[nm](K)); T = sum(A); N = A[-1]
    # layer depths: d = 1, 3, and D(k) = largest d with weight 2^{1-N_d} >= 1e-9
    Dmax = 1
    for d in range(1, (N - 1) // 2 + 1):
        Nd = sum(1 for a in A if a <= 2 * d)
        if 2.0 ** (1 - Nd) >= 1e-9:
            Dmax = d
    for rho in (0.40, 0.20):
        n = int(rho * T); s = tilt(A, rho)
        dpA = dp_counts(A)
        lam_meas = 0.25 * math.log(dpA[n - 2] / dpA[n + 2])
        rAn = dpA[n]
        print(f'\n--- {nm}, k={K}, x={0.5-rho:.2f}:  N={N}, T={T}, n={n}, '
              f's={s:.6e}, |lambda|={abs(lam_meas):.6e},  D(k)={Dmax}')
        print(f"  {'d':>4} {'N_d':>4} {'(A) mu_d err':>13} {'(B) off+ err':>13} "
              f"{'(B) off- err':>13} {'(C) max rel':>12} {'eps_lclt':>10} "
              f"{'(E) parity':>11} {'(F) term/Phi':>13} {'exp(-de^2/2V_d)':>16} {'(F)/that':>10}")
        for d in (1, 3, Dmax):
            B = [a for a in A if a > 2 * d]
            Nd = len(A) - len(B)
            sig = sum(a for a in A if a <= 2 * d)
            sd = sum(a * a for a in A if a <= 2 * d)
            de = d + sig / 2.0
            mu, K2, K3, K4 = cum(B, s)
            w = s * sd / 4.0
            mu_pred = n - sig / 2.0 + w
            dpB = dp_counts(B)
            gB = lambda m: dpB[m] if 0 <= m < len(dpB) else 0.0
            # (C) window test
            Wh = max(4, int(round(de)))          # window half-width ~ delta_d
            ZB = float(np.sum(np.log1p(np.exp(-s * np.asarray(B, float)))))
            ms = np.arange(int(round(mu)) - Wh, int(round(mu)) + Wh + 1)
            ex = np.array([gB(int(m)) for m in ms])
            good = ex > 0
            pred = np.exp(ZB + s * ms - 0.5 * math.log(2 * math.pi * K2)
                          - (ms - mu) ** 2 / (2 * K2))
            rel = np.abs(ex[good] / pred[good] - 1.0)
            eps = (abs(K3) / K2 ** 1.5 + abs(K4) / K2 ** 2
                   + Wh * abs(K3) / K2 ** 2)
            # (E) parity oscillation over the window
            par = abs(np.mean(ex[good][::2]) / np.mean(ex[good][1::2]) - 1.0) \
                if good.sum() > 4 else float('nan')
            # (F) assembled term vs Phi's general term
            term = (gB(n + d) + gB(n - d - sig)) / rAn
            phit = 2.0 ** (1 - Nd) * math.exp(-lam_meas ** 2 * sd / 8.0) \
                * math.cosh(lam_meas * de)
            print(f'  {d:4d} {Nd:4d} {abs(mu-mu_pred)/max(1.0,abs(mu)):13.2e} '
                  f'{abs((n+d-mu)-(de-w))/de:13.2e} {abs((n-d-sig-mu)+(de+w))/de:13.2e} '
                  f'{rel.max():12.2e} {eps:10.2e} {par:11.2e} {term/phit:13.9f} '
                  f'{math.exp(-de*de/(2*K2)):16.9f} {term/phit/math.exp(-de*de/(2*K2)):10.6f}')
