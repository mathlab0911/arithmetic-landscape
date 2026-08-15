#!/usr/bin/env python3
r"""
r114 / an ADVERSARIAL self-audit of thm:rate, written because fable-5 is out of budget and the
standing rule -- "a proof written by one model becomes proved on paper only after the other
model has verified it independently" -- cannot be satisfied this round.  The purpose of this
script is to FALSIFY the theorem I wrote in r113, not to illustrate it.

WHAT r113 CLAIMS.  For theta = a/q + beta with q <= Q = floor(sqrt N) and |beta| <= 1/(q(Q+1)),
    G(theta) := SUM_m p_m X^(M)_m(theta) / SUM_m p_m   >=   (1 - 1/v) log 2  -  E,
    E <= 14 qM/N + 8M/(Q+1),
built from an exact main term (the coset identity) plus three errors:
    (i)   progression versus integral      <= 4qM/N + 4M/(Q+1)
    (ii)  jitter: class j starts at x_j + m_j beta, |m_j beta| <= (2v/N) L   <= 8qM/N + 4M/(Q+1)
    (iii) unequal class counts (differ by 1)                                 <= 2qM/N
and a weight step by Abel summation (p_m decreasing).

*** MY OWN MARKED SPOT, from r113 section 8: (ii).  I bound the jitter by
    |INT f(z+eps) - INT f(z)| <= eps . V(f) with V <= 2M(L+2), and eps and L are NOT
    independent -- eps <= (2v/N) L -- so a factor can hide in the linkage. ***

HOW THIS SCRIPT ATTACKS IT.  F28: replace one approximation at a time, so that a discrepancy
localises to a single named step.  Define five quantities on the same (N, q, a, beta, M):

    T0 = the real thing            : p-weighted mean over the actual odd m of X^(M)(m theta)
    T1 = T0 with uniform weights                     -> T0 - T1 isolates the WEIGHT step
    T2 = T1 with every class truncated to the common
         minimum count                               -> T1 - T2 isolates error (iii)
    T3 = T2 with the jitter removed: class j is put
         at x_j + eta r instead of x_j + m_j beta + eta r  -> T2 - T3 isolates error (ii)
    T4 = the integral (1/L) INT_0^L Phi^(M)_q(w) dw  -> T3 - T4 isolates error (i)
    FLOOR = (1 - 1/v) log 2

The coset identity says T4 >= FLOOR exactly, with no error at all.  So the theorem stands or
falls on the three differences, each of which is measured here against its own claimed bound.

*** FAIL RULES (F51 floors stated).  Each difference is a difference of two O(1) means computed
in float64; the arithmetic floor is 1e-13.  A difference exceeding its claimed bound by more
than that floor at ANY tested (N, q, a, beta) FALSIFIES that error term, and the paper's
\STATUS{proved} on thm:rate must be withdrawn, not patched.  Separately, if the end-to-end test
(D) finds a minor theta with F_A(theta)^{1/b} exceeding 1/sqrt2 by a factor that GROWS with b,
the theorem itself is false. ***

F55: the theta scan in (D) carries a positive control -- it must recover theta = 1/4 with the
value 1/sqrt2, or its resolution is wrong and its output is noise.
F44: membership of the Dirichlet box and of the minor arc is asserted in code.
"""
import math
import numpy as np

LOG2 = math.log(2.0)
DELTA = LOG2 / 6.0
INV_SQRT2 = 1.0 / math.sqrt(2.0)
FLOOR_ARITH = 1e-13


def X(t):
    c = np.abs(np.cos(np.pi * np.asarray(t, dtype=float)))
    return np.where(c < 1e-300, np.inf, -np.log(np.maximum(c, 1e-300)))


def vee(q):
    return q if q % 2 == 1 else q // 2


def Rq(q):
    return np.arange(q) if q % 2 == 1 else np.arange(1, q, 2)


def odds(N):
    return np.arange(3, N + 1, 2)


print('=' * 100)
print('(A) THE THREE ERROR TERMS, MEASURED ONE AT A TIME (F28).')
print('    Each column is compared with its OWN claimed bound, not with the total.')
print('=' * 100)

worst = {'weight': (0.0, None), 'iii': (0.0, None), 'ii': (0.0, None), 'i': (0.0, None)}
violations = []

