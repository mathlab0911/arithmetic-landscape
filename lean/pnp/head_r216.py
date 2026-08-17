#!/usr/bin/env python3
# head_r216.py -- fable-5's r212 optional task: does the head/tail model get the
# s-DEPENDENCE right, not just the scale?
#
# ---------------------------------------------------------------------------
# WHY THIS RUN EXISTS.  rung0_r211 passed: the model reproduces t_1 to 9.9% at every
# (k, s), with nothing fitted.  But reading its own D1 table across s at fixed k:
#
#     k = 1024      s=1      s=1.5    s=2      s=3      s=4
#     lam_mod - s   -0.0038  -0.1130  -0.1320  -0.1014  -0.0425
#     lam_eff - s   -0.1275  -0.0622  -0.1337  +0.0307  +0.0715
#
# the model puts s=1 HIGHEST and the measurement puts it near the BOTTOM.  The model
# fits every t_1 and still disagrees about the shape of the s-dependence.  This run
# asks why, and whether it can be repaired from the mechanism rather than by fitting.
#
# ---------------------------------------------------------------------------
# THE DIAGNOSIS, WRITTEN DOWN BEFORE ANY NUMBER IS PRODUCED.
#
# v1 (r211) approximates  Re G_k(1+2it) = sum_{j<k} w_j rho^j cos(j theta)  by
#
#       H + T sin(k theta),     H := sum_{j<k} w_j ,     T := w_{k-1} rho^k / (2t),
#
# i.e. it evaluates the HEAD AT t = 0.  That is where the error must live, because the
# tail is a geometric sum whose weight really is nearly constant over its effective
# length.  Concretely: at t ~ t_1 = sqrt(s log k / 2k) the tail's effective length is
# 1/|z-1| ~ 1/(2t) ~ sqrt(k / 2 log k), so the weights it samples differ from w_{k-1}
# by 1 + O(s/sqrt(k log k)) -- negligible.
#
# But the HEAD runs to the same place, j ~ 1/(2t), and there
#
#       j theta  ~  2 j t  ~  1 ,
#
# which is NOT small.  The head's phase has turned by order one before the head ends.
# v1 sets cos(j theta) = 1 for all of it.  (Its growth rho^j = e^{2jt^2} IS negligible
# there: 2jt^2 ~ sqrt(log k / k) -> 0.  So the phase is the whole of the error.)
#
# HOW MUCH THIS COSTS, AND WHY IT IS AN s-DEPENDENT COST -- this is the prediction.
#
#   s > 1:  sum_j (j+1)^{-s} converges, so keeping the phase changes H by O(1).
#   s = 1:  sum_j cos(j theta)/(j+1) ~ log(1/theta) ~ log sqrt(k/2log k) ~ (1/2) log k,
#           whereas H = log k + gamma.  THE PHASE HALVES THE HEAD, and it halves it
#           only in the one column where the head diverges.
#
# So the head's phase is exactly an s=1 effect, and s=1 is exactly the column where
# the model and the measurement disagree.  Hence:
#
# MODEL v2:   Re G_k  ~  Hp(theta) + T sin(k theta),   Hp(theta) := sum_{j<k} w_j cos(j theta),
#             first zero where  T = Hp + 1/2.   Still nothing fitted.
#
# Note v2 does NOT change the asymptote: log(Hp+1/2) = log log k - log 2 + o(1) at s=1,
# so lambda - s = -1/2 + (3/2)(log log k)/(log k) + O(1/log k) survives, with a shifted
# O(1/log k).  The claim under test is about the COMPUTABLE range, not the limit.
#
# ---------------------------------------------------------------------------
# PRE-REGISTERED, before the first number.  (25 pairs: s in {1,1.5,2,3,4}, k <= 1024.)
#
#   P1  ACCURACY.  v2's worst |t_model/t_1 - 1| over the 25 pairs is STRICTLY SMALLER
#       than v1's (which was 0.098723).  If v2 is not better, the head phase is not
#       what is wrong with v1 and the diagnosis above is refuted.
#
#   P2  THE POINT: THE IMPROVEMENT MUST BE CONCENTRATED AT s = 1.  Define the
#       improvement I(k,s) := |ratio_v1 - 1| - |ratio_v2 - 1|.  Require
#             mean_k I(k, 1)  >  mean_k I(k, 4).
#       A uniform improvement would mean v2 is simply a better fit, not that the
#       head's phase is the s-dependent mechanism.  THIS IS THE FALSIFIER FOR THE
#       EXPLANATION, as opposed to for the numbers.
#
#   P3  RESOLUTION, BEFORE ANY CLAIM ABOUT ORDERING (the r211 rule: a refutation needs
#       a resolution claim -- applied here to an assertion instead).  lambda = 2kt^2/log k
#       is quadratic in t, so a relative error e in t is 2e in lambda.  Print
#             resolution(k) := 2 * max_s |ratio - 1| * lambda      (in lambda units)
#       beside
#             spread(k)     := max_s (lam_mod - s) - min_s (lam_mod - s).
#       IF resolution >= spread, THEN THE MODEL CANNOT ANSWER THE ORDERING QUESTION AT
#       THIS k, and this run must report that instead of an ordering.  Registered now
#       so the verdict is not chosen after seeing which way it falls.
#
#   P4  ORDERING, admissible only if P3 leaves room.  Does v2 reproduce the measured
#       ordering of (lambda - s) across s at k = 1024?  Kendall-tau-style: count the
#       concordant pairs among the 10 unordered pairs of the five s values.
#
#   INSTRUMENT (runs first, must pass or the run aborts).  Constant weights w_0 = 0,
#       w_j = 1/2: the zero set is proved exactly at t = (1/2)tan(n pi/k), Thm 2(e),
#       proved r205.  The scanner must reproduce t_1 to >= 25 digits.  Reference
#       computed INSIDE the precision block (r202).
#
#   SECOND INSTRUMENT (new here).  v2 must REDUCE to v1 when the phase is switched off:
#       computing Hp at theta = 0 must return H exactly.  A refinement that cannot
#       reproduce the thing it refines is a different model, not a refinement.
#
#   Populations printed.  A verdict over an empty population is a FAIL (F60).
# ---------------------------------------------------------------------------

