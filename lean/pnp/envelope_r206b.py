#!/usr/bin/env python3
# envelope_r206b.py -- a diagnosis that refuted itself, kept because that is the result.
#
# r206 measured lambda_eff = 2k t_1^2/log k and found it near s but NON-MONOTONE, with all
# five exponents jumping the same way at the same k.  Five independent families wobbling in
# the same place is not noise; it is the instrument.  This round proposed a cause and an
# instrument to remove it, and BOTH were wrong.  The refutation is the round's content.
#
# THE PROPOSED DIAGNOSIS.  On the line F_k = 1 + 2 Re G_k(1+2it) = 1 + 2|G_k|cos(phase); the
# phase advances by about 2k dt, so troughs should be spaced pi/k in t, and t_1 -- being
# stuck at a trough -- would be QUANTISED with relative granularity pi/(k t_1), which at
# k = 512, s = 1 is 8% in t and 16% in lambda: the size of the wobble.  (F25's shape, at a
# ladder rather than a lattice.)
#
# THE PROPOSED INSTRUMENT.  t* := smallest t with 2|G_k(1+2it)| = 1 -- the envelope reaching
# the constant term -- which is smooth and would carry no granularity.
#
# ---------------------------------------------------------------------------
# PRE-REGISTERED, before the first number:
#   P1  the zeros are spaced pi/k: k(t_{n+1}-t_n)/pi -> 1, to within 25%.  If not, the
#       diagnosis is wrong and nothing built on it counts.
#   P0  the instrument is well defined: 2|G_k| - 1 must be NEGATIVE at t = 0, or "the
#       smallest t where it reaches 1" does not exist and t* is not a quantity.
#       *** This clause was added after the first run printed "not found" -- recorded as
#       added late, because a pre-registration edited after seeing data is not a
#       pre-registration and saying so is the only thing that keeps the label honest. ***
#   Populations printed; a verdict over an empty population is a FAIL (F60).
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


mp.dps = 30


def w_power(k, s):
    s = mpf(s)
    return [mpf(1) / mpf(j + 1) ** s for j in range(k)]


def w_const(k):
    return [mpf(0)] + [mpf(1) / 2] * (k - 1)


def ReG(w, t):
    rho, th = sqrt(1 + 4 * t * t), atan(2 * t)
    a = mpf(0)
    for j, wj in enumerate(w):
        if wj != 0:
            a += wj * rho ** j * cos(j * th)
    return a


def absG(w, t):
    rho, th = sqrt(1 + 4 * t * t), atan(2 * t)
    re = im = mpf(0)
    for j, wj in enumerate(w):
        if wj != 0:
            re += wj * rho ** j * cos(j * th)
            im += wj * rho ** j * sin(j * th)
    return sqrt(re * re + im * im)


def zeros_of_F(w, t_hi, want=4, n_scan=2000):
    out = []
    f = lambda t: 1 + 2 * ReG(w, t)
    pt, pv = mpf(0), f(mpf(0))
    for i in range(1, n_scan + 1):
        t = mpf(t_hi) * i / n_scan
        v = f(t)
        if pv * v < 0:
            lo, hi = pt, t
            for _ in range(100):
                mid = (lo + hi) / 2
                if f(lo) * f(mid) <= 0:
                    hi = mid
                else:
                    lo = mid
            out.append((lo + hi) / 2)
            if len(out) >= want:
                return out
        pt, pv = t, v
    return out


say("=" * 92)
say("envelope_r206b -- a proposed cause for r206's wobble, and its refutation")
say("=" * 92)

verdicts = []

say()
say("--- INSTRUMENT: constant weights, zero set proved exactly (Thm 2(e), proved at r205) ---")
okI, nI = True, 0
for k in (128, 512):
    ref = tan(pi / k) / 2                    # reference computed INSIDE the block (r202)
    z = zeros_of_F(w_const(k), 4 * ref, want=1)
    nI += 1
    ok = bool(z) and abs(z[0] - ref) / ref < mpf(10) ** (-20)
    okI = okI and ok
    say("  k=%4d proved=%s measured=%s  %s"
        % (k, mp.nstr(ref, 18), mp.nstr(z[0], 18) if z else "none", "ok" if ok else "FAIL"))
