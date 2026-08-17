#!/usr/bin/env python3
# abel_r220.py -- stop modelling the head.  An exact identity for arbitrary weights.
#
# ---------------------------------------------------------------------------
# WHERE THIS CAME FROM.  r219 established, by identity rather than by fitting, that the
# v3 model's error at the true zero is ENTIRELY the geometric-tail replacement:
#       L := F_model(t_1) = 2T sin(k theta) - Omega ,
# with the head contributing nothing.  fable-5's r218 ruling 4 asked for the asymptotics
# of the model equation.  Before doing asymptotics of an approximation, ask whether the
# approximation is needed at all.
#
# ---------------------------------------------------------------------------
# THE IDENTITY, DERIVED ON PAPER BEFORE ANY NUMBER.
#
# Abel summation with S_j = sum_{i<=j} z^i = (z^{j+1}-1)/(z-1):
#
#   sum_{j<k} w_j z^j = w_{k-1} S_{k-1} + sum_{j=0}^{k-2} (w_j - w_{j+1}) S_j
#                     = [ w_{k-1}(z^k - 1) + sum_{j=0}^{k-2} D_j (z^{j+1} - 1) ] / (z-1),
#
# where D_j := w_j - w_{j+1}.  The constants collapse: w_{k-1} + sum_{j<k-1} D_j = w_0.
# So, EXACTLY, for every complex z != 1 and every weight sequence:
#
#   (A)   G_k(z) = [ w_{k-1} z^k + sum_{j=0}^{k-2} D_j z^{j+1} - w_0 ] / (z - 1) .
#
# On the symmetry line z = 1 + 2it = rho e^{i theta}, so z - 1 = 2it and dividing by 2it
# turns a real part into an imaginary part.  With F_k = 1 + 2 Re G_k:
#
#   (B)   F_k(1/2 + it) = 1 + (1/t) [ w_{k-1} rho^k sin(k theta)
#                                     + sum_{j=1}^{k-1} (w_{j-1} - w_j) rho^j sin(j theta) ] .
#
# NO MODEL, NO HEAD, NO TAIL.  One exact sine series whose coefficients are the WEIGHT
# DECREMENTS, plus a single top term.
#
# It contains Theorem 2.  For w_0 >= 0 and w_j = w constant on 1 <= j <= k-1, every D_j
# with j >= 1 vanishes and only D_0 = w_0 - w survives, contributing
# (w_0-w) rho sin(theta)/t = (w_0-w)(2t)/t = 2(w_0-w), since rho sin theta = Im z = 2t.
# Hence F = 1 + 2w_0 - 2w + w rho^k sin(k theta)/t = A + w rho^k sin(k theta)/t.  Exactly
# Theorem 2, recovered as the case where the sine series is empty.
#
# AND IT GIVES A THEOREM IN TWO LINES.  If the weights are NON-INCREASING then every
# D_j >= 0 and w_{k-1} >= 0.  If moreover theta <= pi/k then j theta <= pi for every
# j <= k, so every sine in (B) is >= 0.  Therefore
#
#   (C)   w_0 >= w_1 >= ... >= w_{k-1} >= 0  and  arctan(2t) <= pi/k   ==>   F_k >= 1 ,
#
# hence the first zero satisfies t_1 > (1/2) tan(pi/k), FOR EVERY NON-INCREASING PROFILE.
# The note currently has this only for constant weights, and only when A >= 0
# (Theorem 2(b)).  Here monotonicity replaces the constancy and the A >= 0 hypothesis
# disappears.
#
# ---------------------------------------------------------------------------
# PRE-REGISTERED, before the first number.
#
#   A1  THE IDENTITY.  (B) against direct summation of 1 + 2 sum w_j rho^j cos(j theta),
#       at 60 digits, over a grid of (k, s, t) INCLUDING t far from any zero and t at a
#       zero.  Require agreement to 1e-45 absolute.  This is the whole round: if (B) is
#       wrong nothing else matters.  Two routes to the same number, as always.
#
#   A2  IT CONTAINS THEOREM 2.  For constant weights, (B) against A + w rho^k sin/t at
#       60 digits, three k, three t each.  Require 1e-45.  A general identity that does
#       not collapse to the proved special case is not a generalisation.
#
#   A3  THE THEOREM (C).  For non-increasing profiles, minimise F_k over 400 points of
#       0 < theta <= pi/k and require the minimum to be >= 1 at every (k, s).
#       ANY value below 1 REFUTES (C) and must be printed with its t.
#
#   A4  MONOTONICITY MUST BE DOING WORK -- a control that can fail (F97).  Build profiles
#       that are NOT non-increasing and check whether (C)'s conclusion breaks.  If F stays
#       >= 1 for all of them too, monotonicity is not the hypothesis and (C) is weaker
#       than the truth; say so.  Profiles: an increasing ramp, a bump at j = k/2, and an
#       alternating profile.  REGISTERED EXPECTATION: at least one of the three dips
#       below 1 somewhere in theta <= pi/k.
#
#   A5  SLACK, measured not argued.  Print t_1 / ((1/2)tan(pi/k)) for the decaying
#       profiles.  (C) is sharp for constant weights (Theorem 2(e) puts the zero exactly
#       at theta = pi/k) and is expected to be very slack for decaying ones -- the ratio
#       says how slack, which is what a future sharpening has to beat.  No verdict.
#
#   Populations printed.  Empty population = FAIL (F60).
# ---------------------------------------------------------------------------

