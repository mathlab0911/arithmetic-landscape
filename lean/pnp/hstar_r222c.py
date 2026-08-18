#!/usr/bin/env python3
# hstar_r222c.py -- the SAME derivation, one term further, and criteria that use the
# error term the derivation itself names.
#
# =============================================================================
# *** THIS CRITERION SET IS A REPLACEMENT, AND THE REPLACEMENT IS ASTERISKED. ***
#
# hstar_r222 registered, for every s alike, "relative error < 0.10 at the largest k".
# It recorded FAIL on I1 and I3.  The run is kept, committed, and cited: `hstar_r222.log`.
#
# What failed was the criterion.  Its own header says the derivation drops a correction
# of order t^{s-1} -- and then applies a flat tolerance to a population whose convergence
# RATE therefore varies from t^3 (s=4) to t^{-1/2}... i.e. across five decades.  The
# numbers show exactly that and nothing else:
#
#     s    rel at k=32768     predicted by the dropped term
#    4.0      0.00114          t^3      -> tiny
#    2.0      0.0279           t log t  -> small
#    1.5      0.1562           t^{1/2}  -> |C_s| t^{1/2} / 2 zeta(s) = 0.1615
#    0.75     0.3725           t^{1/4}  -> 2|zeta(s)| t^{1/4} / C_s = 0.3791
#    0.5      0.1277           t^{1/2}  -> 2|zeta(s)| t^{1/2} / C_s = 0.1385
#
# Three of those agree with the dropped term to two significant figures.  So the law was
# not refuted; the criterion measured the RATE and reported it as an error in the LAW.
#
#   RULE (proposed F103): a derivation that names its own error term has already written
#   the criterion.  Registering a round number instead throws that away, and then tests
#   the convergence rate while claiming to test the law.
#
# The repair is not a looser tolerance -- it is to put the named term IN the prediction
# and test what is left.  That is what this file does, and it introduces no fitted
# constant: both coefficients are computed from s.
#
# =============================================================================
# THE TWO-TERM LAW (Mellin: the sine transform has a pole at z = s, the zeta factor at
# z = 1; they exchange dominance exactly at s = 1).  For every s > 0, s not an integer:
#
#     H*(t)/t  =  2 zeta(s)  +  C_s t^{s-1}  +  o(t^{s-1}) + o(1) ,
#     C_s := 2^s Gamma(1-s) sin(pi s / 2) .
#
#   s > 1 : the constant 2 zeta(s) leads, C_s t^{s-1} is the correction -> lambda -> s-1/2
#   s < 1 : C_s t^{s-1} leads and DIVERGES, 2 zeta(s) is the correction -> lambda -> s/2
#   s = 1 : the two poles collide; the confluent case is the Clausen logarithm
#           H*/t -> -2 log(2t) = log k - log log k - log(2 lambda),
#           CONFIRMED at r222 (residual 0.0677 and falling) while the cutoff-heuristic
#           constant 2 gamma - 2 sat at 0.913 and did not move.  That discrimination
#           stands; it is not re-registered here, it is quoted.
#
#     ==========================================================================
#     lambda_infty(s) = max( s/2 , s - 1/2 ),  a KINK at s = 1, which is exactly
#     where sum_j w_j stops converging.  Not a fit: a pole crossing.
#     ==========================================================================
#
# =============================================================================
# PRE-REGISTERED, before re-running.
#
#  J0  INSTRUMENT, FIRST, ABORT ON FAILURE (F86).  Same three controls as r222 --
#      constant weights exact, float64 Abel against 50-digit direct, published t_1 --
#      plus one more that this file needs and r222 did not:
#      J0d  C_s must be computed, not typed.  At s = 0.5 the closed form is exactly
#           sqrt(pi); require agreement to 1e-12.  (F87: a formula and the number
#           printed beside it are not a check on each other.)
#
#  J1  THE TWO-TERM LAW, no fitted constant.  s in {0.5, 0.75, 1.5, 2.5, 3.5}
#      (non-integer, where C_s is finite and unambiguous).  Let
#          R2 := | H*/t  -  2 zeta(s)  -  C_s t^{s-1} |   (residual after both terms)
#          R1 := | the correction term itself |           (the smaller of the two)
#      REQUIRE  R2 / R1 < 1/3  at the largest k, and R2 non-increasing over the last
#      four k.  FLOOR: t_1 is bisected to 1e-14 and H* summed in float64 over <= 32767
#      terms, so the measurement floor is ~1e-12 -- six orders below any R2 here.
#
#  J2  ZERO-PARAMETER PREDICTION OF THE ZERO ITSELF.  Solve, for t, with nothing
#      measured on the right:
#          k^{-s} (1 + 4 t^2)^{k/2}  =  t ( 1 + 2 zeta(s) + C_s t^{s-1} )
#      (that is |X| = t + H* with |sin(k theta)| set to 1, and rho^k kept EXACT rather
#      than replaced by k^lambda).  Compare lambda_pred = 2 k t_pred^2 / log k against
#      lambda_eff.  REQUIRE |lambda_eff - lambda_pred| <= D = 4 pi t_1 / log k at >= 90%
#      of points.  The two approximations this tests, and the only two, are |sin| = 1
#      and the truncation of the head expansion; it CANNOT test either coefficient
#      independently, because H* has been substituted out.
#
#  J3  THE PHASE TRANSITION.  For s in {0.5, 0.75}: lambda_eff at the largest k must
#      exceed the midpoint of the two candidate limits (already PASSED at r222 by 22
#      and 20 quanta; re-run as a regression, not as news).  NEW and reported without
#      a verdict: s in {0.9, 1.1, 1.25} to show the crossover, where the two branches
#      are 0.05, 0.05 and 0.125 apart and the quantum is ~0.012 -- so 0.9 and 1.1 are
#      NOT expected to separate cleanly, and saying so in advance is the point (F86:
#      "consistent with" is not "confirms").
#
#  J4  CONTROL THAT CAN FAIL -- the correction must be case-specific (the r219 L4
#      lesson: a term that improves everything explains nothing).
#      REQUIRE: adding C_s t^{s-1} improves the residual by >= 5x at s = 1.5, AND
#      changes the residual at s = 4 by less than 20% (where the term is spurious --
#      C_4 is the indeterminate 0 x inf, and the honest statement is that the expansion
#      has no computable second term at even integers, so nothing should improve there).
#      If it improves s = 4 as much as s = 1.5, the term is absorbing error, not
#      describing structure.
#
#  J5  REPORTED, NO VERDICT: scan margin in grid steps at every point (F92).
#
#  Populations printed.  Empty population = FAIL (F60).
# =============================================================================

