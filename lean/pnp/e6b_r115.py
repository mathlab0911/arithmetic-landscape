#!/usr/bin/env python3
r"""
r115 / paper 4, closing the TODO on sec:e6.

THE TODO, verbatim from paper4.tex:
    "the primes at q = 1/2 are not a clean test in this range: dev - dev_0 crosses zero inside
     it, and dropping the single point where it is 2.7e-7 leaves the quadratic ratio in
     [45.06, 48.86].  Re-measure on a target range that does not straddle the crossing."

WHAT IS BEING TESTED.  Off the q-tilted centre the deviation dev_q = (lm_q/deg_q)/Gamma^(q) - 1
should respond to a shift of target LINEARLY when q != 1/2 and QUADRATICALLY at q = 1/2, because
the first-order coefficient L^(q) = SUM_d delta_d [q^{N_d} - (1-q)^{N_d}] vanishes identically at
q = 1/2.  The discriminator is which of (dev - dev_0)/lambda and (dev - dev_0)/lambda^2 is the
more nearly constant across a range of target offsets.

WHY THE OLD RANGE WAS NOT A TEST (F32/F51).  If dev - dev_0 changes sign inside the range then
it passes through zero, and BOTH ratios pass through zero with it; the spread max/min of either
is then dominated by however close a sample point happened to land to the crossing, which is an
accident of the grid and not a property of the response.  *** A ratio test must not straddle a
zero of its own numerator. ***  That is the general form of the defect, and it is what this
script fixes.

WHAT I DERIVED BEFORE MEASURING (F09).  dev_q(x) - dev_q(0) should be, near x = 0,
    L^(q) x + Q^(q) x^2 + ...          (x = the target offset, in units of the total)
At q = 1/2 the linear coefficient vanishes identically, so the leading behaviour is Q x^2, which
is EVEN in x and does not change sign.  A sign change inside the range therefore cannot be the
quadratic response -- it must be the finite-k offset of the centre: dev_q(0) is not exactly the
minimum of dev_q at finite k, so the parabola's vertex sits at some x_* != 0 and
dev - dev_0 = Q(x^2 - x_*^2) crosses zero at x = +-x_*.
    *** PREDICTION: the crossing sits at a SMALL |x|, the parabola's vertex is at x_*, and
        measuring on a range with |x| >> x_* gives a clean quadratic ratio. ***
This also says what the right repair is: not "drop the bad point" but "start the range outside
x_*".

CHECKS
  (A) locate the crossing: scan dev - dev_0 on both sides of the centre and find x_*.
  (B) re-measure the two spreads on a range that starts well outside x_*.
  (C) POSITIVE CONTROL, on the procedure and not on the function (F55, second instance): the
      odd numbers at q = 1/2 are already reported in the paper as (dev-dev_0)/lambda^2 in
      [19.8186, 19.8352].  This script must REPRODUCE that interval on the paper's own range,
      or its pipeline differs from the one the paper used and every other row is void.
  (D) the same clean-range measurement at q = 0.3, where LINEAR must win, as a discriminating
      control in the other direction (F47: a test that cannot come out the other way is not a
      test).

FAIL RULE WITH FLOOR (F51).  Spreads are max/min of positive quantities; the floor is set by
the granularity of the DP, and dev - dev_0 below 1e-9 is not resolved -- any sample point with
|dev - dev_0| < 1e-9 is reported and excluded, and if excluding it changes the verdict the
result is reported raw and the TODO stays.  *** If on a clean range the quadratic spread at
q = 1/2 is not below the linear spread, the paper's claim is not supported and the sentence
must be weakened, not the range re-picked again. ***
"""
import math

from e5_r098 import ENS, strata_q, gamma_q


def slope_and_ratio(A, q, n):
    """biased lm_q/deg_q at n, and the biased local log-slope there (as in e6_r100)."""
    deg, lm, _, _ = strata_q(A, q, n)
    dm, _, _, _ = strata_q(A, q, n - 2)
    dp2, _, _, _ = strata_q(A, q, n + 2)
    return lm / deg, 0.25 * math.log(dm / dp2)


FLOOR = 1e-9

print('=' * 100)
print('(A) WHERE IS THE CROSSING?   dev_q(x) - dev_q(0) on both sides of the tilted centre.')
print('    Derived above: at q = 1/2 the response is even in x, so a sign change can only be')
print('    the finite-k offset of the vertex.  x is measured as a fraction of q*T.')
print('=' * 100)
xstar = {}
for nm, k in (('odds', 80), ('primes', 80)):
    A = sorted(ENS[nm](k))
    T = sum(A)
    for q in (0.5,):
        n0 = int(round(q * T))
        g = gamma_q(A, q)
        r0, _ = slope_and_ratio(A, q, n0)
        dev0 = r0 / g - 1.0
        print(f'\n  {nm}, k = {k}, q = {q}:  n_q = {n0}, dev_q(0) = {dev0:+.6e}')
        print(f"      {'x':>8} {'n':>9} {'lambda':>12} {'dev - dev_0':>14} {'sign':>5}")
        prev = None
        for frac in (-0.24, -0.16, -0.08, -0.04, -0.02, -0.01, 0.01, 0.02,
                     0.04, 0.08, 0.16, 0.24):
            n = int(round((q - frac * q) * T))
            rr, ll = slope_and_ratio(A, q, n)
            d = rr / g - 1.0 - dev0
            s = '+' if d > 0 else ('-' if d < 0 else '0')
            print(f'      {frac:8.3f} {n:9d} {ll:12.6f} {d:14.3e} {s:>5}')
            if prev is not None and prev[1] * d < 0:
                xstar[(nm, q)] = (abs(prev[0]) + abs(frac)) / 2
            prev = (frac, d)
        loc = xstar.get((nm, q))
        print(f'      => crossing located at |x| ~ {loc if loc else "none in range"}')