import io
import sys
from mpmath import mp, mpf, sqrt, log, atan, cos, sin, tan, pi

LOG = __file__[:-3] + ".log"
OUT = []


def say(s=""):
    print(s, flush=True)
    OUT.append(s)
    io.open(LOG, "w", encoding="utf-8", newline="\n").write("\n".join(OUT) + "\n")


mp.dps = 60


def w_power(k, s):
    return [mpf(1) / mpf(j + 1) ** mpf(s) for j in range(k)]


def w_const(k, w0='0', w='0.5'):
    return [mpf(w0)] + [mpf(w)] * (k - 1)


def F_direct(w, t):
    """1 + 2 sum_j w_j rho^j cos(j theta) -- the definition."""
    rho, th = sqrt(1 + 4 * t * t), atan(2 * t)
    a = mpf(0)
    for j, wj in enumerate(w):
        if wj != 0:
            a += wj * rho ** j * cos(j * th)
    return 1 + 2 * a


def F_abel(w, t):
    """(B): 1 + (1/t)[ w_{k-1} rho^k sin(k th) + sum_{j>=1} (w_{j-1}-w_j) rho^j sin(j th) ]."""
    k = len(w)
    rho, th = sqrt(1 + 4 * t * t), atan(2 * t)
    acc = w[k - 1] * rho ** k * sin(k * th)
    for j in range(1, k):
        d = w[j - 1] - w[j]
        if d != 0:
            acc += d * rho ** j * sin(j * th)
    return 1 + acc / t


say("=" * 100)
say("abel_r220 -- an EXACT identity for arbitrary weights, and a theorem it gives free")
say("(B)  F_k(1/2+it) = 1 + (1/t)[ w_{k-1} rho^k sin(k th) + sum_j (w_{j-1}-w_j) rho^j sin(j th) ]")
say("derived by Abel summation on paper; nothing here is fitted or approximated")
say("=" * 100)

verdicts = []

# ------------------------------------------------------------------ A1
say()
say("--- A1  THE IDENTITY against direct summation, 60 digits ---")
say("  %5s %6s %14s %22s %12s" % ("s", "k", "t", "F (both routes)", "|diff|"))
okA1, nA1 = True, 0
for ss in ('1', '2', '4'):
    for k in (64, 256, 1024):
        pred = sqrt(mpf(ss) * log(k) / (2 * k))
        for lab, t in (('0.3*pred', pred * mpf('0.3')),
                       ('1.0*pred', pred),
                       ('2.7*pred', pred * mpf('2.7'))):
            a, b = F_direct(w_power(k, ss), t), F_abel(w_power(k, ss), t)
            d = abs(a - b)
            nA1 += 1
            if d > mpf('1e-45'):
                okA1 = False
            say("  %5s %6d %14s %22s %12s"
                % (ss, k, lab, mp.nstr(a, 18), mp.nstr(d, 4)))
say("  cases: %d -> %s" % (nA1, "PASS" if okA1 and nA1 else "FAIL"))
verdicts.append(('A1 identity vs direct summation', okA1 and nA1 > 0))
if not okA1:
    say("ABORTING: the identity is wrong, so nothing below means anything.")
    sys.exit(1)

# ------------------------------------------------------------------ A2
say()
say("--- A2  it must COLLAPSE to Theorem 2 for constant weights ---")
okA2, nA2 = True, 0
for (w0, w) in (('0', '0.5'), ('1', '0.5'), ('1', '1')):
    A = 1 + 2 * mpf(w0) - 2 * mpf(w)
    for k in (64, 256):
        for frac in ('0.4', '0.9'):
            t = mpf(frac) * tan(pi / k) / 2
            rho, th = sqrt(1 + 4 * t * t), atan(2 * t)
            thm2 = A + mpf(w) * rho ** k * sin(k * th) / t
            got = F_abel(w_const(k, w0, w), t)
            d = abs(thm2 - got)
            nA2 += 1
            if d > mpf('1e-45'):
                okA2 = False
            say("  w0=%s w=%s k=%4d A=%s  Thm2=%s  (B)=%s  |diff|=%s"
                % (w0, w, k, mp.nstr(A, 3), mp.nstr(thm2, 14),
                   mp.nstr(got, 14), mp.nstr(d, 4)))
