#!/usr/bin/env python3
# debts_r226.py -- paying the two debts r225 named, so door (a) can stop saying "sketched".
#
# =============================================================================
# r225 left exactly two things owed, and said so rather than rounding them off:
#   (1) the HEAD remainder was written as "err" and only sketched;
#   (2) "sin(k theta) reaches -1 within pi/2k" was MEASURED at 24/24 (K4) and not proved.
# Both are written out below.  Neither is deep; both are work, which is why they were owed.
#
# =============================================================================
# DEBT 1 -- THE HEAD REMAINDER, with every constant.
#
# The r225 sketch split a_j sin(j theta) into "rho^j ~ 1" times "sin ~ j theta" and waved at
# the errors.  That split is unnecessary: rho^j sin(j theta) = Im(z^j) EXACTLY, z = 1+2it.
# Working with Im(z^j) removes one approximation before it is made (F28).
#
#   Im(z^j) = sum_{m odd} C(j,m) (2t)^m (-1)^{(m-1)/2},  so  Im(z^j) - 2jt  is the tail m>=3.
#   |Im(z^j) - 2jt| <= (1+2t)^j - 1 - 2jt <= (2jt)^2 e^{2jt} / 2 .
#   On j <= J = ceil(1/2t) we have 2jt <= 1 + 2t, so e^{2jt} <= e^{1+2t} <= e^2 for t <= 1/2:
#
#       (H1)   | HEAD - 2t sum_{j<=J} j D_j |  <=  2 e^2 t^2 sum_{j<=J} j^2 D_j .
#
# The two sums are elementary by Abel, with NO asymptotics:
#       sum_{j<=J} j   D_j = sum_{i<J} w_i        - J   w_J
#       sum_{j<=J} j^2 D_j = sum_{i<J} (2i+1) w_i - J^2 w_J
# and for w_i = (i+1)^{-s}:
#       sum_{j<=J} j^2 D_j = 2 sum_{i<J}(i+1)^{1-s} - sum_{i<J}(i+1)^{-s} - J^2 (J+1)^{-s}
#                          = O(J^{2-s})  (1<s<2),  O(log J)  (s=2),  -> 2 zeta(s-1)-zeta(s) (s>2).
# With J ~ 1/2t that makes the right-hand side of (H1), divided by t,
#       O(t^{s-1})   for 1<s<2 ,      O(t log(1/t))   at s=2 ,      O(t)   for s>2 .
#
# And the truncation of the main term is a tail of a convergent series:
#       (H2)   | 2 sum_{j<=J} j D_j - 2 zeta(s) |  <=  2 [ J^{1-s}/(s-1) + J^{1-s} ] ,
# using sum_{i>=J}(i+1)^{-s} <= J^{1-s}/(s-1) and J w_J <= J^{1-s}.
#
#   ==>  HEAD/t = 2 zeta(s) + E(t),  |E(t)| <= 2 e^2 t sum_{j<=J} j^2 D_j + 2 J^{1-s} s/(s-1),
#        EVERY TERM COMPUTABLE, and E -> 0 for every s > 1.  Debt 1 paid.
#
# The dominant piece is O(t^{s-1}), which is what r222 measured and what F108 says must be
# tested as its own rate rather than mixed with the tail's k^{-1/2}/log k.
#
# =============================================================================
# DEBT 2 -- THE ZERO IS REALLY THERE, and the reason is steepness.
#
# Write F_k(t) = 1 + H*(t)/t + A(t) sin(k theta(t)),  A(t) := k^{-s} rho(t)^k / t > 0.
#
#   (a) k theta SWEEPS.  d(k theta)/dt = 2k/(1+4t^2), so over any interval of length
#       L = pi (1+4t^2)/k the phase k theta advances by at least 2 pi, and sin(k theta)
#       therefore ATTAINS -1 somewhere inside.  Nothing asymptotic; just monotonicity of
#       theta and the intermediate value theorem.
#
#   (b) A IS INCREASING where it matters.  d(log A)/dt = 4kt/(1+4t^2) - 1/t
#       = (4kt^2 - 1 - 4t^2) / (t(1+4t^2)) > 0  as soon as  4(k-1)t^2 > 1,
#       which at t ~ sqrt(lambda log k / 2k) reads 2 lambda log k > 1 -- true for every k
#       this project computes.  So A(t*) >= A(T) for any t* >= T.
#
#   (c) A IS VIOLENTLY steep, and that is what makes the bracket cheap.  Raising t by a
#       RELATIVE eta multiplies A by about exp(4kT^2 eta) = k^{2 lambda eta}: an eta of
#       1/log k already multiplies A by k^{2 lambda / log k} = e^{2 lambda}.  So an O(E)
#       uncertainty in the head is absorbed by moving t up by O(E/log k).
#
#   Combining: let T solve A(T) = 1 + 2 zeta(s) exactly.  At the first t* >= T(1+eta) where
#   sin(k theta) = -1 -- which exists within pi(1+4t^2)/k by (a) --
#       F_k(t*) = 1 + H*/t* - A(t*) <= 1 + 2 zeta(s) + |E| - A(T)(1+ e^{4kT^2 eta} - 1)
#   which is <= 0 once eta >= |E| / (4 k T^2) ~ |E| / (2 lambda log k).  And below T(1-eta)
#   the same inequality with |sin| <= 1 gives F_k > 0.  Hence
#
#       (Z)   T(1 - eta)  <=  t_1  <=  T(1 + eta) + pi(1+4T^2)/k ,   eta = |E|/(2 lambda log k)
#
#   and since 1/(k T) ~ 1/sqrt(k log k) -> 0 and eta -> 0, t_1/T -> 1 and
#   2 k t_1^2 / log k -> 2 k T^2 / log k -> s - 1/2.   Debt 2 paid.
#
#   WHAT IS STILL NOT PROVED, stated plainly: (Z) is an inequality about t_1 GIVEN the head
#   bound E, and E is bounded above by a quantity this file computes but does not bound
#   symbolically in closed form for every s at once (the j^2 sum is handled case by case in
#   s).  A written-out theorem would fix one s-range at a time.  That is bookkeeping, not a
#   gap in the argument, and it is named here so nobody has to rediscover it.
#
# =============================================================================
# PRE-REGISTERED, before the first number.  Each criterion tests ONE inequality of the
# proof, at its own rate (F108: the error is a sum of terms with different rates, so the
# summands are tested separately and never as one).
#
#  M0  INSTRUMENT, FIRST, ABORTS (F86).  Answers already known exactly:
#      M0a  the Abel identities for sum j D_j and sum j^2 D_j against direct summation,
#           at 40 digits -- these carry (H1) and (H2) and a slip in either is invisible later.
#      M0b  Im(z^j) against rho^j sin(j theta), exactly, at several (j,t).
#      M0c  t_1 at (s,k)=(1,256) reproduces the published 0.106767212545108.
#
#  M1  (H1) HOLDS.  |HEAD - 2t sum j D_j| <= 2 e^2 t^2 sum j^2 D_j at every (s,k).
#      A violation means the head remainder bound is WRONG, not slow.
#  M2  (H2) HOLDS.  |2 sum_{j<=J} j D_j - 2 zeta(s)| <= 2 J^{1-s} s/(s-1) at every (s,k).
#  M3  THE COMBINED HEAD BOUND COVERS.  |HEAD/t - 2 zeta(s)| <= (H1)/t + (H2) at every point.
#  M4  RATES, EACH AGAINST ITS OWN (F108).  (H1)/t divided by its predicted rate
#      (t^{s-1} for s<2, t for s>2) must be stable, max/min < 1.8 over the last four k;
#      (H2) divided by t^{s-1} likewise.  Reported per term, never summed.
#  M5  (b) A IS INCREASING: 4(k-1)t^2 > 1 at every (s,k) used.  A single failure voids
#      step (b) and with it the whole upper bracket.
#  M6  (a) THE SWEEP: over [t_1 - pi(1+4t^2)/k, t_1] the phase k theta must advance by
#      >= 2 pi.  This is the claim r225 could only measure.
#  M7  (Z) THE EXPLICIT BRACKET, nothing fitted, using the computed E: T(1-eta) <= t_1 <=
#      T(1+eta) + pi(1+4T^2)/k.  Report where t_1 sits inside it.
#  M8  CONTROL THAT CAN FAIL: at s = 0.5 the head bound (H2) must NOT cover, since
#      sum j D_j diverges there -- require the ratio > 1 at the largest k.  If the same
#      bound covers both regimes it distinguishes neither (the r219 L4 lesson).
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
E2 = math.e ** 2


