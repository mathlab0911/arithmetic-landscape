#!/usr/bin/env python3
"""
r109 / paper 4 section 4, Step 2: the explicit constants of the probabilistic half.

WHAT I DERIVED ON PAPER BEFORE RUNNING THIS (F09).

Step 2 of prop:rate needs a per-element mean gap: for theta on the minor arcs, the mean of
X_m(theta) = -log|cos(pi m theta)| over the odd residues must exceed the value it takes at
theta = 1/4, which is exactly (1/2) log 2, by a definite amount.  Theorem thm:modfour gives
that mean in closed form: it is -log M_odd(q), and

    -log M_odd(q) = (1 - 1/v) log 2 ,      v = q          (q odd)
                                            v = q/2        (q = 0 mod 4)
                    = +infinity,                           (q = 2 mod 4)

so the gap at modulus q is

    delta(q) = -log M_odd(q) - (1/2) log 2 = (1/2 - 1/v) log 2 .

This is 0 exactly at v = 2, i.e. q = 4 -- the extremal modulus, as it must be -- and positive
elsewhere.  It INCREASES with v, so the smallest positive gap sits at the smallest admissible
v other than 2.  The admissible v are {3,5,7,...} from odd q and {2,4,6,...} from q = 0 mod 4,
so the smallest v after 2 is v = 3, from q = 3.

    ***  PREDICTION:  delta_min = (1/2 - 1/3) log 2 = (1/6) log 2 = 0.1155245...,
         attained at q = 3, and at no other modulus.                              ***

The truncation of Step 1 must not eat this.  Truncating at level M is INACTIVE at modulus q as
long as M exceeds max_j -log|cos(pi j/q)| over the odd residues, and |cos(pi j/q)| >= sin(pi/q)
>= 2/q for the residue closest to q/2, so M = log(q) suffices; taking the Dirichlet parameter
Q and M = log(2Q/pi) makes truncation inactive at EVERY q <= Q that is not 2 mod 4.

For q = 2 mod 4 truncation is active -- one odd residue, j = u = q/2, has cos = 0 -- and there
the truncated mean is computable too.  Writing q = 2u with u odd, the product over the other
u-1 odd residues is u * 2^{1-u} (put x = -1 in (x^u+1)/(x+1)), so the truncated mean is

    [ (u-1) log 2 - log u + M ] / u ,

which for M = log(2Q/pi) and u <= Q/2 is comfortably above (1/2) log 2 + delta_min.

CHECKS RUN HERE
  (A) delta(q) from the closed form vs the direct residue average, q <= 400
  (B) the minimum of delta over q != 4, and where it is attained
  (C) truncation is inactive at every q <= Q not 2 mod 4, for M = log(2Q/pi)
  (D) q = 2 mod 4: the truncated-mean formula vs the direct computation, and its margin
  (E) the assembled Step-2 constant: min over 3 <= q <= Q, q != 4, of
      (truncated mean - (1/2) log 2), for several Q
Fail rule with floor (F51): (A) and (D) are exact arithmetic, so anything above 1e-12 is a real
disagreement.  In (B) and (E) the prediction is an exact rational multiple of log 2; a
minimum attained anywhere but q = 3, or differing from (1/6) log 2 by more than 1e-12, stops
the round.
"""
import math

LOG2 = math.log(2.0)
PRED = LOG2 / 6.0


def R_q(q):
    return list(range(q)) if q % 2 == 1 else [j for j in range(q) if j % 2 == 1]


def mean_X(q, M=None):
    """mean over j in R_q of min(-log|cos(pi j/q)|, M);  M=None means no truncation."""
    tot, js = 0.0, R_q(q)
    for j in js:
        c = abs(math.cos(math.pi * j / q))
        x = math.inf if c < 1e-15 else -math.log(c)
        tot += x if M is None else min(x, M)
    return tot / len(js)


def delta_closed(q):
    """(1/2 - 1/v) log 2, with v = q (q odd) or q/2 (q = 0 mod 4); inf for q = 2 mod 4."""
    if q % 2 == 1:
        v = q
    elif q % 4 == 0:
        v = q // 2
    else:
        return math.inf
    return (0.5 - 1.0 / v) * LOG2


print('=' * 100)
print('(A) delta(q) closed form vs the direct residue average,  q = 3..400')
print('=' * 100)
worst, worstq = 0.0, None
for q in range(3, 401):
    if q % 4 == 2:
        continue
    d = mean_X(q) - 0.5 * LOG2
    if abs(d - delta_closed(q)) > worst:
        worst, worstq = abs(d - delta_closed(q)), q
