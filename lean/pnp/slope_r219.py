#!/usr/bin/env python3
# slope_r219.py -- adversarial second reading of fable-5's r218 section 2.
#
# ---------------------------------------------------------------------------
# WHAT IS BEING READ.  fable-5 explained why the v3 model fits the constant-weight case
# although its LEVEL there is O(1) wrong (r218 section 2):
#
#     "the root of the v3 equation sits where T sin(k theta) crosses, and its slope
#      there is ~ kT ~ k^2/2pi.  A level error eps moves a root by eps/slope, so the
#      root shift is O(1)/O(k^2) in theta, i.e. relative error O(1/k)."
#
# The Dirichlet-kernel part I confirm independently:
#     Hp(theta) = -1/4 + sin((k-1/2)theta) / (4 sin(theta/2))     (w_0=0, w_j=1/2)
# and at theta = pi/k, since (k-1/2)(pi/k) = pi - pi/2k and sin(pi - x) = sin x, the
# quotient is sin(pi/2k)/sin(pi/2k) = 1 EXACTLY, so Hp(pi/k) = 0 and the model's level
# is 1 + 2Hp = 1 while Theorem 2 gives F(pi/k) = A = 0.  The O(1) level error is real.
#
# ---------------------------------------------------------------------------
# WHERE I DISAGREE, DERIVED ON PAPER BEFORE THIS RUN.
#
# The slope was taken from ONE of two terms of the same order.  With
# F_model = 1 + 2 Hp(theta) + 2 T sin(k theta),
#
#   oscillator:   d/dtheta [2 T sin(k theta)]   at theta = pi/k
#                 = 2Tk cos(pi) = -2kT ,  and T = (1/2)rho^k/(2t) ~ k/2pi,
#                 so this is  -k^2/pi .                       <-- fable's term
#
#   THE HEAD:     Hp is NOT slowly varying there.  It is a Dirichlet kernel, i.e. an
#                 oscillation with the SAME k, and theta = pi/k is where its numerator
#                 turns over:
#                 d/dtheta[sin((k-1/2)theta)] = (k-1/2)cos((k-1/2)theta) ~ -k  at pi/k,
#                 over a denominator 4 sin(theta/2) ~ 2 theta = 2pi/k, giving
#                 dHp/dtheta ~ -k^2/2pi, hence 2 dHp/dtheta ~ -k^2/pi .   <-- omitted
#
# The two are EQUAL at leading order, so the true slope is -2k^2/pi, twice fable's, and
#
#         delta = eps/|slope| = pi/(2k^2),      delta/(pi/k) = 1/(2k).
#
# PREDICTION, sharper than the O(1/k) that was claimed:  the relative error of the v3
# root on constant weights is  1/(2k)  with the constant, not merely the rate.
#   k =   64 -> 0.0078125     (measured by opus at r217b: 0.0075795)
#   k =  256 -> 0.001953125   (measured: 0.0019382)
#   k = 1024 -> 0.00048828125 (measured: 0.00048734)
#
# ---------------------------------------------------------------------------
# PRE-REGISTERED, before the first number.
#
#   S1  THE CONSTANT.  Solve the v3 equation on constant weights at k = 64..4096 and
#       compare rel(k) := (t_v3 - t_proved)/t_proved against 1/(2k).
#       Require max_k |rel(k)*2k - 1| < 0.05 over the population.
#       FAIL -> my correction is wrong and fable's rate-only statement is all that is
#       supported.  Reported as such: a rate confirmed and a constant refused.
#
#   S2  THE DECOMPOSITION, which is the actual claim.  Compute the two slope terms
#       numerically at theta = pi/k and require their ratio to approach 1:
#           |2 dHp/dtheta| / |2Tk|  ->  1 ,  require within 0.05 at k >= 512.
#       This is what separates "fable dropped a term" from "I got a factor 2 by luck".
#       Derivatives by central difference, step chosen and PRINTED, with a convergence
#       check at two step sizes so the difference is not trusted blindly.
#
#   S3  THE LEVEL, measured rather than argued.  fable's rule -- "to test the level,
#       evaluate the model at a known point, do not ask its root" -- applied to itself:
#       print F_model(pi/k) and F_exact(pi/k) = A.  Require |F_model - 1| < 1e-9 and
#       |F_exact| < 1e-9, i.e. the level error is exactly 1, not merely O(1).
#
#   S4  DOES THE SAME CORRECTION MATTER FOR DECAYING WEIGHTS?  There Hp converges and
#       is NOT a Dirichlet kernel, so its slope should be lower order than the
#       oscillator's.  Require |2 dHp/dtheta| / |2Tk| < 0.2 at s = 2, 4 for k >= 512.
#       If it is NOT small, then the same omission is present in the decaying analysis
#       too and r217b's 0.03% is partly steepness -- which is fable's own caveat, and
#       this is the measurement of it.
#
#   INSTRUMENT (first; abort).  Constant weights, zero set proved exactly, Thm 2(e),
#     reference computed inside the precision block.  Also: the closed form for Hp must
#     agree with the direct sum to 25 digits -- a second route to the head, since the
#     whole disagreement is about the head.
#
#   Populations printed.  Empty population = FAIL (F60).
# ---------------------------------------------------------------------------

