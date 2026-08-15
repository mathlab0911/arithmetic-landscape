#!/usr/bin/env python3
r"""
r112 / paper 4 section 4: the constants that turn prop:rate into a theorem.

WHAT I DERIVED ON PAPER BEFORE RUNNING THIS (F09).  Six items, in the order the proof uses
them.  Everything below is a LOWER bound on
    G(theta) = SUM_m p_m X^(M)_m(theta) / SUM_m p_m ,   X = -log|cos(pi . )|, p_m = 2/log m,
for theta = a/q + beta, q <= Q = floor(sqrt N), |beta| <= 1/(q(Q+1)), m odd in [3,N].

(1) THE GENERAL COSET IDENTITY, and its Fourier proof.  For every v >= 1 and every t,
        (1/v) SUM_{k<v} X(t + k/v) = (1 - 1/v) log 2 + (1/v) X(v t + tau_v),
        tau_v = 0 (v odd), 1/2 (v even).
    Fourier route (fable, r112): X(t) = log 2 + SUM_{n>=1} (-1)^n cos(2 pi n t)/n, and
    (1/v) SUM_k cos(2 pi n (t + k/v)) = cos(2 pi n t) if v | n and 0 otherwise, so only the
    harmonics v | n survive; writing n = v p and using (-1)^{vp} = (-1)^p for v odd, = 1 for
    v even, the surviving series is (1/v)(X(vt + tau_v) - log 2).  Checked in (A).
    The R_q form of section 4 is the case t = s (q odd) and t = s + 1/q (q even), which is
    why sigma = 1/2 exactly on q = 2 mod 4.

(2) TRUNCATION CANNOT BREAK THE FLOOR, and the margin is a named number.  Truncating at M
    costs (X(z_j) - M)^+ at the residue nearest a pole, at distance d.  Then X(z_j) <=
    log(1/(2d)) while the identity's excess is (1/v) X(v t + tau) >= (1/v) log(1/(pi v d)).
    The floor survives iff M >= log(pi v / 2), and with M = log(2Q/pi) + 1 and v <= Q that is
    1 >= log(pi^2/4) = 0.9032, i.e. *** a margin of exactly 1 - log(pi^2/4) = 0.0968 ***.
    Only one residue can be that close: spacing 1/v >= 1/Q > 2 e^{-M}/pi = 1/(Q e).  Check (D).

(3) q = 2 IS NOT PROSE (fable's marked spot (a)).  There v = 1 and the identity is vacuous:
    the floor (1 - 1/v) log 2 is 0.  But for q = 2, m odd gives m theta = 1/2 + m beta, so
    X_m = -log|sin(pi m beta)| and the phases sweep an arc of length L = N|beta|.  With
        INT_0^x -log|sin pi w| dw = x log 2 + Cl_2(2 pi x)/(2 pi),
    the arc average is EXACTLY  G(L) = log 2 + Cl_2(2 pi {L}) / (2 pi L).

    *** MY FIRST PREDICTION HERE WAS WRONG, AND THIS SCRIPT IS WHAT CAUGHT IT. ***  I wrote
    "min_L G(L) = log2 - 3 Cl_2(pi/3)/(5 pi) = 0.4993 at L = 5/6", by minimising the NUMERATOR
    Cl_2(2 pi L) and forgetting that L also sits in the DENOMINATOR.  The true minimum is
    0.494530 at L = 0.7917.  The conclusion survives (both numbers clear the target) but the
    stated constant did not, and the general lesson goes in the ledger: *the extremiser of one
    factor of a ratio is not the extremiser of the ratio* (append to F03).

    What the PAPER needs is not the exact minimum but a bound provable by hand, and the split
    at L = 1/2 gives one, with both branches clearing (1/2) log 2:
      L <= 1/2 : -log sin(pi .) is convex on (0,1), so the average over [0,L] is at least its
                 midpoint value -log sin(pi L/2) >= -log sin(pi/4) = (1/2) log 2, with equality
                 only in the limit L = 1/2 -- where the two-point midpoint bound
                 (1/2)[phi(L/4) + phi(3L/4)] = 0.5199 shows it is in fact strict;
      L >= 1/2 : 1/(2 pi L) <= 1/pi, so G(L) >= log 2 - Cl_2(pi/3)/pi = 0.3701 > (1/2) log 2.
    Check (B).

(4) THE MAJOR ARC HAS AN EXPLICIT RADIUS.  q = 1 is the same computation with X in place of
    -log|sin|: the arc average is log 2 + Cl_2(2 pi L + pi)/(2 pi L), which exceeds
    (1/2)log2 + delta as soon as L >= L_0 with L_0 < 1.  *** So "minor" can be DEFINED as
    ||theta|| >= 1/N and nothing is left unowned (F04). ***  Check (C).

(5) THE TWO ERROR TERMS, in full.  Group the odd m by residue class mod q.  Class j is an
    arithmetic progression of step 2v in m, hence of step eta = 2 v beta in phase, sweeping
    L = N|beta|.
      (i) progression versus integral: X^(M) has total variation <= 2M per period, so the
          per-class error is <= 2M(L+1), i.e. <= 4qM/N + 4M/(Q+1) in the mean;
     (ii) jitter: class j starts at x_j + m_j beta rather than at x_j, and |m_j beta| <=
          2 v |beta| = (2v/N) L, so replacing the jittered coset average by the true one costs
          at most (jitter) x (total variation) <= 8qM/N + 4M/(Q+1);
    (iii) unequal class counts (they differ by at most 1): <= 2qM/N.
    Total E(N,q,Q) <= 14 qM/N + 8M/(Q+1), which at Q = floor(sqrt N) is O(M/sqrt N).  Check (G).

(6) THE WEIGHTS NEED NO ARGUMENT AT ALL (fable's marked spot (b)).  p_m = 2/log m is
    DECREASING, so by Abel summation a bound valid for every PREFIX passes to the weighted
    mean unchanged.  The block-weight question dissolves.  Checks (E), (F).

FAIL RULE WITH FLOOR (F51).  (A) and (B) are exact identities: floor 1e-12 in the product /
Clausen form, and the F51 lesson of r110 applies -- nothing is compared in a form where a
logarithm amplifies rounding.  (G) compares a measured deficit with a derived UPPER bound: the
rule is that the bound must dominate at every tested (N,q), and if it does not, report raw and
do not promote prop:rate.  F55 (new, r110): the theta scan in (H) carries a positive control --
it must recover theta = 1/4 with the value (1/2) log 2, or its resolution is wrong and its
output is noise.
"""
import math
import numpy as np
import mpmath as mp

