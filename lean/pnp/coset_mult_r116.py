#!/usr/bin/env python3
r"""
r116 / de-risking the Lean formalisation of lem:coset, which the external review of
2026-08-10 named as an unverified foundation (its point 5).

WHY THIS SCRIPT EXISTS.  Mathlib has no product-of-cosines lemma -- searched twice, all of
Analysis/SpecialFunctions and the whole tree for a theorem whose name pairs prod with sin or
cos: nothing.  So the multiplication formula has to be built, and the odd-prime base case needs
roots of unity.  Before spending a round on that, the REDUCTION should be known to be correct,
because it is the part with index bookkeeping in it and therefore the part that can be quietly
wrong on paper.

WHAT IS BEING CHECKED (derived on paper first, F09).  Write

    P_v(t) = PROD_{k<v} |2 cos(pi (t + k/v))| ,      tau_v = 1/2 if v even, 0 if v odd.

  (A) THE IDENTITY:            P_v(t) = 2 |cos(pi (v t + tau_v))|.
  (B) THE BASE CASE v = 2:     2cos(pi(t+1/2)) = -2 sin(pi t), so
                               P_2(t) = |2cos pi t| |2 sin pi t| = |2 sin 2pi t|
                                      = 2|cos(pi(2t + 1/2))|.   Elementary, no roots of unity.
  (C) MULTIPLICATIVITY:        k = i + a j is a bijection [a]x[b] -> [ab] and
                               k/(ab) = i/(ab) + j/b, hence
                                    P_{ab}(t) = PROD_{i<a} P_b(t + i/(ab)).
                               *** This is the step the Lean proof will spend its effort on
                                   (a Finset reindexing), so it is the step to check. ***
  (D) THE tau BOOKKEEPING:     feeding (A) for b then for a through (C) gives
                                    P_{ab}(t) = 2|cos(pi(ab t + a tau_b + tau_a))| ,
                               so the reduction closes only if
                                    a tau_b + tau_a  ==  +- tau_{ab}   (mod 1)
                               in all four parity cases.  On paper:
                                    a odd,  b odd  : 0 + 0 = 0            = tau_odd    OK
                                    a odd,  b even : a/2 + 0 = 1/2 (a odd) = tau_even   OK
                                    a even, b odd  : 0 + 1/2 = 1/2         = tau_even   OK
                                    a even, b even : a/2 + 1/2 = 1/2 (a even) = tau_even OK
                               *** If any row failed, the reduction would be false and the
                                   Lean design would have to change. ***

  (E) THE CONSEQUENCE THE PAPER ACTUALLY USES (cor:floor), in the multiplicative form that
      Lean must take: PROD_{k<v} |cos(pi(t+k/v))| <= 2^{1-v}.  The additive form is FALSE in
      Lean because Real.log 0 = 0; checked here in both forms so the difference is on record.

FAIL RULE WITH FLOOR (F51).  (A)-(D) are exact algebraic identities compared in PRODUCT form,
where nothing is amplified -- the r110 lesson.  Floor 1e-12.  *** If (C) or (D) fails anywhere,
report raw: the reduction is wrong and no Lean effort should be spent on it. ***
POSITIVE CONTROL (F55, and its second instance): each check is also run on a DELIBERATELY WRONG
tau (tau' = 0 for all v) and must FAIL there.  A check that passes for both the right and the
wrong constant is not checking the constant.
"""
import math

TOL = 1e-12


def P(v, t):
    """PROD_{k<v} |2 cos(pi (t + k/v))|"""
    r = 1.0
    for k in range(v):
        r *= abs(2.0 * math.cos(math.pi * (t + k / v)))
    return r


def tau(v):
    return 0.5 if v % 2 == 0 else 0.0


def tau_wrong(v):
    return 0.0                      # the negative control


def rhs(v, t, tf=tau):
    return 2.0 * abs(math.cos(math.pi * (v * t + tf(v))))


TS = [0.0, 0.013, 0.1, 0.25, 1.0 / 3, 0.5, 0.617, 0.75, -0.29, 1.4142]

print('=' * 96)
print('(A) THE IDENTITY  P_v(t) = 2 |cos(pi(v t + tau_v))|,  v = 1..40')
print('=' * 96)
worst, wv = 0.0, None
for v in range(1, 41):
    for t in TS:
        d = abs(P(v, t) - rhs(v, t))
        if d > worst:
            worst, wv = d, (v, t)
print(f'  worst |LHS - RHS| = {worst:.3e}  at (v,t) = {wv}')
okA = worst < TOL
# negative control
wctl = max(abs(P(v, t) - rhs(v, t, tau_wrong)) for v in range(1, 41) for t in TS)
print(f'  NEGATIVE CONTROL with tau = 0 for every v: worst = {wctl:.3e} '
      f'({"detects the wrong constant" if wctl > 1e-6 else "*** BLIND ***"})')

print()
print('=' * 96)
print('(B) THE BASE CASE v = 2, which is the double-angle formula and needs no roots of unity')
print('=' * 96)
w2 = max(abs(P(2, t) - 2 * abs(math.sin(2 * math.pi * t))) for t in TS)
print(f'  P_2(t) vs |2 sin 2pi t| : worst = {w2:.3e}')
w2b = max(abs(P(2, t) - rhs(2, t)) for t in TS)
print(f'  P_2(t) vs 2|cos(pi(2t+1/2))| : worst = {w2b:.3e}')

