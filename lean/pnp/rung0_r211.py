#!/usr/bin/env python3
# rung0_r211.py -- fable-5's r207 Ruling 2, rung 0: the phase picture must POSTDICT the
# known scale sqrt(s log k / 2k) from its own mechanism before it earns an instrument.
#
# THE MODEL, written down before any number is produced.
#
# On the line, z = 1 + 2it, rho = |z|, theta = arg z, and
#     G_k(z) = sum_{j<k} w_j z^j .
# Split it into a HEAD and a TAIL.
#
#   HEAD.  For j small, rho^j ~ 1 and j theta is small, so the head contributes
#          approximately H := sum_{j<k} w_j -- real and positive, the value at t = 0.
#
#   TAIL.  For j near k the weights are nearly constant (w_j varies by a factor
#          1 + s/(lambda log k) -> 1 over the range 1/log rho on which |z|^j drops by e),
#          so the tail is a geometric sum:
#              sum_{j near k} w_j z^j  ~  w_{k-1} z^k / (z - 1) ,
#          of modulus  T := w_{k-1} rho^k / (2t)   -- since z - 1 = 2it --
#          and argument  k theta - pi/2, BECAUSE arg(1/(z-1)) = -pi/2 exactly.
#
#   THE PHASE.  So Re G_k ~ H + T sin(k theta): the tail's quarter-turn converts the
#   cosine into a sine, which is the same quarter turn that corrected this project's
#   cos/sin error at r194.  A zero of F_k = 1 + 2 Re G_k needs Re G_k = -1/2, hence
#
#            T  >=  H + 1/2 ,
#
#   and the first zero sits essentially where that becomes possible.  The model's
#   prediction t_model is therefore the smallest t > 0 with T(t) = H + 1/2.
#
# WHAT THE MODEL PREDICTS ASYMPTOTICALLY.  With w_j ~ (j+1)^-s and 2kt^2 = lambda log k,
#   T = k^{-s} e^{2kt^2} / (2t) = k^{lambda - s} / (2t),
# so T = H + 1/2 gives  k^{lambda - s} = 2t(H + 1/2), and t ~ sqrt(log k / k) gives
#   lambda - s = -1/2 + (log log k)/(2 log k) + O(1/log k).
# So the model DOES reproduce the sqrt(s log k / 2k) SCALE -- that is rung 0's question --
# and it says the constant tends to s - 1/2 with a correction that decays like 1/log k.
#
# ---------------------------------------------------------------------------
# PRE-REGISTERED, before the first number.
#
#   RUNG 0 PASS CRITERION (the gate fable set).  The model, solved for t with no fitted
#     parameter, must reproduce the MEASURED first zero t_1 to within 15% at every (k, s)
#     tested.  Reproducing the scale is the requirement; the 15% band is stated in advance
#     so that "it postdicts the scale" cannot be decided after seeing the numbers.
#   R0-FAIL  If it misses by more than 15% anywhere, rung 0 does NOT pass, the phase
#     instrument is not built, and the miss is reported raw as a finding about the
#     mechanism -- which is the outcome fable named.
#
#   D1 (the consequence, computed either way).  Print the model's own lambda,
#     lambda_model = 2k t_model^2 / log k, beside the measured lambda_eff and beside the
#     asymptote s - 1/2.  If the model fits the data while its asymptote is s - 1/2, then
#     r206's refutation of "shape B" tested a limit the model says is approached like
#     1/log k, and that refutation must be re-stated.  This is registered NOW so that the
#     conclusion cannot be built after the fact.
#
#   INSTRUMENT (passes first).  Constant weights w_0 = 0, w_j = 1/2 have the zero set
#     proved exactly at t = (1/2)tan(n pi/k) (Theorem 2(e), proved r205).  The same code
#     path must reproduce t_1 to >= 25 digits.  Reference computed INSIDE the precision
#     block (r202).
#
#   Populations printed; a verdict over an empty population is a FAIL (F60).
# ---------------------------------------------------------------------------

import io
import sys
from mpmath import mp, mpf, sqrt, log, atan, cos, tan, pi, findroot

LOG = __file__[:-3] + ".log"
OUT = []


def say(s=""):
    print(s, flush=True)
    OUT.append(s)
    io.open(LOG, "w", encoding="utf-8", newline="\n").write("\n".join(OUT) + "\n")


mp.dps = 40


def w_power(k, s):
    s = mpf(s)
    return [mpf(1) / mpf(j + 1) ** s for j in range(k)]


def w_const(k):
    return [mpf(0)] + [mpf(1) / 2] * (k - 1)


def F(w, t):
    rho, th = sqrt(1 + 4 * t * t), atan(2 * t)
    a = mpf(0)
    for j, wj in enumerate(w):
        if wj != 0:
            a += wj * rho ** j * cos(j * th)
    return 1 + 2 * a


def first_zero(w, t_hi, n_scan=1500):
    pt, pv = mpf(0), F(w, mpf(0))
    for i in range(1, n_scan + 1):
        t = mpf(t_hi) * i / n_scan
        v = F(w, t)
        if pv * v < 0:
            lo, hi = pt, t
            for _ in range(120):
                mid = (lo + hi) / 2
                if F(w, lo) * F(w, mid) <= 0:
                    hi = mid
                else:
                    lo = mid
            return (lo + hi) / 2
        pt, pv = t, v
    return None


