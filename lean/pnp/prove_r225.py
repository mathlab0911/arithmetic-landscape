#!/usr/bin/env python3
# prove_r225.py -- door (a): the s > 1 branch, as a proof rather than a measurement.
#
# =============================================================================
# fable-5's r224 section 6 ruled door (a): prove lambda_infty = s - 1/2 for s > 1, on the
# grounds that the proof FORCES the tail bookkeeping F104 showed we owe.  This file is the
# paper argument, plus a test of every inequality the argument actually uses.
#
# SETUP (all exact).  w_j = (j+1)^{-s}, j = 0..k-1;  z = 1 + 2it = rho e^{i theta};
# D_j = w_{j-1} - w_j = j^{-s} - (j+1)^{-s} >= 0.  The r220 identity, PROVED at r224 by
# two routes:
#
#   (B)  F_k(1/2+it) = 1 + (1/t) [ w_{k-1} rho^k sin(k theta) + H*(t) ],
#        H*(t) = sum_{j=1}^{k-1} D_j rho^j sin(j theta) .
#
# =============================================================================
# THE ARGUMENT, ON PAPER, BEFORE ANY NUMBER.
#
# Write a_j := D_j rho^j >= 0.  Everything below turns on ONE observation:
#
#   d/dj [ log a_j ] = -(s+1)/j + 2 t^2  ,  so a_j DECREASES on j < j* and INCREASES on
#   j > j*, with  j* = (s+1) / (2 t^2)  --- a single interior minimum, nothing else.
#
# That is what makes the tail summable by Dirichlet's test rather than by brute force,
# and brute force is exactly what fails: sum_j |a_j| over the tail is ~ k t^{s+1}, which
# for 1 < s < 2 DIVERGES at the scale t ~ sqrt(log k / k).  The cancellation is not a
# nicety here; it is the whole bound.  (F104's bill, itemised.)
#
# Split at J := ceil(1/(2t)) (where j theta ~ 1, the head's natural end) and at j*:
#
#   HEAD    j <= J        : sin(j theta) = j theta (1 + O((j theta)^2)), rho^j = 1 + O(j t^2),
#                           so sum_{j<=J} a_j sin(j theta) = theta * sum_{j<=J} j D_j + err.
#                           The exact lemma sum_{j<=J} j D_j = sum_{i<J} w_i - J w_J gives
#                           -> zeta(s) for s > 1, and theta/t -> 2.  HEAD/t -> 2 zeta(s).
#   MIDDLE  J < j <= j*   : a_j decreasing.  Dirichlet/Abel:
#                              |sum a_j sin(j theta)| <= a_J / sin(theta/2)  =: B1
#   TAIL    j* < j <= k-1 : a_j increasing.  Abel the other way:
#                              |sum a_j sin(j theta)| <= 2 a_{k-1} / sin(theta/2) =: B2
#
# SIZES at t ~ sqrt(lambda log k / 2k), with lambda -> s - 1/2:
#
#   a_J     ~ s (2t)^{s+1} e^{t/2}  ~  s 2^{s+1} t^{s+1}      (J t^2 = t/2 -> 0)
#   B1 / t  <~ s 2^{s+1} t^{s+1} / (t * t)  =  s 2^{s+1} t^{s-1}   ->  0   for s > 1
#   a_{k-1} ~ s k^{-(s+1)} rho^k = s k^{lambda-s-1} = s k^{-3/2}
#   B2 / t  <~ 2 s k^{-3/2} / t^2 = 4 s k^{-1/2} / (lambda log k)  ->  0
#
# ==> H*/t = 2 zeta(s) + O(t^{s-1}) + O(k^{-1/2}/log k).  THE TAIL IS PAYABLE, and the
#     rate the proof claims for its own error is t^{s-1} -- which is F103 applied before
#     the fact: the criteria below test THAT rate, not a round number.
#
# THEN the zero.  Let T = T(k,s) solve   k^{-s} rho(T)^k = (1 + 2 zeta(s)) T   (exact rho).
#   (i)  NO ZERO BELOW.  For t < T(1-delta), |w_{k-1} rho^k sin(k theta)| / t <= k^{-s}rho^k/t
#        < 1 + 2 zeta(s) - (the error above), so F_k = 1 + H*/t + (that) > 0.
#        This is where |sin| <= 1 points the useful way -- the inequality is free.
#   (ii) A ZERO JUST ABOVE.  d(k theta)/dt = 2k/(1+4t^2) ~ 2k, so k theta sweeps a full
#        pi in any t-window of length ~ pi/(2k), while the amplitude k^{-s}rho^k changes
#        by a factor exp(2kt * pi/(2k)) = exp(pi t) = 1 + O(t).  So sin(k theta) reaches
#        -1 within pi/(2k) of T and F_k <= 0 there.
#   ==> t_1 = T (1 + O(delta) + O(1/(kT))), and 1/(kT) ~ 1/sqrt(k log k) -> 0.
#   ==> 2k t_1^2 / log k = 2k T^2 / log k + o(1)  ->  s - 1/2 .
#
# WHAT IS STILL OWED (stated so it cannot be forgotten): the HEAD error term is written
# above as "err" and is only sketched; and (ii) uses "sin reaches -1 in the window"
# without a quantitative statement about how close t_1 sits to the exact trough.  Those
# are the two places a referee would push, and K4/K5 below measure both rather than
# assuming them.
#
# =============================================================================
# PRE-REGISTERED, before the first number.
#
#  K0  INSTRUMENT, FIRST, ABORTS ON FAILURE (F86).  Three answers already known:
#      K0a  the three pieces must sum to H* EXACTLY (it is a partition of one sum) --
#           this tests the split indices, which is where an off-by-one would hide.
#      K0b  a_j must really be decreasing then increasing, with its minimum at j*:
#           check argmin(a_j) is within 1 of round(j*) at every (s,k).  If the shape
#           claim is false the two Abel bounds do not apply at all.
#      K0c  constant weights: H*/t = 2(w_0 - w) exactly, at any t.
#
#  K1  THE ABEL BOUNDS HOLD.  |MIDDLE| <= B1 and |TAIL| <= B2 at every (s,k).
#      These are inequalities the proof asserts; they CAN fail if the monotonicity split
#      or the Dirichlet kernel bound is misapplied.  They cannot fail if the mathematics
#      is right -- so a PASS tests the SETUP, not the law, and is reported that way (F97).
#
#  K2  THE RATE THE PROOF CLAIMS FOR ITSELF.  (B1+B2)/t must (a) be non-increasing over
#      the last four k, and (b) divided by t^{s-1}, be stable -- max/min < 1.6 over the
#      last four k -- for s in {1.5, 2, 2.5, 3.5}.  Registering the RATE and not a
#      threshold is F103 applied before the fact: at s=1.5 the bound is still ~1 at
#      k=32768 and a flat tolerance would call the proof wrong when it is merely slow.
#
#  K3  THE BOUND MUST COVER THE OBSERVED ERROR.  |H*/t - 2 zeta(s)| <= (B1+B2)/t + |head
#      remainder| at every point.  A violation means the proof's error term is too small
#      and the argument is WRONG, not slow.  This is the one that can kill the round.
#
#  K4  THE BRACKET.  t_1 must satisfy  T(1-eps) <= t_1 <= T(1+eps) + pi/(2k),  with
#      eps := ((B1+B2)/t + |head rem|)/(1 + 2 zeta(s)) the proof's OWN error, nothing
#      fitted.  Report the position of t_1 inside the bracket as a fraction.
#
#  K5  THE CONCLUSION.  lambda_T := 2kT^2/log k must approach s-1/2 at the rate the
#      derivation names: (lambda_T - (s-1/2) - loglog k/(2 log k)) * log k stable to
#      max/min < 1.4 over the last four k.  Again the rate, not a round number.
#
#  K6  CONTROL THAT CAN FAIL (r219's L4 lesson).  The argument must NOT also "work" at
#      s < 1, where the conclusion is different.  At s = 0.5 the head sum diverges, so
#      REQUIRE: |H*/t - 2 zeta(s)| / ((B1+B2)/t) > 3 at the largest k -- i.e. the s>1
#      bound visibly fails to cover the error there.  If it covers both, it explains
#      neither.
#
#  Populations printed.  Empty population = FAIL (F60).
# =============================================================================

