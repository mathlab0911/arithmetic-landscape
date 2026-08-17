#!/usr/bin/env python3
# v3_r217b.py -- stop simplifying the model and solve it.
#
# ---------------------------------------------------------------------------
# WHAT r217 SHOWED, AND THE MISTAKE IT EXPOSED IN OUR OWN USE OF THE MODEL.
#
# The model is   Re G_k(1+2it)  ~  Hp(theta) + T sin(k theta),
#   Hp(theta) = sum_{j<k} w_j cos(j theta),   T = w_{k-1} rho^k/(2t),
# so a zero of F_k = 1 + 2 Re G_k is
#
#       (V3)      Hp(theta) + T sin(k theta)  =  -1/2 .
#
# r211 and r216 never solved that.  They solved the THRESHOLD condition T = Hp + 1/2,
# which is (V3) with sin(k theta) set to -1: the earliest t at which a zero becomes
# possible at all.  r217 then took the next step -- the first trough at or after that --
# and found every predicted value OVERSHOOTS (ratio 1.006 to 1.051, never below 1).
# That is the signature of the simplification: when T is comfortably above threshold the
# sine does not need to reach -1, so the zero arrives BEFORE the trough.
#
# So the honest move is not another correction term.  It is to solve the model we wrote
# down four rounds ago instead of a convenience version of it.
#
# ---------------------------------------------------------------------------
# WHAT THIS RUN CANNOT DO, STATED FIRST.
#
# Hp = sum_j w_j cos(j theta) is Re G_k with every rho^j replaced by 1.  The model then
# ADDS the tail's growth as a separate term, so the tail's rho = 1 contribution is
# counted twice.  For decaying weights that double count is O(w_k) = O(k^{-s}) and
# harmless.  FOR CONSTANT WEIGHTS IT IS NOT: there the exact identity (Theorem 2) reads
# F = A + w rho^k sin(k theta)/t with A = 1 + 2w_0 - 2w a CONSTANT, and the model's Hp
# is not A.  r217's M4 discovered this from the other end -- for constant weights the
# threshold equation has NO solution at all, and the run recorded a FAIL because the
# criterion had been written to expect a large error rather than an empty domain.
#
# THE DOMAIN IS THEREFORE PART OF THE CLAIM: this model is a decaying-weight model, and
# the constant-weight case is covered by a theorem instead, not by this.  Registered
# below as N3 in a form that can express "does not apply".
#
# ---------------------------------------------------------------------------
# PRE-REGISTERED, before the first number.  (s in {1,2,4}, 23 sizes, 69 points.)
#
#   N1  ACCURACY, worst case AND mean, against both earlier readings computed in this
#       same run so nothing is quoted:
#           t*      = threshold reading  (r211/r216)
#           t_tr    = first trough after t*  (r217)
#           t_v3    = first solution of (V3)
#       Require BOTH worst |t_v3/t_1 - 1| < worst for t* and for t_tr, AND the same for
#       the means.  Registered on both statistics because r216's P1 failed by using one
#       statistic for a targeted change (F91); here the change is not targeted, so a
#       worst case is admissible -- but the mean is registered beside it either way.
#
#   N2  THE SIGN OF THE ERROR.  r217's trough predictor overshot at 69 of 69 points.
#       If the overshoot was the simplification, v3's errors must lose that one-sidedness:
#       require the fraction of points with t_v3 < t_1 to lie in [0.2, 0.8].  A predictor
#       that is still one-sided has a systematic term left in it, whatever its size.
#
#   N3  DOMAIN, in a form that can say "does not apply".  Run (V3) on constant weights,
#       where Theorem 2 gives the answer exactly.  Three outcomes, all reportable:
#         (a) no solution           -> the model has no domain there; consistent with
#                                      r217's M4 and with the double-count argument above
#         (b) solution, error > 5%  -> the model applies and is wrong there
#         (c) solution, error < 5%  -> the model applies and is RIGHT there, which would
#                                      contradict the double-count argument and would be
#                                      the interesting outcome
#       No verdict is attached; the outcome is recorded and named.
#
#   N4  DOES THE QUANTUM SURVIVE?  If v3 is a genuine predictor then the r216d residual
#       should largely GO AWAY: require worst |lambda_v3 - lambda_eff| to be smaller than
#       the r216d quantum D = 4 pi t_1/log k at >= 90% of points -- the same bound, now
#       applied to a much smaller residual.  This is the check that v3 has not simply
#       absorbed the quantum into a fit: nothing here is fitted, so if the residual
#       collapses, the quantum WAS the simplification and not a separate effect.
#
#   INSTRUMENT (first; abort).  Constant weights, zero set proved exactly (Thm 2(e)),
#     reference inside the precision block, scan range a non-round multiple (F89).
#
#   Populations printed.  Empty population = FAIL (F60).
# ---------------------------------------------------------------------------

