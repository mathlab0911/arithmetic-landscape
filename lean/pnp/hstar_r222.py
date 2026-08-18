#!/usr/bin/env python3
# hstar_r222.py -- the asymptotics of the Abel sine series, done on paper first.
#
# =============================================================================
# WHERE THIS COMES FROM
#
# r220 replaced four rounds of head-plus-tail modelling with an exact identity.  With
# z = 1 + 2it = rho e^{i theta}, w_j the weights, D_j := w_{j-1} - w_j:
#
#   (B)  F_k(1/2+it) = 1 + (1/t) [ w_{k-1} rho^k sin(k theta) + H*(t) ] ,
#        H*(t) := sum_{j=1}^{k-1} D_j rho^j sin(j theta) .
#
# fable-5's r218 ruling 4 asked for the asymptotics of the (now retired) model equation.
# r221 substituted this object for it and asked for ratification.  H* is where
# lim (lambda_eff - s) lives, and this script tests a derivation of it.
#
# The weights throughout are the power family w_j = (j+1)^{-s}, j = 0..k-1, and
#   lambda_eff := 2 k t_1^2 / log k ,   t_1 = the FIRST zero of F_k on the line.
#
# =============================================================================
# THE DERIVATION, ON PAPER, BEFORE ANY NUMBER.
#
# Scales.  At t ~ sqrt(log k / k):  theta = 2t + O(t^3),  log rho = 2t^2 + O(t^4),
# so rho^j = e^{2jt^2}(1+o(1)) uniformly for j <= k, and rho^k = k^lambda (1+o(1))
# once 2kt^2 = lambda log k.  Hence
#
#        H*(t)  ~  sum_{j>=1} D_j e^{2 j t^2} sin(2 j t) ,      D_j = j^{-s} - (j+1)^{-s} .
#
# WHERE H* LIVES.  D_j ~ s j^{-(s+1)}: one power faster than the weights.  Put u = 2jt.
# The exponential is e^{ut}, which is 1 + o(1) until u ~ 1/t, and the sine kills
# everything beyond u ~ 1.  So the sum is concentrated at j ~ 1/(2t), NOT at j ~ k.
# (Checked below: the j ~ k end contributes O(k^{lambda-s-1/2}), smaller than the top
# term of (B) by 1/sqrt(k log k).)  Three regimes, by whether sum_j j D_j converges:
#
#   EXACT LEMMA (Abel again, no asymptotics):
#        sum_{j=1}^{J} j D_j  =  sum_{i=0}^{J-1} w_i  -  J w_J .
#
#   s > 1.  sin(2jt) ~ 2jt on the whole range that matters, so
#        H*/t  ->  2 sum_{i>=0} w_i  =  2 zeta(s) .                              [P1]
#
#   s = 1.  D_j = 1/(j(j+1)).  sum_j sin(2jt)/j^2 = Cl_2(2t) = 2t(1 - log 2t) + O(t^3)
#   (Clausen), and the 1/(j^2(j+1)) remainder contributes exactly 2t to leading order:
#        H*/t  ->  -2 log(2t)  =  log k - log log k - log(2 lambda) .            [P2]
#   The cutoff-at-J heuristic gives 2 log(1/2t) + 2 gamma - 2 instead; it differs by
#   2 gamma - 2 = -0.8456, so this is a place where the crude argument is WRONG by a
#   printable amount, and the run can say which is right.
#
#   0 < s < 1.  Now sum_j j D_j diverges and the integral is the leading term:
#        int_0^inf u^{-s-1} sin u du = Gamma(-s) sin(-pi s/2) = Gamma(1-s) sin(pi s/2)/s ,
#        H*/t^s  ->  2^s Gamma(1-s) sin(pi s / 2) .                              [P3]
#   (At s = 1/2 this is exactly sqrt(pi).)  H*/t itself GROWS, like t^{s-1}.
#
# THE CONSEQUENCE.  At the first zero F_k = 0, so (B) gives w_{k-1} rho^k |sin(k theta)|
# = t + H*, and with w_{k-1} = k^{-s}, rho^k = k^lambda, |sin| -> 1:
#
#        k^{lambda - s}  =  ( t + H* ) * (1 + o(1)) .
#
#   s > 1:  RHS -> (1 + 2 zeta(s)) t,  so (lambda-s) log k = -1/2 log k + 1/2 log log k
#           + O(1), giving   lambda -> s - 1/2 ,  loglog coefficient 1/2.
#   s = 1:  RHS ~ t log k, giving   lambda -> 1/2 ,  loglog coefficient 3/2.
#           (The 3/2 is fable-5's ALT212 number, obtained there from the model.)
#   s < 1:  RHS ~ C_s t^s, giving (lambda-s) log k = -(s/2) log k + (s/2) log log k
#           + O(1), so   lambda -> s/2 ,  loglog coefficient s/2.
#
#        =====================================================================
#        lambda_infty(s) = max( s/2 , s - 1/2 ) , with the kink at s = 1
#        =====================================================================
#
#   The two branches cross exactly where zeta(s) stops converging.  For s > 1 the head
#   is a constant and the zero is set by the top term alone; for s < 1 the head itself
#   diverges and drags the zero outward.  s < 1 has NEVER been measured in this project:
#   every published (s,k) has s >= 1.  So P4 below is a prediction about a region we
#   have not looked at, made before looking.
#
# =============================================================================
# PRE-REGISTERED, before the first number.
#
#  I0  INSTRUMENT -- three controls against answers already known exactly, and THIS IS
#      THE ONE THAT MUST PASS FIRST (F86).  A falsifier for the law alone cannot see a
#      broken apparatus.
#        I0a  Constant weights: only D_0 survives and rho sin theta = 2t exactly, so
#             H*/t = 2(w_0 - w) for EVERY t.  Six (k,t).  Require < 1e-12.
#        I0b  The float64 Abel evaluation against 50-digit mpmath on the DIRECT sum
#             1 + 2 sum w_j rho^j cos(j theta), at three t near t_1.  Require 1e-9
#             absolute.  (These are two different formulae AND two different precisions;
#             a disagreement localises to whichever changed.)
#        I0c  t_1 at (s,k) = (1,256) must reproduce the value this project has published
#             from a different script, 0.106767212545108, to 1e-9.
#      ANY I0 FAILURE ABORTS THE RUN.
#
#  I1  [P1]  s in {1.5, 2, 4}: |H*/t - 2 zeta(s)| / 2 zeta(s) < 0.10 at the largest k,
#      AND non-increasing over the last four k.  FLOOR: t_1 is bisected to 1e-14, so the
#      measurement error here is ~1e-12; the tolerance is entirely about the O(t^{s-1})
#      correction the derivation drops, which is why 10% and a monotonicity clause
#      rather than a tight bound at one point.
#
#  I2  [P2]  s = 1: |H*/t - (log k - log log k - log(2 lambda_eff))| < 0.5 at the largest
#      k and non-increasing over the last four.  The competing (cutoff) prediction sits
#      0.8456 away, so this criterion can distinguish them; BOTH residuals are printed.
#
#  I3  [P3]  s in {0.5, 0.75}: |H*/t^s - 2^s Gamma(1-s) sin(pi s/2)| relative < 0.10 at
#      the largest k and non-increasing over the last four.
#
#  I4  [P4] THE DECISIVE ONE -- a sign, at a stated place, with no constant fitted.
#      At s = 0.5 the two candidate limits are s/2 = 0.25 and s - 1/2 = 0.0.  They differ
#      by 0.25 while the observable's own quantum D = 4 pi t_1 / log k is ~0.008 there,
#      i.e. thirty times smaller -- so the range CAN answer (F32).  REGISTERED:
#        lambda_eff(s=0.5) at the largest k must exceed 0.125, the midpoint.
#      Below 0.125 REFUTES the s/2 branch and is to be reported as a refutation, not
#      explained.  Same test at s = 0.75 (branches 0.375 vs 0.25, midpoint 0.3125).
#
#  I5  CONTROL THAT CAN FAIL (the r219 L4 lesson: a correction that explains both cases
#      explains neither).  The two branches must not both describe everything:
#        H*/t at s = 2 must vary by less than 25% across the k ladder (bounded),
#        H*/t at s = 0.5 must GROW by at least a factor 2 across the same ladder.
#      If s=2 also grows, or s=0.5 is also flat, the regime split is not real.
#
#  I6  REPORTED, NO VERDICT.  lambda_eff against both branches with the quantum beside
#      it; and the scan margin in grid steps at every point (F92 -- "it worked last time"
#      is not evidence, and this project once published 25 values from a scan whose
#      resolution had never been stated).
#
#  Populations printed.  An empty population is a FAIL, not a pass (F60).
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