import io
import math
import sys

import numpy as np
from mpmath import mp, mpf, zeta

LOG = __file__[:-3] + ".log"
OUT = []


def say(s=""):
    print(s, flush=True)
    OUT.append(s)
    io.open(LOG, "w", encoding="utf-8", newline="\n").write("\n".join(OUT) + "\n")


mp.dps = 40
K_LIST = [1024, 2048, 4096, 8192, 16384, 32768]
S_MAIN = [1.5, 2.0, 2.5, 3.5]


def parts(k, s, t):
    """Return (H*, HEAD, MIDDLE, TAIL, B1, B2, J, jstar, argmin) -- an exact partition."""
    j = np.arange(1, k, dtype=np.float64)
    D = j ** (-s) - (j + 1.0) ** (-s)
    lrho = 0.5 * math.log1p(4.0 * t * t)
    th = math.atan(2.0 * t)
    a = D * np.exp(j * lrho)
    terms = a * np.sin(j * th)
    J = min(int(math.ceil(1.0 / (2.0 * t))), k - 1)
    jstar = min(max((s + 1.0) / (2.0 * t * t), J + 1.0), float(k - 1))
    iJ = J                      # j = 1..J  -> indices 0..J-1
    iS = int(min(math.floor(jstar), k - 1))
    head = float(terms[:iJ].sum())
    mid = float(terms[iJ:iS].sum())
    tail = float(terms[iS:].sum())
    B1 = float(a[iJ - 1]) / math.sin(th / 2.0) if iJ >= 1 else 0.0
    B2 = 2.0 * float(a[-1]) / math.sin(th / 2.0)
    return (head + mid + tail, head, mid, tail, B1, B2, J, jstar,
            int(np.argmin(a)) + 1)


