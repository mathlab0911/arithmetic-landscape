#!/usr/bin/env python3
# quantum_r216d.py -- why the constant at s = 1 cannot be settled by computing harder,
# with the rate.
#
# ---------------------------------------------------------------------------
# WHAT dense_r216c ESTABLISHED, and what it left.
#
# On a 23-size grid that is not all powers of two, lambda_eff(k) reverses direction 15
# times at s = 1, 11 at s = 1.5, and 11 at s = 3.  The published five-point columns had
# looked monotone at s = 2, 3, 4; on a real grid they are not.  So the jaggedness is
# universal in s, the scan is not responsible (r216b), and the v2 model reverses ZERO
# times over the same grid.  The oscillation is entirely outside the mechanism as
# modelled.  A smooth mechanism plus a jagged measurement, with the measurement now
# certified, means the jaggedness is a real feature that the model does not contain.
#
# ---------------------------------------------------------------------------
# THE EXPLANATION, DERIVED ON PAPER BEFORE THIS RUN, WITH NO FITTED CONSTANT.
#
# The first zero is a PHASE event: F_k = 1 + 2 Re G_k and Re G_k ~ Hp + T sin(k theta),
# so a zero needs sin(k theta) to reach -(Hp + 1/2)/T.  Two facts fix the picture.
#
#   (a) T = w_{k-1} rho^k/(2t) grows by a factor e^{4 pi t} across ONE period of
#       sin(k theta) -- since the period in theta is 2 pi/k, i.e. Delta t ~ pi/k, and
#       rho^k = e^{2kt^2}.  At t ~ 0.05 that is a factor ~1.9 per period.  So T goes
#       from below the threshold to well above it within about one period.
#   (b) Therefore the first zero lands within ONE PERIOD of the threshold crossing, and
#       WHERE inside that period depends on where the phase k theta happens to be.  The
#       admissible t are quantised with spacing Delta t = pi/k.
#
# Push that through the observable.  lambda = 2k t^2 / log k, so
#
#       Delta lambda  =  (4 k t / log k) * Delta t  =  4 pi t / log k ,
#
# and with t ~ sqrt(s log k / 2k),
#
#       Delta lambda  ~  4 pi sqrt( s / (2 k log k) )      -- decays like 1/sqrt(k log k).
#
# THIS IS THE POINT OF THE RUN.  lambda_eff is not a noisy estimate of a limit; it is a
# QUANTISED observable whose quantum shrinks like 1/sqrt(k log k).  At k = 2048, s = 1
# the quantum is about 0.065, which is comparable to the entire quantity in dispute
# between "lambda -> s" and "lambda -> s - 1/2 approached like log log k / log k".
# So the constant is not merely unsettled; it is unsettleable by this observable at
# sizes we can reach, and the rate says by how much and how slowly that improves.
#
# NOTE WHAT IS BEING RETRACTED.  r206 registered a falsifier P1 -- "the zeros sit on an
# evenly spaced ladder of troughs" -- and shot it down, correctly: with decaying weights
# the gaps run 0.17 to 0.73 in units of pi/k.  The conclusion drawn from that was that
# no quantisation argument is available, and the note says so.  That conclusion does not
# follow.  The zeros need not be evenly spaced for the FIRST one to be pinned to a phase
# grid of spacing pi/k; P1 tested the spacing of the whole ladder and was answered about
# the whole ladder.  A refuted falsifier retires the hypothesis it named, not the
# neighbourhood it was drawn from.
#
# ---------------------------------------------------------------------------
# PRE-REGISTERED, before the first number.  (s in {1, 2, 4}, 23 sizes, 69 points.)
#
#   Q1  THE QUANTUM BOUNDS THE RESIDUAL.  With R(k,s) := lambda_eff - lambda_v2 and
#       D(k,s) := 4 pi t_1 / log k, require |R| <= D at >= 90% of the population.
#       FAIL -> the quantum is not what the residual is made of, and the derivation
#       above is wrong.  Reported as such.
#
#   Q2  THE SHAPE, which is the part that cannot be got by fitting.  If the residual is
#       a phase landing uniformly inside one quantum, then std(R)/D should be near
#       1/sqrt(12) = 0.2887 and should NOT drift with k.  Require the ratio to lie in
#       [0.15, 0.55] in every k-band and the ratio's spread across bands to be under a
#       factor of 2.  A systematic drift means the residual has a trend in it and is
#       not pure quantisation.
#
#   Q3  THE CONSEQUENCE FOR THE NOTE, registered so it is not assembled afterwards.
#       Print D at k = 2048 for each s beside |the gap between the two candidate laws|,
#       which is (log log k)/(2 log k) at s>1 and (3/2)(log log k)/(log k) at s=1.
#       If D exceeds that gap, then no measurement at k <= 2048 can separate the two
#       candidates, and section 4.3 of the note should say that rather than reporting a
#       sequence that fails to settle.
#
#   Q4  A PREDICTION THAT COSTS US SOMETHING.  D is proportional to t_1, so it must
#       scale like sqrt(s) across s at fixed k.  Fit-free check: D(k,4)/D(k,1) should be
#       near 2.  Registered because it is the cheapest way for this story to be wrong.
#
#   INSTRUMENT (first; abort on failure).  Constant weights, zero set proved exactly,
#     Thm 2(e) r205, reference computed inside the precision block, scan range a
#     NON-round multiple of the answer (the defect found and fixed in r216c).
#     Second instrument: for constant weights the quantum picture is EXACT -- the zeros
#     are at theta = n pi/k -- so the measured consecutive spacing must equal pi/k in
#     theta to 20 digits.  A quantum argument that cannot reproduce the case where the
#     quantum is proved has not earned the case where it is not.
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