print(f'  worst |direct - closed form| = {worst:.3e} at q = {worstq}')
print(f"  {'q':>4} {'v':>4} {'-log M_odd':>12} {'delta(q)':>11} {'closed':>11}")
for q in (3, 4, 5, 7, 8, 9, 12, 16, 20):
    v = q if q % 2 == 1 else q // 2
    print(f'  {q:4d} {v:4d} {mean_X(q):12.6f} {mean_X(q)-0.5*LOG2:11.6f} '
          f'{delta_closed(q):11.6f}')

print()
print('=' * 100)
print('(B) the minimum of delta over q != 4  ---  the Step-2 constant, untruncated')
print('=' * 100)
cands = [(delta_closed(q), q) for q in range(3, 2001) if q != 4 and q % 4 != 2]
mn, aq = min(cands)
print(f'  min delta(q) over 3 <= q <= 2000, q != 4 :  {mn:.10f}  at q = {aq}')
print(f'  prediction (1/6) log 2                   :  {PRED:.10f}')
print(f'  |difference| = {abs(mn-PRED):.3e}      delta(4) = {delta_closed(4):.10f} (must be 0)')
runner = sorted(cands)[1]
print(f'  runner-up: q = {runner[1]}, delta = {runner[0]:.6f}  ((1/4) log 2 = {LOG2/4:.6f})')
ok_B = abs(mn - PRED) < 1e-12 and aq == 3 and abs(delta_closed(4)) < 1e-15
print(f'  VERDICT: {"as predicted" if ok_B else "*** FAIL RULE: not as predicted ***"}')

print()
print('=' * 100)
print('(C) truncation is inactive: max_j -log|cos(pi j/q)| vs M = log(2Q/pi), q not 2 mod 4')
print('=' * 100)
for Q in (50, 200, 1000):
    M = math.log(2 * Q / math.pi)
    worstm, wq = 0.0, None
    for q in range(3, Q + 1):
        if q % 4 == 2:
            continue
        mx = max(-math.log(abs(math.cos(math.pi * j / q))) for j in R_q(q))
        if mx > worstm:
            worstm, wq = mx, q
    print(f'  Q = {Q:5d}:  M = {M:7.4f},  max over all such q of max_j X = {worstm:7.4f} '
          f'(at q = {wq})   -> {"inactive" if worstm <= M else "*** ACTIVE ***"}')

print()
print('=' * 100)
print('(D) q = 2 mod 4: truncated mean, formula [(u-1)log2 - log u + M]/u vs direct')
print('=' * 100)
Q = 200
M = math.log(2 * Q / math.pi)
print(f'  M = log(2Q/pi) = {M:.4f} with Q = {Q}')
print(f"  {'q':>5} {'u':>5} {'formula':>11} {'direct':>11} {'diff':>10} "
      f"{'margin over (1/2)log2+delta_min':>32}")
worstd = 0.0
for q in (6, 10, 14, 22, 50, 102, 198):
    u = q // 2
    f = ((u - 1) * LOG2 - math.log(u) + M) / u
    d = mean_X(q, M)
    worstd = max(worstd, abs(f - d))
    print(f'  {q:5d} {u:5d} {f:11.6f} {d:11.6f} {abs(f-d):10.2e} '
          f'{d - 0.5*LOG2 - PRED:32.6f}')
print(f'  worst |formula - direct| = {worstd:.3e}')

print()
print('=' * 100)
print('(E) THE ASSEMBLED STEP-2 CONSTANT.  min over 3 <= q <= Q, q != 4, of')
print('    (truncated mean at M = log(2Q/pi))  -  (1/2) log 2 .')
print('=' * 100)
print(f"  {'Q':>6} {'M':>8} {'min gap':>12} {'at q':>6} {'(1/6) log 2':>13} {'diff':>10}")
allok = True
for Q in (20, 50, 200, 600):
    M = math.log(2 * Q / math.pi)
    best, bq = math.inf, None
    for q in range(3, Q + 1):
        if q == 4:
            continue
        g = mean_X(q, M) - 0.5 * LOG2
        if g < best:
            best, bq = g, q
    ok = (bq == 3) and abs(best - PRED) < 1e-12
    allok &= ok
    print(f'  {Q:6d} {M:8.4f} {best:12.8f} {bq:6d} {PRED:13.8f} {abs(best-PRED):10.2e}'
          f'{"" if ok else "   *** NOT AT q=3 ***"}')
print()
if allok and ok_B:
    print('  => STEP 2 HAS AN EXPLICIT CONSTANT.  For every minor-arc modulus q != 4,')
    print('     mean X >= (1/2) log 2 + (1/6) log 2,  and the binding competitor is q = 3.')
    print('     delta = (1/6) log 2 = 0.1155245301, exactly, and truncation does not eat it.')
else:
    print('  => FAIL RULE fired: report raw, do not write the constant into the paper.')
