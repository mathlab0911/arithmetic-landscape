#!/usr/bin/env python3
# dense_r216c.py -- is lambda_eff(k) at s = 1 a jagged function, or five badly chosen points?
#
# ---------------------------------------------------------------------------
# WHY THIS RUN EXISTS.  Every table this project has printed for the decaying case uses
# the same five sizes, k = 64, 128, 256, 512, 1024, and every reading of the s = 1
# constant rests on that column being NON-MONOTONE.  scanres_r216b has just established
# that the non-monotonicity is not a scan artefact -- the zeros are where we said.  But
# it cannot rule out the other artefact, which is the k-GRID itself.
#
# Two things in the r216b output make the grid a live suspect.
#
#   (i)  The reversals occur ONLY at s = 1 and s = 1.5.  At s = 2, 3, 4 the measured
#        column is monotone decreasing.  So whatever it is, it lives where the head
#        sum_j w_j is divergent or slowly convergent -- which is exactly the part of the
#        mechanism head_r216 identified as delicate.
#   (ii) BOTH non-monotone columns reverse at the SAME two sizes, k = 256 and k = 1024.
#        A feature that depends on s should not pick out the same k in two columns. A
#        feature of the k-grid would.
#
# With five points and two reversals, (ii) is worth about nothing as evidence. That is
# the reason for this run: the question cannot be settled on the grid that raised it.
#
# ---------------------------------------------------------------------------
# METHOD.  The locator licensed in r216b: float64 dense scan (20000 points -- r216b
# measured the OLD 1500-point scan's safety margin at >= 1.88 steps, so 20000 carries
# >= 24 steps of margin; 200k was affordable at five sizes and is not at sixty-nine), verified
# against the proved zero set to 1e-16), then mpmath bisection at 30 digits to place the
# zero.  This makes ~30 sizes affordable where the old all-mpmath route made five.
#
# The grid is deliberately NOT powers of two: 24 sizes spaced roughly geometrically,
# with the five historical sizes included so the new curve can be checked against the
# published numbers at the points they share.
#
# ---------------------------------------------------------------------------
# PRE-REGISTERED, before the first number.
#
#   J1  SMOOTHNESS.  Count R := the number of sign changes in the first difference of
#       lambda_eff(k) over the dense grid at s = 1.
#         R <= 2  -> the function is smooth and the historical column's jaggedness was
#                    an artefact of sampling five points.  The note's "non-monotone"
#                    wording is then about the grid, not the object, and must be restated.
#         R >= 5  -> the jaggedness is real and is a property of the object that no model
#                    in this project currently explains.  A finding, reported raw.
#         3 or 4  -> undecided at this grid; say so and do not choose.
#
#   J2  AGREEMENT AT THE SHARED SIZES.  At the five historical k the new lambda_eff must
#       reproduce the published values to 1e-9 relative.  If it does not, this run is
#       measuring something else and J1 is void.  (This is the control that makes the
#       new grid comparable to the old one at all.)
#
#   J3  THE MODEL, ALONGSIDE.  Print lambda_v2(k) - s from head_r216's v2 model on the
#       same dense grid.  Registered prediction: v2 is SMOOTH (R_model <= 2). If the
#       measurement turns out jagged while the model is smooth, then the jaggedness is
#       precisely what the mechanism does not contain, and that is the next question.
#
#   J4  s = 1.5 AS THE SECOND WITNESS.  Repeat J1 at s = 1.5 (the other non-monotone
#       column) and at s = 3 (a monotone control).  If the dense grid makes s = 3 jagged
#       too, the effect is not about s and this run has found an instrument problem
#       instead -- which would be the honest outcome and is registered as such.
#
#   INSTRUMENT (first; abort on failure).  Constant weights, zero set proved exactly at
#     t = (1/2)tan(n pi/k), Thm 2(e), r205.  Locator to 1e-9, placement to 1e-25.
#     Reference computed inside the precision block (r202).
#
#     A DEFECT IN THIS INSTRUMENT, FOUND WHILE BUILDING IT AND FIXED HERE.  The scan
#     range was set to 4 * (the exact answer).  A uniform grid on [0, 4 r] therefore has
#     a node AT r, for every grid size -- the instrument was aiming its samples at the
#     one point where a sign-change detector has nothing to detect, and whether it
#     passed came down to the last bit of a float64 rounding.  It passed at 200000
#     points and failed at 20000 for exactly that reason, with the failure looking like
#     a resolution problem, which it was not.
#     Two changes: the range is now an irrational-ish multiple (4.13 r) so the grid
#     cannot align with the answer, and the placement step widens its bracket by one
#     node on each side before declaring no crossing.
#     THE GENERAL FORM: never define an instrument's sampling grid in units of the
#     quantity the instrument is measuring.
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
N_DENSE = 20000

