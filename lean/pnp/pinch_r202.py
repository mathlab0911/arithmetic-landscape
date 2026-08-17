#!/usr/bin/env python3
# pinch_r202.py -- rem:pinchformula's k=70 table, recomputed by TWO independent methods,
# to the precision at which they agree and no further.  fable-5's Ruling 1 (r201):
#
#   "Two numbers that disagree in the fifth digit are not a dispute about the fifth digit;
#    they are a dispute about the method, and one of the methods has to be shown to
#    converge before either number means anything."
#
#   Execution order fixed by the ruling: (1) the m_0 convention goes into the text FIRST,
#   because a convention inferred is a convention that will bite; (2) both methods at
#   >= 60 dps with a printed convergence column; (3) per-row truncation to agreed digits.
#   Honest uneven precision beats uniform false precision (F51 / C11 applied to a table).
#
# THE CONVENTION, stated here because r202 also put it in the paper:
#   the interpolating family has layer gaps a_{j+1} - a_j = 2c^j, hence
#       m_j = c^j  for j = 0 .. k-1,  INCLUDING m_0 = 1,
#   so a_1 = 2m_0 + 1 = 3.  At c = 1 this is {3,5,7,...} and NOT the odd numbers
#   {1,3,5,...} of cor:oddsclosed, which have m_0 = 0.  The two profiles differ by the
#   single weight w_0 = 1, so their Gamma^{(q)} differ by exactly 2 -- a different
#   function with different zeros.  The old table's c=1.00 row was therefore not the
#   odd numbers, whatever the surrounding prose said.
#
#   Second thing the display did not say: for non-integer c, m_j = c^j is not an integer,
#   so the interpolating family is a WEIGHT SEQUENCE and not a set of distinct odd
#   numbers.  Everything below is a statement about Gamma^{(q)} as defined by those
#   weights.  (F87 again, same section, same class: the condition forced by the object --
#   here integrality -- is the one missing from the page.)
#
# ---------------------------------------------------------------------------
# PRE-REGISTERED, before the first number (F45/F30; Ruling A -- the method comparison is
# a control, so its parameters are registered too):
#
#   METHOD A: build the polynomial coefficients of Gamma^{(q)}_k in q and call polyroots;
#             take the root nearest 1/2.  Sees every root, so "nearest" is a claim about
#             the whole set and not about where we scanned (F60).
#   METHOD B: never form the polynomial.  Evaluate Gamma^{(q)} by direct summation and
#             find the nearest zero by the ARGUMENT PRINCIPLE alone -- bracket and bisect
#             the smallest radius whose disc is non-empty, read the angle off that circle,
#             polish with Muller, then certify that a slightly smaller disc is empty.
#
#             *Recorded because the log keeps it:* B's first version scanned the critical
#             line, on the assumption -- never written down -- that the nearest zero lies
#             on it.  For every profile here with R > 1 it does NOT: at c = 1.00 the
#             nearest ON-LINE zero is at 0.872 and the nearest zero is at 0.504.  The
#             winding certificate is what said so, by refusing to certify.  On-line-ness
#             is a phenomenon of the BOUNDARY families (R = 1), not a general fact, and
#             an assumption imported from them silently changes what is being measured.
#
#   PRECISION: each method at dps = 60 and dps = 120.  A method is "converged" at a row
#             only where its own two precisions agree; that digit count is printed.
#   PUBLISH:  only the digits on which A and B agree, per row.  A row where they agree on
#             fewer than 3 significant digits is printed as "not resolved", not as a number.
#
#   FALSIFIER 1 (instrument, must pass first).  a_i = 2^i - 1 has the exact zero set
#       q = 1/2 + (i/2) tan(n pi / k)  (rem:leeyanglacunary, proved), so the nearest zero
#       is at distance (1/2) tan(pi/k).  BOTH methods must reproduce it to >= 25 digits.
#       If they do not, no row below counts.
#   FALSIFIER 2 (instrument).  On the odd numbers, prop:nopinch PROVES |q-1/2| < 1/6 is
#       zero-free.  Method B's winding number on |q-1/2| = 1/6 must be 0.
#   FALSIFIER 3 (the claim).  The ratio measured/predicted must stay >= 1 and increase
#       with c, as a finite-k measurement of a quantity going to zero must.  A ratio
#       below 1 would refute the prediction's direction.
# ---------------------------------------------------------------------------

import sys
from mpmath import mp, mpf, mpc, polyroots, sqrt, tan, pi, findroot, quad, exp, mpmathify

OUT = []


def say(s=""):
    print(s)
    OUT.append(s)


CS = ['1.00', '1.10', '1.25', '1.40', '1.60', '1.80', '2.00']
K = 70


def weights_layer(k, c):
    """m_j = c^j for j = 0..k-1 (m_0 = 1 -- the convention above); w_j = m_j 2^-j."""
    c = mpf(c)
    return [c ** j / mpf(2) ** j for j in range(k)]