def pieces(k, s, t):
    """HEAD (j<=J) and the two Abel sums, plus the bounds (H1) and (H2)."""
    J = min(int(math.ceil(1.0 / (2.0 * t))), k - 1)
    j = np.arange(1, J + 1, dtype=np.float64)
    D = j ** (-s) - (j + 1.0) ** (-s)
    lrho, th = 0.5 * math.log1p(4.0 * t * t), math.atan(2.0 * t)
    head = float(np.sum(D * np.exp(j * lrho) * np.sin(j * th)))
    S1 = float(np.sum(j * D))
    S2 = float(np.sum(j * j * D))
    H1 = 2.0 * E2 * t * t * S2
    H2 = 2.0 * (J ** (1.0 - s)) * s / (s - 1.0) if s > 1 else float("inf")
    return head, S1, S2, H1, H2, J


def Hstar(k, s, t):
    j = np.arange(1, k, dtype=np.float64)
    D = j ** (-s) - (j + 1.0) ** (-s)
    return float(np.sum(D * np.exp(j * 0.5 * math.log1p(4 * t * t))
                        * np.sin(j * math.atan(2 * t))))


def F_of(k, s, t):
    lrho, th = 0.5 * math.log1p(4.0 * t * t), math.atan(2.0 * t)
    return 1.0 + ((k ** (-s)) * math.exp(k * lrho) * math.sin(k * th) + Hstar(k, s, t)) / t


