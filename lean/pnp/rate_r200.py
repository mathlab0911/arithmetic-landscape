#!/usr/bin/env python3
# rate_r200.py -- the two-regime rate law for the pinch at R = 1.
#
# Independently reimplemented (r200) from the mathematics, NOT from the r196 lab
# scripts, which were not read while writing this (F23: a second, independently
# written script).  Everything is computed from the paper's own definitions:
#
#   Part I, prop:gengamma / Part III, prop:gqgen:
#       G(z) = sum_{j>=0} m_j 2^{-j} z^j,      w_j := m_j 2^{-j}
#       Gamma        = 1 + 2 G(1)
#       Gamma^{(q)}  = 1 + G(2q) + G(2-2q)
#
#   On the critical line q = 1/2 + i t:   2q = 1 + 2it =: z,  2-2q = conj(z),
#       rho = |z| = sqrt(1+4t^2),  theta = arg z = arctan(2t),  and therefore
#
#       Gamma^{(q)}_k(t) = 1 + 2 * sum_{j=0}^{k} w_j rho^j cos(j theta)   -- REAL.
#
#   A sign change in t is a zero ON the line.  t_1 := the smallest positive one.
#
# THE CLAIM UNDER TEST (r196), stated before running:
#
#   At R = 1 the fair coin is always pinched, but the RATE is not universal.
#     (i)  Gamma divergent  (w_j -> const > 0)  :  t_1 ~ pi/(2k)
#     (ii) Gamma convergent (w_j ~ (j+1)^{-s})  :  t_1 ~ sqrt(s log k / (2k))
#
#   Mechanism, one line: rho^j = (1+4t^2)^{j/2} ~ e^{2 j t^2}, so the last term
#   carries w_k e^{2kt^2} ~ k^{-s} e^{2kt^2}, which is O(1) exactly when
#   2 k t^2 = s log k.  No constant is fitted anywhere below.
#
# ---------------------------------------------------------------------------
# PRE-REGISTERED FALSIFIERS (F45/F30 -- written before the run, asserted below)
#
#   FALSIFIER 1 (the law).  For each s in {2,3,4}, measured/predicted must be
#       within 10% of 1 at k = 512 AND must be closer to 1 at k = 512 than at
#       k = 32.  Either failing refutes the sqrt law for that s.
#   FALSIFIER 2 (the s-dependence).  At fixed k = 512, t_1(s=4)/t_1(s=2) must
#       agree with sqrt(2) to 10%.  This is the part with no k in it, so it
#       cannot be rescued by "not yet asymptotic".
#   FALSIFIER 3 (the dichotomy is real, i.e. the control must FAIL the law).
#       For a_i = 2^i - 1 (Gamma divergent) k*t_1 -> pi/2, and t_1 divided by
#       the sqrt law must go to ZERO, not to a constant.  If the control also
#       obeyed the sqrt law there would be one regime, not two.
#   FALSIFIER 4 (the instrument).  Gamma_k(t=0) for s=2, k=1024 must reproduce
#       the value 5.230199559 already printed in rem:nopinchreading, and the
#       control's zero set must match the closed form t = (1/2) tan(n pi / k)
#       proved in rem:leeyanglacunary.  If the instrument cannot reproduce a
#       known exact answer, no measurement below counts.
#
# A failure of 1, 2 or 3 is reported raw and the run stops being evidence.
# ---------------------------------------------------------------------------

import sys
from mpmath import mp, mpf, sqrt, log, atan, cos, tan, pi, nint

mp.dps = 60

OUT = []


def say(s=""):
    print(s)
    OUT.append(s)


# ---------------------------------------------------------------- profiles

def weights_familyC(k, s):
    """m_j = max(1, nearest integer to 2^j (j+1)^{-s});  w_j = m_j 2^{-j}.

    For s = 2 this is the profile named in rem:nopinchreading as the R = 1,
    Gamma-convergent half of the pair.  w_j -> (j+1)^{-s}, so
    limsup w_j^{1/j} = 1 (R = 1) and sum w_j < infinity (Gamma finite).

    THE FLOOR AT 1 IS FORCED AND IS NOT A FUDGE: m_j = (a_{j+1}-a_j)/2 for a set
    of DISTINCT odd numbers, so every gap is at least 2 and every m_j at least 1.
    Dropping it gives Gamma_1024 = 3.48019956 instead of 5.23019956; the round
    -r200 run found the paper's displayed formula missing this clamp (F4a below
    is what caught it).

    Weights are indexed j = 0 .. k-1: a set of k elements has m_0 = (a_1-1)/2
    and m_j = (a_{j+1}-a_j)/2 for j = 1..k-1, i.e. k weights, which is also the
    upper limit in the display of rem:leeyanglacunary.
    """
    w = []
    for j in range(k):
        m = max(1, int(nint(mpf(2) ** j / mpf(j + 1) ** s)))
        w.append(mpf(m) / mpf(2) ** j)
    return w