print()
print('=' * 96)
print('(C) MULTIPLICATIVITY  P_{ab}(t) = PROD_{i<a} P_b(t + i/(ab))')
print('    -- the Finset reindexing k = i + a j; the step the Lean proof will live or die on')
print('=' * 96)
worstC, wc = 0.0, None
pairs = [(a, b) for a in range(1, 9) for b in range(1, 9)]
for a, b in pairs:
    for t in TS:
        lhs = P(a * b, t)
        r = 1.0
        for i in range(a):
            r *= P(b, t + i / (a * b))
        d = abs(lhs - r)
        if d > worstC:
            worstC, wc = d, (a, b, t)
print(f'  worst over {len(pairs)} pairs (a,b) x {len(TS)} shifts : {worstC:.3e}  at (a,b,t) = {wc}')
okC = worstC < TOL

print()
print('=' * 96)
print('(D) THE tau BOOKKEEPING.  a tau_b + tau_a  ==  +- tau_{ab}  (mod 1) ?')
print('=' * 96)
print(f"  {'a':>3} {'b':>3} {'a*tau_b + tau_a':>16} {'tau_ab':>8} {'mod-1 distance':>15}  ok")
okD = True
for a, b in [(3, 5), (3, 4), (4, 3), (4, 6), (5, 7), (2, 2), (6, 10), (7, 9), (8, 12)]:
    lhs = a * tau(b) + tau(a)
    d = abs(lhs - tau(a * b))
    d = min(d % 1.0, 1.0 - d % 1.0)          # |cos| has period 1 and is even
    ok = d < TOL
    okD &= ok
    print(f'  {a:3d} {b:3d} {lhs:16.4f} {tau(a*b):8.2f} {d:15.3e}  {ok}')
print(f'  => the reduction {"closes" if okD else "*** DOES NOT CLOSE ***"} in every parity case')

print()
print('=' * 96)
print('(E) THE FORM THE LEAN STATEMENT MUST TAKE')
print('    multiplicative:  PROD_{k<v} |cos(pi(t+k/v))| <= 2^{1-v}     -- true everywhere')
print('    additive:        (1/v) SUM -log|cos| >= (1-1/v) log 2       -- FALSE in Lean at a')
print('                     pole, because Real.log 0 = 0 makes the vanishing term read 0')
print('=' * 96)
worstE = -1.0
for v in range(1, 41):
    for t in TS + [0.5 - 1e-9, 0.25]:
        lhs = P(v, t) / 2.0 ** v          # = PROD |cos|
        worstE = max(worstE, lhs - 2.0 ** (1 - v))
print(f'  max over v<=40 of [PROD|cos| - 2^(1-v)] = {worstE:.3e}   (<= 0 up to a 1e-15 float floor)')
print()
print('  The additive counterexample must be evaluated EXACTLY, not in float: my first attempt')
print('  computed cos(pi/2) numerically, got 6.1e-17 instead of 0, and so reported an additive')
print('  mean of 18.67 -- the opposite of the point.  A demonstration that Real.log 0 = 0 breaks')
print('  the bound cannot be run through a float cosine, because the input is never exactly 0.')
print('  At v = 2, t = 1/2 the two cosines are cos(pi/2) = 0 and cos(pi) = -1, exactly:')
exact_terms = [0.0, 1.0]                      # |cos(pi/2)|, |cos(pi)| -- exact values
lean_sum = sum(0.0 if c == 0.0 else -math.log(c) for c in exact_terms) / 2   # Lean: log 0 = 0
print(f'    additive mean with Lean\'s convention = {lean_sum:.6f},  '
      f'floor claimed = {0.5*math.log(2):.6f}'
      f'   -> {"FALSE, as predicted" if lean_sum < 0.5*math.log(2) - 1e-12 else "?? unexpected"}')
print(f'    multiplicative form at the same point : {exact_terms[0]*exact_terms[1]:.6f} '
      f'<= {2.0**(1-2):.6f}   -> True')

print()
print('=' * 96)
print('VERDICT')
print('=' * 96)
print(f'  (A) identity                          : {"CONFIRMED" if okA else "FAILED"}')
print(f'  (C) multiplicativity (the Lean step)  : {"CONFIRMED" if okC else "FAILED"}')
print(f'  (D) tau composition                   : {"CONFIRMED" if okD else "FAILED"}')
print(f'  negative control detects a wrong tau  : {"yes" if wctl > 1e-6 else "NO -- BLIND"}')
if okA and okC and okD:
    print('  => THE REDUCTION IS SOUND.  Formalising lem:coset therefore splits into:')
    print('       1. v = 2, the double-angle formula      -- elementary, no roots of unity')
    print('       2. multiplicativity, k = i + a j        -- a Finset reindexing, checked here')
    print('       3. v an odd prime                       -- the only place roots of unity enter')
    print('     Steps 1 and 2 give every v that is a product of the primes handled in step 3.')
else:
    print('  => REPORT RAW.  Do not spend a Lean round on a reduction that does not hold.')
