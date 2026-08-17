#!/usr/bin/env python3
# divide_r204.py -- testing the conjectured dividing line of Track M part (iv).
#
# The conjecture (r196, restated for the note): at R = 1 the pinch always happens, and
#
#        sum_j w_j = infinity   ->   t_1 ~ pi/(2k)
#        sum_j w_j < infinity,  w_j ~ (j+1)^-s   ->   t_1 ~ sqrt(s log k / 2k)
#
# so the dividing line is the CONVERGENCE OF sum w_j and nothing finer.
#
# THE LINE HAS NEVER BEEN TESTED ON THE LINE.  Every divergent-side profile measured so
# far has CONSTANT weights (w_j = 1/2 or 1), which r203's Theorem 2 now covers outright.
# Every convergent-side profile decays like a power.  So the evidence is consistent with
# a different and weaker statement --
#
#        "constant weights -> pi/2k ;  decaying weights -> sqrt law"
#
# -- which would put the dividing line at DECAY, not at SUMMABILITY.  The two hypotheses
# separate exactly on profiles that decay but are not summable.
#
#   THE HARMONIC FAMILY  w_j = 1/(j+1):  w_j -> 0, sum = infinity, R = 1.
#
#   PRE-REGISTERED DECISION RULE, before the first number:
#     * if k*t_1 -> pi/2 = 1.5707963  ->  the dividing line is SUMMABILITY.  Confirmed at
#       the sharpest point available, on a profile the existing theorem does not cover.
#     * if t_1 / sqrt(1*log k / 2k) -> a constant instead  ->  the conjecture as stated is
#       REFUTED and the dividing line is decay, not summability.
#     * if neither, report raw and stop; a third rate is a finding and not a failure.
#
#   FALSIFIER (instrument, passes first).  On w_j = 1/2 constant, Theorem 2 gives the
#   zero set EXACTLY at t = (1/2)tan(n pi/k) when w_0 = 0.  The same code path must
#   reproduce t_1 = (1/2)tan(pi/k) to >= 30 digits.  References are computed INSIDE the
#   precision block (r202).
#
#   SECOND FAMILY, to separate "not summable" from "barely not summable":
#   w_j = 1/((j+2) log(j+2)) -- still divergent, but only just.  Same decision rule.
#
#   CONTROL on the other side: w_j = (j+1)^-1.5, summable, must follow the sqrt law with
#   s = 1.5 and must NOT give k*t_1 -> pi/2.
#
#   Every check prints its population and fails at zero (F60/F78).

import sys
from mpmath import mp, mpf, mpc, sqrt, log, atan, cos, tan, pi

OUT = []


def say(s=""):
    print(s)
    OUT.append(s)


mp.dps = 60


def w_const(k):
    return [mpf(0)] + [mpf(1) / 2] * (k - 1)


def w_harmonic(k):
    return [mpf(1) / (j + 1) for j in range(k)]


def w_loglog(k):
    return [mpf(1) / ((j + 2) * log(j + 2)) for j in range(k)]


def w_power(k, s):
    return [mpf(1) / mpf(j + 1) ** mpf(s) for j in range(k)]


def F(w, t):
    """1 + 2 Re G_k(1+2it), by direct summation."""
    rho = sqrt(1 + 4 * t * t)
    th = atan(2 * t)
    acc = mpf(0)
    for j, wj in enumerate(w):
        if wj != 0:
            acc += wj * rho ** j * cos(j * th)
    return 1 + 2 * acc


def first_zero(w, t_hi, n_scan=3000):
    prev_t, prev_v = mpf(0), F(w, mpf(0))
    for i in range(1, n_scan + 1):
        t = mpf(t_hi) * i / n_scan
        v = F(w, t)
        if prev_v * v < 0:
            lo, hi = prev_t, t
            for _ in range(160):
                mid = (lo + hi) / 2
                if F(w, lo) * F(w, mid) <= 0:
                    hi = mid
                else:
                    lo = mid
            return (lo + hi) / 2
        prev_t, prev_v = t, v
    return None


say("=" * 92)
say("divide_r204 -- is the dividing line SUMMABILITY, or merely DECAY?")
say("The two hypotheses separate on profiles that decay but do not sum.  Nothing measured")
say("so far lives there: every divergent-side profile to date has CONSTANT weights.")
say("=" * 92)

verdicts = []