say("  cases: %d -> %s" % (nA2, "PASS" if okA2 and nA2 else "FAIL"))
verdicts.append(('A2 collapses to Theorem 2', okA2 and nA2 > 0))

# ------------------------------------------------------------------ A3
say()
say("--- A3  THE THEOREM: non-increasing weights => F_k >= 1 for theta <= pi/k ---")
say("  %5s %6s %22s %14s" % ("s", "k", "min F over theta<=pi/k", "at theta/(pi/k)"))
okA3, nA3 = True, 0
PROFILES = [('1', w_power), ('1.5', w_power), ('2', w_power), ('4', w_power)]
for ss, mk in PROFILES:
    for k in (64, 256, 1024):
        w = mk(k, ss)
        best, bestx = None, None
        for i in range(1, 401):
            th = pi / k * mpf(i) / 400
            t = tan(th) / 2
            v = F_abel(w, t)
            if best is None or v < best:
                best, bestx = v, mpf(i) / 400
        nA3 += 1
        if best < 1:
            okA3 = False
        say("  %5s %6d %22s %14s" % (ss, k, mp.nstr(best, 16), mp.nstr(bestx, 5)))
# a non-power profile that is still non-increasing, as a second witness
for k in (256, 1024):
    w = [mpf(1) / log(mpf(j + 2)) for j in range(k)]
    best = min(F_abel(w, tan(pi / k * mpf(i) / 400) / 2) for i in range(1, 401))
    nA3 += 1
    if best < 1:
        okA3 = False
    say("  %5s %6d %22s %14s" % ('1/log', k, mp.nstr(best, 16), "-"))
say("  cases: %d -> %s" % (nA3, "PASS" if okA3 and nA3 else "FAIL -- (C) IS REFUTED"))
verdicts.append(('A3 theorem (C) holds', okA3 and nA3 > 0))

# ------------------------------------------------------------------ A4
say()
say("--- A4  CONTROL: does monotonicity do the work?  (profiles that are NOT decreasing) ---")
say("  registered expectation: at least one of the three dips below 1 in theta <= pi/k")
dips = 0
nA4 = 0
for name, build in (
        ('ramp  w_j = (j+1)/k',       lambda k: [mpf(j + 1) / k for j in range(k)]),
        ('bump  at j = k/2',          lambda k: [mpf(1) / mpf(j + 1) + (mpf(3) if j == k // 2 else mpf(0)) for j in range(k)]),
        ('alternating 1, 0.1, 1, ...', lambda k: [mpf(1) if j % 2 == 0 else mpf('0.1') for j in range(k)]),
):
    for k in (64, 256):
        w = build(k)
        best, bestx = None, None
        for i in range(1, 401):
            th = pi / k * mpf(i) / 400
            v = F_abel(w, tan(th) / 2)
            if best is None or v < best:
                best, bestx = v, mpf(i) / 400
        nA4 += 1
        below = best < 1
        if below:
            dips += 1
        say("  %-28s k=%4d  min F = %s  at theta/(pi/k)=%s   %s"
            % (name, k, mp.nstr(best, 14), mp.nstr(bestx, 4),
               "DIPS BELOW 1" if below else "stays >= 1"))
a4 = dips > 0
say("  profiles dipping below 1: %d of %d  -> %s" % (dips, nA4,
    "PASS: monotonicity is load-bearing" if a4 else
    "FAIL: the conclusion holds without monotonicity, so (C) is weaker than the truth"))
verdicts.append(('A4 monotonicity is load-bearing', a4))

# ------------------------------------------------------------------ A5
say()
say("--- A5  SLACK of the new bound (no verdict; this is what a sharpening must beat) ---")
say("  %5s %6s %18s %18s %10s" % ("s", "k", "t_1 (measured)", "(1/2)tan(pi/k)", "ratio"))
KNOWN = {('1', 64): '0.186199681452', ('1', 256): '0.106767212545', ('1', 1024): '0.0543428673092',
         ('2', 64): '0.302342703', ('2', 256): '0.1472309802', ('2', 1024): '0.0794766675',
         ('4', 64): '0.4555441314', ('4', 256): '0.2165900295', ('4', 1024): '0.1173883585'}
for (ss, k), v in sorted(KNOWN.items(), key=lambda x: (x[0][0], x[0][1])):
    lb = tan(pi / k) / 2
    say("  %5s %6d %18s %18s %10s"
        % (ss, k, v, mp.nstr(lb, 12), mp.nstr(mpf(v) / lb, 6)))
say("  (t_1 values are quoted from dense_r216c / quantum_r216d logs; the bound is computed here)")

say()
say("=" * 100)
for tag, v in verdicts:
    say("  [%s] %s" % (tag, "PASS" if v else "FAIL"))
say()
say("interpretation belongs in the report, not here.")
say("done.")
sys.exit(0 if all(v for _, v in verdicts) else 1)
