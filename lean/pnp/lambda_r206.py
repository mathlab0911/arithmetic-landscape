#!/usr/bin/env python3
# lambda_r206.py -- the s = 1 constant, and the observable the mechanism actually predicts.
#
# fable-5's r205 §2: pre-register the two candidate shapes and the discriminating column
# before the first new number; if neither fits, the constant stays unsettled and is said to be.
#
# ---------------------------------------------------------------------------
# FIRST, THE OBSERVABLE.  Every round so far reported  t_1 / sqrt(s log k / 2k).  But the
# mechanism does not predict t_1; it predicts the SCALE:
#
#        k^{-s} e^{2kt^2} = O(1)   <=>   2 k t_1^2 = lambda log k     with lambda = s.
#
# So the quantity the hypothesis names is
#
#        lambda_eff(k, s)  :=  2 k t_1^2 / log k ,
#
# and the ratio we have been printing is sqrt(lambda_eff / s) -- which HALVES every
# discrepancy before we look at it.  A 13% error in lambda shows up as 6% in the ratio.
# (F32: when a test does not resolve, first ask whether the observable is the one the
# hypothesis predicts.)  Everything below is reported in lambda.
#
# ---------------------------------------------------------------------------
# PRE-REGISTERED, before the first number.
#
#   SHAPE A (the paper's law, with a finite-size correction):
#       lambda_eff(k) -> s, with the approach governed by a correction of size
#       a/log k  or  b*loglog k/log k.  DISCRIMINATOR: (lambda_eff - s)*log k should
#       settle to a constant a (first form), or (lambda_eff - s)*log k/loglog k should
#       settle to b (second form).  One of the two columns going flat decides which.
#
#   SHAPE B (a genuinely different exponent at small s):
#       lambda_eff(k) -> s - 1/2.  This is what a naive stationary-phase balance gives,
#       k^{-s} e^{2kt^2} ~ t rather than ~ 1, since the oscillatory sum near j = k
#       contributes an extra 1/theta.  DISCRIMINATOR: lambda_eff - (s - 1/2) -> 0.
#
#   DECISION RULE.  For each s, over the largest three k:
#     * |lambda_eff - s| decreasing and < 0.10           -> SHAPE A
#     * |lambda_eff - (s-1/2)| decreasing and < 0.10     -> SHAPE B
#     * neither                                          -> UNSETTLED, report raw.
#   The verdict is per s.  A law that holds for s >= 2 and fails at s = 1 is itself a
#   finding, and is to be reported as one rather than smoothed over.
#
#   FALSIFIER (instrument, must pass first).  Constant weights w_0 = 0, w_j = 1/2 have
#   the zero set proved exactly at t = (1/2)tan(n pi/k) (Theorem 2(e), raised to *proved*
#   by fable-5's independent reading at r205).  The same code path must reproduce
#   t_1 = (1/2)tan(pi/k) to >= 25 digits.  *** The reference is computed INSIDE the
#   precision block: r202 lost a run to a 15-digit reference. ***
#
#   Every table prints its population; a verdict over an empty population is a FAIL (F60).
# ---------------------------------------------------------------------------

import sys
from mpmath import mp, mpf, sqrt, log, atan, cos, tan, pi

OUT = []


def say(s=""):
    print(s)
    OUT.append(s)


mp.dps = 40

SS = ['1', '1.5', '2', '3', '4']
KS = [64, 128, 256, 512, 1024, 2048]


def w_power(k, s):
    s = mpf(s)
    return [mpf(1) / mpf(j + 1) ** s for j in range(k)]


def w_const(k):
    return [mpf(0)] + [mpf(1) / 2] * (k - 1)


def F(w, t):
    rho = sqrt(1 + 4 * t * t)
    th = atan(2 * t)
    acc = mpf(0)
    for j, wj in enumerate(w):
        if wj != 0:
            acc += wj * rho ** j * cos(j * th)
    return 1 + 2 * acc


def first_zero(w, t_hi, n_scan=1500):
    """Scan upward FROM ZERO -- so 'first' is a claim about (0, t_hi), not about a window."""
    prev_t, prev_v = mpf(0), F(w, mpf(0))
    for i in range(1, n_scan + 1):
        t = mpf(t_hi) * i / n_scan
        v = F(w, t)
        if prev_v * v < 0:
            lo, hi = prev_t, t
            for _ in range(120):
                mid = (lo + hi) / 2
                if F(w, lo) * F(w, mid) <= 0:
                    hi = mid
                else:
                    lo = mid
            return (lo + hi) / 2
        prev_t, prev_v = t, v
    return None