verdicts.append(('instrument', okI and nI > 0))
say("  cases: %d -> %s" % (nI, "PASS" if okI and nI > 0 else "FAIL"))

say()
say("--- P1: are the zeros of F spaced pi/k?   k*(t_{n+1}-t_n)/pi, four zeros ---")
okP1, nP1 = True, 0
for ss in ('1', '2'):
    for k in (256, 1024):
        w = w_power(k, ss)
        pred = sqrt(mpf(ss) * log(k) / (2 * k))
        zs = zeros_of_F(w, 3 * pred, want=4)
        if len(zs) < 3:
            say("  s=%-4s k=%5d  only %d zeros in range" % (ss, k, len(zs)))
            continue
        gaps = [k * (zs[i + 1] - zs[i]) / pi for i in range(len(zs) - 1)]
        nP1 += 1
        bad = [g for g in gaps if abs(g - 1) >= mpf('0.25')]
        if bad:
            okP1 = False
        say("  s=%-4s k=%5d  gaps: %s   %s"
            % (ss, k, ", ".join(mp.nstr(g, 6) for g in gaps),
               "" if not bad else "<-- not 1"))
verdicts.append(('P1 spacing', okP1 and nP1 > 0))
say("  cases: %d -> %s" % (nP1, "PASS" if okP1 and nP1 > 0 else
                           "FAIL -- the ladder reading is wrong"))

say()
say("--- P0 (added after the first run; see the header): is t* even defined? ---")
say("    t* was to be the smallest t with 2|G_k| = 1, which needs 2|G_k(1)| - 1 < 0 at t = 0.")
say("  %6s %6s %20s" % ("s", "k", "2|G_k(1)| - 1  at t=0"))
okP0, nP0 = True, 0
for ss in ('1', '2', '4'):
    for k in (256, 1024):
        v = 2 * absG(w_power(k, ss), mpf(0)) - 1
        nP0 += 1
        if v > 0:
            okP0 = False
        say("  %6s %6d %20s %s" % (ss, k, mp.nstr(v, 10), "" if v < 0 else "<-- positive"))
verdicts.append(('P0 instrument defined', okP0 and nP0 > 0))
say("  cases: %d -> %s" % (nP0, "PASS" if okP0 and nP0 > 0 else
                           "FAIL -- |G_k| starts LARGE and t* does not exist"))

say()
say("=" * 92)
for tag, v in verdicts:
    say("  [%s] %s" % (tag, "PASS" if v else "FAIL"))
say()
say("WHAT THIS ROUND ESTABLISHES, which is not what it set out to establish:")
say("  1. The zeros of F are NOT a uniform ladder when the weights decay.  Gaps run")
say("     0.17-0.73 in units of pi/k, not 1.  The evenly spaced ladder theta_n = n pi/k")
say("     is a CONSTANT-WEIGHT phenomenon (Theorem 2(e)), not a general one -- and the")
say("     'doubled ladder' fingerprint must be stated with that scope in the note.")
say("  2. The proposed instrument t* does not exist: |G_k| is already far above the")
say("     threshold at t = 0 (it is essentially Gamma_k/2), so there is no first crossing")
say("     from below.  The zero is produced by the PHASE turning, not by the envelope")
say("     growing -- which also means the quantisation story was the wrong picture.")
say("  3. Therefore the s = 1 constant remains UNSETTLED, and the two shapes registered")
say("     at r206 stand as: shape B (lambda -> s-1/2) refuted; shape A (lambda -> s)")
say("     consistent but not monotone, |lambda-s| = 0.02 to 0.16 at the largest k.")
say()
say("done.")
sys.exit(0)