S_LIST = [0.5, 0.75, 1.0, 1.5, 2.0, 4.0]
K_LIST = [256, 512, 1024, 2048, 4096, 8192, 16384, 32768]
EULER = 0.5772156649015329


# ---------------------------------------------------------------- the object
def decrements(k, s):
    """D_j = w_{j-1} - w_j for j = 1..k-1, with w_j = (j+1)^{-s}."""
    j = np.arange(1, k, dtype=np.float64)
    return j ** (-s) - (j + 1.0) ** (-s)


def F_abel(k, s, t, D=None):
    """(B) in float64.  Every term is O(1) here, which the direct sum is not."""
    if D is None:
        D = decrements(k, s)
    rho2 = 1.0 + 4.0 * t * t
    lrho = 0.5 * math.log(rho2)
    th = math.atan(2.0 * t)
    j = np.arange(1, k, dtype=np.float64)
    hstar = float(np.sum(D * np.exp(j * lrho) * np.sin(j * th)))
    top = (k ** (-s)) * math.exp(k * lrho) * math.sin(k * th)
    return 1.0 + (top + hstar) / t, hstar, top


def Hstar_only(k, s, t, D=None):
    if D is None:
        D = decrements(k, s)
    lrho = 0.5 * math.log1p(4.0 * t * t)
    th = math.atan(2.0 * t)
    j = np.arange(1, k, dtype=np.float64)
    return float(np.sum(D * np.exp(j * lrho) * np.sin(j * th)))