def zeros_upto(w, t_hi, howmany=1):
    """the first `howmany` sign changes of F, located in float64 and placed in mpmath."""
    w64 = np.array([float(x) for x in w])
    ts = np.linspace(0.0, float(t_hi), N_DENSE + 1)[1:]
    vals = F_dense(w64, ts)
    idx = np.where(np.sign(vals[:-1]) * np.sign(vals[1:]) < 0)[0]
    step = float(ts[1] - ts[0])
    out = []
    for i in idx[:howmany]:
        z = bisect_mp(w, ts[i], ts[i + 1], widen=step)
        if z is not None:
            out.append(z)
    return out


def t_model_v2(w64, k):
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


say("=" * 100)
say("quantum_r216d -- lambda_eff is a QUANTISED observable; the quantum is 4 pi t_1/log k")
say("derived on paper before the run; nothing below is fitted")
say("=" * 100)

verdicts = []

# ------------------------------------------------------------------ instruments
say()
say("--- INSTRUMENT 1: constant weights, zero set proved exactly (Thm 2(e), r205) ---")
okI, nI = True, 0
for k in (64, 256, 1024):
    ref = tan(pi / k) / 2                             # inside the precision block (r202)
    z = zeros_upto(w_const(k), mpf('4.13') * ref, 1)  # NOT a round multiple (r216c defect)
    rel = abs(z[0] - ref) / ref if z else mpf(1)
    nI += 1
    if rel > mpf(10) ** (-25):
        okI = False
    say("  k=%5d proved=%s got=%s rel=%s"
        % (k, mp.nstr(ref, 18), mp.nstr(z[0], 18) if z else "none", mp.nstr(rel, 4)))
say("  cases: %d -> %s" % (nI, "PASS" if okI and nI else "FAIL"))
verdicts.append(('instrument 1', okI and nI > 0))
if not okI:
    sys.exit(1)

say()
say("--- INSTRUMENT 2: where the quantum is PROVED, it must come out exactly pi/k ---")
say("    (constant weights: zeros at theta = n pi/k, so consecutive spacing in theta is pi/k)")
okQ, nQ = True, 0
for k in (64, 256):
    ref = tan(pi / k) / 2
    zs = zeros_upto(w_const(k), mpf('4.13') * ref, 3)
    if len(zs) < 2:
        okQ = False
        say("  k=%5d  fewer than two zeros found -- FAIL" % k)
        continue
    ths = [atan(2 * z) for z in zs]
    for a in range(len(ths) - 1):
        d = ths[a + 1] - ths[a]
        rel = abs(d - pi / k) / (pi / k)
        nQ += 1
        if rel > mpf(10) ** (-20):
            okQ = False
        say("  k=%5d  spacing in theta = %s   pi/k = %s   rel=%s"
            % (k, mp.nstr(d, 18), mp.nstr(pi / k, 18), mp.nstr(rel, 4)))
say("  cases: %d -> %s" % (nQ, "PASS" if okQ and nQ else "FAIL"))
verdicts.append(('instrument 2 (quantum exact where proved)', okQ and nQ > 0))
if not okQ:
    say("ABORTING: the quantum picture fails the case where the quantum is a theorem.")
    sys.exit(1)

# ------------------------------------------------------------------ the run
say()
say("--- the residual against the quantum ---")
say("  %5s %6s %14s %14s %14s %12s %10s"
    % ("s", "k", "lam_eff-s", "lam_v2-s", "R=residual", "D=quantum", "|R|/D"))