import io
import sys
from mpmath import mp, mpf, sqrt, log, atan, cos, sin, tan, pi, findroot

LOG = __file__[:-3] + ".log"
OUT = []


def say(s=""):
    print(s, flush=True)
    OUT.append(s)
    io.open(LOG, "w", encoding="utf-8", newline="\n").write("\n".join(OUT) + "\n")


mp.dps = 40


def w_const(k):
    return [mpf(0)] + [mpf(1) / 2] * (k - 1)


def w_power(k, s):
    return [mpf(1) / mpf(j + 1) ** mpf(s) for j in range(k)]


def Hp_sum(w, th):
    """the head, by direct summation."""
    a = mpf(0)
    for j, wj in enumerate(w):
        if wj != 0:
            a += wj * cos(j * th)
    return a


def Hp_closed(k, th):
    """the head for w_0=0, w_j=1/2: -1/4 + sin((k-1/2)th)/(4 sin(th/2))."""
    return -mpf(1) / 4 + sin((k - mpf(1) / 2) * th) / (4 * sin(th / 2))


def T_of(w, k, t):
    rho = sqrt(1 + 4 * t * t)
    return w[-1] * rho ** k / (2 * t)


def Fmodel(w, k, t):
    """1 + 2 Hp(theta) + 2 T sin(k theta) -- the model, as written at r211."""
    th = atan(2 * t)
    return 1 + 2 * Hp_sum(w, th) + 2 * T_of(w, k, t) * sin(k * th)


def v3_root(w, k, t_lo, t_hi):
    """first root of the model above t_lo, by bisection on a bracketing pair."""
    a, b = mpf(t_lo), mpf(t_hi)
    fa, fb = Fmodel(w, k, a), Fmodel(w, k, b)
    if fa * fb > 0:
        return None
    for _ in range(200):
        m = (a + b) / 2
        if fa * Fmodel(w, k, m) <= 0:
            b = m
        else:
            a, fa = m, Fmodel(w, k, m)
    return (a + b) / 2


say("=" * 100)
say("slope_r219 -- adversarial second reading of fable-5's r218 section 2")
say("claim under test: the root's accuracy on constant weights is 1/(2k), not 1/k,")
say("because the Dirichlet-kernel head has the SAME O(k^2) slope as the oscillator.")
say("=" * 100)

verdicts = []
KS = [64, 128, 256, 512, 1024, 2048, 4096]

# ------------------------------------------------------------------ instrument
say()
say("--- INSTRUMENT: the closed form for the head against direct summation ---")
okI, nI = True, 0
for k in (64, 512):
    th = pi / k
    a, b = Hp_sum(w_const(k), th), Hp_closed(k, th)
    d = abs(a - b)
    nI += 1
    if d > mpf(10) ** (-25):
        okI = False
    say("  k=%5d  sum=%s  closed=%s  |diff|=%s"
        % (k, mp.nstr(a, 14), mp.nstr(b, 14), mp.nstr(d, 4)))
say("  cases: %d -> %s" % (nI, "PASS" if okI and nI else "FAIL"))
verdicts.append(('instrument (two routes to the head)', okI and nI > 0))
if not okI:
    sys.exit(1)

# ------------------------------------------------------------------ S3
say()
say("--- S3  THE LEVEL, at the point where the answer is proved (theta = pi/k) ---")
say("  fable's own rule applied to fable's argument: ask the model its VALUE, not its root")
okL, nL = True, 0
for k in (64, 256, 1024):
    t = tan(pi / k) / 2                      # inside the precision block (r202)
    th = atan(2 * t)
    lev_model = 1 + 2 * Hp_sum(w_const(k), th)
    lev_exact = mpf(1) + 2 * mpf(0) - 2 * (mpf(1) / 2)     # A = 1 + 2w_0 - 2w = 0
    Fex = lev_exact + 2 * T_of(w_const(k), k, t) * sin(k * th)
    nL += 1
    if abs(lev_model - 1) > mpf('1e-9') or abs(Fex) > mpf('1e-9'):
        okL = False
    say("  k=%5d  1+2Hp(pi/k) = %s      F_exact(pi/k) = A + 2T sin(pi) = %s"
        % (k, mp.nstr(lev_model, 16), mp.nstr(Fex, 6)))