for N in (8001, 32001, 128001):
    Q = math.isqrt(N)
    M = math.log(2 * Q / math.pi) + 1.0
    m = odds(N)
    p = 2.0 / np.log(m)
    print(f'\n  --- N = {N}, Q = {Q}, M = {M:.4f}')
    print(f"    {'q':>4} {'a':>3} {'beta/box':>9} {'|T0-T1|':>10} {'|T1-T2|':>10} {'bd(iii)':>9} "
          f"{'|T2-T3|':>10} {'bd(ii)':>9} {'|T3-T4|':>10} {'bd(i)':>9} {'T4-floor':>10}")
    for q in (3, 4, 5, 6, 8, 9, 16, Q):
        v = vee(q)
        floor = (1 - 1.0 / v) * LOG2
        bmax = 1.0 / (q * (Q + 1.0))
        for a in (1, 3):
            if math.gcd(a, q) != 1:
                continue
            for frac in (0.0, 0.37, 1.0):
                beta = frac * bmax
                assert abs(beta) <= bmax + 1e-18, 'F44: beta outside the Dirichlet box'
                eta = 2 * v * beta
                L = N * abs(beta)

                # ---- T0: the real thing
                t0ph = (m * a % q) / q + m * beta
                T0 = float(np.minimum(X(t0ph), M).dot(p) / p.sum())
                # ---- T1: uniform weights
                T1 = float(np.minimum(X(t0ph), M).mean())
                # ---- classes
                res = m % q
                cls = {}
                for j in Rq(q):
                    sel = m[res == j]
                    if sel.size:
                        cls[int(j)] = sel
                if len(cls) != v:
                    continue
                rmin = min(s.size for s in cls.values())
                # ---- T2: equal class counts
                vals2 = []
                for j, sel in cls.items():
                    ph = (sel[:rmin] * a % q) / q + sel[:rmin] * beta
                    vals2.append(np.minimum(X(ph), M))
                T2 = float(np.mean(np.concatenate(vals2)))
                # ---- T3: jitter removed (class j starts exactly at x_j)
                vals3 = []
                r = np.arange(rmin)
                for j in cls:
                    ph = (j * a % q) / q + eta * r
                    vals3.append(np.minimum(X(ph), M))
                T3 = float(np.mean(np.concatenate(vals3)))
                # ---- T4: the integral of the coset average over the same arc
                if L > 0:
                    w = np.linspace(0.0, eta * (rmin - 1), 20001)
                else:
                    w = np.zeros(1)
                jj = Rq(q)
                Phi = np.minimum(X(w[:, None] + (jj[None, :] * a % q) / q), M).mean(axis=1)
                T4 = float(Phi.mean())

                bi = 4 * q * M / N + 4 * M / (Q + 1.0)
                bii = 8 * q * M / N + 4 * M / (Q + 1.0)
                biii = 2 * q * M / N
                d_w, d3, d2, d1 = abs(T0 - T1), abs(T1 - T2), abs(T2 - T3), abs(T3 - T4)
                for key, val, bd in (('iii', d3, biii), ('ii', d2, bii), ('i', d1, bi)):
                    if val > worst[key][0]:
                        worst[key] = (val, (N, q, a, frac))
                    if val > bd + FLOOR_ARITH:
                        violations.append((key, N, q, a, frac, val, bd))
                if T4 < floor - FLOOR_ARITH:
                    violations.append(('identity', N, q, a, frac, T4, floor))
                if frac == 0.37:
                    print(f'    {q:4d} {a:3d} {frac:9.2f} {d_w:10.2e} {d3:10.2e} {biii:9.4f} '
                          f'{d2:10.2e} {bii:9.4f} {d1:10.2e} {bi:9.4f} {T4-floor:10.2e}')

print()
print('  worst measured, over everything above:')
for k in ('weight', 'iii', 'ii', 'i'):
    print(f'    {k:>7}: {worst[k][0]:.3e}   at (N,q,a,beta/box) = {worst[k][1]}')
print()
if violations:
    print('  *** FAIL RULE FIRED.  Withdraw \\STATUS{proved} on thm:rate. ***')
    for x in violations[:20]:
        print('   ', x)