import io
import sys
from mpmath import mp, mpf, sqrt, log, atan, cos, tan, pi

LOG = __file__[:-3] + ".log"
OUT = []


def say(s=""):
    print(s, flush=True)
    OUT.append(s)
    io.open(LOG, "w", encoding="utf-8", newline="\n").write("\n".join(OUT) + "\n")


mp.dps = 30


def w_power(k, s):
    s = mpf(s)
    return [mpf(1) / mpf(j + 1) ** s for j in range(k)]


def w_const(k):
    return [mpf(0)] + [mpf(1) / 2] * (k - 1)


def F(w, t):
    """1 + 2 Re G_k(1+2it), exactly (the object itself, not a model)."""
    rho, th = sqrt(1 + 4 * t * t), atan(2 * t)
    a = mpf(0)
    for j, wj in enumerate(w):
        if wj != 0:
            a += wj * rho ** j * cos(j * th)
    return 1 + 2 * a


def first_zero(w, t_hi, n_scan=1500):
    """scan upward FROM ZERO and bisect the first sign change (numerical conventions)."""
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


def head_phased(w, t):
    """Hp(theta) = sum_{j<k} w_j cos(j theta).  At t = 0 this is sum_j w_j = H."""
    th = atan(2 * t)
    a = mpf(0)
    for j, wj in enumerate(w):
        if wj != 0:
            a += wj * cos(j * th)
    return a


def t_model(w, k, phased):
    """smallest t > 0 with T(t) = HEAD(t) + 1/2,  T = w_{k-1} rho^k /(2t).

    phased=False is v1 (head at t=0); phased=True is v2 (head keeps its phase).
    T dives then grows; locate the minimum of T - HEAD, then bisect to its right.
    """
    wk = w[-1]
    H0 = sum(w)

    def gap(t):
        T = wk * (1 + 4 * t * t) ** (mpf(k) / 2) / (2 * t)
        h = head_phased(w, t) if phased else H0
        return T - (h + mpf(1) / 2)

    lo, hi = mpf('1e-12'), mpf('0.9')
    n = 700 if phased else 4000          # phased gap costs O(k) per evaluation
    best_t, best_v = None, None
    for i in range(1, n + 1):
        t = lo + (hi - lo) * i / n
        v = gap(t)
        if best_v is None or v < best_v:
            best_v, best_t = v, t
    if best_v > 0:
        return None
    a, b = best_t, hi
    if gap(a) * gap(b) > 0:
        return None
    for _ in range(120):
        m = (a + b) / 2
        if gap(a) * gap(m) <= 0:
            b = m
        else:
            a = m
    return (a + b) / 2


say("=" * 100)
say("head_r216 -- does the head/tail model get the s-DEPENDENCE, or only the scale?")
say("v1 (r211): Re G_k ~ H + T sin(k theta),   H  = sum_j w_j          [head at t = 0]")
say("v2 (here): Re G_k ~ Hp(theta) + T sin(k theta), Hp = sum_j w_j cos(j theta)")
say("both solve T = HEAD + 1/2 for t.  Nothing is fitted in either.")
say("=" * 100)

verdicts = []

