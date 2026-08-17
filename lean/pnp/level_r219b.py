#!/usr/bin/env python3
# level_r219b.py -- N2's leftover, measured instead of argued.
#
# ---------------------------------------------------------------------------
# WHAT IS OWED.  r217b registered N2 (the sign of the error) and it FAILED: v3 sits
# below the measurement at 66 of 69 points, mean 3e-4.  fable-5's r218 section 3 names a
# candidate -- v3 sets every rho^j in the head to 1, and restoring
#
#         Omega(t) := 2 sum_{j<k} w_j (rho^j - 1) cos(j theta)
#
# raises the level (weights concentrated at small j, where cos > 0) and delays the
# crossing, which is the observed sign -- and calls it "candidate, not claim".
#
# fable's rule from section 2 is: TO TEST THE LEVEL, EVALUATE THE MODEL AT A KNOWN POINT,
# DO NOT ASK ITS ROOT.  For decaying weights there is no theorem giving a known point.
# But there is something better and it costs nothing: t_1 ITSELF is a point where the
# exact answer is known, because F(t_1) = 0 by construction.  So
#
#         L := F_model(t_1)          IS the level error at the true zero, signed,
#
# and the candidate is testable without any asymptotics: if the omitted head growth is
# what is missing, then Omega(t_1) should CANCEL L.
#
# ---------------------------------------------------------------------------
# PRE-REGISTERED, before the first number.  (s in {1,2,4}, k in {256,512,1024,2048}.)
#
#   L1  THE SIGN.  N2 says the model's root is EARLY, so the model must already be
#       negative at t_1: require L < 0 at every point.  If L > 0 anywhere then the
#       one-sidedness in N2 does not come from the level at all and fable's candidate is
#       addressing the wrong quantity.
#
#   L2  THE CANDIDATE.  Require |L + Omega| < 0.25 |L| at every point -- i.e. restoring
#       the head's growth accounts for at least three quarters of the level error.
#       FAIL -> the head's growth is not the missing term, or not the only one.
#
#   L3  THE CONSEQUENCE, registered so it is not assembled afterwards.  If L2 passes,
#       predict the corrected root by t_1 ~ t_v3 + (L + Omega ... ) is NOT what is done
#       here -- instead simply report the implied root shift L/|dF_model/dt| at t_1 and
#       compare it with the measured shift t_1 - t_v3.  Require agreement within 25%.
#       This is the check that L is being converted into a root correctly, and it is the
#       step where a slope is involved -- so it is separated from L2 on purpose, because
#       r218 section 2 is precisely a case of a slope silently doing the work.
#
#   L4  A CONTROL THAT MUST FAIL.  Apply the same decomposition on CONSTANT weights,
#       where r219 established that the level error is exactly 1 and the head is a
#       Dirichlet kernel.  There Omega should NOT cancel L, because the level error there
#       is the double count, not the head's growth.  Require |L + Omega| > 0.25|L|.
#       A correction that "explains" both cases explains neither.
#
#   INSTRUMENT (first; abort).  Constant weights, first zero proved exactly (Thm 2(e)),
#     reference inside the precision block.  And: F_model + Omega must equal F_exact
#     up to the tail approximation only -- checked by requiring that at t_1,
#     |F_model + Omega - (the exact F, which is 0)| is SMALLER than |L|, i.e. that
#     adding Omega moves toward the truth rather than merely moving.
#
#   Populations printed.  Empty population = FAIL (F60).
# ---------------------------------------------------------------------------

import io
import sys
import numpy as np
from mpmath import mp, mpf, sqrt, log, atan, cos, sin, tan, pi

LOG = __file__[:-3] + ".log"
OUT = []


def say(s=""):
    print(s, flush=True)
    OUT.append(s)
    io.open(LOG, "w", encoding="utf-8", newline="\n").write("\n".join(OUT) + "\n")


mp.dps = 40
SS = ['1', '2', '4']
KS = [256, 512, 1024, 2048]


def w_power(k, s):
    return [mpf(1) / mpf(j + 1) ** mpf(s) for j in range(k)]


def w_const(k):
    return [mpf(0)] + [mpf(1) / 2] * (k - 1)