pts = []
for ss in SS:
    for k in KGRID:
        w = w_power(k, ss)
        w64 = np.array([float(x) for x in w])
        pred = sqrt(mpf(ss) * log(k) / (2 * k))
        zs = zeros_upto(w, 3 * pred, 1)
        tm = t_model_v2(w64, k)
        if not zs or tm is None:
            say("  %5s %6d  not found" % (ss, k))
            continue
        t1 = zs[0]
        le = 2 * k * t1 * t1 / log(k) - mpf(ss)
        lm = 2 * k * tm * tm / log(k) - mpf(ss)
        R = le - lm
        D = 4 * pi * t1 / log(k)
        pts.append((ss, k, le, lm, R, D))
        say("  %5s %6d %14s %14s %14s %12s %10s"
            % (ss, k, mp.nstr(le, 6), mp.nstr(lm, 6), mp.nstr(R, 6),
               mp.nstr(D, 5), mp.nstr(abs(R) / D, 4)))
    say("")

n_pop = len(pts)
say("  population: %d points" % n_pop)
if n_pop == 0:
    say("EMPTY POPULATION -- FAIL.")
    sys.exit(1)

# ------------------------------------------------------------------ Q1
say()
say("--- Q1  the quantum bounds the residual (>= 90% of points) ---")
inside = sum(1 for _, _, _, _, R, D in pts if abs(R) <= D)
frac = mpf(inside) / n_pop
q1 = frac >= mpf('0.9')
say("  |R| <= D at %d of %d points = %s  -> %s"
    % (inside, n_pop, mp.nstr(frac, 4), "PASS" if q1 else "FAIL"))
verdicts.append(('Q1 quantum bounds residual', q1))

# ------------------------------------------------------------------ Q2
say()
say("--- Q2  the SHAPE: std(R)/D near 1/sqrt(12)=0.2887 and not drifting with k ---")
BANDS = [(64, 152), (181, 431), (512, 1150), (1290, 2048)]
say("  %16s %8s %14s %14s" % ("k band", "points", "std(R/D)", "in [0.15,0.55]?"))
ratios = []
for lo, hi in BANDS:
    sel = [(R / D) for ss, k, le, lm, R, D in pts if lo <= k <= hi]
    if len(sel) < 3:
        continue
    m = sum(sel) / len(sel)
    sd = sqrt(sum((x - m) ** 2 for x in sel) / (len(sel) - 1))
    ratios.append(sd)
    say("  %16s %8d %14s %14s"
        % ("%d-%d" % (lo, hi), len(sel), mp.nstr(sd, 5),
           "yes" if mpf('0.15') <= sd <= mpf('0.55') else "NO"))
q2 = (len(ratios) >= 3
      and all(mpf('0.15') <= r <= mpf('0.55') for r in ratios)
      and max(ratios) / min(ratios) < 2)
say("  spread across bands: %s  -> %s"
    % (mp.nstr(max(ratios) / min(ratios), 4) if ratios else "n/a", "PASS" if q2 else "FAIL"))
verdicts.append(('Q2 shape consistent with uniform phase', q2))

# ------------------------------------------------------------------ Q3
say()
say("--- Q3  can any k <= 2048 separate the two candidate laws? ---")
say("  %5s %8s %14s %20s %12s" % ("s", "k", "quantum D", "gap between laws", "separable?"))
for ss in SS:
    row = [p for p in pts if p[0] == ss and p[1] == 2048]
    if not row:
        continue
    _, k, le, lm, R, D = row[0]
    ll = log(log(mpf(k))) / log(mpf(k))
    gap = (mpf(3) / 2) * ll if ss == '1' else ll / 2
    say("  %5s %8d %14s %20s %12s"
        % (ss, k, mp.nstr(D, 5), mp.nstr(gap, 5), "yes" if gap > D else "NO"))
say()
say("  Where the answer is NO, the quantum of the observable is larger than the whole")
say("  difference the measurement is being asked to detect.")

# ------------------------------------------------------------------ Q4
say()
say("--- Q4  D must scale like sqrt(s): D(k,4)/D(k,1) should be near 2 ---")
rr = []
for k in KGRID:
    a = [p for p in pts if p[0] == '4' and p[1] == k]
    b = [p for p in pts if p[0] == '1' and p[1] == k]
    if a and b:
        rr.append(a[0][5] / b[0][5])
if rr:
    m = sum(rr) / len(rr)
    say("  mean D(k,4)/D(k,1) over %d sizes = %s   (sqrt(4/1) = 2)" % (len(rr), mp.nstr(m, 6)))
    q4 = mpf('1.7') <= m <= mpf('2.3')
    say("  -> %s" % ("PASS" if q4 else "FAIL -- D does not scale like sqrt(s)"))
    verdicts.append(('Q4 sqrt(s) scaling', q4))

say()
say("=" * 100)
for tag, v in verdicts:
    say("  [%s] %s" % (tag, "PASS" if v else "FAIL"))
say()
say("interpretation belongs in the report, not here.")
say("done.")
sys.exit(0 if all(v for _, v in verdicts) else 1)