def F_direct_mp(k, s, t):
    """The definition, at 50 digits.  Only ever used as a control."""
    t = mpf(t)
    rho, th = msqrt(1 + 4 * t * t), matan(2 * t)
    a = mpf(0)
    for jj in range(k):
        a += mpf(1) / mpf(jj + 1) ** mpf(s) * rho ** jj * mcos(jj * th)
    return 1 + 2 * a


def first_zero(k, s):
    """Scan up from 0 with >= 20 points per half period of sin(k theta), then bisect.
    Returns (t_1, margin_in_steps, n_grid).  The margin is printed, never assumed."""
    D = decrements(k, s)
    # generous upper end: the largest lambda we could plausibly be looking at is s+1
    t_hi = math.sqrt((s + 1.0) * math.log(k) / (2.0 * k)) * 2.0
    half_periods = k * math.atan(2 * t_hi) / math.pi
    n = int(max(2000, 20 * half_periods))
    ts = np.linspace(t_hi / n, t_hi, n)
    vals = np.array([F_abel(k, s, float(x), D)[0] for x in ts])
    idx = np.nonzero(vals <= 0.0)[0]
    if len(idx) == 0:
        return None, None, n
    i = int(idx[0])
    lo, hi = (ts[i - 1], ts[i]) if i > 0 else (ts[0] / 2, ts[0])
    # margin: how many grid steps wide is the excursion that produced this crossing?
    jdx = i
    while jdx + 1 < len(vals) and vals[jdx + 1] <= 0.0:
        jdx += 1
    margin = float(jdx - i + 1)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if hi - lo < 1e-15 * max(1.0, hi):
            break
        if F_abel(k, s, mid, D)[0] <= 0.0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi), margin, n