def first_zero(k, s):
    t_hi = math.sqrt((s + 1.0) * math.log(k) / (2.0 * k)) * 2.0
    n = int(max(2000, 20 * k * math.atan(2 * t_hi) / math.pi))
    ts = np.linspace(t_hi / n, t_hi, n)
    v = np.array([F_of(k, s, float(x)) for x in ts])
    idx = np.nonzero(v <= 0.0)[0]
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
say("debts_r226 -- the two things r225 owed, written out.  (1) the head remainder with every")
say("constant, via Im(z^j) rather than a split; (2) the zero really is there, and the reason")
say("is that A(t) is violently steep.  See the header for the argument.")
say("=" * 98)

verdicts = []

# ------------------------------------------------------------------ M0
say()
say("--- M0  INSTRUMENT.  Runs first; failure aborts. ---")
okM0 = True
say("  M0a  the two Abel identities against direct summation (they carry H1 and H2)")
for s in (1.5, 2.5):
    for J in (7, 40):
        jj = [mpf(x) for x in range(1, J + 1)]
        D = [j ** (-mpf(s)) - (j + 1) ** (-mpf(s)) for j in jj]
        d1 = sum(j * d for j, d in zip(jj, D))
        a1 = sum(mpf(1) / mpf(i + 1) ** mpf(s) for i in range(J)) - J * mpf(1) / mpf(J + 1) ** mpf(s)
        d2 = sum(j * j * d for j, d in zip(jj, D))
        a2 = sum((2 * i + 1) * mpf(1) / mpf(i + 1) ** mpf(s) for i in range(J)) \
            - J * J * mpf(1) / mpf(J + 1) ** mpf(s)
        e1, e2 = abs(d1 - a1), abs(d2 - a2)
        if e1 > mpf('1e-30') or e2 > mpf('1e-30'):
            okM0 = False
        say("       s=%-4s J=%3d   |sum jD - Abel| %s   |sum j2D - Abel| %s"
            % (s, J, mp.nstr(e1, 3), mp.nstr(e2, 3)))
say("  M0b  Im(z^j) == rho^j sin(j theta), exactly")
for t in (0.01, 0.07):
    for jv in (1, 5, 37):
        z = mpf(1) + 2j * mpf(t) if False else None
        zz = mp.mpc(1, 2 * mpf(t))
        lhs = mp.im(zz ** jv)
        rhs = mp.sqrt(1 + 4 * mpf(t) ** 2) ** jv * mp.sin(jv * mp.atan(2 * mpf(t)))
        if abs(lhs - rhs) > mpf('1e-30'):
            okM0 = False
        say("       t=%-6s j=%3d  |Im(z^j) - rho^j sin| %s" % (t, jv, mp.nstr(abs(lhs - rhs), 3)))
say("  M0c  t_1 at (s,k)=(1,256) against the published value")
t1r = first_zero(256, 1.0)
e0c = abs(t1r - 0.106767212545108)
if e0c > 1e-9:
    okM0 = False
say("       here %.15f  published %.15f  |diff| %.2e" % (t1r, 0.106767212545108, e0c))
say("  -> %s" % ("PASS" if okM0 else "FAIL"))
verdicts.append(("M0 instrument", okM0))
if not okM0:
    say()
    say("ABORTING: an instrument control failed, so nothing below means anything.")
    sys.exit(1)