import io
import math
import sys

import numpy as np
from mpmath import mp, mpf, sqrt as msqrt, atan as matan, cos as mcos, gamma, zeta

LOG = __file__[:-3] + ".log"
OUT = []


def say(s=""):
    print(s, flush=True)
    OUT.append(s)
    io.open(LOG, "w", encoding="utf-8", newline="\n").write("\n".join(OUT) + "\n")


mp.dps = 50
K_LIST = [256, 512, 1024, 2048, 4096, 8192, 16384, 32768]
S_TWOTERM = [0.5, 0.75, 1.5, 2.5, 3.5]
S_ALL = [0.5, 0.75, 0.9, 1.0, 1.1, 1.25, 1.5, 2.0, 2.5, 3.5, 4.0]


def C_of(s):
    """C_s, COMPUTED (F87), in the reflected form -- see the r222c note in the header.

    Gamma(1-s) Gamma(s) = pi / sin(pi s) and sin(pi s) = 2 sin(pi s/2) cos(pi s/2), so
        C_s = 2^s Gamma(1-s) sin(pi s/2) = 2^{s-1} pi / ( Gamma(s) cos(pi s/2) ) .
    Identical function, but the poles of Gamma(1-s) at s = 1,2,3,... and the zeros of
    sin(pi s/2) at even s have cancelled ALGEBRAICALLY.  What is left is a pole exactly
    at ODD s -- which is where t^{s-1} collides with one of the analytic powers
    t^0, t^2, t^4, ...  s=1 is the first of that family and the only one that moves
    lambda_infty.  r222b CRASHED at s=4 on the uncancelled form; that was a defect of
    the expression, not of the mathematics, and finding it produced the statement above.
    """
    return float(mpf(2) ** (mpf(s) - 1) * mp.pi / (gamma(mpf(s)) * mp.cos(mp.pi * mpf(s) / 2)))


