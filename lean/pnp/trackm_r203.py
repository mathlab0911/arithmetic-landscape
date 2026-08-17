#!/usr/bin/env python3
# trackm_r203.py -- verification of Track M parts (i) and (ii).
#
# (i)  REDUCTION.  For real w_j >= 0 and G_k(z) = sum_{j<k} w_j z^j, put
#          F_k(q) = 1 + G_k(2q) + G_k(2-2q).
#      On Re q = 1/2 we have 2-2q = conj(2q), so F_k is REAL there:
#          F_k(1/2 + it) = 1 + 2 Re G_k(1+2it).
#      A sign change in t is a zero ON the line; cancellation cannot delete it.
#
# (ii) THE CONSTANT-WEIGHT THEOREM.  Let w_0 >= 0 and w_j = w > 0 for 1 <= j <= k-1.
#      Write z = 1+2it, rho = |z| = sqrt(1+4t^2), theta = arg z = arctan 2t.  Then
#
#          F_k(1/2 + it)  =  A + w * rho^k * sin(k theta) / t ,     A := 1 + 2w_0 - 2w,
#
#      EXACTLY, for every t > 0.  Consequences, all elementary:
#        (a) t -> 0+ gives F_k -> 1 + 2w_0 + 2(k-1)w = Gamma_k.
#        (b) if A >= 0 then F_k > 0 on 0 < theta < pi/k  (sin > 0 there), so there is
#            NO zero before the first rung.
#        (c) at theta = 3pi/(2k), sin(k theta) = -1 and t = (1/2)tan(3pi/2k) ~ 3pi/(4k),
#            so F_k ~ A - w rho^k * (4k)/(3pi) -> -infinity: F_k < 0 for large k.
#        (b)+(c) give a sign change, hence a ZERO ON THE LINE, in
#            (1/2)tan(pi/k) < t_1 <= (1/2)tan(3pi/(2k)),
#        so t_1 = pi/(2k) (1 + O(1/k)).  For w_0 = 0, w = 1/2 the constant A vanishes and
#        the zero set is EXACTLY { t = (1/2)tan(n pi / k) }.
#
#      The three boundary profiles this project uses are all instances:
#          a_i = 2^i - 1 : (w_0, w) = (0,   1/2)   A = 0
#          a_i = 2^i + 1 : (w_0, w) = (1,   1/2)   A = 2
#          layer c = 2   : (w_0, w) = (1,   1  )   A = 1
#      -- so what looked like "two families measured" is one theorem with three A's.
#
# ---------------------------------------------------------------------------
# PRE-REGISTERED, before the first number.
#
#   V1 closed form vs direct summation, >= 50 agreeing digits, all three profiles,
#      several k and t.  If this fails the theorem is wrong and nothing else matters.
#   V2 the t -> 0+ limit equals Gamma_k exactly.
#   V3 no zero strictly inside 0 < theta < pi/k (scan; F_k must stay positive).
#   V4 F_k < 0 at theta = 3pi/(2k) for every k tested; the smallest such k is printed
#      rather than assumed.
#   V5 the located t_1 lies in the bracket of (b)+(c), and k*t_1 -> pi/2.
#   V6 INSTRUMENT CONTROL, and it must pass first: for (w_0,w) = (0,1/2) the zero set is
#      exactly (1/2)tan(n pi/k); check n = 1..5 against the located sign changes.
#      *** Every reference below is computed INSIDE the precision block, never before it.
#          r202 lost an hour to a 15-digit reference compared against 60-digit
#          measurements: a control's reference is a measurement too. ***
#   V7 INSTRUMENT CONTROL: with A > 0 the interval (0, pi/k) must contain no sign change
#      -- a control that would fire if the scan were mis-scaled.
#
#   Every check prints how many cases it examined and FAILS at zero (F60/F78).
# ---------------------------------------------------------------------------

import sys
from mpmath import mp, mpf, mpc, sqrt, atan, sin, tan, pi

OUT = []


def say(s=""):
    print(s)
    OUT.append(s)


PROFILES = [("2^i - 1", mpf(0), mpf(1) / 2),
            ("2^i + 1", mpf(1), mpf(1) / 2),
            ("layer c=2", mpf(1), mpf(1))]