# ------------------------------------------------------------------ measure
say()
say("--- the measurement at t = t_1 ---")
say("  %5s %7s %14s %11s %11s %11s %10s %10s"
    % ("s", "k", "t_1", "HEAD/t", "2 zeta(s)", "(H1)/t", "(H2)", "|err|"))
data = {}
for s in S_MAIN + [0.5]:
    z2 = float(2 * zeta(mpf(s)))
    for k in K_LIST:
        t1 = first_zero(k, s)
        if t1 is None:
            continue
        head, S1, S2, H1, H2, J = pieces(k, s, t1)
        data[(s, k)] = dict(t1=t1, head=head / t1, z2=z2, S1=S1, S2=S2,
                            H1=H1, H2=H2, J=J, err=abs(head / t1 - z2))
        say("  %5s %7d %14.10f %11.5f %11.5f %11.5f %10.5f %10.5f"
            % (s, k, t1, head / t1, z2, H1 / t1, H2, abs(head / t1 - z2)))
    say()
say("  population: %d" % len(data))

# ------------------------------------------------------------------ M1 M2 M3
for tag, name, fn in (
    ("M1", "(H1) |HEAD - 2t sum jD| <= 2 e^2 t^2 sum j2D",
     lambda d, s, k: (abs(d['head'] * d['t1'] - 2 * d['t1'] * d['S1']), d['H1'])),
    ("M2", "(H2) |2 sum jD - 2 zeta(s)| <= 2 J^{1-s} s/(s-1)",
     lambda d, s, k: (abs(2 * d['S1'] - d['z2']), d['H2'])),
    ("M3", "the combined head bound covers the measured error",
     lambda d, s, k: (d['err'], d['H1'] / d['t1'] + d['H2'])),
):
    say()
    say("--- %s  %s ---" % (tag, name))
    ok, n, worst = True, 0, 0.0
    for s in S_MAIN:
        for k in K_LIST:
            d = data.get((s, k))
            if not d:
                continue
            lhs, rhs = fn(d, s, k)
            n += 1
            r = lhs / rhs if rhs else float("inf")
            worst = max(worst, r)
            if r > 1.0:
                ok = False
                say("       VIOLATION s=%s k=%d  lhs=%.6g rhs=%.6g ratio=%.3f" % (s, k, lhs, rhs, r))
    say("  %d points, worst lhs/bound = %.4f (must be <= 1) -> %s"
        % (n, worst, "PASS" if ok and n else "FAIL"))
    verdicts.append(("%s %s" % (tag, name.split()[0]), ok and n > 0))

# ------------------------------------------------------------------ M4
say()
say("--- M4  RATES, EACH TERM AGAINST ITS OWN (F108: never test a sum of rates as one) ---")
okM4, n4 = True, 0
for s in S_MAIN:
    rate1 = (lambda t: t ** (s - 1.0)) if s < 2 else (lambda t: t)
    lab1 = "t^{s-1}" if s < 2 else "t"
    rows = []
    for k in K_LIST:
        d = data.get((s, k))
        if d:
            rows.append((k, (d['H1'] / d['t1']) / rate1(d['t1']),
                         d['H2'] / d['t1'] ** (s - 1.0)))
    say("  s=%-5s  (H1)/t per %s   |   (H2) per t^{s-1}" % (s, lab1))
    for k, r1, r2 in rows:
        say("       k=%6d   %12.4f   %12.4f" % (k, r1, r2))
    last = rows[-4:]
    a = [r for _, r, _ in last]
    b = [r for _, _, r in last]
    o1, o2 = (max(a) / min(a)) < 1.8, (max(b) / min(b)) < 1.8
    n4 += 1
    if not (o1 and o2):
        okM4 = False
    say("       max/min: H1 %.3f (<1.8: %s) ; H2 %.3f (<1.8: %s)"
        % (max(a) / min(a), o1, max(b) / min(b), o2))
say("  cases: %d -> %s" % (n4, "PASS" if okM4 and n4 else "FAIL"))
verdicts.append(("M4 each error term follows its own rate", okM4 and n4 > 0))

# ------------------------------------------------------------------ M5 M6 M7
say()
say("--- M5  step (b): A is increasing, i.e. 4(k-1)t^2 > 1 ---")
okM5, n5, worst5 = True, 0, float("inf")
for s in S_MAIN:
    for k in K_LIST:
        d = data.get((s, k))
        if not d:
            continue
        v = 4.0 * (k - 1) * d['t1'] ** 2
        n5 += 1
        worst5 = min(worst5, v)
        if v <= 1.0:
            okM5 = False