say("=" * 100)
say("hstar_r222 -- asymptotics of the Abel sine series H*, derived on paper (see header)")
say("  [P1] s>1 : H*/t   -> 2 zeta(s)")
say("  [P2] s=1 : H*/t   -> log k - log log k - log(2 lambda)")
say("  [P3] s<1 : H*/t^s -> 2^s Gamma(1-s) sin(pi s/2)")
say("  [P4]       lambda_infty(s) = max(s/2, s-1/2), kink at s=1 where zeta stops converging")
say("=" * 100)

verdicts = []

# ------------------------------------------------------------------ I0
say()
say("--- I0  INSTRUMENT.  Controls against answers already known exactly.  Runs FIRST. ---")

say("  I0a  constant weights: H*/t must equal 2(w_0 - w) at EVERY t (only D_0 survives)")
okI0a, nI0a = True, 0
for k in (64, 512, 4096):
    for t in (0.003, 0.05):
        w0, w = 0.0, 0.5
        j = np.arange(1, k, dtype=np.float64)
        D = np.zeros(k - 1)
        D[0] = w0 - w
        lrho = 0.5 * math.log1p(4.0 * t * t)
        th = math.atan(2.0 * t)
        hs = float(np.sum(D * np.exp(j * lrho) * np.sin(j * th)))
        err = abs(hs / t - 2.0 * (w0 - w))
        nI0a += 1
        if err > 1e-12:
            okI0a = False
        say("       k=%5d  t=%-7s  H*/t = %+.15f   target %+.1f   err %.2e"
            % (k, t, hs / t, 2 * (w0 - w), err))
say("       cases: %d -> %s" % (nI0a, "PASS" if okI0a and nI0a else "FAIL"))

say("  I0b  float64 Abel vs 50-digit mpmath on the DIRECT sum (two formulae, two precisions)")
okI0b, nI0b = True, 0
for (s, k) in ((1.0, 256), (2.0, 256), (0.5, 256)):
    t1, _, _ = first_zero(k, s)
    for mult in (0.8, 1.0, 1.2):
        t = t1 * mult
        a = F_abel(k, s, t)[0]
        b = float(F_direct_mp(k, s, t))
        nI0b += 1
        if abs(a - b) > 1e-9:
            okI0b = False
        say("       s=%-4s k=%4d  t=%.10f   abel %+0.12f   direct %+0.12f   |diff| %.2e"
            % (s, k, t, a, b, abs(a - b)))
say("       cases: %d -> %s" % (nI0b, "PASS" if okI0b and nI0b else "FAIL"))

say("  I0c  t_1 at (s,k)=(1,256) against this project's published value, from another script")
t1_ref, _, _ = first_zero(256, 1.0)
PUB = 0.106767212545108
okI0c = abs(t1_ref - PUB) < 1e-9
say("       here %.15f   published %.15f   |diff| %.2e -> %s"
    % (t1_ref, PUB, abs(t1_ref - PUB), "PASS" if okI0c else "FAIL"))

verdicts.append(("I0 instrument", okI0a and okI0b and okI0c))
if not (okI0a and okI0b and okI0c):
    say()
    say("ABORTING: an instrument control failed, so nothing below means anything.")
    sys.exit(1)

# ------------------------------------------------------------------ measure
say()
say("--- the measurement: t_1, lambda_eff, and H* at t_1 ---")
say("  %5s %7s %18s %11s %10s %9s %8s"
    % ("s", "k", "t_1", "lambda_eff", "H*/t", "H*/t^s", "margin"))
data = {}
for s in S_LIST:
    for k in K_LIST:
        t1, margin, ngrid = first_zero(k, s)
        if t1 is None:
            say("  %5s %7d   NO ZERO FOUND in the scanned range (grid %d)" % (s, k, ngrid))
            continue
        lam = 2.0 * k * t1 * t1 / math.log(k)
        hs = Hstar_only(k, s, t1)
        data[(s, k)] = (t1, lam, hs / t1, hs / t1 ** s, margin)
        say("  %5s %7d %18.14f %11.6f %10.5f %9.5f %8.1f"
            % (s, k, t1, lam, hs / t1, hs / t1 ** s, margin))
    say()
say("  population: %d points" % len(data))
if len(data) == 0:
    say("FAIL: empty population (F60)")
    sys.exit(1)