def t_model(w, k):
    """smallest t > 0 with T(t) = H + 1/2, where T = w_{k-1} rho^k /(2t), H = sum w_j."""
    H = sum(w)
    wk = w[-1]
    g = lambda t: wk * (1 + 4 * t * t) ** (mpf(k) / 2) / (2 * t) - (H + mpf(1) / 2)
    # T is large for tiny t (1/2t blows up) and large again for big t; the crossing we
    # want is the FIRST t where T comes back UP to H+1/2 after its minimum.  Locate the
    # minimum, then bisect to its right.
    lo, hi = mpf('1e-12'), mpf('0.9')
    n = 4000
    best_t, best_v = None, None
    for i in range(1, n + 1):
        t = lo + (hi - lo) * i / n
        v = wk * (1 + 4 * t * t) ** (mpf(k) / 2) / (2 * t)
        if best_v is None or v < best_v:
            best_v, best_t = v, t
    if best_v > H + mpf(1) / 2:
        return None                      # never dips below the threshold: no crossing
    a, b = best_t, hi
    if g(a) * g(b) > 0:
        return None
    for _ in range(200):
        m = (a + b) / 2
        if g(a) * g(m) <= 0:
            b = m
        else:
            a = m
    return (a + b) / 2


say("=" * 96)
say("rung0_r211 -- does the phase picture postdict the sqrt(s log k / 2k) scale?")
say("model: Re G_k ~ H + T sin(k theta),  T = w_{k-1} rho^k /(2t),  H = sum_j w_j")
say("       first zero possible when T = H + 1/2.  No fitted parameter.")
say("=" * 96)

verdicts = []

say()
say("--- INSTRUMENT: constant weights, zero set proved exactly (Thm 2(e)) ---")
okI, nI = True, 0
for k in (64, 256):
    ref = tan(pi / k) / 2                      # computed here, at mp.dps = 40 (r202)
    got = first_zero(w_const(k), 4 * ref)
    rel = abs(got - ref) / ref if got else mpf(1)
    nI += 1
    if rel > mpf(10) ** (-25):
        okI = False
    say("  k=%4d proved=%s measured=%s rel=%s"
        % (k, mp.nstr(ref, 20), mp.nstr(got, 20) if got else "none", mp.nstr(rel, 4)))
verdicts.append(('instrument', okI and nI > 0))
say("  cases: %d -> %s" % (nI, "PASS" if okI and nI > 0 else "FAIL"))
if not okI:
    sys.exit(1)

SS = ['1', '1.5', '2', '3', '4']
KS = [64, 128, 256, 512, 1024]

say()
say("--- RUNG 0: model against measurement, no fitted parameter ---")
say("  %5s %5s %16s %16s %10s %10s %10s %10s"
    % ("s", "k", "t_1 measured", "t_model", "ratio", "lam_eff", "lam_model", "s-1/2"))
rows = []
n_pop = 0
worst = mpf(0)
for ss in SS:
    s = mpf(ss)
    for k in KS:
        w = w_power(k, ss)
        pred = sqrt(s * log(k) / (2 * k))
        t1 = first_zero(w, 3 * pred)
        tm = t_model(w, k)
        if t1 is None or tm is None:
            say("  %5s %5d  not found" % (ss, k))
            continue
        r = tm / t1
        lam_eff = 2 * k * t1 * t1 / log(k)
        lam_mod = 2 * k * tm * tm / log(k)
        n_pop += 1
        worst = max(worst, abs(r - 1))
        rows.append((ss, k, t1, tm, r, lam_eff, lam_mod))
        say("  %5s %5d %16s %16s %10s %10s %10s %10s"
            % (ss, k, mp.nstr(t1, 10), mp.nstr(tm, 10), mp.nstr(r, 6),
               mp.nstr(lam_eff, 6), mp.nstr(lam_mod, 6), mp.nstr(s - mpf(1) / 2, 4)))
    say("")

ok0 = n_pop > 0 and worst < mpf('0.15')
verdicts.append(('rung 0 (15% band)', ok0))
say("  population: %d   worst |model/measured - 1| = %s   -> %s"
    % (n_pop, mp.nstr(worst, 5), "PASS" if ok0 else "FAIL"))

say()
say("--- D1: the consequence, registered before the run ---")
if rows:
    say("  %5s %8s %12s %12s %12s" % ("s", "k", "lam_eff - s", "lam_mod - s", "target -0.5"))
    for ss, k, t1, tm, r, le, lm in rows:
        s = mpf(ss)
        say("  %5s %8d %12s %12s %12s"
            % (ss, k, mp.nstr(le - s, 5), mp.nstr(lm - s, 5), "-0.5"))
    say()
    say("  The model's own lambda sits well ABOVE s - 1/2 at these k, because the")
    say("  approach is  lambda - s = -1/2 + (log log k)/(2 log k) + O(1/log k),  and")
    say("  at k = 1024 the correction term alone is %s."
        % mp.nstr(log(log(mpf(1024))) / (2 * log(mpf(1024))), 5))
else:
    verdicts.append(('D1 population', False))

say()
say("=" * 96)
for tag, v in verdicts:
    say("  [%s] %s" % (tag, "PASS" if v else "FAIL"))
allok = all(v for _, v in verdicts)
say()
if allok:
    say("RUNG 0: PASSED.  The phase picture reproduces the measured first zero with no")
    say("  fitted parameter, so it has earned the instrument.  AND -- per D1, registered")
    say("  in advance -- its asymptote is s - 1/2 with a 1/log k approach, which means")
    say("  r206's refutation of 'shape B' tested a limit this model says is approached")
    say("  far too slowly to be seen at k <= 2048.  That refutation must be re-stated.")
else:
    say("RUNG 0: NOT PASSED.  The instrument is not built.  Reporting raw, which is the")
    say("  outcome fable-5 named: a miss here is a finding about the mechanism.")
say()
say("done.")
sys.exit(0 if allok else 1)