def Z2_of(s):
    return float(2 * zeta(mpf(s)))


def decrements(k, s):
    j = np.arange(1, k, dtype=np.float64)
    return j ** (-s) - (j + 1.0) ** (-s)


def F_abel(k, s, t, D=None):
    if D is None:
        D = decrements(k, s)
    lrho = 0.5 * math.log1p(4.0 * t * t)
    th = math.atan(2.0 * t)
    j = np.arange(1, k, dtype=np.float64)
    hstar = float(np.sum(D * np.exp(j * lrho) * np.sin(j * th)))
    top = (k ** (-s)) * math.exp(k * lrho) * math.sin(k * th)
    return 1.0 + (top + hstar) / t, hstar


def F_direct_mp(k, s, t):
    t = mpf(t)
    rho, th = msqrt(1 + 4 * t * t), matan(2 * t)
    a = mpf(0)
    for jj in range(k):
        a += mpf(1) / mpf(jj + 1) ** mpf(s) * rho ** jj * mcos(jj * th)
    return 1 + 2 * a


def first_zero(k, s):
    D = decrements(k, s)
    t_hi = math.sqrt((s + 1.0) * math.log(k) / (2.0 * k)) * 2.0
    n = int(max(2000, 20 * k * math.atan(2 * t_hi) / math.pi))
    ts = np.linspace(t_hi / n, t_hi, n)
    vals = np.array([F_abel(k, s, float(x), D)[0] for x in ts])
    idx = np.nonzero(vals <= 0.0)[0]
    if len(idx) == 0:
        return None, None
    i = int(idx[0])
    lo, hi = (ts[i - 1], ts[i]) if i > 0 else (ts[0] / 2, ts[0])
    j = i
    while j + 1 < len(vals) and vals[j + 1] <= 0.0:
        j += 1
    margin = float(j - i + 1)
    for _ in range(200):
        if hi - lo < 1e-15 * max(1.0, hi):
            break
        mid = 0.5 * (lo + hi)
        if F_abel(k, s, mid, D)[0] <= 0.0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi), margin


def predict_t(k, s):
    """J2: solve k^-s (1+4t^2)^{k/2} = t(1 + 2 zeta(s) + C_s t^{s-1}).  Nothing measured."""
    z2, cs = Z2_of(s), C_of(s)

    def g(t):
        lhs = math.exp(-s * math.log(k) + 0.5 * k * math.log1p(4 * t * t))
        rhs = t * (1.0 + z2 + cs * t ** (s - 1.0))
        return lhs - rhs

    t0 = math.sqrt(max(s / 2, s - 0.5) * math.log(k) / (2.0 * k))
    grid = np.geomspace(t0 / 50.0, t0 * 4.0, 4000)
    vals = np.array([g(float(x)) for x in grid])
    cross = [i for i in range(1, len(grid)) if vals[i - 1] <= 0.0 < vals[i]]
    if not cross:
        return None
    i = cross[0]
    lo, hi = float(grid[i - 1]), float(grid[i])
    for _ in range(200):
        if hi - lo < 1e-15 * max(1.0, hi):
            break
        mid = 0.5 * (lo + hi)
        if g(mid) > 0.0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


say("=" * 100)
say("hstar_r222b -- the two-term head law, with the derivation's OWN error term in the")
say("               prediction instead of a round number in the tolerance.")
say("   H*/t = 2 zeta(s) + C_s t^{s-1} + ... ,  C_s = 2^s Gamma(1-s) sin(pi s/2)")
say("   lambda_infty(s) = max(s/2, s-1/2):  a kink at s=1, where sum_j w_j stops converging")
say("   *** criteria REPLACED after hstar_r222.log, which is kept and cited (see header)")
say("=" * 100)