def parts(w, k, t):
    """returns (Hp, T, k*theta, Omega) at t, all at 40 digits."""
    rho, th = sqrt(1 + 4 * t * t), atan(2 * t)
    Hp = mpf(0)
    Om = mpf(0)
    for j, wj in enumerate(w):
        if wj == 0:
            continue
        c = cos(j * th)
        Hp += wj * c
        Om += wj * (rho ** j - 1) * c
    T = w[-1] * rho ** k / (2 * t)
    return Hp, T, k * th, 2 * Om


def F_exact(w, t):
    rho, th = sqrt(1 + 4 * t * t), atan(2 * t)
    a = mpf(0)
    for j, wj in enumerate(w):
        if wj != 0:
            a += wj * rho ** j * cos(j * th)
    return 1 + 2 * a


def F_model(w, k, t):
    Hp, T, kth, _ = parts(w, k, t)
    return 1 + 2 * Hp + 2 * T * sin(kth)


def first_zero_exact(w, t_hi, n=40000):
    """dense scan then bisect, at 40 digits via float64 location."""
    w64 = np.array([float(x) for x in w])
    kk = len(w64)
    j = np.arange(kk)
    ts = np.linspace(0.0, float(t_hi), n + 1)[1:]
    rho = np.sqrt(1.0 + 4.0 * ts * ts)
    th = np.arctan(2.0 * ts)
    out = np.empty_like(ts)
    for a in range(0, len(ts), 3000):
        b = min(a + 3000, len(ts))
        L = np.log(rho[a:b])[:, None] * j[None, :]
        ph = th[a:b][:, None] * j[None, :]
        out[a:b] = 1.0 + 2.0 * (w64[None, :] * np.exp(L) * np.cos(ph)).sum(axis=1)
    idx = np.where(np.sign(out[:-1]) * np.sign(out[1:]) < 0)[0]
    if len(idx) == 0:
        return None
    lo, hi = mpf(float(ts[idx[0]])), mpf(float(ts[idx[0] + 1]))
    flo = F_exact(w, lo)
    if flo * F_exact(w, hi) > 0:
        return None
    for _ in range(160):
        m = (lo + hi) / 2
        if flo * F_exact(w, m) <= 0:
            hi = m
        else:
            lo, flo = m, F_exact(w, m)
    return (lo + hi) / 2


def v3_root(w, k, lo, hi):
    a, b = mpf(lo), mpf(hi)
    fa = F_model(w, k, a)
    if fa * F_model(w, k, b) > 0:
        return None
    for _ in range(160):
        m = (a + b) / 2
        if fa * F_model(w, k, m) <= 0:
            b = m
        else:
            a, fa = m, F_model(w, k, m)
    return (a + b) / 2


say("=" * 100)
say("level_r219b -- N2's leftover: measure the model's LEVEL at the true zero")
say("L := F_model(t_1).  Since F_exact(t_1) = 0 by construction, L IS the level error,")
say("signed, at a point where the answer is known without any theorem.")
say("=" * 100)

verdicts = []

say()
say("--- INSTRUMENT: constant weights, first zero proved exactly (Thm 2(e), r205) ---")
okI, nI = True, 0
for k in (256, 1024):
    ref = tan(pi / k) / 2
    got = first_zero_exact(w_const(k), mpf('4.13') * ref)     # non-round multiple (F89)
    rel = abs(got - ref) / ref if got else mpf(1)
    nI += 1
    if rel > mpf(10) ** (-25):
        okI = False
    say("  k=%5d proved=%s got=%s rel=%s"
        % (k, mp.nstr(ref, 18), mp.nstr(got, 18) if got else "none", mp.nstr(rel, 4)))
say("  cases: %d -> %s" % (nI, "PASS" if okI and nI else "FAIL"))
verdicts.append(('instrument', okI and nI > 0))
if not okI:
    sys.exit(1)

say()
say("--- L1/L2: the level at the true zero, and whether the head's growth cancels it ---")
say("  %5s %6s %16s %16s %16s %10s"
    % ("s", "k", "L = F_model(t1)", "Omega", "L + Omega", "|L+Om|/|L|"))