# ------------------------------------------------------------------ I1
say()
say("--- I1  [P1]  s>1:  H*/t -> 2 zeta(s) ---")
okI1, nI1 = True, 0
for s in (1.5, 2.0, 4.0):
    tgt = float(2 * zeta(s))
    rels = []
    for k in K_LIST:
        if (s, k) in data:
            rels.append((k, abs(data[(s, k)][2] - tgt) / tgt))
    say("  s=%-4s target 2*zeta(s) = %.6f" % (s, tgt))
    for k, r in rels:
        say("       k=%6d   H*/t = %10.5f   rel = %.4e" % (k, data[(s, k)][2], r))
    last4 = [r for _, r in rels[-4:]]
    mono = all(last4[i + 1] <= last4[i] * 1.0000001 for i in range(len(last4) - 1))
    good = rels[-1][1] < 0.10
    nI1 += 1
    if not (mono and good):
        okI1 = False
    say("       final rel %.4e (<0.10: %s), non-increasing over last 4: %s"
        % (rels[-1][1], good, mono))
say("  cases: %d -> %s" % (nI1, "PASS" if okI1 and nI1 else "FAIL"))
verdicts.append(("I1 s>1 head -> 2 zeta(s)", okI1 and nI1 > 0))

# ------------------------------------------------------------------ I2
say()
say("--- I2  [P2]  s=1:  H*/t -> log k - log log k - log(2 lambda)   (Clausen) ---")
say("      the cutoff heuristic predicts 2*log(1/2t) + 2 gamma - 2 instead; both printed")
say("  %7s %10s %12s %10s %12s %10s"
    % ("k", "H*/t", "Clausen", "resid", "cutoff", "resid"))
okI2, resI2 = True, []
for k in K_LIST:
    if (1.0, k) not in data:
        continue
    t1, lam, hot, _, _ = data[(1.0, k)]
    pc = math.log(k) - math.log(math.log(k)) - math.log(2.0 * lam)
    pk = 2.0 * math.log(1.0 / (2.0 * t1)) + 2.0 * EULER - 2.0
    resI2.append((k, abs(hot - pc)))
    say("  %7d %10.5f %12.5f %10.5f %12.5f %10.5f"
        % (k, hot, pc, hot - pc, pk, hot - pk))
last4 = [r for _, r in resI2[-4:]]
monoI2 = all(last4[i + 1] <= last4[i] * 1.0000001 for i in range(len(last4) - 1))
goodI2 = resI2[-1][1] < 0.5
okI2 = monoI2 and goodI2 and len(resI2) > 0
say("  final |resid| %.5f (<0.5: %s), non-increasing over last 4: %s;  cases: %d -> %s"
    % (resI2[-1][1], goodI2, monoI2, len(resI2), "PASS" if okI2 else "FAIL"))
verdicts.append(("I2 s=1 head ~ log k (Clausen constant)", okI2))

# ------------------------------------------------------------------ I3
say()
say("--- I3  [P3]  s<1:  H*/t^s -> 2^s Gamma(1-s) sin(pi s/2) ---")
okI3, nI3 = True, 0
for s in (0.5, 0.75):
    tgt = float(2 ** s * gamma(1 - s) * mp.sin(mp.pi * s / 2))
    rels = []
    for k in K_LIST:
        if (s, k) in data:
            rels.append((k, abs(data[(s, k)][3] - tgt) / tgt))
    say("  s=%-4s target = %.6f" % (s, tgt))
    for k, r in rels:
        say("       k=%6d   H*/t^s = %10.5f   rel = %.4e" % (k, data[(s, k)][3], r))
    last4 = [r for _, r in rels[-4:]]
    mono = all(last4[i + 1] <= last4[i] * 1.0000001 for i in range(len(last4) - 1))
    good = rels[-1][1] < 0.10
    nI3 += 1
    if not (mono and good):
        okI3 = False
    say("       final rel %.4e (<0.10: %s), non-increasing over last 4: %s"
        % (rels[-1][1], good, mono))