say("=" * 96)
say("lambda_r206 -- the s = 1 constant, measured in the observable the mechanism predicts")
say("   lambda_eff(k,s) := 2 k t_1^2 / log k       (the paper's law says lambda_eff -> s)")
say("=" * 96)

verdicts = []

# ---------------------------------------------------------------- instrument
say()
say("--- FALSIFIER (instrument): constant weights, zero set PROVED exactly (Thm 2(e)) ---")
okI, nI = True, 0
for k in (64, 256):
    ref = tan(pi / k) / 2          # computed here, at mp.dps = 40 (r202's lesson)
    got = first_zero(w_const(k), 4 * ref)
    rel = abs(got - ref) / ref
    nI += 1
    say("  k=%4d  proved=%s  measured=%s  rel=%s"
        % (k, mp.nstr(ref, 20), mp.nstr(got, 20), mp.nstr(rel, 4)))
    if rel > mpf(10) ** (-25):
        okI = False
okI = okI and nI > 0
verdicts.append(('instrument', okI))
say("  cases: %d -> %s" % (nI, "PASS" if okI else "FAIL"))
if not okI:
    say()
    say("VERDICT: instrument failed.  Nothing below counts.")
    open(__file__[:-3] + ".log", "w").write("\n".join(OUT) + "\n")
    sys.exit(1)

# ---------------------------------------------------------------- the measurement
LAM = {}
for ss in SS:
    s = mpf(ss)
    say()
    say("--- w_j = (j+1)^-%s ---" % ss)
    say("  %6s %20s %12s %12s %14s %14s"
        % ("k", "t_1", "lambda_eff", "lam - s", "(lam-s)logk", "(lam-s)logk/loglogk"))
    LAM[ss] = {}
    for k in KS:
        w = w_power(k, ss)
        pred = sqrt(s * log(k) / (2 * k))
        t1 = first_zero(w, 3 * pred)
        if t1 is None:
            say("  %6d  NO ZERO in (0, 3*predicted)" % k)
            continue
        lam = 2 * k * t1 * t1 / log(k)
        d = lam - s
        LAM[ss][k] = lam
        say("  %6d %20s %12s %12s %14s %14s"
            % (k, mp.nstr(t1, 14), mp.nstr(lam, 8), mp.nstr(d, 6),
               mp.nstr(d * log(k), 6), mp.nstr(d * log(k) / log(log(k)), 6)))

# ---------------------------------------------------------------- decision
say()
say("=" * 96)
say("DECISION, by the rule registered before the run")
say("=" * 96)
n_dec = 0
rows = []
for ss in SS:
    s = mpf(ss)
    ks = sorted(LAM[ss])
    if len(ks) < 3:
        continue
    last3 = ks[-3:]
    dA = [abs(LAM[ss][k] - s) for k in last3]
    dB = [abs(LAM[ss][k] - (s - mpf(1) / 2)) for k in last3]
    decA = dA[0] > dA[1] > dA[2] and dA[2] < mpf('0.10')
    decB = dB[0] > dB[1] > dB[2] and dB[2] < mpf('0.10')
    v = "SHAPE A (lambda -> s)" if decA else ("SHAPE B (lambda -> s-1/2)" if decB else "UNSETTLED")
    n_dec += 1
    rows.append((ss, v, dA[2], dB[2]))
    say("  s=%-4s  |lam-s| -> %-10s  |lam-(s-1/2)| -> %-10s   %s"
        % (ss, mp.nstr(dA[2], 4), mp.nstr(dB[2], 4), v))

ok_pop = n_dec == len(SS)
verdicts.append(('population', ok_pop))
say()
say("  exponents decided: %d of %d -> %s"
    % (n_dec, len(SS), "PASS" if ok_pop else "FAIL -- a verdict over an empty population"))

say()
allA = all(v == "SHAPE A (lambda -> s)" for _, v, _, _ in rows)
anyU = any(v == "UNSETTLED" for _, v, _, _ in rows)
if allA:
    say("CONCLUSION: SHAPE A everywhere -- lambda_eff -> s, including at s = 1.")
    say("  The paper's law stands as written; the s = 1 'anomaly' was the observable,")
    say("  not the mathematics: the ratio to sqrt(s log k/2k) halves every discrepancy.")
elif anyU:
    say("CONCLUSION: at least one exponent is UNSETTLED.  Reported raw; the constant stays")
    say("  unsettled in the note, said plainly -- which was the third registered outcome.")
else:
    say("CONCLUSION: see the per-s verdicts above.")
say()
say("done.")

open(__file__[:-3] + ".log", "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(v for _, v in verdicts) else 1)