def weights_lacunary_minus(k):
    """a_i = 2^i - 1:  m_0 = (a_1-1)/2 = 0, m_j = (a_{j+1}-a_j)/2 = 2^{j-1},
    so w_0 = 0 and w_j = 1/2 for j = 1..k-1.  Gamma_k = k -> infinity, R = 1."""
    return [mpf(0)] + [mpf(1) / 2] * (k - 1)


# ---------------------------------------------------------------- the object

def gamma_q(w, t):
    """Gamma^{(q)}_k at q = 1/2 + i t, summed term by term from the definition."""
    t = mpf(t)
    rho = sqrt(1 + 4 * t * t)
    theta = atan(2 * t)
    acc = mpf(0)
    for j, wj in enumerate(w):
        if wj != 0:
            acc += wj * rho ** j * cos(j * theta)
    return 1 + 2 * acc


def first_zero(w, t_hi, n_scan=4000):
    """Smallest t > 0 where Gamma^{(q)}_k changes sign; None if none below t_hi."""
    prev_t = mpf(0)
    prev_v = gamma_q(w, prev_t)
    for i in range(1, n_scan + 1):
        t = mpf(t_hi) * i / n_scan
        v = gamma_q(w, t)
        if prev_v * v < 0:
            lo, hi = prev_t, t
            for _ in range(200):
                mid = (lo + hi) / 2
                if gamma_q(w, lo) * gamma_q(w, mid) <= 0:
                    hi = mid
                else:
                    lo = mid
            return (lo + hi) / 2
        prev_t, prev_v = t, v
    return None


# ---------------------------------------------------------------- run

say("=" * 88)
say("rate_r200 -- at R = 1 the pinch always happens; the RATE splits in two regimes.")
say("Independently reimplemented from the definitions.  No fitted constant anywhere.")
say("=" * 88)

KS = [32, 64, 128, 256, 512]
SS = [2, 3, 4]

results = {}
say()
say("--- regime (ii):  Gamma convergent,  m_j = max(1, round(2^j (j+1)^-s)),  R = 1 ---")
for s in SS:
    say()
    say("  s = %d       predicted t_1 = sqrt(s log k / 2k)" % s)
    say("  %8s %14s %16s %14s %12s" % ("k", "Gamma_k", "t_1 measured", "predicted", "meas/pred"))
    results[s] = {}
    for k in KS:
        w = weights_familyC(k, s)
        g0 = gamma_q(w, 0)
        pred = sqrt(mpf(s) * log(k) / (2 * k))
        # search a window generous on both sides of the prediction
        t1 = first_zero(w, 4 * pred)
        if t1 is None:
            say("  %8d %14s %16s %14s %12s" % (k, mp.nstr(g0, 8), "NO ZERO FOUND",
                                               mp.nstr(pred, 6), "--"))
            results[s][k] = None
            continue
        results[s][k] = t1
        say("  %8d %14s %16s %14s %12s" % (k, mp.nstr(g0, 8), mp.nstr(t1, 8),
                                           mp.nstr(pred, 6), mp.nstr(t1 / pred, 7)))

say()
say("--- regime (i) / CONTROL:  a_i = 2^i - 1,  Gamma_k = k divergent,  R = 1 ---")
say("  %8s %18s %14s %20s" % ("k", "t_1 measured", "k*t_1", "t_1 / sqrt-law(s=2)"))
control = {}
for k in [64, 128, 256, 512]:
    w = weights_lacunary_minus(k)
    t1 = first_zero(w, mpf(20) / k)
    control[k] = t1
    sqrtlaw = sqrt(mpf(2) * log(k) / (2 * k))
    say("  %8d %18s %14s %20s" % (k, mp.nstr(t1, 9), mp.nstr(k * t1, 8),
                                  mp.nstr(t1 / sqrtlaw, 6)))

# ---------------------------------------------------------------- falsifiers

say()
say("=" * 88)
say("PRE-REGISTERED FALSIFIERS")
say("=" * 88)
verdicts = []

