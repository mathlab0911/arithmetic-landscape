#!/usr/bin/env python3
# note1tab_r208.py -- the numbers printed in the Track M note's worked example.
#
# Written because the first draft of that table was TYPED rather than computed, and two
# of the six entries were wrong in the seventh digit.  The note itself contains the rule
# this violated ("a formula and the number it is supposed to produce, printed in the same
# sentence, are not a check on each other"), which is the least comfortable place to break
# it.  So: the table is generated here, printed here, and copied from here.
#
# The family is Theorem 2(e)'s A = 0 case: w_0 = 0, w_j = 1/2 for 1 <= j <= k-1, whose
# zero set on the line is EXACTLY t_n = (1/2) tan(n pi / k).
#
# PRE-REGISTERED (F45/F86):
#   C1  every printed t_n must be a zero of the DIRECT SUM to >= 40 digits.  The closed
#       form is what we are printing; the direct sum is what tests it, and it is the
#       instrument control -- if it fails, the table does not go in the note.
#   C2  k*t_n/pi must approach n/2, since t_n ~ (1/2)(n pi/k) for n pi/k small.
#   Population printed; a verdict over an empty population is a FAIL (F60).

import io
import sys
from mpmath import mp, mpf, mpc, sqrt, atan, cos, tan, pi

mp.dps = 60
OUT = []


def say(s=""):
    print(s)
    OUT.append(s)


def w_A0(k):
    """w_0 = 0, w_j = 1/2 for 1 <= j <= k-1  (Theorem 2(e), A = 0)."""
    return [mpf(0)] + [mpf(1) / 2] * (k - 1)


def F_direct(w, t):
    """1 + 2 Re G_k(1+2it), summed term by term -- no closed form used."""
    rho, th = sqrt(1 + 4 * t * t), atan(2 * t)
    a = mpf(0)
    for j, wj in enumerate(w):
        if wj != 0:
            a += wj * rho ** j * cos(j * th)
    return 1 + 2 * a


say("=" * 84)
say("note1tab_r208 -- the worked-example table of the Track M note")
say("family: w_0 = 0, w_j = 1/2  (A = 0);  closed form t_n = (1/2) tan(n pi / k)")
say("=" * 84)

K = 32
w = w_A0(K)
say()
say("  k = %d" % K)
say("  %3s %30s %16s %22s" % ("n", "t_n = (1/2)tan(n pi/k)", "k t_n / pi", "F_direct at t_n"))
n_ok, n_tot = 0, 0
rows = []
for n in (1, 2, 3):
    t = tan(n * pi / K) / 2                 # computed HERE, at mp.dps = 60 (r202)
    val = F_direct(w, t)
    ratio = K * t / pi
    ok = abs(val) < mpf(10) ** (-40)
    n_tot += 1
    n_ok += 1 if ok else 0
    rows.append((n, t, ratio))
    say("  %3d %30s %16s %22s %s"
        % (n, mp.nstr(t, 18), mp.nstr(ratio, 7), mp.nstr(val, 6), "ok" if ok else "FAIL"))

say()
say("  [C1] every printed t_n is a zero of the direct sum to 40+ digits: %d of %d -> %s"
    % (n_ok, n_tot, "PASS" if n_ok == n_tot and n_tot > 0 else "FAIL"))
c2 = all(abs(r - mpf(n) / 2) < mpf('0.06') for n, _, r in rows)
say("  [C2] k t_n / pi approaches n/2 (small angle): %s  over %d row(s)"
    % ("PASS" if c2 and rows else "FAIL", len(rows)))

say()
say("COPY THESE STRINGS INTO THE NOTE, and nothing else:")
for n, t, r in rows:
    say("  n=%d   t_n = %s   k t_n / pi = %s" % (n, mp.nstr(t, 18), mp.nstr(r, 7)))
say()
say("done.")

io.open(__file__[:-3] + ".log", "w", encoding="utf-8", newline="\n").write("\n".join(OUT) + "\n")
sys.exit(0 if (n_ok == n_tot and n_tot > 0 and c2) else 1)