verdicts = []

# ------------------------------------------------------------------ J0
say()
say("--- J0  INSTRUMENT.  Runs first; any failure aborts. ---")
okJ0 = True

say("  J0a  constant weights: only D_0 survives and rho sin theta = 2t, so H*/t = 2(w_0-w)")
n0a = 0
for k in (64, 512, 4096):
    for t in (0.003, 0.05):
        w0, w = 0.0, 0.5
        j = np.arange(1, k, dtype=np.float64)
        D = np.zeros(k - 1)
        D[0] = w0 - w
        hs = float(np.sum(D * np.exp(j * 0.5 * math.log1p(4 * t * t))
                          * np.sin(j * math.atan(2 * t))))
        e = abs(hs / t - 2 * (w0 - w))
        n0a += 1
        if e > 1e-12:
            okJ0 = False
        say("       k=%5d t=%-6s  H*/t=%+.15f  target %+.1f  err %.2e" % (k, t, hs / t, 2 * (w0 - w), e))
say("       cases: %d" % n0a)

say("  J0b  float64 Abel vs 50-digit mpmath on the DIRECT sum")
n0b = 0
for (s, k) in ((1.0, 256), (2.0, 256), (0.5, 256)):
    t1, _ = first_zero(k, s)
    for m in (0.8, 1.0, 1.2):
        a = F_abel(k, s, t1 * m)[0]
        b = float(F_direct_mp(k, s, t1 * m))
        n0b += 1
        if abs(a - b) > 1e-9:
            okJ0 = False
        say("       s=%-4s k=%4d  abel %+.12f  direct %+.12f  |diff| %.2e" % (s, k, a, b, abs(a - b)))
say("       cases: %d" % n0b)

say("  J0c  t_1 at (s,k)=(1,256) against the published value from another script")
t1r, _ = first_zero(256, 1.0)
e0c = abs(t1r - 0.106767212545108)
if e0c > 1e-9:
    okJ0 = False
say("       here %.15f  published %.15f  |diff| %.2e" % (t1r, 0.106767212545108, e0c))

say("  J0d  C_s is computed, not typed: C_{1/2} must equal sqrt(pi)")
e0d = abs(C_of(0.5) - math.sqrt(math.pi))
if e0d > 1e-12:
    okJ0 = False
say("       C_0.5 = %.15f   sqrt(pi) = %.15f   err %.2e" % (C_of(0.5), math.sqrt(math.pi), e0d))

say("  -> %s" % ("PASS" if okJ0 else "FAIL"))
verdicts.append(("J0 instrument", okJ0))
if not okJ0:
    say()
    say("ABORTING: an instrument control failed, so nothing below means anything.")
    sys.exit(1)

# ------------------------------------------------------------------ measure
say()
say("--- the measurement ---")
say("  %5s %7s %18s %11s %11s %8s %8s" % ("s", "k", "t_1", "lambda_eff", "H*/t", "quantum", "margin"))
data = {}
for s in S_ALL:
    for k in K_LIST:
        t1, margin = first_zero(k, s)
        if t1 is None:
            say("  %5s %7d   NO ZERO IN RANGE" % (s, k))
            continue
        lam = 2.0 * k * t1 * t1 / math.log(k)
        _, hs = F_abel(k, s, t1)
        q = 4 * math.pi * t1 / math.log(k)
        data[(s, k)] = (t1, lam, hs / t1, q, margin)
        say("  %5s %7d %18.14f %11.6f %11.5f %8.5f %8.1f" % (s, k, t1, lam, hs / t1, q, margin))
    say()
say("  population: %d points" % len(data))
if not data:
    say("FAIL: empty population (F60)")
    sys.exit(1)