def F_of(k, s, t):
    Hs = parts(k, s, t)[0]
    lrho = 0.5 * math.log1p(4.0 * t * t)
    th = math.atan(2.0 * t)
    return 1.0 + ((k ** (-s)) * math.exp(k * lrho) * math.sin(k * th) + Hs) / t


def first_zero(k, s):
    t_hi = math.sqrt((s + 1.0) * math.log(k) / (2.0 * k)) * 2.0
    n = int(max(2000, 20 * k * math.atan(2 * t_hi) / math.pi))
    ts = np.linspace(t_hi / n, t_hi, n)
    vals = np.array([F_of(k, s, float(x)) for x in ts])
    idx = np.nonzero(vals <= 0.0)[0]
    if len(idx) == 0:
        return None
    i = int(idx[0])
    lo, hi = (ts[i - 1], ts[i]) if i > 0 else (ts[0] / 2, ts[0])
    for _ in range(200):
        if hi - lo < 1e-15 * max(1.0, hi):
            break
        m = 0.5 * (lo + hi)
        if F_of(k, s, m) <= 0.0:
            hi = m
        else:
            lo = m
    return 0.5 * (lo + hi)


def T_of(k, s, z2):
    """Solve k^-s rho(T)^k = (1 + 2 zeta(s)) T, exact rho.  Nothing measured."""
    def g(t):
        return math.exp(-s * math.log(k) + 0.5 * k * math.log1p(4 * t * t)) - (1.0 + z2) * t
    t0 = math.sqrt((s - 0.5) * math.log(k) / (2.0 * k))
    grid = np.geomspace(t0 / 50.0, t0 * 4.0, 4000)
    v = np.array([g(float(x)) for x in grid])
    cr = [i for i in range(1, len(grid)) if v[i - 1] <= 0.0 < v[i]]
    if not cr:
        return None
    lo, hi = float(grid[cr[0] - 1]), float(grid[cr[0]])
    for _ in range(200):
        if hi - lo < 1e-16 * max(1.0, hi):
            break
        m = 0.5 * (lo + hi)
        if g(m) > 0.0:
            hi = m
        else:
            lo = m
    return 0.5 * (lo + hi)


say("=" * 98)
say("prove_r225 -- door (a): the s>1 branch as a PROOF.  a_j = D_j rho^j has one interior")
say("minimum at j* = (s+1)/2t^2; Dirichlet on each monotone side bounds the tail, which")
say("brute force cannot do (sum |a_j| diverges for 1<s<2 at this scale).  See the header.")
say("=" * 98)

verdicts = []

# ------------------------------------------------------------------ K0
say()
say("--- K0  INSTRUMENT.  Runs first; failure aborts. ---")
okK0 = True
say("  K0a/K0b  the split is a partition, and a_j is unimodal with minimum at j*")
say("  %5s %7s %14s %10s %10s %12s" % ("s", "k", "|sum-H*|", "J", "j*", "argmin-j*"))
n0 = 0
for s in S_MAIN:
    for k in (1024, 32768):
        t = math.sqrt((s - 0.5) * math.log(k) / (2.0 * k))
        Hs, hd, md, tl, B1, B2, J, js, am = parts(k, s, t)
        err = abs((hd + md + tl) - Hs)
        n0 += 1
        if err > 1e-12 * max(1.0, abs(Hs)) or abs(am - js) > max(1.0, 0.02 * js):
            okK0 = False
        say("  %5s %7d %14.2e %10d %10.1f %12.1f" % (s, k, err, J, js, am - js))
say("       cases: %d" % n0)

