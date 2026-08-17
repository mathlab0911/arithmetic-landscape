#!/usr/bin/env python3
# trough_r217.py -- the loose thread from r216d, pulled: is the first zero simply the
# FIRST TROUGH after the model's continuous crossing?
#
# ---------------------------------------------------------------------------
# THE THREAD.  r216d established that the residual R = lambda_eff - lambda_v2 is bounded
# by the quantum D = 4 pi t_1/log k at 69 of 69 points, with nothing fitted.  But its
# shape statistic DRIFTED: std(R/D) came out 0.332, 0.244, 0.222, 0.218 across four k
# bands, against 1/sqrt(12) = 0.2887 for a phase landing uniformly.  Inside the
# registered band, and not flat.  A drifting shape statistic means the residual is not
# the thing I said it was, only close to it.
#
# ---------------------------------------------------------------------------
# THE SHARPER PICTURE, DERIVED ON PAPER BEFORE THIS RUN.
#
# v2 says Re G_k ~ Hp(theta) + T sin(k theta), so F_k = 0 needs
#
#         T sin(k theta) = -(Hp + 1/2) ,
#
# which is EASIEST at a trough of the sine, k theta = 3 pi/2 + 2 pi n.  Let t* be the
# continuous solution of T = Hp + 1/2 -- that is exactly the v2 model, the point at
# which a trough would first do the job.  Then the actual first zero should be
#
#         t_1  ~  the first TROUGH at or after t* ,
#
# and troughs sit at t = (1/2) tan( (3 pi/2 + 2 pi n)/k ), spacing pi/k in t.  So the
# residual is not "a phase" -- it is the DISTANCE FROM t* TO THE NEXT TROUGH, which is a
# computable number, not a random one.
#
# WHY THE SHAPE STATISTIC DRIFTS, on this picture.  T multiplies by g := e^{4 pi t_1}
# across one period.  When g is large the sine does not need to reach -1: the condition
# is met before the trough, and even in the previous period, so the zero smears EARLY
# and the spread is wide.  When g -> 1 the zero is pinned to the trough itself.
# Measured: g = 10.4 at k = 64 and 1.64 at k = 2048.  Wide spread at small k, narrow at
# large k -- which is the drift, with its sign.
#
# IF THIS IS RIGHT IT IS NOT A RESIDUAL BUT A FORMULA: t_1 = first trough after t*.
#
# ---------------------------------------------------------------------------
# PRE-REGISTERED, before the first number.  (s in {1,2,4}, 23 sizes, 69 points.)
#
#   M1  ARE THE ZEROS ON THE TROUGH GRID AT ALL?  Let psi := frac( k theta_1/(2 pi) - 3/4 )
#       and dev := |psi - round(psi)|, the distance to the nearest trough in units of the
#       period.  A zero unrelated to the grid gives dev uniform on [0, 1/2], mean 0.25.
#       REQUIRE mean(dev) < 0.25 over the population, AND < 0.15 in the largest-k band.
#       FAIL -> the trough picture is wrong and r216d's quantum is a coincidence of
#       magnitude rather than a mechanism.  That would be the important outcome.
#
#   M2  THE DRIFT MUST BE EXPLAINED BY g.  Registered: dev decreases as g decreases.
#       Require mean(dev) in the largest-k band to be strictly smaller than in the
#       smallest-k band, and the Spearman-style concordance between dev and g over the
#       whole population to exceed 0.5.  FAIL -> the drift in r216d has some other cause
#       and this run has not found it.
#
#   M3  THE PAYOFF: A FORMULA, NOT A BOUND.  Define t_trough := the smallest trough
#       >= t*.  Require worst |t_trough/t_1 - 1| over the population to be STRICTLY
#       SMALLER than v2's own worst (which is what t* alone achieves in the same run,
#       computed here rather than quoted).  If it is, the first zero has a closed
#       predictor and section 4.3 of the note can carry one.
#
#   M4  A COST.  M3's predictor can only be believed if it also works where the answer is
#       PROVED.  For constant weights the zero set is exactly t = (1/2)tan(n pi/k)
#       (Thm 2(e), r205), i.e. every rung, not every second one -- so the trough
#       predictor must NOT be applied there and must be seen to fail there.  Registered
#       so that a predictor which happens to fit the decaying case is not quietly
#       assumed to be general: print its error on the constant case and expect it to be
#       LARGE.  A predictor whose domain is not tested is a predictor with no domain.
#
#   INSTRUMENT (first; abort on failure).  Constant weights, zero set proved exactly,
#     reference inside the precision block, scan range a NON-round multiple (F89).
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
N_DENSE = 20000
KGRID = [64, 76, 90, 107, 128, 152, 181, 215, 256, 304, 362, 431, 512,
         609, 724, 861, 1024, 1150, 1290, 1448, 1625, 1824, 2048]