pts = []
for ss in SS:
    for k in KS:
        w = w_power(k, ss)
        pred = sqrt(mpf(ss) * log(k) / (2 * k))
        t1 = first_zero_exact(w, 3 * pred)
        if t1 is None:
            say("  %5s %6d  no zero" % (ss, k))
            continue
        Hp, T, kth, Om = parts(w, k, t1)
        L = 1 + 2 * Hp + 2 * T * sin(kth)
        r = abs(L + Om) / abs(L)
        pts.append((ss, k, t1, L, Om, r))
        say("  %5s %6d %16s %16s %16s %10s"
            % (ss, k, mp.nstr(L, 8), mp.nstr(Om, 8), mp.nstr(L + Om, 8), mp.nstr(r, 5)))
    say("")

n = len(pts)
say("  population: %d points" % n)
if n == 0:
    say("EMPTY POPULATION -- FAIL.")
    sys.exit(1)

neg = sum(1 for p in pts if p[3] < 0)
l1 = neg == n
say()
say("--- L1  sign: the model must already be negative at t_1 (its root is early) ---")
say("  L < 0 at %d of %d  -> %s" % (neg, n, "PASS" if l1 else "FAIL"))
verdicts.append(('L1 sign of the level error', l1))

worst = max(p[5] for p in pts)
l2 = worst < mpf('0.25')
say()
say("--- L2  candidate: does the head's growth account for >= 3/4 of it? ---")
say("  worst |L+Omega|/|L| = %s  -> %s" % (mp.nstr(worst, 5), "PASS" if l2 else "FAIL"))
verdicts.append(('L2 head growth is the missing term', l2))

# ---------------------------------------------------------------- L3
say()
say("--- L3  converting the level into a root shift (the step where a slope acts) ---")
say("  %5s %6s %16s %16s %10s" % ("s", "k", "L/|dF/dt| at t1", "t1 - t_v3", "ratio"))
okL3, nL3 = True, 0
for ss, k, t1, L, Om, r in pts:
    h = t1 * mpf(10) ** -10
    d = (F_model(w_power(k, ss), k, t1 + h) - F_model(w_power(k, ss), k, t1 - h)) / (2 * h)
    shift_pred = -L / d
    w = w_power(k, ss)
    tv = v3_root(w, k, t1 * mpf('0.5'), t1 * mpf('1.02'))
    if tv is None:
        say("  %5s %6d  v3 root not bracketed" % (ss, k))
        continue
    shift_meas = t1 - tv
    ratio = shift_pred / shift_meas if shift_meas != 0 else mpf(0)
    nL3 += 1
    if abs(ratio - 1) > mpf('0.25'):
        okL3 = False
    say("  %5s %6d %16s %16s %10s"
        % (ss, k, mp.nstr(shift_pred, 8), mp.nstr(shift_meas, 8), mp.nstr(ratio, 6)))
say("  cases: %d -> %s" % (nL3, "PASS" if okL3 and nL3 else "FAIL"))
verdicts.append(('L3 level converts to the observed shift', okL3 and nL3 > 0))

# ---------------------------------------------------------------- L4
say()
say("--- L4  CONTROL: on constant weights the same correction must NOT explain it ---")
say("  (there the level error is the double count, established at r219, not head growth)")
okL4, nL4 = True, 0
for k in (256, 1024):
    w = w_const(k)
    t1 = tan(pi / k) / 2
    Hp, T, kth, Om = parts(w, k, t1)
    L = 1 + 2 * Hp + 2 * T * sin(kth)
    r = abs(L + Om) / abs(L)
    nL4 += 1
    if r <= mpf('0.25'):
        okL4 = False
    say("  k=%5d  L=%s  Omega=%s  |L+Om|/|L|=%s"
        % (k, mp.nstr(L, 8), mp.nstr(Om, 8), mp.nstr(r, 5)))
say("  -> %s" % ("PASS: the correction is specific to the decaying case"
                 if okL4 and nL4 else
                 "FAIL: it 'explains' both cases, so it explains neither"))
verdicts.append(('L4 control: correction is case-specific', okL4 and nL4 > 0))

say()
say("=" * 100)
for tag, v in verdicts:
    say("  [%s] %s" % (tag, "PASS" if v else "FAIL"))
say()
say("interpretation belongs in the report, not here.")
say("done.")
sys.exit(0 if all(v for _, v in verdicts) else 1)