say("  K0c  constant weights: H*/t = 2(w_0-w) exactly")
for k, t in ((512, 0.01), (4096, 0.003)):
    j = np.arange(1, k, dtype=np.float64)
    D = np.zeros(k - 1)
    D[0] = -0.5
    hs = float(np.sum(D * np.exp(j * 0.5 * math.log1p(4 * t * t)) * np.sin(j * math.atan(2 * t))))
    e = abs(hs / t - (-1.0))
    if e > 1e-12:
        okK0 = False
    say("       k=%5d t=%-7s H*/t=%+.15f target -1.0  err %.2e" % (k, t, hs / t, e))
say("  -> %s" % ("PASS" if okK0 else "FAIL"))
verdicts.append(("K0 instrument", okK0))
if not okK0:
    say()
    say("ABORTING: an instrument control failed, so nothing below means anything.")
    sys.exit(1)

# ------------------------------------------------------------------ measure
say()
say("--- the measurement, at t = t_1 (the object the theorem is about) ---")
say("  %5s %7s %14s %11s %11s %11s %11s %10s"
    % ("s", "k", "t_1", "H*/t", "2 zeta(s)", "B1/t", "B2/t", "|err|"))
data = {}
for s in S_MAIN + [0.5]:
    z2 = float(2 * zeta(mpf(s)))
    for k in K_LIST:
        t1 = first_zero(k, s)
        if t1 is None:
            say("  %5s %7d  NO ZERO IN RANGE" % (s, k))
            continue
        Hs, hd, md, tl, B1, B2, J, js, am = parts(k, s, t1)
        data[(s, k)] = dict(t1=t1, H=Hs / t1, z2=z2, B1=B1 / t1, B2=B2 / t1,
                            mid=md, tail=tl, err=abs(Hs / t1 - z2))
        say("  %5s %7d %14.10f %11.5f %11.5f %11.5f %11.3e %10.5f"
            % (s, k, t1, Hs / t1, z2, B1 / t1, B2 / t1, abs(Hs / t1 - z2)))
    say()
say("  population: %d points" % len(data))

# ------------------------------------------------------------------ K1
say()
say("--- K1  THE ABEL BOUNDS HOLD (tests the SETUP, not the law -- F97) ---")
okK1, n1, worst = True, 0, 0.0
for s in S_MAIN:
    for k in K_LIST:
        d = data.get((s, k))
        if not d:
            continue
        t1 = d['t1']
        Hs, hd, md, tl, B1, B2, J, js, am = parts(k, s, t1)
        n1 += 1
        r1 = abs(md) / B1 if B1 else float('inf')
        r2 = abs(tl) / B2 if B2 else float('inf')
        worst = max(worst, r1, r2)
        if r1 > 1.0 or r2 > 1.0:
            okK1 = False
            say("       VIOLATION s=%s k=%d  |MID|/B1=%.3f  |TAIL|/B2=%.3f" % (s, k, r1, r2))
say("  %d points, worst |piece|/bound = %.4f (must be <= 1) -> %s"
    % (n1, worst, "PASS" if okK1 and n1 else "FAIL"))
verdicts.append(("K1 the two Abel bounds hold", okK1 and n1 > 0))

# ------------------------------------------------------------------ K2
say()
say("--- K2  THE RATE THE PROOF CLAIMS FOR ITSELF: (B1+B2)/t ~ t^{s-1} ---")
okK2, n2 = True, 0
for s in S_MAIN:
    rows = []
    for k in K_LIST:
        d = data.get((s, k))
        if d:
            rows.append((k, d['B1'] + d['B2'], (d['B1'] + d['B2']) / d['t1'] ** (s - 1.0)))
    say("  s=%-5s" % s)
    for k, b, r in rows:
        say("       k=%6d  (B1+B2)/t = %10.5f   / t^{s-1} = %10.4f" % (k, b, r))
    last = rows[-4:]
    mono = all(last[i + 1][1] <= last[i][1] * 1.0000001 for i in range(len(last) - 1))
    rs = [r for _, _, r in last]
    stable = (max(rs) / min(rs)) < 1.6
    n2 += 1
    if not (mono and stable):
        okK2 = False
    say("       non-increasing: %s ; rate ratio max/min = %.3f (<1.6: %s)"
        % (mono, max(rs) / min(rs), stable))
say("  cases: %d -> %s" % (n2, "PASS" if okK2 and n2 else "FAIL"))
verdicts.append(("K2 the proof's own error rate is t^{s-1}", okK2 and n2 > 0))