SS = ['1', '2', '4']


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
    step = float(ts[1] - ts[0])
    return bisect_mp(w, ts[idx[0]], ts[idx[0] + 1], widen=step)


def t_star(w64, k):
    """the v2 continuous crossing: smallest t>0 with w_{k-1} rho^k/(2t) = Hp(t) + 1/2."""
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


def next_trough(tstar, k):
    """smallest t = (1/2)tan((3pi/2 + 2 pi n)/k) with t >= tstar, n = 0,1,2,..."""
    th = atan(2 * tstar)
    n = int(floor((k * th - 3 * pi / 2) / (2 * pi))) + 1
    if n < 0:
        n = 0
    for _ in range(4):
        thn = (3 * pi / 2 + 2 * pi * n) / k
        if thn >= pi / 2:
            return None, n
        t = tan(thn) / 2
        if t >= tstar:
            return t, n
        n += 1
    return None, n


say("=" * 100)
say("trough_r217 -- is the first zero the FIRST TROUGH after the model's crossing?")
say("troughs: k theta = 3pi/2 + 2 pi n, i.e. t = (1/2)tan((3pi/2+2 pi n)/k), spacing pi/k")
say("derived on paper before the run; nothing fitted")
say("=" * 100)

verdicts = []

say()
say("--- INSTRUMENT: constant weights, zero set proved exactly (Thm 2(e), r205) ---")
okI, nI = True, 0
for k in (64, 256, 1024):
    ref = tan(pi / k) / 2
    got = first_zero(w_const(k), mpf('4.13') * ref)          # non-round multiple (F89)
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

# ------------------------------------------------------------------ the run
say()
say("--- the trough picture, point by point ---")
say("  %5s %6s %14s %14s %14s %9s %9s %9s"
    % ("s", "k", "t_1", "t* (v2)", "t_trough", "dev", "g", "ratio_tr"))
pts = []
for ss in SS:
    for k in KGRID:
        w = w_power(k, ss)
        w64 = np.array([float(x) for x in w])
        pred = sqrt(mpf(ss) * log(k) / (2 * k))
        t1 = first_zero(w, 3 * pred)
        ts_ = t_star(w64, k)
        if t1 is None or ts_ is None:
            say("  %5s %6d  not found" % (ss, k))
            continue
        ttr, n = next_trough(ts_, k)
        th1 = atan(2 * t1)
        x = k * th1 / (2 * pi) - mpf(3) / 4
        psi = x - floor(x)
        dev = min(psi, 1 - psi)
        g = mp.e ** (4 * pi * t1)
        r_star = ts_ / t1
        r_tr = (ttr / t1) if ttr else None
        pts.append((ss, k, t1, ts_, ttr, dev, g, r_star, r_tr))
        say("  %5s %6d %14s %14s %14s %9s %9s %9s"
            % (ss, k, mp.nstr(t1, 9), mp.nstr(ts_, 9),
               mp.nstr(ttr, 9) if ttr else "none",
               mp.nstr(dev, 4), mp.nstr(g, 4),
               mp.nstr(r_tr, 6) if r_tr else "-"))
    say("")

n_pop = len(pts)
say("  population: %d points" % n_pop)
if n_pop == 0:
    say("EMPTY POPULATION -- FAIL.")
    sys.exit(1)

# ------------------------------------------------------------------ M1
say()
say("--- M1  are the zeros on the trough grid?  (unrelated -> mean dev = 0.25) ---")
BANDS = [(64, 152), (181, 431), (512, 1150), (1290, 2048)]
say("  %16s %8s %14s" % ("k band", "points", "mean dev"))
band_dev = []
for lo, hi in BANDS:
    sel = [p[5] for p in pts if lo <= p[1] <= hi]
    if len(sel) < 3:
        continue
    m = sum(sel) / len(sel)
    band_dev.append((lo, hi, m))
    say("  %16s %8d %14s" % ("%d-%d" % (lo, hi), len(sel), mp.nstr(m, 5)))