import io
import sys
import numpy as np
from mpmath import mp, mpf, sqrt, log, atan, cos, tan, pi, floor

LOG = __file__[:-3] + ".log"
OUT = []


def say(s=""):
    print(s, flush=True)
    OUT.append(s)
    io.open(LOG, "w", encoding="utf-8", newline="\n").write("\n".join(OUT) + "\n")


mp.dps = 30
N_DENSE = 10000   # r216b measured the old 1500-point scan safety margin at >= 1.88
                  # steps; 10000 carries >= 12 steps.  Stated, not assumed.
KGRID = [64, 76, 90, 107, 128, 152, 181, 215, 256, 304, 362, 431, 512,
         609, 724, 861, 1024, 1150, 1290, 1448, 1625, 1824, 2048]
SS = ['1', '2', '4']


def w_power(k, s):
    return [mpf(1) / mpf(j + 1) ** mpf(s) for j in range(k)]


def F_dense(w64, ts):
    k = len(w64)
    j = np.arange(k)
    rho = np.sqrt(1.0 + 4.0 * ts * ts)
    th = np.arctan(2.0 * ts)
    out = np.empty_like(ts)
    for a in range(0, len(ts), 3000):
        b = min(a + 3000, len(ts))
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
    lo, hi = mpf(lo), mpf(hi)
    flo = F_mp(w, lo)
    if flo * F_mp(w, hi) > 0:
        if widen is None:
            return None
        lo, hi = lo - mpf(widen), hi + mpf(widen)
        if lo <= 0:
            lo = hi / 10 ** 6
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
    return bisect_mp(w, ts[idx[0]], ts[idx[0] + 1], widen=float(ts[1] - ts[0]))


# ---------------------------------------------------------------- the three readings
def _model_parts(w64, k, ts):
    """returns (Hp, T, k*theta) on a float64 grid of t."""
    j = np.arange(k)
    rho = np.sqrt(1.0 + 4.0 * ts * ts)
    th = np.arctan(2.0 * ts)
    T = w64[-1] * np.exp(k * np.log(rho)) / (2.0 * ts)
    Hp = np.empty_like(ts)
    for a in range(0, len(ts), 3000):
        b = min(a + 3000, len(ts))
        Hp[a:b] = (w64[None, :] * np.cos(th[a:b][:, None] * j[None, :])).sum(axis=1)
    return Hp, T, k * th


def t_threshold(w64, k):
    """r211/r216: first t with T = Hp + 1/2  (i.e. (V3) with sin set to -1)."""
    ts = np.linspace(1e-9, 0.9, 4000)
    Hp, T, _ = _model_parts(w64, k, ts)
    g = T - (Hp + 0.5)
    i = int(np.argmin(g))
    if g[i] > 0:
        return None
    lo, hi = float(ts[i]), 0.9

    def gg(t):
        a, b, _ = _model_parts(w64, k, np.array([t]))
        return b[0] - (a[0] + 0.5)
    if gg(lo) * gg(hi) > 0:
        return None
    for _ in range(80):
        m = 0.5 * (lo + hi)
        if gg(lo) * gg(m) <= 0:
            hi = m
        else:
            lo = m
    return mpf(float(0.5 * (lo + hi)))