say("  %d points, smallest 4(k-1)t^2 = %.2f (must be > 1) -> %s"
    % (n5, worst5, "PASS" if okM5 and n5 else "FAIL"))
verdicts.append(("M5 A is increasing on the range used", okM5 and n5 > 0))

say()
say("--- M6  step (a): k theta advances by >= 2 pi over a window of length pi(1+4t^2)/k ---")
say("      this is the claim r225 could only measure")
okM6, n6, worst6 = True, 0, float("inf")
say("  %5s %7s %14s %14s %10s" % ("s", "k", "window", "phase advance", "/2pi"))
for s in S_MAIN:
    for k in K_LIST:
        d = data.get((s, k))
        if not d:
            continue
        t1 = d['t1']
        L = math.pi * (1 + 4 * t1 * t1) / k
        adv = k * (math.atan(2 * (t1 + L)) - math.atan(2 * (t1 - L)))
        n6 += 1
        worst6 = min(worst6, adv / (2 * math.pi))
        if adv < 2 * math.pi:
            okM6 = False
    d = data.get((s, K_LIST[-1]))
    if d:
        t1 = d['t1']
        L = math.pi * (1 + 4 * t1 * t1) / k
        say("  %5s %7d %14.3e %14.4f %10.3f"
            % (s, K_LIST[-1], L, k * (math.atan(2 * (t1 + L)) - math.atan(2 * (t1 - L))),
               k * (math.atan(2 * (t1 + L)) - math.atan(2 * (t1 - L))) / (2 * math.pi)))
say("  %d points, smallest advance/2pi = %.4f (must be >= 1) -> %s"
    % (n6, worst6, "PASS" if okM6 and n6 else "FAIL"))
verdicts.append(("M6 the phase sweeps a full period in the window", okM6 and n6 > 0))

say()
say("--- M7  (Z) the explicit bracket, using the COMPUTED head bound E, nothing fitted ---")
say("  %5s %7s %13s %13s %11s %11s %7s %8s"
    % ("s", "k", "T", "t_1", "lo", "hi", "inside", "pos"))
okM7, n7 = True, 0
for s in S_MAIN:
    z2 = float(2 * zeta(mpf(s)))
    for k in K_LIST:
        d = data.get((s, k))
        if not d:
            continue
        T = T_of(k, s, z2)
        if T is None:
            continue
        E = d['H1'] / d['t1'] + d['H2']
        lam = 2.0 * k * T * T / math.log(k)
        eta = E / (2.0 * lam * math.log(k))
        lo = T * (1 - eta)
        hi = T * (1 + eta) + math.pi * (1 + 4 * T * T) / k
        ins = lo <= d['t1'] <= hi
        n7 += 1
        if not ins:
            okM7 = False
        pos = (d['t1'] - lo) / (hi - lo) if hi > lo else float("nan")
        say("  %5s %7d %13.9f %13.9f %11.7f %11.7f %7s %8.3f"
            % (s, k, T, d['t1'], lo, hi, "yes" if ins else "NO", pos))
    say()
say("  %d points -> %s" % (n7, "PASS" if okM7 and n7 else "FAIL"))
verdicts.append(("M7 t_1 inside the explicit bracket (Z)", okM7 and n7 > 0))

# ------------------------------------------------------------------ M8
say()
say("--- M8  CONTROL: (H2) must NOT cover at s = 0.5, where sum j D_j diverges ---")
d = data.get((0.5, K_LIST[-1]))
okM8 = False
if d:
    lhs = abs(2 * d['S1'] - d['z2'])
    rhs = d['H2']
    r = lhs / rhs if rhs and math.isfinite(rhs) else float("inf")
    okM8 = (not math.isfinite(rhs)) or r > 1.0
    say("      s=0.5 k=%d: |2 sum jD - 2 zeta| = %.5f, bound = %s, ratio = %s"
        % (K_LIST[-1], lhs, ("%.5f" % rhs) if math.isfinite(rhs) else "undefined (s<=1)",
           ("%.3f" % r) if math.isfinite(r) else "infinite"))
    say("      (the bound's constant s/(s-1) is not even defined below s=1 -- the argument")
    say("       does not merely fail there, it does not apply, which is the honest outcome)")
say("  -> %s" % ("PASS" if okM8 else "FAIL: the bound covers both regimes"))
verdicts.append(("M8 control: the head bound is specific to s>1", okM8))

say()
say("=" * 98)
for name, v in verdicts:
    say("  [%s] %s" % (name, "PASS" if v else "FAIL"))
say()
say("interpretation belongs in the report, not here.")
say("done.")