# ---------------------------------------------------------------- instrument
say()
say("--- FALSIFIER (instrument): constant w = 1/2, w_0 = 0 -> t_1 = (1/2)tan(pi/k) exactly ---")
okI, nI = True, 0
for k in (64, 128):
    ref = tan(pi / k) / 2                    # computed here, at mp.dps = 60 (r202)
    got = first_zero(w_const(k), 4 * ref)
    d = abs(got - ref) / ref
    nI += 1
    say("  k=%4d  exact=%s  measured=%s  rel.diff=%s"
        % (k, mp.nstr(ref, 24), mp.nstr(got, 24), mp.nstr(d, 4)))
    if d > mpf(10) ** (-30):
        okI = False
okI = okI and nI > 0
verdicts.append(('instrument', okI))
say("  cases: %d  -> %s" % (nI, "PASS" if okI else "FAIL"))
if not okI:
    say()
    say("VERDICT: the instrument cannot reproduce a proved exact value.  Stop.")
    open(__file__[:-3] + ".log", "w").write("\n".join(OUT) + "\n")
    sys.exit(1)

# ---------------------------------------------------------------- the test
KS = [64, 128, 256, 512, 1024]

FAMS = [
    ("harmonic  1/(j+1)",        w_harmonic, "divergent"),
    ("1/((j+2)log(j+2))",        w_loglog,   "divergent, barely"),
    ("power s=1.5",              lambda k: w_power(k, '1.5'), "convergent"),
]

results = {}
for name, wf, side in FAMS:
    say()
    say("--- %s   (%s) ---" % (name, side))
    say("  %6s %14s %22s %14s %16s" % ("k", "Gamma_k", "t_1", "k*t_1", "t_1/sqrt-law"))
    results[name] = {}
    for k in KS:
        w = wf(k)
        gam = 1 + 2 * sum(w)
        # search wide enough to contain BOTH candidate scales
        t_hi = max(mpf(20) / k, 4 * sqrt(mpf(2) * log(k) / (2 * k)))
        t1 = first_zero(w, t_hi)
        if t1 is None:
            say("  %6d %14s %22s" % (k, mp.nstr(gam, 8), "NO ZERO FOUND"))
            continue
        s_eff = mpf('1.5') if 'power' in name else mpf(1)
        law = sqrt(s_eff * log(k) / (2 * k))
        results[name][k] = t1
        say("  %6d %14s %22s %14s %16s"
            % (k, mp.nstr(gam, 8), mp.nstr(t1, 16), mp.nstr(k * t1, 10),
               mp.nstr(t1 / law, 8)))

# ---------------------------------------------------------------- decision
say()
say("=" * 92)
say("DECISION, by the rule registered before the run")
say("=" * 92)
say("  pi/2 = %s" % mp.nstr(pi / 2, 10))
n_dec = 0
verdict_lines = []
for name, wf, side in FAMS:
    r = results[name]
    if len(r) < 2:
        continue
    ks = sorted(r)
    kt = [k * r[k] for k in ks]
    s_eff = mpf('1.5') if 'power' in name else mpf(1)
    ratio = [r[k] / sqrt(s_eff * log(k) / (2 * k)) for k in ks]
    d_pi = abs(kt[-1] - pi / 2)
    flat_sqrt = abs(ratio[-1] - ratio[-2]) < abs(ratio[-1]) / 20
    n_dec += 1
    if d_pi < mpf('0.02'):
        v = "follows pi/2k"
    elif flat_sqrt:
        v = "follows the sqrt law (ratio settling)"
    else:
        v = "NEITHER -- report raw"
    verdict_lines.append((name, side, mp.nstr(kt[-1], 8), mp.nstr(ratio[-1], 6), v))
    say("  %-22s %-20s k*t_1=%-12s t_1/sqrt=%-10s  %s"
        % (name, side, mp.nstr(kt[-1], 8), mp.nstr(ratio[-1], 6), v))

ok_pop = n_dec == len(FAMS)
verdicts.append(('population', ok_pop))
say()
say("  families decided: %d of %d  -> %s"
    % (n_dec, len(FAMS), "PASS" if ok_pop else "FAIL -- a family produced no verdict"))

say()
harm = [v for v in verdict_lines if v[0].startswith('harmonic')]
if harm and harm[0][4] == "follows pi/2k":
    say("CONCLUSION: the dividing line is SUMMABILITY.  A profile that DECAYS but does not")
    say("SUM still takes the pi/2k rate, so the split is not decay-versus-constant.  This is")
    say("the first divergent-side profile measured that Theorem 2 does not already cover.")
elif harm:
    say("CONCLUSION: the conjecture as stated is REFUTED or unresolved on the harmonic family;")
    say("see the row above.  The dividing line is not summability as written.")
say()
say("done.")

open(__file__[:-3] + ".log", "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(v for _, v in verdicts) else 1)