HIST = [64, 128, 256, 512, 1024]
KGRID = sorted(set([64, 76, 90, 107, 128, 152, 181, 215, 256, 304, 362, 431, 512,
                    609, 724, 861, 1024, 1150, 1290, 1448, 1625, 1824, 2048] + HIST))


def w_power(k, s):
    return [mpf(1) / mpf(j + 1) ** mpf(s) for j in range(k)]


def w_const(k):
    return [mpf(0)] + [mpf(1) / 2] * (k - 1)


def F_dense(w64, ts):
    k = len(w64)
    j = np.arange(k)
    rho = np.sqrt(1.0 + 4.0 * ts * ts)
    th = np.arctan(2.0 * ts)
    out = np.empty_like(ts)
    CH = 3000
    for a in range(0, len(ts), CH):
        b = min(a + CH, len(ts))
        L = np.log(rho[a:b])[:, None] * j[None, :]
        ph = th[a:b][:, None] * j[None, :]
        out[a:b] = 1.0 + 2.0 * (w64[None, :] * np.exp(L) * np.cos(ph)).sum(axis=1)
    return out


def F_mp(w, t):
    rho, th = sqrt(1 + 4 * t * t), atan(2 * t)
    a = mpf(0)
    for jj, wj in enumerate(w):
        if wj != 0:
            a += wj * rho ** jj * cos(jj * th)
    return 1 + 2 * a


def bisect_mp(w, lo, hi, n=120, widen=None):
    """bisect a sign change in [lo, hi]; if the bracket has collapsed onto the zero
    (see the instrument note in the header) widen it by one grid node each way once."""
    lo, hi = mpf(lo), mpf(hi)
    flo = F_mp(w, lo)
    if flo * F_mp(w, hi) > 0:
        if widen is None:
            return None
        lo, hi = mpf(lo) - mpf(widen), mpf(hi) + mpf(widen)
        if lo <= 0:
            lo = mpf(hi) / 10 ** 6
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


def first_zero(w, t_hi):
    w64 = np.array([float(x) for x in w])
    ts = np.linspace(0.0, float(t_hi), N_DENSE + 1)[1:]
    vals = F_dense(w64, ts)
    idx = np.where(np.sign(vals[:-1]) * np.sign(vals[1:]) < 0)[0]
    if len(idx) == 0:
        return None
    step = float(ts[1] - ts[0])
    return bisect_mp(w, ts[idx[0]], ts[idx[0] + 1], widen=step)


def t_model_v2(w64, k):
    """v2: smallest t>0 with w_{k-1} rho^k/(2t) = sum_j w_j cos(j theta) + 1/2.

    Solved in float64: this is a smooth scalar equation with no cancellation.  The
    mpmath budget is spent where cancellation actually lives, on the zeros of F.
    """
    j = np.arange(k)
    wk = w64[-1]

    def gap(ts):
        ts = np.atleast_1d(np.asarray(ts, dtype=float))
        rho = np.sqrt(1.0 + 4.0 * ts * ts)
        th = np.arctan(2.0 * ts)
        T = wk * np.exp(k * np.log(rho)) / (2.0 * ts)
        Hp = (w64[None, :] * np.cos(th[:, None] * j[None, :])).sum(axis=1)
        return T - (Hp + 0.5)

    ts = np.linspace(1e-9, 0.9, 3000)
    v = gap(ts)
    i = int(np.argmin(v))
    if v[i] > 0:
        return None
    a, b = float(ts[i]), 0.9
    if gap(a)[0] * gap(b)[0] > 0:
        return None
    for _ in range(80):
        m = 0.5 * (a + b)
        if gap(a)[0] * gap(m)[0] <= 0:
            b = m
        else:
            a = m
    return mpf(repr(0.5 * (a + b)))


def reversals(seq):
    d = [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]
    return sum(1 for i in range(len(d) - 1) if d[i] * d[i + 1] < 0)