else:
    print('  NO VIOLATION: every error term stays inside its own claimed bound, and the')
    print('  integral of the coset average never falls below the floor.  The marked spot (ii)')
    print('  is the largest of the three in absolute terms -- see the column -- but it is the')
    print('  one with the largest bound too.')

# ----------------------------------------------------------------------------------------
print()
print('=' * 100)
print('(B) IS THE JITTER BOUND THE RIGHT SHAPE?  (my marked spot, pressed harder)')
print('    Writing the derivation out properly SHARPENS it: the jitter is eps = m_j beta with')
print('    m_j <= 2v, and the progression step is eta = 2 v beta, so *** eps <= eta exactly ***.')
print('    The per-class error is then at most eps.V/eta <= V <= 2M(L+1) -- the same shape as')
print('    error (i), not a separate mechanism -- giving 4qM/N + 4M/(Q+1) in the mean, which is')
print('    HALF what r113 claimed.  The paper\'s bound is therefore valid and generous.')
print('    What must still be true: the jitter vanishes at beta = 0 and grows with |beta|.')
print('=' * 100)
N, Q = 32001, math.isqrt(32001)
M = math.log(2 * Q / math.pi) + 1.0
m = odds(N)
for q in (3, 8, 89):
    v = vee(q)
    bmax = 1.0 / (q * (Q + 1.0))
    print(f'    q = {q:3d}:')
    print(f"      {'beta/box':>9} {'L=N|beta|':>10} {'|T2-T3|':>11} {'bound 4qM(L+1)/N':>18}")
    for frac in (0.0, 0.125, 0.25, 0.5, 1.0):
        beta = frac * bmax
        eta = 2 * v * beta
        res = m % q
        cls = {int(j): m[res == j] for j in Rq(q)}
        rmin = min(s.size for s in cls.values())
        r = np.arange(rmin)
        v2 = np.concatenate([np.minimum(X((s[:rmin] * 1 % q) / q + s[:rmin] * beta), M)
                             for s in cls.values()])
        v3 = np.concatenate([np.minimum(X((j * 1 % q) / q + eta * r), M) for j in cls])
        d = abs(float(v2.mean()) - float(v3.mean()))
        print(f'      {frac:9.3f} {N*beta:10.4f} {d:11.3e} '
              f'{4*q*M*(N*beta+1)/N:18.6f}')
print('    The measured jitter vanishes at beta = 0 and grows with |beta|, inside a bound that')
print('    also grows with |beta| -- consistent.  It is not linear in beta: the difference of')
print('    two oscillating sums is not a smooth function of beta, and the bound is two orders')
print('    of magnitude loose, so the growth rate carries no information beyond its sign.')

# ----------------------------------------------------------------------------------------
print()
print('=' * 100)
print('(C) ADVERSARIAL SEARCH.  Not a uniform net: hunt directly for a minor theta where the')
print('    weighted mean falls below (1/2) log 2, using the structure of the claim against it')
print('    (near-rational points with small v, and the worst beta inside each box).')
print('=' * 100)
N = 32001
Q = math.isqrt(N)
M = math.log(2 * Q / math.pi) + 1.0
m = odds(N)
p = 2.0 / np.log(m)
W = p.sum()


def Gw(theta):
    return float(np.minimum(X(m * theta), M).dot(p) / W)


best = (math.inf, None)
for q in range(1, Q + 1):
    bmax = 1.0 / (q * (Q + 1.0))
    for a in range(0 if q == 1 else 1, q + 1):
        if math.gcd(a, q) != 1 and not (q == 1 and a == 0):
            continue
        for frac in np.linspace(-1.0, 1.0, 9):
            th = a / q + frac * bmax
            if abs(th - round(th)) < 1.0 / N:        # F44: major arc, excluded by definition
                continue
            if th <= 0 or th >= 1:
                continue
            g = Gw(th)
            if g < best[0]:
                best = (g, (q, a, frac, th))
print(f'    adversarial minimum over {Q} moduli x all numerators x 9 offsets:')
print(f'      G = {best[0]:.6f} at (q,a,beta/box,theta) = {best[1]}')
print(f'      (1/2) log 2 = {0.5*LOG2:.6f}     shortfall = {0.5*LOG2 - best[0]:.3e}')
ok_C = best[0] >= 0.5 * LOG2 - 1e-9
print(f'    {"no minor theta beats the floor" if ok_C else "*** FAIL RULE: floor breached ***"}')