# ---------------------------------------------------------------- instruments
say()
say("--- INSTRUMENT 1: constant weights, zero set proved exactly (Thm 2(e), r205) ---")
okI, nI = True, 0
for k in (64, 256):
    ref = tan(pi / k) / 2                      # computed HERE, at mp.dps = 30 (r202)
    got = first_zero(w_const(k), 4 * ref)
    rel = abs(got - ref) / ref if got else mpf(1)
    nI += 1
    if rel > mpf(10) ** (-25):
        okI = False
    say("  k=%4d  proved=%s  measured=%s  rel=%s"
        % (k, mp.nstr(ref, 20), mp.nstr(got, 20) if got else "none", mp.nstr(rel, 4)))
say("  cases: %d -> %s" % (nI, "PASS" if okI and nI > 0 else "FAIL"))
verdicts.append(('instrument 1 (exact zero set)', okI and nI > 0))
if not okI:
    say("ABORTING: the scanner is wrong, so nothing downstream means anything.")
    sys.exit(1)

say()
say("--- INSTRUMENT 2: v2 must reduce to v1 when the phase is switched off ---")
okR, nR = True, 0
for ss in ('1', '2', '4'):
    for k in (64, 256):
        w = w_power(k, ss)
        H = sum(w)
        Hp0 = head_phased(w, mpf(0))
        d = abs(Hp0 - H)
        nR += 1
        if d > mpf(10) ** (-25):
            okR = False
        say("  s=%-4s k=%4d  H=%s  Hp(0)=%s  |diff|=%s"
            % (ss, k, mp.nstr(H, 12), mp.nstr(Hp0, 12), mp.nstr(d, 4)))
say("  cases: %d -> %s" % (nR, "PASS" if okR and nR > 0 else "FAIL"))
verdicts.append(('instrument 2 (v2 contains v1)', okR and nR > 0))
if not okR:
    say("ABORTING: v2 is not a refinement of v1.")
    sys.exit(1)

# ---------------------------------------------------------------- the run
SS = ['1', '1.5', '2', '3', '4']
KS = [64, 128, 256, 512, 1024]

say()
say("--- v1 against v2, no fitted parameter in either ---")
say("  %5s %6s %14s %14s %14s %10s %10s"
    % ("s", "k", "t_1 measured", "t_v1", "t_v2", "ratio v1", "ratio v2"))

data = {}
worst1, worst2 = mpf(0), mpf(0)
n_pop = 0
for ss in SS:
    for k in KS:
        w = w_power(k, ss)
        pred = sqrt(mpf(ss) * log(k) / (2 * k))
        t1 = first_zero(w, 3 * pred)
        m1 = t_model(w, k, phased=False)
        m2 = t_model(w, k, phased=True)
        if t1 is None or m1 is None or m2 is None:
            say("  %5s %6d  not found (t1=%s v1=%s v2=%s)"
                % (ss, k, t1 is not None, m1 is not None, m2 is not None))
            continue
        r1, r2 = m1 / t1, m2 / t1
        n_pop += 1
        worst1 = max(worst1, abs(r1 - 1))
        worst2 = max(worst2, abs(r2 - 1))
        data[(ss, k)] = (t1, m1, m2, r1, r2)
        say("  %5s %6d %14s %14s %14s %10s %10s"
            % (ss, k, mp.nstr(t1, 9), mp.nstr(m1, 9), mp.nstr(m2, 9),
               mp.nstr(r1, 6), mp.nstr(r2, 6)))
    say("")

say("  population: %d pairs" % n_pop)
if n_pop == 0:
    verdicts.append(('population', False))
    say("EMPTY POPULATION -- every verdict below would be vacuous.  FAIL.")
    sys.exit(1)

# ---------------------------------------------------------------- P1
say()
say("--- P1  accuracy: v2 strictly better than v1 in the worst case ---")
say("  worst |ratio-1|   v1 = %s    v2 = %s" % (mp.nstr(worst1, 6), mp.nstr(worst2, 6)))
p1 = worst2 < worst1
verdicts.append(('P1 v2 strictly better', p1))
say("  -> %s" % ("PASS" if p1 else "FAIL -- the head phase is not what is wrong with v1"))

# ---------------------------------------------------------------- P2
say()
say("--- P2  the improvement must be CONCENTRATED at s = 1 (the explanation's falsifier) ---")
say("  %5s %14s %14s %14s" % ("s", "mean|r1-1|", "mean|r2-1|", "mean improvement"))
imp = {}
for ss in SS:
    e1 = [abs(data[(ss, k)][3] - 1) for k in KS if (ss, k) in data]
    e2 = [abs(data[(ss, k)][4] - 1) for k in KS if (ss, k) in data]
    if not e1:
        continue
    m1 = sum(e1) / len(e1)
    m2 = sum(e2) / len(e2)
    imp[ss] = m1 - m2
    say("  %5s %14s %14s %14s" % (ss, mp.nstr(m1, 6), mp.nstr(m2, 6), mp.nstr(m1 - m2, 6)))