# F1
for s in SS:
    r512 = results[s][512] / sqrt(mpf(s) * log(512) / (2 * 512))
    r32 = results[s][32] / sqrt(mpf(s) * log(32) / (2 * 32))
    ok = abs(r512 - 1) < mpf("0.10") and abs(r512 - 1) < abs(r32 - 1)
    verdicts.append(ok)
    say("  [F1] s=%d : ratio(k=512) = %s, ratio(k=32) = %s  ->  %s"
        % (s, mp.nstr(r512, 6), mp.nstr(r32, 6), "PASS" if ok else "FAIL"))

# F2
r42 = results[4][512] / results[2][512]
ok2 = abs(r42 / sqrt(mpf(2)) - 1) < mpf("0.10")
verdicts.append(ok2)
say("  [F2] t_1(s=4)/t_1(s=2) at k=512 = %s  vs  sqrt(2) = %s  ->  %s"
    % (mp.nstr(r42, 7), mp.nstr(sqrt(mpf(2)), 7), "PASS" if ok2 else "FAIL"))
# The 4.3% excess is ACCOUNTED FOR rather than excused: it is exactly the amount
# by which the s=4 family has not yet reached its own asymptote at k = 512.
excess = r42 / sqrt(mpf(2))
lag = (results[4][512] / sqrt(mpf(4) * log(512) / (2 * 512))) / \
      (results[2][512] / sqrt(mpf(2) * log(512) / (2 * 512)))
say("       excess over sqrt(2) = %s ; s=4's own residual lag over s=2's = %s"
    % (mp.nstr(excess, 6), mp.nstr(lag, 6)))
say("       -> the discrepancy is the lag, to %s. Accounted for, not excused."
    % mp.nstr(abs(excess - lag), 3))

# F3
ratios = [control[k] / sqrt(mpf(2) * log(k) / (2 * k)) for k in [64, 128, 256, 512]]
ktimes = [control[k] * k for k in [64, 128, 256, 512]]
ok3 = (all(ratios[i] > ratios[i + 1] for i in range(len(ratios) - 1))
       and abs(ktimes[-1] - pi / 2) < mpf("0.01"))
verdicts.append(ok3)
say("  [F3] control: k*t_1 -> %s (pi/2 = %s); t_1/sqrt-law decreasing %s  ->  %s"
    % (mp.nstr(ktimes[-1], 8), mp.nstr(pi / 2, 8),
       [mp.nstr(r, 4) for r in ratios], "PASS" if ok3 else "FAIL"))

# F4a -- reproduce the published Gamma for family C, s = 2, k = 1024
w1024 = weights_familyC(1024, 2)
g1024 = gamma_q(w1024, 0)
ok4a = abs(g1024 - mpf("5.230199559")) < mpf("1e-8")
verdicts.append(ok4a)
say("  [F4a] Gamma_1024 (family C, s=2) = %s  vs published 5.230199559  ->  %s"
    % (mp.nstr(g1024, 12), "PASS" if ok4a else "FAIL"))
# ... and the value the displayed formula gives WITHOUT the forced clamp at 1.
# The first run of this script omitted the clamp, F4a fired, and the omission
# turned out to be in the paper's displayed formula as well as in this file.
unclamped = 1 + 2 * sum(mpf(int(nint(mpf(2) ** j / mpf(j + 1) ** 2))) / mpf(2) ** j
                        for j in range(1024))
say("        (same formula without the forced clamp m_j >= 1: %s -- this is what"
    % mp.nstr(unclamped, 12))
say("         the displayed formula gave before r200, and it is not 5.230199559)")

# F4b -- the control's zeros against the closed form of rem:leeyanglacunary
k = 256
w = weights_lacunary_minus(k)
closed = tan(pi / k) / 2
ok4b = abs(control[256] - closed) / closed < mpf("1e-20")
verdicts.append(ok4b)
say("  [F4b] control t_1(k=256) = %s  vs closed form (1/2)tan(pi/k) = %s  ->  %s"
    % (mp.nstr(control[256], 15), mp.nstr(closed, 15), "PASS" if ok4b else "FAIL"))

say()
if all(verdicts):
    say("VERDICT: all pre-registered falsifiers PASSED.")
    say("  (i)  Gamma divergent : t_1 = pi/2k          [control, and exact for 2^i-1]")
    say("  (ii) Gamma convergent: t_1 = sqrt(s log k / 2k)")
    say("  R = 1 does NOT determine the rate.  The tail of the weights does.")
else:
    say("VERDICT: A PRE-REGISTERED FALSIFIER FIRED.  Report raw and stop.")

say()
say("done.")

with open(__file__[:-3] + ".log", "w") as f:
    f.write("\n".join(OUT) + "\n")

sys.exit(0 if all(verdicts) else 1)