# ------------------------------------------------------------------ J1
say()
say("--- J1  THE TWO-TERM LAW, no fitted constant ---")
say("      R1 = |smaller term|, R2 = |H*/t - 2 zeta(s) - C_s t^{s-1}|;  require R2/R1 < 1/3")
okJ1, nJ1 = True, 0
for s in S_TWOTERM:
    z2, cs = Z2_of(s), C_of(s)
    say("  s=%-5s 2 zeta(s) = %+.6f   C_s = %+.6f" % (s, z2, cs))
    say("       %7s %11s %12s %12s %11s %9s" % ("k", "H*/t", "2 zeta(s)", "C_s t^{s-1}", "R2", "R2/R1"))
    rows = []
    for k in K_LIST:
        if (s, k) not in data:
            continue
        t1, lam, hot, q, _ = data[(s, k)]
        corr = cs * t1 ** (s - 1.0)
        r2 = abs(hot - z2 - corr)
        r1 = min(abs(z2), abs(corr))
        rows.append((k, r2, r2 / r1))
        say("       %7d %11.5f %12.6f %12.6f %11.6f %9.4f" % (k, hot, z2, corr, r2, r2 / r1))
    last4 = [r for _, r, _ in rows[-4:]]
    mono = all(last4[i + 1] <= last4[i] * 1.0000001 for i in range(len(last4) - 1))
    good = rows[-1][2] < 1.0 / 3.0
    nJ1 += 1
    if not (mono and good):
        okJ1 = False
    say("       final R2/R1 = %.4f (<1/3: %s), R2 non-increasing over last 4: %s"
        % (rows[-1][2], good, mono))
say("  cases: %d -> %s" % (nJ1, "PASS" if okJ1 and nJ1 else "FAIL"))
verdicts.append(("J1 two-term head law", okJ1 and nJ1 > 0))

say()
say("--- J1-diag  WHY, REPORTED WITHOUT A VERDICT.  Not a criterion; a diagnosis. ---")
say("      The r222 header dismissed the j ~ k end of H* as negligible.  It compared it")
say("      to the TOP TERM of the identity, which it is indeed smaller than by")
say("      1/sqrt(k log k).  It never compared it to the term it would actually have to")
say("      outrank: the head's own correction C_s t^{s-1}.  Geometric tail estimate,")
say("      derived not fitted:   TAIL ~ s k^{lambda-s-1} / (2 t^2)   as a share of H*/t.")
say("  %5s %7s %12s %12s %12s %9s" % ("s", "k", "R2", "TAIL est", "|C_s|t^{s-1}", "R2/TAIL"))
for s in S_TWOTERM:
    z2, cs = Z2_of(s), C_of(s)
    for k in K_LIST[-3:]:
        if (s, k) not in data:
            continue
        t1, lam, hot, q, _ = data[(s, k)]
        r2 = abs(hot - z2 - cs * t1 ** (s - 1.0))
        tail = s * k ** (lam - s - 1.0) / (2.0 * t1 * t1)
        say("  %5s %7d %12.6f %12.6f %12.6f %9.2f"
            % (s, k, r2, tail, abs(cs) * t1 ** (s - 1.0), r2 / tail if tail else float("nan")))
    say()

# ------------------------------------------------------------------ J2
say()
say("--- J2  ZERO-PARAMETER prediction of the zero (nothing measured on the right) ---")
say("  %5s %7s %11s %12s %12s %10s %6s" % ("s", "k", "lam_eff", "lam_pred", "resid", "quantum", "in D?"))
inD, tot = 0, 0
for s in S_TWOTERM + [2.0, 4.0]:
    for k in K_LIST:
        if (s, k) not in data:
            continue
        t1, lam, hot, q, _ = data[(s, k)]
        tp = predict_t(k, s)
        if tp is None:
            say("  %5s %7d   no solution to the balance equation" % (s, k))
            continue
        lp = 2.0 * k * tp * tp / math.log(k)
        tot += 1
        ok = abs(lam - lp) <= q
        inD += 1 if ok else 0
        say("  %5s %7d %11.6f %12.6f %12.6f %10.5f %6s" % (s, k, lam, lp, lam - lp, q, "yes" if ok else "no"))
    say()