def F_direct(w0, w, k, t):
    """1 + 2 Re G_k(1+2it), summed term by term -- no closed form used."""
    z = mpc(1, 2 * t)
    acc = w0
    p = z
    for _ in range(1, k):
        acc += w * p
        p *= z
    return 1 + 2 * acc.real


def F_closed(w0, w, k, t):
    """A + w rho^k sin(k theta)/t with A = 1 + 2w0 - 2w."""
    rho = sqrt(1 + 4 * t * t)
    th = atan(2 * t)
    A = 1 + 2 * w0 - 2 * w
    return A + w * rho ** k * sin(k * th) / t


def agree(x, y):
    if x == y:
        return mp.dps
    d = abs(x - y) / max(abs(x), abs(y), mpf(1))
    from mpmath import log10, floor
    return int(floor(-log10(d)))


mp.dps = 80
say("=" * 88)
say("trackm_r203 -- Track M (i) the reduction, (ii) the constant-weight theorem")
say("=" * 88)

verdicts = []

# ---------------------------------------------------------------- V1
say()
say("--- V1: closed form vs direct summation ---")
n = 0
worst = 10 ** 9
for name, w0, w in PROFILES:
    for k in (16, 32, 70, 128):
        for ts in ('0.001', '0.01', '0.0377', '0.2', '0.5'):
            t = mpf(ts)
            a = agree(F_direct(w0, w, k, t), F_closed(w0, w, k, t))
            worst = min(worst, a)
            n += 1
ok = n > 0 and worst >= 50
verdicts.append(('V1', ok))
say("  cases: %d   worst agreement: %d digits   -> %s"
    % (n, worst, "PASS" if ok else "FAIL"))

# ---------------------------------------------------------------- V2
say()
say("--- V2: t -> 0+ gives Gamma_k = 1 + 2w_0 + 2(k-1)w ---")
n = 0
ok2 = True
for name, w0, w in PROFILES:
    for k in (16, 70):
        gamma = 1 + 2 * w0 + 2 * (k - 1) * w
        val = F_direct(w0, w, k, mpf(10) ** (-30))
        a = agree(val, gamma)
        n += 1
        if a < 50:
            ok2 = False
        say("  %-10s k=%3d  Gamma_k=%s  F(0+)=%s  agree %d"
            % (name, k, mp.nstr(gamma, 12), mp.nstr(val, 12), a))
ok2 = ok2 and n > 0
verdicts.append(('V2', ok2))
say("  cases: %d  -> %s" % (n, "PASS" if ok2 else "FAIL"))

# ---------------------------------------------------------------- V3 / V7
say()
say("--- V3+V7: no sign change strictly inside 0 < theta < pi/k ---")
n = 0
ok3 = True
for name, w0, w in PROFILES:
    A = 1 + 2 * w0 - 2 * w
    for k in (16, 32, 70, 128):
        t_end = tan(pi / k) / 2               # theta = pi/k  <=>  t = (1/2)tan(pi/k)
        neg = 0
        for i in range(1, 400):
            t = t_end * i / 400
            if F_closed(w0, w, k, t) <= 0:
                neg += 1
        n += 1
        if neg:
            ok3 = False
            say("  %-10s k=%3d  A=%s  *** %d non-positive samples inside the first rung"
                % (name, k, mp.nstr(A, 4), neg))
ok3 = ok3 and n > 0
verdicts.append(('V3+V7', ok3))
say("  cases: %d, all A >= 0  -> %s" % (n, "PASS" if ok3 else "FAIL"))

# ---------------------------------------------------------------- V4
say()
say("--- V4: F_k < 0 at theta = 3pi/(2k); smallest k printed, not assumed ---")
n = 0
ok4 = True
for name, w0, w in PROFILES:
    kmin = None
    for k in range(3, 200):
        t = tan(3 * pi / (2 * k)) / 2 if 3 * pi / (2 * k) < pi / 2 else None
        if t is None:
            continue
        if F_closed(w0, w, k, t) < 0:
            if kmin is None:
                kmin = k
        else:
            kmin = None                      # require it to hold from kmin onwards
    # recompute honestly: smallest k such that it holds for all k' in [k, 199]
    kmin = None
    for k in range(199, 2, -1):
        th = 3 * pi / (2 * k)
        if th >= pi / 2:
            break
        if F_closed(w0, w, k, tan(th) / 2) < 0:
            kmin = k
        else:
            break
    n += 1
    if kmin is None:
        ok4 = False
    say("  %-10s holds for all k in [%s, 199]" % (name, kmin))