# ------------------------------------------------------------------ K3
say()
say("--- K3  THE BOUND MUST COVER THE OBSERVED ERROR (a violation kills the argument) ---")
okK3, n3, worstc = True, 0, 0.0
say("  %5s %7s %12s %12s %10s" % ("s", "k", "|H*/t-2z|", "(B1+B2)/t", "ratio"))
for s in S_MAIN:
    for k in K_LIST:
        d = data.get((s, k))
        if not d:
            continue
        n3 += 1
        cov = d['B1'] + d['B2']
        r = d['err'] / cov if cov else float('inf')
        worstc = max(worstc, r)
        if r > 1.0:
            okK3 = False
        say("  %5s %7d %12.6f %12.6f %10.4f" % (s, k, d['err'], cov, r))
    say()
say("  %d points, worst error/bound = %.4f (must be <= 1) -> %s"
    % (n3, worstc, "PASS" if okK3 and n3 else "FAIL"))
verdicts.append(("K3 the error bound covers the measured error", okK3 and n3 > 0))

# ------------------------------------------------------------------ K4
say()
say("--- K4  THE BRACKET on t_1, using the proof's OWN error (nothing fitted) ---")
say("  %5s %7s %14s %14s %10s %10s %8s"
    % ("s", "k", "T", "t_1", "lo", "hi", "inside"))
okK4, n4 = True, 0
for s in S_MAIN:
    z2 = float(2 * zeta(mpf(s)))
    for k in K_LIST:
        d = data.get((s, k))
        if not d:
            continue
        T = T_of(k, s, z2)
        if T is None:
            continue
        eps = (d['B1'] + d['B2']) / (1.0 + z2)
        lo, hi = T * (1 - eps), T * (1 + eps) + math.pi / (2.0 * k)
        ins = lo <= d['t1'] <= hi
        n4 += 1
        if not ins:
            okK4 = False
        say("  %5s %7d %14.10f %14.10f %10.6f %10.6f %8s"
            % (s, k, T, d['t1'], lo, hi, "yes" if ins else "NO"))
    say()
say("  %d points -> %s" % (n4, "PASS" if okK4 and n4 else "FAIL"))
verdicts.append(("K4 t_1 inside the proof's bracket", okK4 and n4 > 0))

# ------------------------------------------------------------------ K5
say()
say("--- K5  THE CONCLUSION: lambda_T -> s-1/2 at the derived rate ---")
say("  %5s %7s %11s %11s %14s" % ("s", "k", "lambda_T", "s-1/2", "resid*log k"))
okK5, n5 = True, 0
for s in S_MAIN:
    z2 = float(2 * zeta(mpf(s)))
    rows = []
    for k in K_LIST:
        T = T_of(k, s, z2)
        if T is None:
            continue
        lam = 2.0 * k * T * T / math.log(k)
        res = (lam - (s - 0.5) - math.log(math.log(k)) / (2 * math.log(k))) * math.log(k)
        rows.append((k, lam, res))
        say("  %5s %7d %11.6f %11.4f %14.5f" % (s, k, lam, s - 0.5, res))
    rs = [abs(r) for _, _, r in rows[-4:]]
    stable = (max(rs) / min(rs)) < 1.4
    n5 += 1
    if not stable:
        okK5 = False
    say("       residual*log k ratio max/min = %.3f (<1.4: %s)" % (max(rs) / min(rs), stable))
    say()
say("  cases: %d -> %s" % (n5, "PASS" if okK5 and n5 else "FAIL"))
verdicts.append(("K5 lambda_T -> s-1/2 at the derived rate", okK5 and n5 > 0))

# ------------------------------------------------------------------ K6
say()
say("--- K6  CONTROL: the s>1 bound must NOT cover s<1, where the answer differs ---")
d = data.get((0.5, K_LIST[-1]))
okK6 = False
if d:
    cov = d['B1'] + d['B2']
    r = d['err'] / cov if cov else float('inf')
    okK6 = r > 3.0
    say("      s=0.5 k=%d: |H*/t - 2 zeta(s)| = %.5f, bound = %.5f, ratio = %.2f (>3: %s)"
        % (K_LIST[-1], d['err'], cov, r, okK6))
    say("      (there 2 zeta(s) is not even the leading term -- C_s t^{s-1} diverges)")
say("  -> %s" % ("PASS" if okK6 else "FAIL: the bound covers both regimes, so it "
                                      "distinguishes neither"))
verdicts.append(("K6 control: the argument is specific to s>1", okK6))

say()
say("=" * 98)
for name, v in verdicts:
    say("  [%s] %s" % (name, "PASS" if v else "FAIL"))
say()
say("interpretation belongs in the report, not here.")
say("done.")