fracJ2 = inD / tot if tot else 0.0
okJ2 = tot > 0 and fracJ2 >= 0.90
say("  within the quantum at %d of %d = %.3f -> %s" % (inD, tot, fracJ2, "PASS" if okJ2 else "FAIL"))
verdicts.append(("J2 zero-parameter prediction within the quantum", okJ2))

# ------------------------------------------------------------------ J3
say()
say("--- J3  THE PHASE TRANSITION: lambda_infty(s) = max(s/2, s-1/2) ---")
say("  %5s %7s %11s %9s %9s %10s %9s %9s"
    % ("s", "k", "lam_eff", "s/2", "s-1/2", "midpoint", "quantum", "gap/D"))
okJ3, nJ3 = True, 0
for s in (0.5, 0.75):
    ks = [k for k in K_LIST if (s, k) in data]
    k = ks[-1]
    t1, lam, hot, q, _ = data[(s, k)]
    mid = 0.5 * (s / 2 + (s - 0.5))
    nJ3 += 1
    if not lam > mid:
        okJ3 = False
    say("  %5s %7d %11.6f %9.4f %9.4f %10.4f %9.5f %9.1f"
        % (s, k, lam, s / 2, s - 0.5, mid, q, (lam - mid) / q))
say("  regression cases: %d -> %s" % (nJ3, "PASS" if okJ3 and nJ3 else "FAIL"))
verdicts.append(("J3 s/2 branch for s<1", okJ3 and nJ3 > 0))
say()
say("  the crossover, REPORTED WITHOUT A VERDICT (the branches are 0.05 apart at")
say("  s = 0.9 and 1.1, against a quantum of ~0.012, so this cannot be decisive):")
say("  %5s %7s %11s %9s %9s %11s" % ("s", "k", "lam_eff", "s/2", "s-1/2", "branch gap"))
for s in (0.9, 1.0, 1.1, 1.25):
    for k in (8192, 32768):
        if (s, k) not in data:
            continue
        t1, lam, hot, q, _ = data[(s, k)]
        say("  %5s %7d %11.6f %9.4f %9.4f %11.4f" % (s, k, lam, s / 2, s - 0.5, abs(s / 2 - (s - 0.5))))

# ------------------------------------------------------------------ J4
say()
say("--- J4  CONTROL: the correction must be case-specific, not an error sponge ---")
say("      require >=5x improvement at s=1.5, and <20% change at s=4 (no computable")
say("      second term there: C_4 is the indeterminate 0 x inf)")
okJ4 = True
for s, kind in ((1.5, "must improve >=5x"), (4.0, "must change <20%")):
    k = K_LIST[-1]
    if (s, k) not in data:
        continue
    t1, lam, hot, q, _ = data[(s, k)]
    z2 = Z2_of(s)
    r_one = abs(hot - z2)
    try:
        corr = C_of(s) * t1 ** (s - 1.0)
        if not math.isfinite(corr):
            corr = 0.0
    except Exception:
        corr = 0.0
    r_two = abs(hot - z2 - corr)
    ratio = r_one / r_two if r_two > 0 else float("inf")
    ok = (ratio >= 5.0) if s == 1.5 else (abs(r_two - r_one) / r_one < 0.20)
    okJ4 = okJ4 and ok
    say("      s=%-4s k=%d  one-term resid %.6f  two-term resid %.6f  ratio %.2f  %s -> %s"
        % (s, k, r_one, r_two, ratio, kind, "PASS" if ok else "FAIL"))
say("  -> %s" % ("PASS" if okJ4 else "FAIL: the correction is absorbing error, not describing it"))
verdicts.append(("J4 control: the correction is case-specific", okJ4))

say()
say("=" * 100)
for name, v in verdicts:
    say("  [%s] %s" % (name, "PASS" if v else "FAIL"))
say()
say("interpretation belongs in the report, not here.")
say("done.")