def t_trough(tstar, k):
    """r217: first trough t = (1/2)tan((3pi/2+2 pi n)/k) at or after tstar."""
    if tstar is None:
        return None
    th = atan(2 * tstar)
    n = max(0, int(floor((k * th - 3 * pi / 2) / (2 * pi))) + 1)
    for _ in range(4):
        thn = (3 * pi / 2 + 2 * pi * n) / k
        if thn >= pi / 2:
            return None
        t = tan(thn) / 2
        if t >= tstar:
            return t
        n += 1
    return None


def t_v3(w64, k, t_hi):
    """SOLVE THE MODEL: first t > 0 with Hp(theta) + T sin(k theta) = -1/2."""
    # 8000 points over [0, 3 t_pred]: the model's sine has period pi/k in t, which is
    # ~78 periods at k=2048, so this is ~100 samples per period.  Stated because an
    # unstated scan resolution is exactly what r216b had to go back and measure.
    ts = np.linspace(1e-9, float(t_hi), 8000)
    Hp, T, kth = _model_parts(w64, k, ts)
    v = Hp + T * np.sin(kth) + 0.5
    idx = np.where(np.sign(v[:-1]) * np.sign(v[1:]) < 0)[0]
    if len(idx) == 0:
        return None
    i = idx[0]

    def f(t):
        a, b, c = _model_parts(w64, k, np.array([t]))
        return a[0] + b[0] * np.sin(c[0]) + 0.5
    lo, hi = float(ts[i]), float(ts[i + 1])
    if f(lo) * f(hi) > 0:
        return None
    for _ in range(80):
        m = 0.5 * (lo + hi)
        if f(lo) * f(m) <= 0:
            hi = m
        else:
            lo = m
    return mpf(float(0.5 * (lo + hi)))


say("=" * 100)
say("v3_r217b -- solve the model instead of simplifying it:  Hp + T sin(k theta) = -1/2")
say("compared against the threshold reading (r211/r216) and the trough reading (r217),")
say("both recomputed here.  Nothing fitted anywhere.")
say("=" * 100)

verdicts = []

say()
say("--- INSTRUMENT: constant weights, zero set proved exactly (Thm 2(e), r205) ---")
okI, nI = True, 0
for k in (64, 256, 1024):
    ref = tan(pi / k) / 2
    w = [mpf(0)] + [mpf(1) / 2] * (k - 1)
    got = first_zero(w, mpf('4.13') * ref)
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
say("--- the three readings of one model, against the measurement ---")
say("  %5s %6s %13s %10s %10s %10s"
    % ("s", "k", "t_1", "thr/t_1", "trough/t1", "v3/t_1"))
pts = []
for ss in SS:
    for k in KGRID:
        w = w_power(k, ss)
        w64 = np.array([float(x) for x in w])
        pred = sqrt(mpf(ss) * log(k) / (2 * k))
        t1 = first_zero(w, 3 * pred)
        if t1 is None:
            say("  %5s %6d  measurement not found" % (ss, k))
            continue
        ta = t_threshold(w64, k)
        tb = t_trough(ta, k)
        tc = t_v3(w64, k, 3 * pred)
        if ta is None or tb is None or tc is None:
            say("  %5s %6d  a reading is undefined (thr=%s trough=%s v3=%s)"
                % (ss, k, ta is not None, tb is not None, tc is not None))
            continue
        pts.append((ss, k, t1, ta / t1, tb / t1, tc / t1))
        say("  %5s %6d %13s %10s %10s %10s"
            % (ss, k, mp.nstr(t1, 9), mp.nstr(ta / t1, 6),
               mp.nstr(tb / t1, 6), mp.nstr(tc / t1, 6)))
    say("")

