#!/usr/bin/env python3
# scanres_r216b.py -- is the s = 1 non-monotonicity a property of the object, or of our scan?
#
# ---------------------------------------------------------------------------
# WHY THIS RUN EXISTS.  Every measured t_1 in this project, from rate_r200 through
# lambda_r206 to head_r216, comes from the SAME routine: evaluate F_k on 1500 points of
# [0, 3 t_pred] and bisect the first sign change.  That routine has a resolution --
# dt = 3 t_pred / 1500 -- and it has never been stated, let alone tested.
#
# It matters because of what it can do wrong.  Scanning can only MISS a zero, never
# invent one: if F dips below 0 and returns inside one step, the scan steps over it and
# reports a LATER zero as the first.  So every t_1 we have published is an UPPER BOUND
# on the true first zero at the stated resolution, and the lambda_eff table inherits it.
#
# And the suspicion is specific, not generic.  head_r216 produced a model whose s = 1
# column is SMOOTH and MONOTONE in k --
#       lam_v2 - s = -0.0248, -0.0804, -0.1219, -0.1469, -0.1649   at k = 64..1024
# -- while the measurement it is fitting is NOT:
#       lam_eff - s = +0.0671, +0.0489, +0.0525, -0.1409, -0.1275 .
# A smooth mechanism plus a jagged measurement is exactly the signature of a measurement
# artefact, and the artefact we have not excluded is the scan.
#
# THIS APPLIES THE RULE WE WROTE AT r211 TO OURSELVES AGAIN.  "A refutation needs a
# resolution claim."  The unsettled constant at s = 1 is reported on the strength of a
# sequence that does not settle.  A sequence that does not settle is evidence only if
# the instrument could have seen it settle.
#
# ---------------------------------------------------------------------------
# METHOD.  Two independent passes, as everywhere here.
#   PASS A (dense, float64):  evaluate F_k on N = 200000 points of [0, 3 t_pred] with
#     numpy.  Terms w_j rho^j cos(j theta) are O(1) at these sizes and the sum is O(1),
#     so the relative error is ~ k * 2^-53 ~ 1e-13 -- far below any effect at issue.
#     This pass LOCATES sign changes; it is not trusted to place them.
#   PASS B (mpmath, 30 digits):  every sign change PASS A reports earlier than the
#     published t_1 is re-confirmed and bisected at 30 digits.  A candidate that
#     PASS B cannot confirm is discarded and reported as discarded.
#
# ---------------------------------------------------------------------------
# PRE-REGISTERED, before the first number.
#
#   Q1  DOES THE PUBLISHED VALUE MOVE?  For each (k, s), does the dense scan find a
#       confirmed sign change strictly below the published t_1 (relative gap > 1e-9)?
#       - If NO for all 25 pairs: the 1500-point scan was adequate, the resolution is
#         stated for the first time and the lambda_eff table stands.
#       - If YES anywhere: every t_1 this project has published at that (k, s) is wrong
#         and so is the lambda_eff entry built on it.  Report it as such.
#
#   Q2  THE CONSEQUENCE, registered so it cannot be assembled afterwards.  If any s = 1
#       entry moves, recompute lam_eff on the corrected t_1 and ask whether the s = 1
#       column becomes MONOTONE in k.  If it does, the "non-monotone, therefore
#       unsettled" reading in the note's section 4.3 rests on an artefact and must be
#       restated -- and head_r216's v2 model was right where the measurement was wrong.
#       If it stays non-monotone, the non-monotonicity is a property of the object and
#       the note's reading survives a real test it had not yet had.
#
#   Q3  RESOLUTION, STATED WHATEVER HAPPENS.  Print dt = 3 t_pred / 1500 and the
#       narrowest confirmed sign-change interval found, for every pair.  The ratio is
#       the safety margin the old scans were running on without knowing it.
#
#   INSTRUMENT (runs first; abort on failure).  Constant weights, zero set proved exactly
#     at t = (1/2)tan(n pi/k) (Thm 2(e), r205).  BOTH passes must reproduce t_1: PASS A
#     to 1e-9 relative, PASS B to 1e-25.  Reference computed inside the precision block.
#
#   CROSS-INSTRUMENT.  PASS A and PASS B must agree on the constant-weight case to 1e-9,
#     which is what licenses PASS A to be used as a locator at all.
#
#   Populations printed.  An empty population is a FAIL (F60).
# ---------------------------------------------------------------------------

import io
import sys
import numpy as np
from mpmath import mp, mpf, sqrt, log, atan, cos, tan, pi

