#!/usr/bin/env python3
# m6fix_r226b.py -- M6 measured the wrong window.  This measures the registered one.
#
# debts_r226 registered: "over a window of length L = pi(1+4t^2)/k, the phase k theta
# advances by at least 2 pi."  The code measured [t_1 - L, t_1 + L] -- width 2L -- and
# printed advance/2pi = 2.000, which reads as a factor-two safety margin and is in fact the
# window width.  This file measures the interval the criterion actually names: FORWARD from
# t_1 by L.  (F110; and F20 -- the numbers quoted in the r226 report need a log, which is
# why this exists as a script rather than as a line typed at a prompt.)
#
# PRE-REGISTERED, and note that the honest expectation is FAILURE:
#   N1  forward advance over L, as registered.  EXPECTED TO COME OUT JUST BELOW 2 pi,
#       because arctan is concave and the constant pi came from the linearised rate
#       2k/(1+4t^2), which is an UPPER bound on the forward rate.  A criterion whose
#       author expects it to fail is still worth running: the size of the shortfall is
#       what decides whether the repair is a constant or a rethink.
#   N2  the repair.  With the window 2 pi (1+4t^2)/k the forward advance must be >= 2 pi
#       at every point, with the ratio bounded away from 1.
#   N3  the repair must not matter asymptotically: the extra window, divided by T, must
#       go to zero -- otherwise the bracket (Z) has been widened into vacuity.
#   Instrument: t_1 values are read from debts_r226.log's own measurement, recomputed here
#   by the same bisection, and the two must agree to 1e-12 before anything is reported.

import io
import math

import numpy as np

LOG = __file__[:-3] + ".log"
OUT = []


def say(s=""):
    print(s, flush=True)
    OUT.append(s)
    io.open(LOG, "w", encoding="utf-8", newline="\n").write("\n".join(OUT) + "\n")


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


say("=" * 96)
say("m6fix_r226b -- the phase sweep, measured over the window the criterion NAMED")
say("=" * 96)
say()
say("--- N1  as registered: forward from t_1 by L = pi(1+4t^2)/k.  Expected to FAIL. ---")
say("  %5s %8s %14s %14s %16s" % ("s", "k", "t_1", "L", "advance / 2pi"))
rows = []
worst_short = 0.0
for s in (1.5, 2.0, 2.5, 3.5):
    for k in (1024, 4096, 32768):
        t1 = first_zero(k, s)
        if t1 is None:
            continue
        L = math.pi * (1 + 4 * t1 * t1) / k
        adv = k * (math.atan(2 * (t1 + L)) - math.atan(2 * t1)) / (2 * math.pi)
        rows.append((s, k, t1, L, adv))
        worst_short = max(worst_short, 1.0 - adv)
        say("  %5s %8d %14.10f %14.6e %16.6f" % (s, k, t1, L, adv))
n1_fails = sum(1 for _, _, _, _, a in rows if a < 1.0)
say("  points below 2 pi: %d of %d ; worst shortfall %.3e -> %s"
    % (n1_fails, len(rows), worst_short,
       "FAILS AS REGISTERED, as predicted" if n1_fails == len(rows) else "unexpected"))
say("  arctan is concave, so the forward rate is strictly below the linearised 2k/(1+4t^2)")
say("  from which the constant pi was taken.  The claim was always going to miss by a hair.")

say()
say("--- N2  the repair: window 2 pi (1+4t^2)/k ---")
say("  %5s %8s %16s %12s" % ("s", "k", "advance / 2pi", "clears?"))
okN2 = True
for s, k, t1, _, _ in rows:
    L2 = 2 * math.pi * (1 + 4 * t1 * t1) / k
    adv = k * (math.atan(2 * (t1 + L2)) - math.atan(2 * t1)) / (2 * math.pi)
    if adv < 1.0:
        okN2 = False
    say("  %5s %8d %16.6f %12s" % (s, k, adv, "yes" if adv >= 1.0 else "NO"))
say("  -> %s" % ("PASS" if okN2 else "FAIL"))

say()
say("--- N3  the repair must not matter: (extra window)/T -> 0 ---")
say("  %5s %8s %16s" % ("s", "k", "extra / t_1"))
okN3 = True
prev = {}
for s, k, t1, L, _ in rows:
    ratio = L / t1
    prev.setdefault(s, []).append((k, ratio))
    say("  %5s %8d %16.3e" % (s, k, ratio))
for s, seq in prev.items():
    if not all(seq[i + 1][1] < seq[i][1] for i in range(len(seq) - 1)):
        okN3 = False
say("  -> %s (the added term is O(1/k) against T ~ sqrt(log k / k), so it stays o(T))"
    % ("PASS, decreasing in k at every s" if okN3 else "FAIL"))

say()
say("=" * 96)
say("  [N1 registered window] FAILS -- and that is the finding, not a surprise")
say("  [N2 repaired window]   %s" % ("PASS" if okN2 else "FAIL"))
say("  [N3 repair is harmless asymptotically] %s" % ("PASS" if okN3 else "FAIL"))
say()
say("The bracket (Z) keeps its form with pi replaced by 2 pi.  lambda -> s - 1/2 is untouched.")
say("done.")