n = len(pts)
say("  population: %d points" % n)
if n == 0:
    say("EMPTY POPULATION -- FAIL.")
    sys.exit(1)


def stats(i):
    e = [abs(p[i] - 1) for p in pts]
    return max(e), sum(e) / len(e)


wa, ma = stats(3)
wb, mb = stats(4)
wc, mc = stats(5)

say()
say("--- N1  accuracy ---")
say("  %28s %14s %14s" % ("reading", "worst |.-1|", "mean |.-1|"))
say("  %28s %14s %14s" % ("threshold  (r211/r216)", mp.nstr(wa, 6), mp.nstr(ma, 6)))
say("  %28s %14s %14s" % ("first trough after it (r217)", mp.nstr(wb, 6), mp.nstr(mb, 6)))
say("  %28s %14s %14s" % ("SOLVE THE MODEL (v3)", mp.nstr(wc, 6), mp.nstr(mc, 6)))
n1 = wc < wa and wc < wb and mc < ma and mc < mb
say("  -> %s" % ("PASS" if n1 else "FAIL"))
verdicts.append(('N1 v3 best on both statistics', n1))

say()
say("--- N2  one-sidedness: the trough reading overshot everywhere; does v3? ---")
below_b = sum(1 for p in pts if p[4] < 1)
below_c = sum(1 for p in pts if p[5] < 1)
say("  trough reading below the measurement at %d of %d" % (below_b, n))
say("  v3       reading below the measurement at %d of %d" % (below_c, n))
frac = mpf(below_c) / n
n2 = mpf('0.2') <= frac <= mpf('0.8')
say("  fraction = %s  -> %s" % (mp.nstr(frac, 4), "PASS" if n2 else
                                "FAIL -- a systematic term is still in there"))
verdicts.append(('N2 v3 not one-sided', n2))

say()
say("--- N3  DOMAIN: run v3 where Theorem 2 gives the answer (constant weights) ---")
for k in (64, 256, 1024):
    ref = tan(pi / k) / 2
    w64 = np.array([0.0] + [0.5] * (k - 1))
    tc = t_v3(w64, k, float(4 * ref))
    if tc is None:
        say("  k=%5d  outcome (a): NO SOLUTION -- the model has no domain here" % k)
    else:
        rel = abs(tc - ref) / ref
        tag = "(b) applies and is wrong" if rel > mpf('0.05') else "(c) applies and is RIGHT"
        say("  k=%5d  outcome %s: v3=%s proved=%s rel=%s"
            % (k, tag, mp.nstr(tc, 12), mp.nstr(ref, 12), mp.nstr(rel, 5)))
say("  (no verdict attached; the outcome is the finding)")

say()
say("--- N4  does the r216d quantum survive, or WAS it the simplification? ---")
inside = 0
worst_rel = mpf(0)
for ss, k, t1, ra, rb, rc in pts:
    lam_e = 2 * k * t1 * t1 / log(k)
    tc = rc * t1
    lam_3 = 2 * k * tc * tc / log(k)
    D = 4 * pi * t1 / log(k)
    if abs(lam_3 - lam_e) <= D:
        inside += 1
    worst_rel = max(worst_rel, abs(lam_3 - lam_e) / D)
say("  |lambda_v3 - lambda_eff| <= D at %d of %d = %s"
    % (inside, n, mp.nstr(mpf(inside) / n, 4)))
say("  worst ratio |lambda_v3 - lambda_eff| / D = %s" % mp.nstr(worst_rel, 5))
n4 = mpf(inside) / n >= mpf('0.9')
say("  -> %s" % ("PASS" if n4 else "FAIL"))
verdicts.append(('N4 residual within the quantum', n4))

say()
say("=" * 100)
for tag, v in verdicts:
    say("  [%s] %s" % (tag, "PASS" if v else "FAIL"))
say()
say("interpretation belongs in the report, not here.")
say("done.")
sys.exit(0 if all(v for _, v in verdicts) else 1)