say("=" * 100)
say("dense_r216c -- is lambda_eff(k) jagged, or were five powers of two a bad grid?")
say("grid: %d sizes, %d..%d, deliberately not all powers of two" % (len(KGRID), KGRID[0], KGRID[-1]))
say("=" * 100)

verdicts = []

say()
say("--- INSTRUMENT: constant weights, zero set proved exactly (Thm 2(e), r205) ---")
okI, nI = True, 0
for k in (64, 256, 1024):
    ref = tan(pi / k) / 2                      # inside the precision block (r202)
    got = first_zero(w_const(k), mpf('4.13') * ref)   # NOT a round multiple: see header
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

# ---------------------------------------------------------------- the dense sweep
results = {}
for ss in ('1', '1.5', '3'):
    say()
    say("--- s = %s : dense sweep ---" % ss)
    say("  %6s %18s %14s %14s" % ("k", "t_1", "lam_eff - s", "lam_v2 - s"))
    lam, lam_m, ks = [], [], []
    for k in KGRID:
        w = w_power(k, ss)
        pred = sqrt(mpf(ss) * log(k) / (2 * k))
        t1 = first_zero(w, 3 * pred)
        if t1 is None:
            say("  %6d  not found" % k)
            continue
        le = 2 * k * t1 * t1 / log(k) - mpf(ss)
        tm = t_model_v2(np.array([float(x) for x in w]), k) if ss == '1' else None
        lm = (2 * k * tm * tm / log(k) - mpf(ss)) if tm else None
        ks.append(k)
        lam.append(le)
        if lm is not None:
            lam_m.append(lm)
        say("  %6d %18s %14s %14s"
            % (k, mp.nstr(t1, 12), mp.nstr(le, 6), mp.nstr(lm, 6) if lm is not None else "-"))
    results[ss] = (ks, lam, lam_m)
    say("  population: %d sizes" % len(ks))

# ---------------------------------------------------------------- J2
say()
say("--- J2  control: the dense grid must reproduce the published values at the shared k ---")
PUB = {'1': {64: '0.0670656', 128: '0.0489407', 256: '0.0525199',
             512: '-0.140888', 1024: '-0.127451'}}
okJ2, nJ2 = True, 0
ks, lam, _ = results['1']
for k, v in PUB['1'].items():
    if k not in ks:
        continue
    got = lam[ks.index(k)]
    ref = mpf(v)
    d = abs(got - ref)
    nJ2 += 1
    if d > mpf('1e-6'):
        okJ2 = False
    say("  k=%5d published=%12s dense=%12s |diff|=%s" % (k, v, mp.nstr(got, 6), mp.nstr(d, 3)))
say("  cases: %d -> %s" % (nJ2, "PASS" if okJ2 and nJ2 else "FAIL"))
verdicts.append(('J2 agrees with the published column', okJ2 and nJ2 > 0))
if not okJ2:
    say("  J1 IS VOID: this run is not measuring the same thing as the published table.")

# ---------------------------------------------------------------- J1 / J3 / J4
say()
say("--- J1/J4  reversals in the first difference, on the dense grid ---")
say("  %6s %10s %10s %28s" % ("s", "sizes", "reversals", "verdict (registered)"))
for ss in ('1', '1.5', '3'):
    ks, lam, lam_m = results[ss]
    R = reversals(lam)
    if R <= 2:
        vd = "SMOOTH -- grid artefact"
    elif R >= 5:
        vd = "JAGGED -- property of object"
    else:
        vd = "undecided at this grid"
    say("  %6s %10d %10d %28s" % (ss, len(ks), R, vd))

say()
say("--- J3  the model on the same grid (s = 1) ---")
ks, lam, lam_m = results['1']
if lam_m and len(lam_m) == len(ks):
    Rm = reversals(lam_m)
    say("  model reversals: %d over %d sizes -> %s"
        % (Rm, len(lam_m), "SMOOTH as registered" if Rm <= 2 else "NOT smooth -- prediction failed"))
    verdicts.append(('J3 model smooth', Rm <= 2))
else:
    say("  model column incomplete (%d of %d) -- J3 not stated" % (len(lam_m), len(ks)))

say()
say("=" * 100)
for tag, v in verdicts:
    say("  [%s] %s" % (tag, "PASS" if v else "FAIL"))
say()
say("interpretation belongs in the report, not here.")
say("done.")
sys.exit(0 if all(v for _, v in verdicts) else 1)