def weights_lacunary_minus(k):
    """a_i = 2^i - 1: w_0 = 0, w_j = 1/2 for j = 1..k-1."""
    return [mpf(0)] + [mpf(1) / 2] * (k - 1)


def weights_odds(k):
    """{1,3,5,...}: m_0 = 0, m_j = 1, so w_0 = 0 and w_j = 2^-j."""
    return [mpf(0)] + [mpf(1) / mpf(2) ** j for j in range(1, k)]


def gamma_q(w, q):
    """Gamma^{(q)} = 1 + G(2q) + G(2-2q) by direct summation (METHOD B's evaluator)."""
    a, b = 2 * q, 2 - 2 * q
    acc = mpc(1)
    pa, pb = mpc(1), mpc(1)
    for wj in w:
        if wj != 0:
            acc += wj * (pa + pb)
        pa *= a
        pb *= b
    return acc


def coeffs(w):
    """METHOD A: coefficients of Gamma^{(q)} as a polynomial in q, highest degree first.

    (2q)^j = sum_i C(j,i) ... -- expand both (2q)^j and (2-2q)^j binomially and add.
    """
    n = len(w) - 1
    co = [mpf(0)] * (n + 1)          # co[i] = coefficient of q^i
    co[0] += 1
    from mpmath import binomial
    for j, wj in enumerate(w):
        if wj == 0:
            continue
        # (2q)^j
        co[j] += wj * mpf(2) ** j
        # (2-2q)^j = sum_i C(j,i) 2^{j-i} (-2q)^i
        for i in range(j + 1):
            co[i] += wj * binomial(j, i) * mpf(2) ** (j - i) * (mpf(-2) ** i)
    while len(co) > 1 and co[-1] == 0:
        co.pop()
    return list(reversed(co))         # polyroots wants highest first


def nearest_A(w):
    """polyroots over the whole set."""
    co = coeffs(w)
    rts = polyroots(co, maxsteps=200, extraprec=400)
    best = min(rts, key=lambda r: abs(r - mpf(1) / 2))
    return abs(best - mpf(1) / 2), best