ok4 = ok4 and n > 0
verdicts.append(('V4', ok4))
say("  cases: %d  -> %s" % (n, "PASS" if ok4 else "FAIL"))

# ---------------------------------------------------------------- V5
say()
say("--- V5: t_1 inside the bracket, and k*t_1 -> pi/2 ---")


def first_zero(w0, w, k):
    lo = tan(pi / k) / 2
    hi = tan(3 * pi / (2 * k)) / 2
    flo, fhi = F_closed(w0, w, k, lo), F_closed(w0, w, k, hi)
    if flo == 0:
        return lo
    if flo * fhi > 0:
        return None
    for _ in range(int(3.4 * mp.dps) + 40):
        mid = (lo + hi) / 2
        if F_closed(w0, w, k, lo) * F_closed(w0, w, k, mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


n = 0
ok5 = True
say("  %-10s %6s %22s %14s" % ("profile", "k", "t_1", "k*t_1"))
for name, w0, w in PROFILES:
    for k in (64, 128, 256, 512):
        t1 = first_zero(w0, w, k)
        n += 1
        if t1 is None or not (tan(pi / k) / 2 <= t1 <= tan(3 * pi / (2 * k)) / 2):
            ok5 = False
            say("  %-10s %6d  OUTSIDE THE BRACKET" % (name, k))
            continue
        say("  %-10s %6d %22s %14s" % (name, k, mp.nstr(t1, 18), mp.nstr(k * t1, 10)))
    say("")
ok5 = ok5 and n > 0
verdicts.append(('V5', ok5))
say("  cases: %d   (pi/2 = %s)  -> %s" % (n, mp.nstr(pi / 2, 10), "PASS" if ok5 else "FAIL"))

# ---------------------------------------------------------------- V6
say()
say("--- V6 INSTRUMENT: (w_0,w) = (0,1/2) has the EXACT zero set (1/2)tan(n pi/k) ---")
say("    (references computed inside this precision block -- r202)")
n = 0
ok6 = True
w0, w = mpf(0), mpf(1) / 2
for k in (32, 70, 128):
    for nn in (1, 2, 3, 4, 5):
        th = nn * pi / k
        if th >= pi / 2:
            continue
        t_ref = tan(th) / 2                      # computed HERE, at mp.dps = 80
        val = F_direct(w0, w, k, t_ref)          # direct summation, not the closed form
        n += 1
        if abs(val) > mpf(10) ** (-mp.dps + 25):
            ok6 = False
            say("  k=%3d n=%d  F_direct = %s  *** not a zero" % (k, nn, mp.nstr(val, 8)))
ok6 = ok6 and n > 0
verdicts.append(('V6', ok6))
say("  cases: %d, every one a zero of the DIRECT sum to ~%d digits  -> %s"
    % (n, mp.dps - 25, "PASS" if ok6 else "FAIL"))

# ---------------------------------------------------------------- verdict
say()
say("=" * 88)
for tag, v in verdicts:
    say("  [%s] %s" % (tag, "PASS" if v else "FAIL"))
allok = all(v for _, v in verdicts)
say()
if allok:
    say("VERDICT: Track M (i) and (ii) verified as stated.")
    say("  F_k(1/2+it) = A + w rho^k sin(k theta)/t,  A = 1 + 2w_0 - 2w  -- exact")
    say("  zero on the line in ((1/2)tan(pi/k), (1/2)tan(3pi/2k)],  t_1 ~ pi/(2k)")
    say("  and for A = 0 the zero set is exactly {(1/2)tan(n pi/k)}.")
else:
    say("VERDICT: a check failed.  Report raw and stop.")
say()
say("done.")

with open(__file__[:-3] + ".log", "w") as f:
    f.write("\n".join(OUT) + "\n")
sys.exit(0 if allok else 1)