say("  cases: %d -> %s" % (nI3, "PASS" if okI3 and nI3 else "FAIL"))
verdicts.append(("I3 s<1 head ~ t^s with the Gamma constant", okI3 and nI3 > 0))

# ------------------------------------------------------------------ I4
say()
say("--- I4  [P4] THE DECISIVE TEST: which branch does lambda_eff go to, for s < 1? ---")
say("      registered BEFORE the run: lambda_eff must exceed the midpoint of the two")
say("      candidate limits.  Below it REFUTES the s/2 branch.")
say("  %5s %7s %11s %9s %9s %10s %9s %8s"
    % ("s", "k", "lambda_eff", "s/2", "s-1/2", "midpoint", "quantum", "verdict"))
okI4, nI4 = True, 0
for s in (0.5, 0.75):
    ks = [k for k in K_LIST if (s, k) in data]
    for k in ks:
        t1, lam, _, _, _ = data[(s, k)]
        mid = 0.5 * (s / 2 + (s - 0.5))
        q = 4 * math.pi * t1 / math.log(k)
        v = "s/2" if lam > mid else "s-1/2"
        say("  %5s %7d %11.6f %9.4f %9.4f %10.4f %9.5f %8s"
            % (s, k, lam, s / 2, s - 0.5, mid, q, v))
    kk = ks[-1]
    lam = data[(s, kk)][1]
    mid = 0.5 * (s / 2 + (s - 0.5))
    nI4 += 1
    if not lam > mid:
        okI4 = False
    say("       at k=%d: lambda_eff = %.6f vs midpoint %.4f -> %s"
        % (kk, lam, mid, "s/2 branch" if lam > mid else "REFUTED"))
say("  cases: %d -> %s" % (nI4, "PASS" if okI4 and nI4 else "FAIL"))
verdicts.append(("I4 lambda -> s/2 for s<1", okI4 and nI4 > 0))

# ------------------------------------------------------------------ I5
say()
say("--- I5  CONTROL: the two regimes must not both describe everything ---")
say("      registered: H*/t bounded (<25% spread) at s=2, and growing (>=2x) at s=0.5")
okI5 = True
for s, kind in ((2.0, "bounded"), (0.5, "growing")):
    vs = [data[(s, k)][2] for k in K_LIST if (s, k) in data]
    spread = (max(vs) - min(vs)) / min(vs)
    ratio = vs[-1] / vs[0]
    if kind == "bounded":
        ok = spread < 0.25
    else:
        ok = ratio >= 2.0
    okI5 = okI5 and ok
    say("      s=%-4s  H*/t from %.4f to %.4f   spread %.3f   ratio %.3f   %s -> %s"
        % (s, vs[0], vs[-1], spread, ratio, kind, "PASS" if ok else "FAIL"))
say("  -> %s" % ("PASS" if okI5 else "FAIL: a law that covers both cases distinguishes neither"))
verdicts.append(("I5 control: the regimes are distinct", okI5))

# ------------------------------------------------------------------ I6
say()
say("--- I6  lambda_eff against BOTH branches, with the quantum beside it (no verdict) ---")
say("      predicted = branch + a*loglog k/log k, a = s/2 (s<1), 3/2 (s=1), 1/2 (s>1)")
say("  %5s %7s %11s %12s %12s %10s"
    % ("s", "k", "lambda_eff", "pred(branch)", "resid", "quantum"))
for s in S_LIST:
    a = s / 2 if s < 1 else (1.5 if s == 1.0 else 0.5)
    br = max(s / 2, s - 0.5)
    for k in K_LIST:
        if (s, k) not in data:
            continue
        t1, lam, _, _, _ = data[(s, k)]
        pred = br + a * math.log(math.log(k)) / math.log(k)
        q = 4 * math.pi * t1 / math.log(k)
        say("  %5s %7d %11.6f %12.6f %12.6f %10.5f" % (s, k, lam, pred, lam - pred, q))
    say()

say("=" * 100)
for name, v in verdicts:
    say("  [%s] %s" % (name, "PASS" if v else "FAIL"))
say()
say("interpretation belongs in the report, not here.")
say("done.")