def nearest_B(w, r_hi='1.5'):
    """Independent of METHOD A: never forms the polynomial, and never assumes the zero
    lies on the critical line -- which is the assumption the FIRST version of this
    function made, and it was false for every profile with R > 1.  (Kept in the log:
    that version measured the nearest ON-LINE zero, which is a different quantity, and
    the winding certificate is what said so.)

    Locate the nearest zero by the ARGUMENT PRINCIPLE alone: find the smallest radius
    whose disc contains a zero by bracketing and bisecting the winding number; read the
    angle off by minimising |f| on that circle; polish with Muller on the directly
    summed function; certify that a slightly smaller disc is empty.
    """
    half = mpf(1) / 2
    f = lambda q: gamma_q(w, q)

    lo, hi = None, None
    r = mpf(r_hi)
    for _ in range(30):
        if abs(winding(w, r, N=400)) > mpf('0.5'):
            hi = r
            r = r / 2
        else:
            lo = r
            break
    if hi is None:
        return None, None, None
    if lo is None:
        lo = mpf(0)

    for _ in range(24):
        mid = (lo + hi) / 2
        if abs(winding(w, mid, N=400)) > mpf('0.5'):
            hi = mid
        else:
            lo = mid

    best_th, best_v = None, None
    for i in range(360):
        th = 2 * pi * i / 360
        v = abs(f(half + hi * exp(mpc(0, 1) * th)))
        if best_v is None or v < best_v:
            best_v, best_th = v, th

    z0 = half + hi * exp(mpc(0, 1) * best_th)
    try:
        z = findroot(f, (z0, z0 * (1 + mpf('1e-6')), z0 * (1 - mpf('1e-6'))),
                     solver='muller', tol=mpf(10) ** (-mp.dps + 10))
    except Exception:
        return None, None, None
    d = abs(z - half)
    wind = winding(w, d * (1 - mpf(10) ** (-mp.dps // 4)), N=800)
    return d, z, wind


def winding(w, r, N=2000):
    """(1/2 pi i) * contour integral of f'/f -- counted by argument accumulation."""
    f = lambda t: gamma_q(w, mpf(1) / 2 + r * exp(mpc(0, 1) * t))
    tot = mpf(0)
    prev = f(mpf(0))
    for i in range(1, N + 1):
        cur = f(2 * pi * i / N)
        d = (cur / prev)
        from mpmath import arg
        tot += arg(d)
        prev = cur
    return tot / (2 * pi)


def agree_digits(x, y):
    """number of leading significant decimal digits on which x and y agree"""
    if x == 0 or y == 0:
        return 0
    d = abs(x - y) / max(abs(x), abs(y))
    if d == 0:
        return mp.dps
    from mpmath import log10, floor
    return int(floor(-log10(d)))


def trunc(x, nd):
    return mp.nstr(x, max(nd, 1), strip_zeros=False)


say("=" * 90)
say("pinch_r202 -- rem:pinchformula's k=70 table by two independent methods.")
say("Publish only the digits on which they agree.  Convention: m_j = c^j INCLUDING m_0 = 1.")
say("=" * 90)

# ---------------------------------------------------------------- falsifiers first

say()
say("--- FALSIFIER 1 (instrument): a_i = 2^i - 1, exact nearest zero = (1/2)tan(pi/k) ---")
ok1 = True
for k in [32, 64]:
    mp.dps = 60                      # precision FIRST, reference SECOND -- see the note below
    exact = tan(pi / k) / 2
    w = weights_lacunary_minus(k)
    dA, _ = nearest_A(w)
    dB, _, wB = nearest_B(w, r_hi='0.2')
    gA, gB = agree_digits(dA, exact), agree_digits(dB, exact)
    say("  k=%3d  exact=%s" % (k, mp.nstr(exact, 30)))
    say("         A   =%s   agreeing digits: %d" % (mp.nstr(dA, 30), gA))
    say("         B   =%s   agreeing digits: %d   winding inside: %s"
        % (mp.nstr(dB, 30), gB, mp.nstr(wB, 4)))
    if gA < 25 or gB < 25:
        ok1 = False
say("  [F1] %s" % ("PASS -- both instruments reproduce a proved exact value"
                   if ok1 else "FAIL -- an instrument cannot reproduce a known exact value"))

say()
say("--- FALSIFIER 2 (instrument): odd numbers, prop:nopinch proves |q-1/2|<1/6 zero-free ---")
mp.dps = 60
wo = weights_odds(K)
wd = winding(wo, mpf(1) / 6)
ok2 = abs(wd) < mpf('1e-20')
say("  winding on |q-1/2| = 1/6 : %s   [F2] %s" % (mp.nstr(wd, 8), "PASS" if ok2 else "FAIL"))

if not (ok1 and ok2):
    say()
    say("VERDICT: an instrument control failed.  Reporting raw and stopping; no row below counts.")
    with open(__file__[:-3] + ".log", "w") as f:
        f.write("\n".join(OUT) + "\n")
    sys.exit(1)

# ---------------------------------------------------------------- the table

say()
say("--- the table, k = 70 ---")
say("  %6s %14s %26s %26s %6s %6s %5s  %s"
    % ("c", "predicted", "method A (polyroots)", "method B (line+winding)",
       "convA", "convB", "A~B", "cert"))

rows = []
for cs in CS:
    c = mpf(cs)
    pred = 1 / c - mpf(1) / 2
    res = {}
    winds = {}
    for dps in (60, 120):
        mp.dps = dps
        w = weights_layer(K, c)
        dA, _ = nearest_A(w)
        dB, _, wB = nearest_B(w)
        res[dps] = (dA, dB)
        winds[dps] = wB
    mp.dps = 120
    convA = agree_digits(res[60][0], res[120][0])
    convB = agree_digits(res[60][1], res[120][1])
    ab = agree_digits(res[120][0], res[120][1])
    certified = abs(winds[120]) < mpf('1e-6')
    rows.append((cs, pred, res[120][0], res[120][1], convA, convB, ab, certified))
    say("  %6s %14s %26s %26s %6d %6d %5d  %s"
        % (cs, mp.nstr(pred, 8), mp.nstr(res[120][0], 20), mp.nstr(res[120][1], 20),
           convA, convB, ab, "cert" if certified else "NOT-CERT"))

# ---------------------------------------------------------------- publish

say()
say("--- WHAT MAY BE PRINTED: min(convA, convB, A~B) significant digits, per row ---")
say("  %6s %14s %18s %10s %8s" % ("c", "predicted", "measured", "digits", "ratio"))
ok3 = True
n_ratios = 0
prev_ratio = None
for cs, pred, dA, dB, convA, convB, ab, certified in rows:
    nd = min(convA, convB, ab)
    if not certified:
        nd = 0
    if nd < 3:
        say("  %6s %14s %18s %10s %8s" % (cs, mp.nstr(pred, 8), "not resolved", nd, "--"))
        continue
    nd = min(nd, 12)
    val = mp.nstr(dA, nd)
    ratio = dA / pred if pred != 0 else None
    rs = mp.nstr(ratio, 5) if ratio is not None else "--"
    say("  %6s %14s %18s %10d %8s" % (cs, mp.nstr(pred, 8), val, nd, rs))
    if ratio is not None:
        if ratio < 1:
            ok3 = False
        if prev_ratio is not None and ratio < prev_ratio:
            ok3 = False
        prev_ratio = ratio
        n_ratios += 1

say()
if n_ratios == 0:
    say("  [F3] EXAMINED NOTHING -- no row produced a ratio, so this is not a pass (F60).")
    ok3 = False
else:
    say("  [F3] ratio >= 1 and increasing in c, over %d row(s): %s"
        % (n_ratios, "PASS" if ok3 else "FAIL"))
say()
say("done.")

with open(__file__[:-3] + ".log", "w") as f:
    f.write("\n".join(OUT) + "\n")
sys.exit(0)