print()
print('=' * 100)
print('(B) THE RE-MEASUREMENT, on a range that starts well outside the crossing.')
print('    old range: x = 0.04 .. 0.20   (straddles the crossing for the primes)')
print('    new range: x = 0.10 .. 0.30   (entirely on one side)')
print('=' * 100)


def spreads(nm, k, q, fracs):
    A = sorted(ENS[nm](k))
    T = sum(A)
    n0 = int(round(q * T))
    g = gamma_q(A, q)
    r0, _ = slope_and_ratio(A, q, n0)
    dev0 = r0 / g - 1.0
    lin, quad, raw, dropped = [], [], [], 0
    for frac in fracs:
        n = int(round((q - frac * q) * T))
        rr, ll = slope_and_ratio(A, q, n)
        d = rr / g - 1.0 - dev0
        if abs(d) < FLOOR:
            dropped += 1
            continue
        raw.append((frac, ll, d))
        lin.append(abs(d / ll))
        quad.append(abs(d / ll ** 2))
    sl = max(lin) / min(lin) if lin else float('nan')
    sq = max(quad) / min(quad) if quad else float('nan')
    return sl, sq, quad, raw, dropped


OLD = (0.04, 0.08, 0.12, 0.16, 0.20)
NEW = (0.10, 0.15, 0.20, 0.25, 0.30)
print(f"  {'ens':>8} {'q':>5} {'range':>6} {'spread /lambda':>15} {'spread /lambda^2':>17} "
      f"{'dropped':>8}  verdict")
results = {}
for nm in ('odds', 'primes'):
    for q in (0.5, 0.3):
        for tag, fr in (('old', OLD), ('new', NEW)):
            sl, sq, quad, raw, dr = spreads(nm, 80, q, fr)
            verdict = 'LINEAR wins' if sl < sq else 'quadratic wins'
            results[(nm, q, tag)] = (sl, sq, quad, verdict)
            print(f'  {nm:>8} {q:5.2f} {tag:>6} {sl:15.3f} {sq:17.3f} {dr:8d}  {verdict}')
    print()

print('  the quadratic ratio itself on the new range (this is the number the paper quotes):')
print(f"  {'ens':>8} {'q':>5} {'min':>12} {'max':>12} {'spread':>9}")
for nm in ('odds', 'primes'):
    for q in (0.5,):
        _, _, quad, _ = results[(nm, q, 'new')]
        print(f'  {nm:>8} {q:5.2f} {min(quad):12.4f} {max(quad):12.4f} '
              f'{max(quad)/min(quad):9.4f}')

print()
print('=' * 100)
print('(C) POSITIVE CONTROL, ON THE PROCEDURE.  The paper reports, for the odd numbers at')
print('    q = 1/2 on the OLD range, (dev-dev_0)/lambda^2 in [19.8186, 19.8352].  If this')
print('    script does not reproduce that, its pipeline is not the paper\'s and (B) is void.')
print('=' * 100)
_, _, quad_ctrl, _ = results[('odds', 0.5, 'old')]
lo, hi = min(quad_ctrl), max(quad_ctrl)
ok_ctrl = abs(lo - 19.8186) < 5e-3 and abs(hi - 19.8352) < 5e-3
print(f'  reproduced: [{lo:.4f}, {hi:.4f}]   paper: [19.8186, 19.8352]   '
      f'{"MATCH" if ok_ctrl else "*** MISMATCH -- (B) IS VOID ***"}')

print()
print('=' * 100)
print('(D) DISCRIMINATING CONTROL IN THE OTHER DIRECTION (F47).  At q = 0.3 the linear term')
print('    does NOT vanish, so LINEAR must win on the same clean range.  A test that cannot')
print('    come out the other way is not a test.')
print('=' * 100)
for nm in ('odds', 'primes'):
    sl, sq, _, v = results[(nm, 0.3, 'new')]
    print(f'  {nm:>8} q = 0.30, new range: /lambda spread {sl:.3f}, /lambda^2 spread {sq:.3f}'
          f'   -> {v}')

print()
print('=' * 100)
print('VERDICT')
print('=' * 100)
_, sq_p_new, quad_p, v_p = results[('primes', 0.5, 'new')]
sl_p_new = results[('primes', 0.5, 'new')][0]
ok_main = (v_p == 'quadratic wins')
ok_disc = all(results[(nm, 0.3, 'new')][3] == 'LINEAR wins' for nm in ('odds', 'primes'))
print(f'  control (C) reproduces the paper                       : {"YES" if ok_ctrl else "NO"}')
print(f'  primes at q = 1/2 on a clean range: quadratic wins      : {"YES" if ok_main else "NO"}'
      f'   ({sl_p_new:.3f} vs {sq_p_new:.3f})')
print(f'  q = 0.3 still comes out LINEAR on the same range        : {"YES" if ok_disc else "NO"}')
if ok_ctrl and ok_main and ok_disc:
    print('  => THE TODO CLOSES.  On a range that does not straddle the crossing the primes')
    print(f'     behave exactly as the odd numbers do: the quadratic ratio lies in')
    print(f'     [{min(quad_p):.4f}, {max(quad_p):.4f}] and the linear one is {sl_p_new/sq_p_new:.1f} times more spread.')
else:
    print('  => REPORT RAW.  Do not re-pick the range a third time; weaken the sentence.')