LOG = __file__[:-3] + ".log"
OUT = []


def say(s=""):
    print(s, flush=True)
    OUT.append(s)
    io.open(LOG, "w", encoding="utf-8", newline="\n").write("\n".join(OUT) + "\n")


mp.dps = 30

SS = ['1', '1.5', '2', '3', '4']
KS = [64, 128, 256, 512, 1024]
N_DENSE = 200000
N_OLD = 1500


# ------------------------------------------------------------------ float64 pass
def F_dense(w64, ts):
    """F_k(1/2+it) for an array of t, float64.  w64 is a numpy array of weights."""
    k = len(w64)
    j = np.arange(k)
    rho = np.sqrt(1.0 + 4.0 * ts * ts)
    th = np.arctan(2.0 * ts)
    out = np.empty_like(ts)
    # chunk over t to keep the (len(ts), k) array from exploding
    CH = 4000
    for a in range(0, len(ts), CH):
        b = min(a + CH, len(ts))
        L = np.log(rho[a:b])[:, None] * j[None, :]
        ph = th[a:b][:, None] * j[None, :]
        out[a:b] = 1.0 + 2.0 * (w64[None, :] * np.exp(L) * np.cos(ph)).sum(axis=1)
    return out


# ------------------------------------------------------------------ mpmath pass
def F_mp(w, t):
    rho, th = sqrt(1 + 4 * t * t), atan(2 * t)
    a = mpf(0)
    for jj, wj in enumerate(w):
        if wj != 0:
            a += wj * rho ** jj * cos(jj * th)
    return 1 + 2 * a


def bisect_mp(w, lo, hi, n=120):
    lo, hi = mpf(lo), mpf(hi)
    flo = F_mp(w, lo)
    if flo * F_mp(w, hi) > 0:
        return None
    for _ in range(n):
        m = (lo + hi) / 2
        if flo * F_mp(w, m) <= 0:
            hi = m
        else:
            lo, flo = m, F_mp(w, m)
    return (lo + hi) / 2


def first_zero_old(w, t_hi, n_scan=N_OLD):
    """the routine every previous run used, reproduced verbatim."""
    pt, pv = mpf(0), F_mp(w, mpf(0))
    for i in range(1, n_scan + 1):
        t = mpf(t_hi) * i / n_scan
        v = F_mp(w, t)
        if pv * v < 0:
            return bisect_mp(w, pt, t)
        pt, pv = t, v
    return None


def w_power(k, s):
    return [mpf(1) / mpf(j + 1) ** mpf(s) for j in range(k)]


def w_const(k):
    return [mpf(0)] + [mpf(1) / 2] * (k - 1)


say("=" * 100)
say("scanres_r216b -- is the s=1 non-monotonicity in the object, or in our 1500-point scan?")
say("PASS A: %d-point float64 locator.   PASS B: mpmath at %d digits, confirms and places."
    % (N_DENSE, mp.dps))
say("=" * 100)

verdicts = []

# ---------------------------------------------------------------- instrument
say()
say("--- INSTRUMENT: constant weights, zero set proved exactly (Thm 2(e), r205) ---")
okI = True
nI = 0
for k in (64, 256):
    ref = tan(pi / k) / 2                       # computed HERE, inside the precision block
    w = w_const(k)
    w64 = np.array([float(x) for x in w])
    ts = np.linspace(0.0, float(4 * ref), N_DENSE + 1)[1:]
    vals = F_dense(w64, ts)
    idx = np.where(np.sign(vals[:-1]) * np.sign(vals[1:]) < 0)[0]
    aA = float(ts[idx[0]]) if len(idx) else None
    bB = bisect_mp(w, ts[idx[0]], ts[idx[0] + 1]) if len(idx) else None
    relA = abs(mpf(aA) - ref) / ref if aA else mpf(1)
    relB = abs(bB - ref) / ref if bB else mpf(1)
    nI += 1
    if relA > mpf('1e-9') or relB > mpf(10) ** (-25):
        okI = False
    say("  k=%4d proved=%s" % (k, mp.nstr(ref, 20)))
    say("         PASS A rel=%s   PASS B rel=%s" % (mp.nstr(relA, 4), mp.nstr(relB, 4)))
say("  cases: %d -> %s" % (nI, "PASS" if okI and nI else "FAIL"))
verdicts.append(('instrument (both passes vs proved zero set)', okI and nI > 0))
if not okI:
    say("ABORTING: the locator is not licensed, so nothing below means anything.")
    sys.exit(1)