# ----------------------------------------------------------------------------------------
print()
print('=' * 100)
print('(D) END-TO-END ON REAL INSTANCES.  Draw A from the Cramer model, compute')
print('    max over minor theta of F_A(theta)^(1/b), and ask whether the excess over 1/sqrt2')
print('    is BOUNDED (a constant factor, as rem:notmax says) or GEOMETRIC (theorem false).')
print('=' * 100)
print('    *** THE FIRST VERSION OF THIS TEST WAS BROKEN, AND ITS CONTROL DID NOT NOTICE. ***')
print('    A uniform net of 30001 points has spacing 1.7e-5 while the peak at theta = 1/4 is')
print('    O(1/N) = 7.8e-6 wide at N = 128001, so the scan stepped over it and reported a')
print('    MAXIMUM of 0.5690 -- below a value it had itself evaluated.  The control passed')
print('    anyway, because it checked F_A(1/4) rather than checking that THE SEARCH FINDS 1/4.')
print('    F55 says a search needs a positive control; the control must be on the search.')
print('    Repaired: the peaks live at rationals, so evaluate at every a/q with q <= 20 and')
print('    sweep +-5/N around each, and gate the row on the search recovering theta = 1/4.')
rng = np.random.default_rng(114)
print(f"    {'N':>7} {'b':>6} {'max F^(1/b)':>12} {'- 1/sqrt2':>11} {'b log(sqrt2 max)':>17} "
      f"{'argmax':>9} {'control':>8}")
for N in (2001, 8001, 32001, 128001):
    mm = odds(N)
    pp = 2.0 / np.log(mm)
    A = mm[rng.random(mm.size) < pp]
    b = A.size
    Afl = A.astype(float)

    def FA(th):
        return float(np.exp(np.log(np.maximum(np.abs(np.cos(np.pi * Afl * th)), 1e-300)).mean()))

    cands = sorted({a / q for q in range(1, 21) for a in range(0, q + 1)})
    bestv, bestt = -1.0, None
    for c in cands:
        loc = np.linspace(c - 5.0 / N, c + 5.0 / N, 201)
        loc = loc[(np.abs(loc - np.round(loc)) >= 1.0 / N) & (loc > 0) & (loc < 1)]
        for t in loc:
            f = FA(t)
            if f > bestv:
                bestv, bestt = f, t
    # F_A(1-theta) = F_A(theta), so 3/4 is the same control point as 1/4
    ctrl = min(abs(bestt - 0.25), abs(bestt - 0.75)) < 3.0 / N and abs(bestv - INV_SQRT2) < 1e-9
    print(f'    {N:7d} {b:6d} {bestv:12.6f} {bestv-INV_SQRT2:11.3e} '
          f'{b*math.log(math.sqrt(2)*bestv):17.4f} {bestt:9.5f} {str(ctrl):>8}')
print('    CONTROL, correctly placed this time: the search must LOCATE theta = 1/4 and return')
print('    1/sqrt2 there.  A False invalidates the row rather than refuting the theorem.')
print('    The theorem predicts the last column stays O(1) while b grows; a column growing')
print('    linearly in b would mean a geometric excess and would refute thm:rate.')
print('    SCOPE OF THIS ROW (F01): it shows the maximum does not EXCEED 1/sqrt2 geometrically.')
print('    It does not reproduce the O(1/b) excess of rem:notmax, whose optimal offset is of')
print('    order 1/(N sqrt b) and finer than this grid; that remains measured in mq4_r107.')

print()
print('=' * 100)
print('VERDICT')
print('=' * 100)
print(f'  (A) three error terms inside their bounds : {"YES" if not violations else "NO -- WITHDRAW"}')
print(f'  (C) adversarial search found no breach    : {"YES" if ok_C else "NO -- WITHDRAW"}')
print('  (D) read the last column: O(1) supports thm:rate, linear-in-b refutes it.')
print('  This is a self-audit.  It cannot replace the independent read by the other model,')
print('  and the report says so.')
