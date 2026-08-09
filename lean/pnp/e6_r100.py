#!/usr/bin/env python3
"""
r100 / (i) audit of fable's last one-liner, (ii) E6 of spec_paper4_concept_r097.

(i) THE TERMWISE MINIMALITY THEOREM (fable r099 judgement 2, design status).
    Claim: each term f_N(q) = q^N + (1-q)^N is symmetric and convex in q and minimised at
    q = 1/2, so Gamma^{(q)}(A) >= Gamma(A) for EVERY A, with equality only at q = 1/2.
    On paper:
        f_N(1-q) = f_N(q)                                   symmetric
        f_N'(q)  = N [ q^{N-1} - (1-q)^{N-1} ]              zero at q=1/2
        f_N''(q) = N(N-1) [ q^{N-2} + (1-q)^{N-2} ] >= 0    convex for N >= 2
      N >= 2: q^{N-1} strictly increasing, so f' < 0 below 1/2 and > 0 above: strict min.
      N in {0,1}: f_N is constant (2 and 1), so the inequality holds with equality.
    Any A with |A| >= 2 has some d with N_d >= 2 (take d >= (a_2-1)/2, which is <= D),
    so the minimum of Gamma^{(q)} is STRICT.  The one-liner is correct.
    Checked numerically below over N and q.

(ii) E9 AUDIT, done before spending Lean time.  The spec asks to formalise
     "Phi(0) = Gamma, i.e. 1 + SUM 2^{1-N_d} = gapSeries".  That is FALSE as written:
     paper 1's window identity is W_D(A) = Gamma(A) + (2D+1) 2^{-k}, tail included, and
     Phi(0) = W_D.  Paper 3's rem:lam0 states it correctly WITH the tail.  Moreover
     windowSeries_eq_gapSeries is already in the Lean canon, so E9 item 1 is both
     misstated and already done.  Measured below.  The genuinely new Lean target is the
     termwise inequality of (i).

(iii) E6: under bias, is Q^{(q)} = (dev_q - dev_q(0))/lambda_q^2 constant in x?
      Shape only, no model fitting, per the spec.
"""
import math

from e5_r098 import ENS, strata_q, gamma_q          # reuse the audited r098 pipeline


# ---------------------------------------------------------------- (i)
print('=' * 96)
print('(i) termwise minimality:  f_N(q) = q^N + (1-q)^N  vs its value 2^{1-N} at q=1/2')
print('=' * 96)
print(f"  {'N':>3} " + ''.join(f'{q:>11.2f}' for q in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8))
      + f"{'  f_N(1/2)':>12}")
worst = 0.0
for N in (0, 1, 2, 3, 5, 10, 30):
    row = []
    for q in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8):
        v = q ** N + (1 - q) ** N
        row.append(v)
        worst = min(worst, v - 2.0 ** (1 - N))
    print(f'  {N:3d} ' + ''.join(f'{v:11.6f}' for v in row) + f'{2.0**(1-N):12.6f}')
print(f'  min over the grid of  f_N(q) - 2^(1-N)  =  {worst:.3e}   '
      f'(must be >= 0; equality at q=1/2 and at N<=1)')

# symmetry and convexity, numerically, on a fine grid
import statistics
bad_sym = bad_cvx = 0.0
for N in range(0, 40):
    for i in range(1, 1000):
        q = i / 1000.0
        bad_sym = max(bad_sym, abs((q ** N + (1 - q) ** N) - ((1 - q) ** N + q ** N)))
        if 1 <= i <= 998:
            a = (q - .001) ** N + (1 - q + .001) ** N
            b = q ** N + (1 - q) ** N
            c = (q + .001) ** N + (1 - q - .001) ** N
            bad_cvx = min(bad_cvx, a - 2 * b + c)
print(f'  symmetry residual over N<40, 999 q-values: {bad_sym:.2e}')
print(f'  min second difference (convexity, h=1e-3):  {bad_cvx:.2e}  (>= 0 up to rounding)')

# ---------------------------------------------------------------- (ii)
print()
print('=' * 96)
print('(ii) E9 audit:  Phi(0) = 1 + SUM 2^{1-N_d}  vs  Gamma  vs  Gamma + (2D+1)2^{-k}')
print('=' * 96)
print(f"  {'ens':>8} {'k':>4} {'Phi(0)':>16} {'Gamma':>16} {'Phi(0)-Gamma':>14} "
      f"{'(2D+1)2^-k':>13}")
for nm, k in (('odds', 20), ('odds', 30), ('primes', 20), ('primes', 30)):
    A = sorted(ENS[nm](k)); D = (A[-1] - 1) // 2
    phi0 = gamma_q(A, 0.5)
    gam = sum(a / 2.0 ** (j + 1) for j, a in enumerate(A))
    tail = (2 * D + 1) / 2.0 ** k
    print(f'  {nm:>8} {k:4d} {phi0:16.10f} {gam:16.10f} {phi0-gam:14.3e} {tail:13.3e}')