say("  -> %s" % ("PASS: the level error is exactly 1" if okL and nL else "FAIL"))
verdicts.append(('S3 level error is exactly 1', okL and nL > 0))

# ------------------------------------------------------------------ S2
say()
say("--- S2  THE DECOMPOSITION: are the two slope terms the same order? ---")
say("  central differences at two step sizes, both printed; ratio must -> 1")
say("  %6s %16s %16s %10s %10s"
    % ("k", "|2 dHp/dth|", "|2 T k|", "ratio h1", "ratio h2"))
okS2, nS2 = True, 0
for k in KS:
    w = w_const(k)
    t = tan(pi / k) / 2
    th = atan(2 * t)
    Tk = 2 * T_of(w, k, t) * k
    rr = []
    for frac in (mpf(10) ** -8, mpf(10) ** -10):
        h = th * frac
        dH = 2 * (Hp_sum(w, th + h) - Hp_sum(w, th - h)) / (2 * h)
        rr.append(abs(dH) / abs(Tk))
    if k >= 512:
        nS2 += 1
        if abs(rr[0] - 1) > mpf('0.05'):
            okS2 = False
    say("  %6d %16s %16s %10s %10s"
        % (k, mp.nstr(abs(2 * (Hp_sum(w, th + th * mpf(10) ** -8)
                               - Hp_sum(w, th - th * mpf(10) ** -8))
                         / (2 * th * mpf(10) ** -8)), 10),
           mp.nstr(abs(Tk), 10), mp.nstr(rr[0], 6), mp.nstr(rr[1], 6)))
say("  cases at k>=512: %d -> %s" % (nS2, "PASS" if okS2 and nS2 else "FAIL"))
verdicts.append(('S2 head slope equals oscillator slope', okS2 and nS2 > 0))

# ------------------------------------------------------------------ S1
say()
say("--- S1  THE CONSTANT: rel(k) against 1/(2k) ---")
say("  %6s %20s %20s %14s %12s"
    % ("k", "t proved (Thm 2e)", "t from the model", "rel", "rel * 2k"))
okS1, nS1 = True, 0
for k in KS:
    w = w_const(k)
    ref = tan(pi / k) / 2
    root = v3_root(w, k, ref * mpf('1.0000001'), ref * mpf('1.2'))
    if root is None:
        say("  %6d  no root bracketed" % k)
        continue
    rel = (root - ref) / ref
    prod = rel * 2 * k
    nS1 += 1
    if abs(prod - 1) > mpf('0.05'):
        okS1 = False
    say("  %6d %20s %20s %14s %12s"
        % (k, mp.nstr(ref, 16), mp.nstr(root, 16), mp.nstr(rel, 8), mp.nstr(prod, 8)))
say("  cases: %d -> %s" % (nS1, "PASS" if okS1 and nS1 else "FAIL"))
verdicts.append(('S1 the constant is 1/(2k)', okS1 and nS1 > 0))

# ------------------------------------------------------------------ S4
say()
say("--- S4  does the omission matter for DECAYING weights too? ---")
say("  there Hp converges and is not a Dirichlet kernel, so its slope should be lower order")
say("  %5s %6s %16s %16s %10s" % ("s", "k", "|2 dHp/dth|", "|2 T k|", "ratio"))
okS4, nS4 = True, 0
for ss in ('2', '4'):
    for k in (512, 1024, 2048):
        w = w_power(k, ss)
        t = sqrt(mpf(ss) * log(k) / (2 * k))       # at the scale, not at a root
        th = atan(2 * t)
        h = th * mpf(10) ** -8
        dH = abs(2 * (Hp_sum(w, th + h) - Hp_sum(w, th - h)) / (2 * h))
        Tk = abs(2 * T_of(w, k, t) * k)
        r = dH / Tk
        nS4 += 1
        if r >= mpf('0.2'):
            okS4 = False
        say("  %5s %6d %16s %16s %10s"
            % (ss, k, mp.nstr(dH, 10), mp.nstr(Tk, 10), mp.nstr(r, 6)))
say("  cases: %d -> %s" % (nS4, "PASS -- the head is flat there, as expected"
                           if okS4 and nS4 else
                           "FAIL -- the same omission is present in the decaying analysis"))
verdicts.append(('S4 head flat for decaying weights', okS4 and nS4 > 0))

say()
say("=" * 100)
for tag, v in verdicts:
    say("  [%s] %s" % (tag, "PASS" if v else "FAIL"))
say()
say("interpretation belongs in the report, not here.")
say("done.")
sys.exit(0 if all(v for _, v in verdicts) else 1)