p2 = ('1' in imp and '4' in imp and imp['1'] > imp['4'])
verdicts.append(('P2 improvement concentrated at s=1', p2))
say("  improvement at s=1 = %s   at s=4 = %s"
    % (mp.nstr(imp.get('1', 0), 6), mp.nstr(imp.get('4', 0), 6)))
say("  -> %s" % ("PASS" if p2 else
                 "FAIL -- v2 improves uniformly, so the head phase is not the s-dependent part"))

# ---------------------------------------------------------------- P3
say()
say("--- P3  RESOLUTION before any ordering claim (lambda is quadratic in t) ---")
say("  %6s %16s %16s %14s" % ("k", "resolution(lam)", "spread v2(lam)", "admissible?"))
admissible = {}
for k in KS:
    rows = [(ss, data[(ss, k)]) for ss in SS if (ss, k) in data]
    if not rows:
        continue
    lam = {}
    worstk = mpf(0)
    for ss, (t1, m1, m2, r1, r2) in rows:
        lam[ss] = 2 * k * m2 * m2 / log(k) - mpf(ss)
        worstk = max(worstk, abs(r2 - 1))
    lam_typ = max(mpf(ss) for ss in [mpf(x) for x in SS]) * 0 + mpf(1)   # lambda ~ s ~ O(1)
    # resolution in lambda units: relative error e in t is 2e in lambda = 2kt^2/log k,
    # and lambda itself is of size s, so the absolute resolution is 2 e s.  Use the
    # LARGEST s in the column, which is the least favourable to a claim.
    res = 2 * worstk * max(mpf(x) for x in SS)
    spr = max(lam.values()) - min(lam.values())
    ok = spr > res
    admissible[k] = ok
    say("  %6d %16s %16s %14s"
        % (k, mp.nstr(res, 5), mp.nstr(spr, 5), "yes" if ok else "NO"))
say()
say("  Where the answer is NO, the model's own error bar is wider than the entire")
say("  spread it is being asked to order.  No ordering claim is admissible there,")
say("  and this was registered before the numbers were seen.")

# ---------------------------------------------------------------- P4
say()
say("--- P4  ordering at k = 1024, stated only where P3 leaves room ---")
k = 1024
rows = [(ss, data[(ss, k)]) for ss in SS if (ss, k) in data]
if rows and admissible.get(k):
    lam_m, lam_e = {}, {}
    for ss, (t1, m1, m2, r1, r2) in rows:
        lam_m[ss] = 2 * k * m2 * m2 / log(k) - mpf(ss)
        lam_e[ss] = 2 * k * t1 * t1 / log(k) - mpf(ss)
    conc = tot = 0
    for i in range(len(SS)):
        for j in range(i + 1, len(SS)):
            a, b = SS[i], SS[j]
            if a in lam_m and b in lam_m:
                tot += 1
                if (lam_m[a] - lam_m[b]) * (lam_e[a] - lam_e[b]) > 0:
                    conc += 1
    say("  concordant pairs: %d of %d" % (conc, tot))
    verdicts.append(('P4 ordering', tot > 0 and 2 * conc > tot))
else:
    say("  NOT STATED: P3 refused at k = %d.  The model cannot resolve this ordering," % k)
    say("  and reporting one anyway would be a claim the instrument does not support.")
    say("  (The ordering the numbers happen to show is printed above and is not a finding.)")

# ---------------------------------------------------------------- close
say()
say("--- lambda table, both models beside the measurement ---")
say("  %5s %6s %14s %14s %14s" % ("s", "k", "lam_eff - s", "lam_v1 - s", "lam_v2 - s"))
for ss in SS:
    for k in KS:
        if (ss, k) not in data:
            continue
        t1, m1, m2, r1, r2 = data[(ss, k)]
        s = mpf(ss)
        say("  %5s %6d %14s %14s %14s"
            % (ss, k,
               mp.nstr(2 * k * t1 * t1 / log(k) - s, 6),
               mp.nstr(2 * k * m1 * m1 / log(k) - s, 6),
               mp.nstr(2 * k * m2 * m2 / log(k) - s, 6)))
    say("")

say("=" * 100)
for tag, v in verdicts:
    say("  [%s] %s" % (tag, "PASS" if v else "FAIL"))
allok = all(v for _, v in verdicts)
say()
say("verdict recorded; interpretation belongs in the report, not here.")
say("done.")
sys.exit(0 if allok else 1)