# ---------------------------------------------------------------- the run
say()
say("--- Q1/Q3: does a %d-point scan find a zero the %d-point scan stepped over? ---"
    % (N_DENSE, N_OLD))
say("  %5s %6s %16s %16s %12s %12s %10s"
    % ("s", "k", "t_1 published", "t_1 dense", "rel change", "dt(old)", "dip/dt"))

moved = []
rows = {}
n_pop = 0
for ss in SS:
    for k in KS:
        w = w_power(k, ss)
        w64 = np.array([float(x) for x in w])
        pred = sqrt(mpf(ss) * log(k) / (2 * k))
        t_hi = 3 * pred
        dt_old = t_hi / N_OLD

        t_pub = first_zero_old(w, t_hi)
        ts = np.linspace(0.0, float(t_hi), N_DENSE + 1)[1:]
        vals = F_dense(w64, ts)
        idx = np.where(np.sign(vals[:-1]) * np.sign(vals[1:]) < 0)[0]
        if t_pub is None or len(idx) == 0:
            say("  %5s %6d  not found (pub=%s dense=%d)" % (ss, k, t_pub is not None, len(idx)))
            continue
        t_den = bisect_mp(w, ts[idx[0]], ts[idx[0] + 1])
        if t_den is None:
            say("  %5s %6d  dense candidate NOT CONFIRMED by mpmath -- discarded" % (ss, k))
            continue
        # width of the confirmed negative excursion, in units of the old step
        i0 = idx[0]
        i1 = i0
        while i1 + 1 < len(vals) and vals[i1 + 1] < 0:
            i1 += 1
        dip = mpf(float(ts[min(i1 + 1, len(ts) - 1)] - ts[i0]))
        rel = (t_pub - t_den) / t_pub
        n_pop += 1
        rows[(ss, k)] = (t_pub, t_den, rel)
        if rel > mpf('1e-9'):
            moved.append((ss, k, t_pub, t_den, rel))
        say("  %5s %6d %16s %16s %12s %12s %10s"
            % (ss, k, mp.nstr(t_pub, 10), mp.nstr(t_den, 10), mp.nstr(rel, 4),
               mp.nstr(dt_old, 4), mp.nstr(dip / dt_old, 4)))
    say("")

say("  population: %d pairs;  entries that moved: %d" % (n_pop, len(moved)))
if n_pop == 0:
    say("EMPTY POPULATION -- FAIL.")
    sys.exit(1)

q1_clean = (len(moved) == 0)
verdicts.append(('Q1 published scan adequate', q1_clean))
say("  -> %s" % ("the 1500-point scan was adequate; the resolution is now stated"
                 if q1_clean else
                 "AT LEAST ONE PUBLISHED t_1 IS WRONG -- see below"))

# ---------------------------------------------------------------- Q2
say()
say("--- Q2: the consequence for the s=1 column (registered in advance) ---")
say("  %5s %6s %16s %16s" % ("s", "k", "lam_eff published", "lam_eff dense"))
mono = {}
for ss in SS:
    seq = []
    for k in KS:
        if (ss, k) not in rows:
            continue
        t_pub, t_den, rel = rows[(ss, k)]
        lp = 2 * k * t_pub * t_pub / log(k) - mpf(ss)
        ld = 2 * k * t_den * t_den / log(k) - mpf(ss)
        seq.append(ld)
        say("  %5s %6d %16s %16s" % (ss, k, mp.nstr(lp, 6), mp.nstr(ld, 6)))
    if len(seq) >= 3:
        dec = all(seq[i + 1] < seq[i] for i in range(len(seq) - 1))
        inc = all(seq[i + 1] > seq[i] for i in range(len(seq) - 1))
        mono[ss] = dec or inc
        say("        monotone in k after correction: %s" % ("YES" if mono[ss] else "no"))
    say("")

say()
say("=" * 100)
for tag, v in verdicts:
    say("  [%s] %s" % (tag, "PASS" if v else "FAIL"))
say()
if not q1_clean:
    say("MOVED ENTRIES -- every previously published t_1 at these (k,s) is an upper bound")
    say("that the denser scan has now beaten, and the lambda_eff entries built on them")
    say("are wrong by the amount shown:")
    for ss, k, a, b, r in moved:
        say("    s=%-4s k=%5d  %s -> %s   (%s)"
            % (ss, k, mp.nstr(a, 10), mp.nstr(b, 10), mp.nstr(r, 4)))
say()
say("interpretation belongs in the report, not here.")
say("done.")
sys.exit(0 if q1_clean else 1)