allm = sum(p[5] for p in pts) / n_pop
last = band_dev[-1][2] if band_dev else mpf(1)
m1 = allm < mpf('0.25') and last < mpf('0.15')
say("  overall mean dev = %s   largest-k band = %s   -> %s"
    % (mp.nstr(allm, 5), mp.nstr(last, 5), "PASS" if m1 else "FAIL"))
verdicts.append(('M1 zeros sit on the trough grid', m1))

# ------------------------------------------------------------------ M2
say()
say("--- M2  the drift is explained by the per-period growth g = e^{4 pi t_1} ---")
first_band = band_dev[0][2] if band_dev else None
conc = tot = 0
for a in range(len(pts)):
    for b in range(a + 1, len(pts)):
        ga, da = pts[a][6], pts[a][5]
        gb, db = pts[b][6], pts[b][5]
        if ga == gb or da == db:
            continue
        tot += 1
        if (ga - gb) * (da - db) > 0:
            conc += 1
frac = mpf(conc) / tot if tot else mpf(0)
m2 = (first_band is not None and last < first_band and frac > mpf('0.5'))
say("  mean dev: smallest-k band %s  ->  largest-k band %s"
    % (mp.nstr(first_band, 5) if first_band else "n/a", mp.nstr(last, 5)))
say("  concordant (g, dev) pairs: %d of %d = %s" % (conc, tot, mp.nstr(frac, 5)))
say("  -> %s" % ("PASS" if m2 else "FAIL -- the drift has another cause"))
verdicts.append(('M2 drift explained by g', m2))

# ------------------------------------------------------------------ M3
say()
say("--- M3  formula vs bound: does the trough predictor beat t* alone? ---")
w_star = max(abs(p[7] - 1) for p in pts)
have = [p for p in pts if p[8] is not None]
w_tr = max(abs(p[8] - 1) for p in have) if have else None
say("  worst |t*/t_1 - 1|        (v2 alone)      = %s   over %d points"
    % (mp.nstr(w_star, 6), n_pop))
say("  worst |t_trough/t_1 - 1|  (v2 + troughs)  = %s   over %d points"
    % (mp.nstr(w_tr, 6) if w_tr else "n/a", len(have)))
m3 = w_tr is not None and len(have) == n_pop and w_tr < w_star
say("  -> %s" % ("PASS -- the first zero has a closed predictor" if m3 else
                 "FAIL -- the trough step does not improve on the continuous crossing"))
verdicts.append(('M3 trough predictor beats t* alone', m3))
if have:
    mean_tr = sum(abs(p[8] - 1) for p in have) / len(have)
    mean_st = sum(abs(p[7] - 1) for p in pts) / n_pop
    say("  mean |.-1|:  v2 alone %s   v2+troughs %s"
        % (mp.nstr(mean_st, 6), mp.nstr(mean_tr, 6)))

# ------------------------------------------------------------------ M4
say()
say("--- M4  the predictor's DOMAIN: it must FAIL on constant weights, where every rung")
say("        is a zero (Thm 2(e)) and the trough grid is the wrong grid ---")
okD, nD = True, 0
for k in (64, 256, 1024):
    ref = tan(pi / k) / 2                       # the proved first zero, theta = pi/k
    w64 = np.array([0.0] + [0.5] * (k - 1))
    ts_ = t_star(w64, k)
    if ts_ is None:
        say("  k=%5d  no continuous crossing for the constant case" % k)
        continue
    ttr, n = next_trough(ts_, k)
    if ttr is None:
        say("  k=%5d  no trough found" % k)
        continue
    rel = abs(ttr - ref) / ref
    nD += 1
    if rel < mpf('0.05'):
        okD = False                              # it should NOT fit here
    say("  k=%5d proved t_1=%s  trough predictor=%s  rel error=%s"
        % (k, mp.nstr(ref, 12), mp.nstr(ttr, 12), mp.nstr(rel, 5)))
say("  -> %s" % ("PASS: the predictor visibly fails outside its domain, as registered"
                 if okD and nD else
                 "FAIL: it fits the constant case too, so the trough grid is not what is"
                 " doing the work"))
verdicts.append(('M4 predictor fails outside its domain', okD and nD > 0))

say()
say("=" * 100)
for tag, v in verdicts:
    say("  [%s] %s" % (tag, "PASS" if v else "FAIL"))
say()
say("interpretation belongs in the report, not here.")
say("done.")
sys.exit(0 if all(v for _, v in verdicts) else 1)