mp.mp.dps = 40
LOG2 = math.log(2.0)
DELTA = LOG2 / 6.0
TARGET = 0.5 * LOG2 + DELTA          # what the mean must clear for q != 4
CL2MAX = float(mp.clsin(2, mp.pi / 3))   # Cl_2(pi/3), the maximum of Cl_2 on (0, 2 pi)


def X(t):
    c = np.abs(np.cos(np.pi * np.asarray(t, dtype=float)))
    return np.where(c < 1e-300, np.inf, -np.log(np.maximum(c, 1e-300)))


def tau(v):
    return 0.0 if v % 2 == 1 else 0.5


print('=' * 100)
print('(A) THE COSET IDENTITY AND ITS FOURIER PROOF')
print('=' * 100)
rng = np.random.default_rng(112)
worst = 0.0
for v in range(1, 61):
    for t in rng.random(200) - 0.5:
        k = np.arange(v)
        lhs = float(np.prod(np.abs(np.cos(np.pi * (t + k / v)))))
        rhs = 2.0 ** (1 - v) * abs(math.cos(math.pi * (v * t + tau(v))))
        worst = max(worst, abs(lhs - rhs))
print(f'  product form, v = 1..60, 200 random t each      : worst |LHS-RHS| = {worst:.3e}')

print('  Fourier mechanism: the coset average annihilates every harmonic with v not dividing n,')
print('  so the two partial sums below are EQUAL TERM BY TERM, not merely close.')
NMAX = 3000
worstF, wv = 0.0, None
for v in (1, 2, 3, 4, 5, 6, 7, 8, 12, 16):
    for t in rng.random(40) - 0.5:
        n = np.arange(1, NMAX + 1)
        k = np.arange(v)
        A = (np.where(n % 2 == 0, 1.0, -1.0)
             * np.cos(2 * np.pi * np.outer(n, t + k / v)).mean(axis=1) / n).sum()
        p = np.arange(1, NMAX // v + 1)
        sgn = 1.0 if v % 2 == 0 else np.where(p % 2 == 0, 1.0, -1.0)
        B = (sgn * np.cos(2 * np.pi * p * (v * t)) / p).sum() / v
        worstF = max(worstF, abs(A - B))
        if abs(A - B) >= worstF:
            wv = v
print(f'  Fourier partial sums to n = {NMAX}, 10 values of v : worst |A-B| = {worstF:.3e} '
      f'(at v = {wv})')
print(f'  (A) VERDICT: {"identity and its Fourier proof both confirmed" if worst < 1e-12 and worstF < 1e-9 else "*** FAIL RULE ***"}')

print()
print('=' * 100)
print('(B) q = 2, WITH A PROOF AND A CONSTANT.  arc average G(L) = log2 + Cl_2(2pi{L})/(2pi L)')
print('=' * 100)
print(f'  Cl_2(pi/3) = {CL2MAX:.10f}   (the maximum of the Clausen function on (0, 2 pi))')
pred = LOG2 - 3 * CL2MAX / (5 * math.pi)
print(f'  MY FALSIFIED PREDICTION  log2 - 3 Cl_2(pi/3)/(5 pi) = {pred:.10f}  (claimed at L = 5/6;')
print('  wrong, because L is in the denominator too -- the extremiser of Cl_2 is not the')
print('  extremiser of Cl_2(2 pi L)/L.  Kept in the log on purpose.)')
print(f'  half log 2                                  = {0.5*LOG2:.10f}   <- what the theorem needs')
print(f'  target with the margin, (1/2) log2 + delta   = {TARGET:.10f}')


def Gclausen(L):
    return LOG2 + float(mp.clsin(2, 2 * mp.pi * (L % 1.0))) / (2 * math.pi * L)


def Gdirect(L, n=400001):
    w = np.linspace(1e-12, L, n)
    return float(np.trapezoid(-np.log(np.abs(np.sin(np.pi * w))), w) / L)


Ls = np.linspace(0.01, 6.0, 6000)
vals = np.array([Gclausen(L) for L in Ls])
i = int(np.argmin(vals))
print(f'  TRUE minimum over L in (0,6]:  {vals[i]:.6f} at L = {Ls[i]:.6f}   '
      f'(measured, not proved; clears (1/2)log2 + delta by {vals[i]-TARGET:.6f})')
print(f"  {'L':>8} {'Clausen form':>15} {'direct quadrature':>19} {'diff':>10}")
for L in (0.25, 0.5, 5.0 / 6.0, 1.0, 3.0):
    gc, gd = Gclausen(L), Gdirect(L)
    print(f'  {L:8.4f} {gc:15.8f} {gd:19.8f} {abs(gc-gd):10.2e}')
print()
print('  THE BOUND THAT IS PROVABLE BY HAND (this is what goes in the paper):')
phi = lambda w: -math.log(abs(math.sin(math.pi * w)))
conv = np.array([Gclausen(L) - (-math.log(math.sin(math.pi * L / 2)))
                 for L in np.linspace(0.01, 0.5, 5000)])
b1 = -math.log(math.sin(math.pi * 0.25))
b2 = LOG2 - CL2MAX / math.pi
b1s = 0.5 * (phi(0.125) + phi(0.375))
print(f'    L <= 1/2 (convexity, midpoint):  G >= -log sin(pi L/2) >= -log sin(pi/4) = '
      f'{b1:.6f} = (1/2) log 2')
print(f'       midpoint bound valid at every L (min over L of G - midpoint bound) : '
      f'{conv.min():.3e}  (must be >= 0)')
print(f'       at the endpoint L = 1/2 the two-point midpoint bound gives          : '
      f'{b1s:.6f}  (so the inequality is strict there)')
print(f'    L >= 1/2 (Clausen, 1/(2 pi L) <= 1/pi):  G >= log2 - Cl_2(pi/3)/pi     = '
      f'{b2:.6f}')
okB = (conv.min() >= -1e-12) and b1 >= 0.5 * LOG2 - 1e-12 and b2 > 0.5 * LOG2
print(f'  (B) VERDICT: {"both branches clear (1/2) log 2, so q = 2 has a proof" if okB else "*** FAIL RULE ***"}')
print('  NOTE what the theorem actually needs: mean >= (1/2) log2 - o(1) at EVERY minor theta.')
print('  The delta margin exists only so Hoeffding can take a bite, and the bite can be taken')
print('  as o(1) instead -- so q = 1 and q = 2 do not need the margin, only (1/2) log 2.')

print()
print('=' * 100)
print('(C) q = 1: the explicit major-arc radius.   arc average = log2 + Cl_2(2 pi L + pi)/(2 pi L)')
print('=' * 100)


def Gmajor(L):
    return LOG2 + float(mp.clsin(2, 2 * mp.pi * L + mp.pi)) / (2 * math.pi * L)


print(f"  {'L':>8} {'arc average':>14} {'>= target?':>11}")
L0 = None
for L in (0.1, 0.3, 0.5, 0.6993, 0.8, 1.0, 2.0, 5.0):
    g = Gmajor(L)
    print(f'  {L:8.4f} {g:14.8f} {str(g >= TARGET):>11}')
grid = np.linspace(0.01, 3.0, 30000)
gv = np.array([Gmajor(L) for L in grid])
above = grid[gv >= TARGET]
L0 = above.min() if above.size else None
print(f'  smallest L with arc average >= target: L_0 = {L0:.6f}')
print(f'  and the average stays above the target for every larger L: '
      f'{bool((gv[grid >= L0] >= TARGET).all())}')
print(f'  => defining the major arc as ||theta|| < 1/N is safe (L_0 = {L0:.4f} < 1), and no')
print('     theta is left unowned (F04).')

print()
print('=' * 100)
print('(D) THE TRUNCATION MARGIN IS A NAMED CONSTANT:  1 - log(pi^2/4)')
print('=' * 100)
marg = 1.0 - math.log(math.pi ** 2 / 4)
print(f'  M >= log(pi v/2) is needed;  M = log(2Q/pi) + 1 and v <= Q give margin '
      f'1 - log(pi^2/4) = {marg:.6f}')
print('  pole separation: spacing 1/v >= 1/Q must exceed 2 e^{-M}/pi = 1/(Q e) -- true, factor e.')
print(f"  direct check:  {'Q':>6} {'M':>8} {'min over q<=Q of [min_t Phi^(M) - floor]':>44}")
for Q in (40, 200, 1000):
    M = math.log(2 * Q / math.pi) + 1.0
    worstg, wq = math.inf, None
    for q in range(2, Q + 1):
        v = q if q % 2 else q // 2
        s = np.linspace(0, 1.0 / v, 8001)
        j = np.arange(q) if q % 2 else np.arange(1, q, 2)
        g = float(np.minimum(X(s[:, None] + j[None, :] / q), M).mean(axis=1).min()
                  - (1 - 1.0 / v) * LOG2)
        if g < worstg:
            worstg, wq = g, q
    print(f'                 {Q:6d} {M:8.4f} {worstg:44.3e}   (at q = {wq})')

# ---------------------------------------------------------------------------------------
print()
print('=' * 100)
print('(E)/(F) THE BLOCK-WEIGHT QUESTION DISSOLVES:  p_m = 2/log m is DECREASING, so Abel')
print('        summation passes any prefix bound to the weighted mean.  Class balance at both')
print('        ends of q <= sqrt N is checked anyway (fable\'s marked spot (b)).')
print('=' * 100)


def make(N):
    m = np.arange(3, N + 1, 2)
    return m, 2.0 / np.log(m), (2.0 / np.log(m)).sum()


for N in (8001, 32001, 128001):
    m, p, W = make(N)
    Q = math.isqrt(N)
    M = math.log(2 * Q / math.pi) + 1.0
    mono = bool((np.diff(p) < 0).all())
    print(f'  N = {N:7d}, Q = {Q:4d}:  p decreasing = {mono}')
    print(f"      {'q':>6} {'v':>5} {'max cnt':>8} {'min cnt':>8} {'|G(a/q) - floor|':>18} "
          f"{'derived bound':>14}")
    for q in (3, Q // 2 if Q // 2 % 2 else Q // 2 + 1, Q):
        v = q if q % 2 else q // 2
        res = m % q
        cnt = np.bincount(res, minlength=q)
        cnt = cnt[np.arange(q) if q % 2 else np.arange(1, q, 2)]
        t = (m * 1 % q) / q
        g = float(np.minimum(X(t), M).dot(p) / W)
        floor = (1 - 1.0 / v) * LOG2
        bound = 14 * q * M / N + 8 * M / (Q + 1.0)
        print(f'      {q:6d} {v:5d} {cnt.max():8d} {cnt.min():8d} {abs(g-floor):18.6f} '
              f'{bound:14.6f}')

print()
print('=' * 100)
print('(G) THE ASSEMBLED BOUND.   deficit := floor(q) - min over the Dirichlet box of G ;')
print('    bound := 14qM/N + 8M/(Q+1).   TWO SEPARATE QUESTIONS, and only the second is')
print('    informative at accessible N: (i) does the bound dominate -- it does, but at these N')
print('    the bound is larger than the floor itself, so that is nearly vacuous; (ii) does the')
print('    measured deficit have the DERIVED SHAPE qM/N?  The last column is deficit*N/(qM) and')
print('    a roughly constant column is the real evidence (F27: report the constant column).')
print('=' * 100)
bad = []
for N in (8001, 32001, 128001):
    m, p, W = make(N)
    Q = math.isqrt(N)
    M = math.log(2 * Q / math.pi) + 1.0
    print(f'  --- N = {N}, Q = {Q}, M = {M:.4f}')
    print(f"      {'q':>6} {'v':>5} {'floor':>10} {'min box G':>11} {'deficit':>11} "
          f"{'bound':>10} {'ok':>4} {'deficit*N/(qM)':>15}")
    for q in (2, 3, 4, 5, 6, 8, 9, 16, Q):
        v = q if q % 2 else q // 2
        floor = (1 - 1.0 / v) * LOG2
        bmax = 1.0 / (q * (Q + 1.0))
        best = math.inf
        for b in np.linspace(0.0, bmax, 201):
            t = (m * 1 % q) / q + m * b
            best = min(best, float(np.minimum(X(t), M).dot(p) / W))
        bound = 14 * q * M / N + 8 * M / (Q + 1.0)
        deficit = floor - best
        ok = deficit <= bound
        if not ok:
            bad.append((N, q, deficit, bound))
        print(f'      {q:6d} {v:5d} {floor:10.6f} {best:11.6f} {deficit:11.3e} '
              f'{bound:10.6f} {str(ok):>4} {deficit*N/(q*M):15.4f}')
print()
print('  ' + ('*** FAIL RULE: the derived bound does not dominate; do not promote ***'
              if bad else 'the derived bound dominates the measured deficit at every tested (N,q).'))
for b_ in bad:
    print('   ', b_)

print()
print('=' * 100)
print('(H) GLOBAL CHECK WITH A POSITIVE CONTROL (F55).  Scan G over the minor arc')
print('    ||theta|| >= 1/N.  The control: the scan must recover theta = 1/4 with (1/2)log2.')
print('=' * 100)
N = 8001
m, p, W = make(N)
Q = math.isqrt(N)
M = math.log(2 * Q / math.pi) + 1.0


def Gt(t):
    return float(np.minimum(X(m * t), M).dot(p) / W)


coarse = np.linspace(1.0 / N, 0.5, 40001)
cv = np.array([Gt(t) for t in coarse])
refined = []
for idx in np.argsort(cv)[:250]:
    loc = np.linspace(max(1.0 / N, coarse[idx] - 2.0 / N), min(0.5, coarse[idx] + 2.0 / N), 401)
    lv = np.array([Gt(t) for t in loc])
    k = int(np.argmin(lv))
    refined.append((lv[k], loc[k]))
best, bestt = min(refined)
ctrl = abs(bestt - 0.25) < 3.0 / N and abs(best - 0.5 * LOG2) < 1e-3
print(f'  global min G = {best:.6f} at theta = {bestt:.6f}      [(1/2) log2 = {0.5*LOG2:.6f}]')
print(f'  POSITIVE CONTROL: {"passed -- the scan resolves the dip at 1/4" if ctrl else "*** FAILED: resolution wrong, output is noise ***"}')
away = [x for x in refined if abs(x[1] - 0.25) > 0.005]
lo = min(away)
bnd = 14 * 3 * M / N + 8 * M / (Q + 1.0)
print(f'  best away from 1/4: G = {lo[0]:.6f} at theta = {lo[1]:.6f}, shortfall vs target = '
      f'{TARGET-lo[0]:.3e}, bound = {bnd:.6f}')

print()
print('=' * 100)
print('SUMMARY')
print('=' * 100)
print(f'  coset identity + Fourier proof   : {"CONFIRMED" if worst < 1e-12 and worstF < 1e-9 else "FAILED"}')
print(f'  q = 2: my closed form for the minimiser was FALSIFIED (0.4993 at 5/6 claimed; true')
print(f'         minimum {vals[i]:.6f} at L = {Ls[i]:.4f}).  The hand-provable two-branch bound')
print(f'         holds: {b1:.6f} and {b2:.6f}, both >= (1/2) log 2 = {0.5*LOG2:.6f} : '
      f'{"CONFIRMED" if okB else "FAILED"}')
print(f'  major-arc radius  L_0 = {L0:.4f} < 1, so ||theta|| >= 1/N is a safe minor arc')
print(f'  truncation margin  1 - log(pi^2/4) = {marg:.6f}')
print(f'  derived error bound dominates    : {"YES" if not bad else "NO"}')
print(f'  positive control on the scan     : {"passed" if ctrl else "FAILED"}')
