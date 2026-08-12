# r1weighted_r134.py -- the resolution, and the instruction it produces.
#
# Two facts that look contradictory:
#   (A) the Edgeworth expansion predicts P_s[S=m] to a relative 3e-5 at k = 64 (r1edgeworth_133b)
#   (B) the fourth-order Taylor error of log G~ is ~840 at the edge of R1, and still 2.7-9.4 at
#       the effective radius where |G~| has fallen to k^-10 (r1remainder_134, r1radius_134)
#
# Both are true.  The resolution is that the inversion integral is dominated by |theta| <~ 1/sigma,
# far inside either radius, and the Taylor error there is tiny.  Bounding the error by its
# SUPREMUM over R1 throws that away.
#
# Measured here: the |G~|-WEIGHTED Taylor error, which is what actually enters the integral.
#     Ebar = int |G~(th)| E(th) dth  /  int |G~(th)| dth
# Prediction: Ebar << 1 and Ebar ~ the fifth-order budget, while sup E is O(100).
import math, cmath
from r1budget_r133 import profile, solve_s, cumulants

def tilt(a, s): return 1.0 / (1.0 + math.exp(min(700.0, s * a)))

def setup(name, k, x):
    A = profile(name, k); T = sum(A); n = int((0.5 - x) * T)
    s = solve_s(A, n); B = [a for a in A if a > 2]
    mu, K2, K3, K4 = cumulants(B, s)
    S5 = sum(a**5 * tilt(a, s) * (1 - tilt(a, s)) for a in B)
    return A, B, s, mu, K2, K3, K4, S5

def logG(B, s, th):
    tot = 0j
    for a in B:
        p = tilt(a, s)
        tot += cmath.log(1 - p + p * cmath.exp(2j * math.pi * a * th))
    return tot

print('sup versus weighted Taylor error on R1.  x = 0.20, R1 = |theta| <= (log k)/sigma.')
print('  %8s %5s %11s %11s %11s %11s %10s'
      % ('profile', 'k', 'sup E', 'weighted E', 'ratio', 'fifth budget', 'Ebar/fifth'))
for name in ('odds', 'primes'):
    for k in (100, 200, 300, 450):
        A, B, s, mu, K2, K3, K4, S5 = setup(name, k, 0.20)
        sg = math.sqrt(K2); th0 = math.log(k) / sg
        M = 900
        num = den = 0.0; supE = 0.0
        for i in range(M + 1):
            th = th0 * i / M
            lg = logG(B, s, th)
            w = math.exp(lg.real)
            u = 2 * math.pi * th
            poly = 1j*mu*u - K2*u*u/2 - 1j*K3*u**3/6 + K4*u**4/24
            e = abs(lg - poly)
            supE = max(supE, e)
            num += w * e; den += w
        Ebar = num / den
        # the fifth-order budget evaluated at the scale that dominates, |theta| ~ 1/sigma
        thd = 1.0 / sg
        fifth = (2 * math.pi * thd) ** 5 * S5
        print('  %8s %5d %11.4e %11.4e %11.1f %11.4e %10.4f'
              % (name, k, supE, Ebar, supE / Ebar, fifth, Ebar / fifth))
    print()

print('and how the weighted error scales -- it must be the thing that vanishes')
print('  %8s %6s %6s %11s %9s' % ('profile', 'k1', 'k2', 'Ebar(k2)', 'exponent'))
for name in ('odds', 'primes'):
    vals = {}
    for k in (150, 300, 600):
        A, B, s, mu, K2, K3, K4, S5 = setup(name, k, 0.20)
        sg = math.sqrt(K2); th0 = math.log(k) / sg
        M = 700; num = den = 0.0
        for i in range(M + 1):
            th = th0 * i / M
            lg = logG(B, s, th); w = math.exp(lg.real)
            u = 2 * math.pi * th
            poly = 1j*mu*u - K2*u*u/2 - 1j*K3*u**3/6 + K4*u**4/24
            num += w * abs(lg - poly); den += w
        vals[k] = num / den
    e = math.log(vals[150] / vals[600]) / math.log(4.0)
    print('  %8s %6d %6d %11.4e %9.3f' % (name, 150, 600, vals[600], e))