print('  Phi(0) - Gamma equals the tail term, not zero: the spec drops it, paper 3 does not.')

# ---------------------------------------------------------------- (iii)
print()
print('=' * 96)
print('(iii) E6: shape of Q^{(q)} = (dev_q - dev_q(0)) / lambda_q^2  across x, under bias')
print('      dev_q = (lm_q/deg_q)/Gamma^{(q)} - 1 ;  lambda_q = (1/4)log(r^q(n-2)/r^q(n+2))')
print('=' * 96)


def slope_and_ratio(A, q, n):
    """biased lm_q/deg_q at n, and the biased local log-slope there."""
    deg, lm, _, _ = strata_q(A, q, n)
    dm, _, _, _ = strata_q(A, q, n - 2)
    dp2, _, _, _ = strata_q(A, q, n + 2)
    return lm / deg, 0.25 * math.log(dm / dp2)


for nm, k in (('odds', 80), ('primes', 80)):
    A = sorted(ENS[nm](k)); T = sum(A)
    for q in (0.3, 0.5):
        n0 = int(round(q * T))
        g = gamma_q(A, q)
        r0, l0 = slope_and_ratio(A, q, n0)
        dev0 = r0 / g - 1.0
        print(f'\n  {nm}, k={k}, q={q}:  n_q={n0}, Gamma^(q)={g:.6f}, dev_q(0)={dev0:+.3e}')
        print(f"      {'x=(q-rho)':>10} {'lambda_q':>12} {'dev_q':>12} "
              f"{'(dev-dev0)/lam^2':>18}")
        for frac in (0.04, 0.08, 0.12, 0.16, 0.20):
            n = int(round((q - frac * q) * T))          # move x = frac*q toward 0
            rr, ll = slope_and_ratio(A, q, n)
            dev = rr / g - 1.0
            qhat = (dev - dev0) / ll ** 2 if ll else float('nan')
            print(f'      {frac*q:10.4f} {ll:12.4e} {dev:+12.3e} {qhat:18.4f}')

# ---------------------------------------------------------------- (iv)
print()
print('=' * 96)
print('(iv) linear vs quadratic.  At q=1/2 the reflection symmetry lm(n)=lm(T-n) kills the')
print('     odd orders in lambda (paper 3\'s cosh pairing).  At q != 1/2 complementation maps')
print('     q to 1-q, NOT q to q, so the symmetry is broken and a LINEAR term should survive.')
print('     Structural prediction: the first-order coefficient is')
print('        L^{(q)} = SUM_d delta_d [ q^{N_d} - (1-q)^{N_d} ],   identically 0 at q=1/2.')
print('=' * 96)


def Lq(A, q):
    A = sorted(A); k = len(A); D = (A[-1] - 1) // 2
    tot = 0.0; j = 0; sig = 0
    for d in range(1, D + 1):
        while j < k and A[j] <= 2 * d:
            sig += A[j]; j += 1
        t = q ** j - (1 - q) ** j
        de = d + sig / 2.0
        if abs(t) * de < 1e-15 and d > 4:
            break
        tot += de * t
    return tot


print(f"  {'ens':>8} {'k':>4} {'q':>5} {'L^(q)':>14} {'L^(q)/Gamma^(q)':>17}")
for nm, k in (('odds', 80), ('primes', 80)):
    for q in (0.3, 0.4, 0.5, 0.6, 0.7):
        A = sorted(ENS[nm](k))
        print(f'  {nm:>8} {k:4d} {q:5.2f} {Lq(A,q):14.5f} {Lq(A,q)/gamma_q(A,q):17.5f}')

print()
print('  spread of the two candidate ratios across the same x-range (max/min):')
print(f"  {'ens':>8} {'q':>5} {'dev/lambda spread':>19} {'dev/lambda^2 spread':>21}  verdict")
for nm, k in (('odds', 80), ('primes', 80)):
    A = sorted(ENS[nm](k)); T = sum(A)
    for q in (0.3, 0.5):
        n0 = int(round(q * T)); g = gamma_q(A, q)
        r0, l0 = slope_and_ratio(A, q, n0); dev0 = r0 / g - 1.0
        lin, quad = [], []
        for frac in (0.04, 0.08, 0.12, 0.16, 0.20):
            n = int(round((q - frac * q) * T))
            rr, ll = slope_and_ratio(A, q, n)
            dev = rr / g - 1.0
            lin.append(abs((dev - dev0) / ll))
            quad.append(abs((dev - dev0) / ll ** 2))
        sl, sq = max(lin) / min(lin), max(quad) / min(quad)
        v = 'LINEAR wins' if sl < sq else 'quadratic wins'
        print(f'  {nm:>8} {q:5.2f} {sl:19.3f} {sq:21.3f}  {v}')
